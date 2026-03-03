import argparse
import html
import os
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MicroCodePart1Fetcher/1.0"


def read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def fetch_text(url: str, cookie: str | None, timeout: int = 25) -> str:
    headers = {"User-Agent": USER_AGENT}
    if cookie:
        headers["Cookie"] = cookie
    req = Request(url, headers=headers)
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def find_part_section(page_html: str, part_number: int) -> str | None:
    no_script_html = re.sub(r"<script\b[^>]*>.*?</script>", "", page_html, flags=re.IGNORECASE | re.DOTALL)
    no_script_html = re.sub(r"<style\b[^>]*>.*?</style>", "", no_script_html, flags=re.IGNORECASE | re.DOTALL)
    match = re.search(
        rf"(<section[^>]*>.*?<h2[^>]*>\s*Part\s+{part_number}\s*</h2>.*?</section>)",
        no_script_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1) if match else None


def section_to_markdown(section_html: str, title: str, part_number: int) -> str:
    token_re = re.compile(
        r"(<h[23][^>]*>.*?</h[23]>|<p[^>]*>.*?</p>|<li[^>]*>.*?</li>|<pre[^>]*><code[^>]*>.*?</code></pre>)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    lines = [f"# {title}", "", f"## Part {part_number}", ""]
    for token in token_re.findall(section_html):
        t = token.lower()
        if t.startswith("<h2") or t.startswith("<h3"):
            txt = strip_tags(token)
            if txt.lower().startswith("part "):
                continue
            if txt:
                lines.append(f"### {txt}")
                lines.append("")
        elif t.startswith("<li"):
            txt = strip_tags(token)
            if txt:
                lines.append(f"- {txt}")
        elif t.startswith("<pre"):
            code_match = re.search(r"<code[^>]*>(.*?)</code>", token, flags=re.IGNORECASE | re.DOTALL)
            code = strip_tags(code_match.group(1)) if code_match else ""
            if code:
                lines.append("```")
                lines.append(code)
                lines.append("```")
                lines.append("")
        else:
            txt = strip_tags(token)
            if txt:
                lines.append(txt)
                lines.append("")
    return "\n".join(lines).strip() + "\n"


def extract_title(page_html: str) -> str:
    no_script_html = re.sub(r"<script\b[^>]*>.*?</script>", "", page_html, flags=re.IGNORECASE | re.DOTALL)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", no_script_html, flags=re.IGNORECASE | re.DOTALL)
    return strip_tags(h1.group(1)) if h1 else "Untitled Challenge"


def extract_input_url(page_html: str, base: str, fallback_id: str) -> str:
    m = re.search(r'href="(/challenges/[0-9a-f\-]{36}/input(?:\.txt)?)"', page_html, flags=re.IGNORECASE)
    if m:
        return f"{base}{m.group(1)}"
    return f"{base}/challenges/{fallback_id}/input"


def next_chall_dir(root: Path) -> Path:
    max_id = 0
    for p in root.iterdir():
        if p.is_dir():
            m = re.fullmatch(r"chall(\d+)", p.name)
            if m:
                max_id = max(max_id, int(m.group(1)))
    return root / f"chall{max_id + 1}"


def challenge_id_from_url(url: str) -> str:
    m = re.search(r"/challenges/([0-9a-f\-]{36})", url)
    if not m:
        raise ValueError("Invalid challenge URL format.")
    return m.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch only Part 1 + input for a MicroCode challenge")
    parser.add_argument("url", help="Challenge URL")
    parser.add_argument("--out", default=None, help="Output folder, e.g. chall3")
    parser.add_argument("--cookie", default=None, help="Full Cookie header value")
    args = parser.parse_args()

    root = Path.cwd()
    env = read_env_file(root / ".env")
    cookie = args.cookie or os.getenv("MC_COOKIE") or env.get("MC_COOKIE")

    url = args.url.strip()
    challenge_id = challenge_id_from_url(url)
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    page_html = fetch_text(url, cookie=cookie)
    title = extract_title(page_html)
    section = find_part_section(page_html, 1)
    if not section:
        raise RuntimeError("Part 1 section not found in fetched HTML.")

    out_dir = Path(args.out) if args.out else next_chall_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)

    statement_md = section_to_markdown(section, title, 1)
    input_url = extract_input_url(page_html, base, challenge_id)

    input_text = ""
    input_status = "input not fetched"
    try:
        input_text = fetch_text(input_url, cookie=cookie)
        if input_text and not input_text.endswith("\n"):
            input_text += "\n"
        if input_text.lstrip().startswith("<!DOCTYPE html"):
            input_status = "input endpoint returned HTML (session likely invalid)"
            input_text = ""
        else:
            input_status = f"input fetched via {input_url}"
    except HTTPError as exc:
        input_status = f"input protected (HTTP {exc.code})"

    (out_dir / "challenge_url.txt").write_text(url + "\n", encoding="utf-8")
    (out_dir / "part1_statement.md").write_text(statement_md, encoding="utf-8")
    (out_dir / "input.txt").write_text(input_text, encoding="utf-8")
    (out_dir / "fetch_part1_status.txt").write_text(input_status + "\n", encoding="utf-8")

    print(f"[saved] {out_dir}")
    print(f"[title] {title}")
    print(f"[part] Part 1 fetched")
    print(f"[input] {input_status}")


if __name__ == "__main__":
    main()
