from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - runtime dependency guard
    print(
        "Missing dependency: playwright\n"
        "Install with:\n"
        "  pip install playwright\n"
        "  playwright install chromium"
    )
    raise


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


def parse_cookie_header(cookie_header: str, domain: str) -> list[dict[str, str]]:
    cookies: list[dict[str, str]] = []
    for part in cookie_header.split(";"):
        chunk = part.strip()
        if not chunk or "=" not in chunk:
            continue
        name, value = chunk.split("=", 1)
        name = name.strip()
        value = value.strip()
        if name:
            cookies.append({"name": name, "value": value, "domain": domain, "path": "/"})
    return cookies


def find_target_form(page, part: int):
    forms = page.locator("form")
    count = forms.count()
    for idx in range(count):
        form = forms.nth(idx)
        if form.locator("input[name='answer']").count() == 0:
            continue
        part_input = form.locator("input[name='part']")
        if part_input.count() > 0:
            value = part_input.first.get_attribute("value")
            if value == str(part):
                return form
    for idx in range(count):
        form = forms.nth(idx)
        if form.locator("input[name='answer']").count() > 0:
            return form
    return None


def infer_outcome(response_text: str, page, part: int) -> str:
    lowered = response_text.lower()
    if '"correct":true' in lowered or '"correct",true' in lowered:
        return "correct"
    if '"correct":false' in lowered or '"correct",false' in lowered:
        return "incorrect"
    if page.get_by_text("Not Quite", exact=False).count() > 0:
        return "incorrect"
    if page.get_by_text("Continue", exact=False).count() > 0:
        return "likely-correct"
    if page.get_by_text("Correct", exact=False).count() > 0:
        return "likely-correct"
    # If the answer form for this part is gone, the part is usually validated.
    if find_target_form(page, part) is None:
        return "likely-correct"
    return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit a MicroCode answer via browser automation.")
    parser.add_argument("challenge", help="Challenge folder (e.g. chall6) or direct challenge URL")
    parser.add_argument("answer", help="Answer to submit")
    parser.add_argument("--part", type=int, default=2, help="Part number to submit (default: 2)")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    parser.add_argument("--timeout", type=int, default=30000, help="Timeout in milliseconds")
    args = parser.parse_args()

    root = Path.cwd()
    env = read_env_file(root / ".env")
    cookie_header = os.getenv("MC_COOKIE") or env.get("MC_COOKIE")
    if not cookie_header:
        raise RuntimeError("MC_COOKIE not found in environment or .env")

    challenge_value = args.challenge.strip()
    if re.match(r"^https?://", challenge_value, flags=re.IGNORECASE):
        challenge_url = challenge_value
    else:
        challenge_url_path = root / challenge_value / "challenge_url.txt"
        if not challenge_url_path.exists():
            raise FileNotFoundError(f"Missing challenge URL file: {challenge_url_path}")
        challenge_url = challenge_url_path.read_text(encoding="utf-8-sig").strip()

    parsed = urlparse(challenge_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid challenge URL: {challenge_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context()
        cookies = parse_cookie_header(cookie_header, parsed.netloc)
        if not cookies:
            browser.close()
            raise RuntimeError("Could not parse cookies from MC_COOKIE")
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto(challenge_url, wait_until="domcontentloaded", timeout=args.timeout)
        page.wait_for_load_state("networkidle", timeout=args.timeout)

        form = find_target_form(page, args.part)
        if form is None:
            outcome = "already-solved" if page.get_by_text("Correct", exact=False).count() > 0 else "unknown"
            print(f"[url] {challenge_url}")
            print(f"[part] {args.part}")
            print(f"[answer] {args.answer}")
            print("[http] none")
            print(f"[result] {outcome}")
            browser.close()
            if outcome == "already-solved":
                return
            raise RuntimeError(
                "Could not find submission form. Verify login cookie and that this part is unlocked."
            )

        answer_input = form.locator("input[name='answer']").first
        answer_input.fill(args.answer)

        post_response = None

        def is_submit_response(resp) -> bool:
            try:
                req = resp.request
                if req.method.upper() != "POST":
                    return False
                if req.url != page.url:
                    return False
                return "next-action" in {k.lower() for k in req.headers.keys()}
            except Exception:
                return False

        try:
            with page.expect_response(is_submit_response, timeout=args.timeout) as response_info:
                form.locator("button[type='submit']").first.click()
            post_response = response_info.value
            try:
                response_text = post_response.text()
            except Exception:
                # Some responses don't expose a retrievable body in Chromium protocol.
                response_text = ""
        except PlaywrightTimeoutError:
            form.locator("button[type='submit']").first.click()
            response_text = ""

        outcome = infer_outcome(response_text, page, args.part)
        status_code = post_response.status if post_response else "unknown"

        print(f"[url] {challenge_url}")
        print(f"[part] {args.part}")
        print(f"[answer] {args.answer}")
        print(f"[http] {status_code}")
        print(f"[result] {outcome}")

        browser.close()

    if outcome in {"incorrect", "unknown"}:
        sys.exit(2)


if __name__ == "__main__":
    main()
