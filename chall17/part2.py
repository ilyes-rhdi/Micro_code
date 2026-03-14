from heapq import heappush, heappop
import sys

# --------------------------------------------------
# Réglages
# --------------------------------------------------

# True si ton énoncé custom utilise le keypad miroir en part 2
USE_MIRRORED_BACKUP_LAYOUT = False

# True seulement si ton juge veut vraiment (hex_value + 1)
# L'exemple 802794 montre que normalement il faut False
USE_PLUS_ONE = False


# --------------------------------------------------
# Keypads
# --------------------------------------------------

# Keypad hex
HEX = {
    '0': (0, 0), '1': (1, 0), '2': (2, 0),
    '3': (0, 1), '4': (1, 1), '5': (2, 1),
    '6': (0, 2), '7': (1, 2), '8': (2, 2),
    '9': (0, 3), 'A': (1, 3), 'B': (2, 3),
    'C': (0, 4), 'D': (1, 4), 'E': (2, 4),
    'F': (1, 5), '#': (2, 5),
}

# Layout standard (celui du puzzle original / part 1)
DIR_STANDARD = {
    '^': (1, 0), '#': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1),
}

# Layout miroir (ta variante backup chain)
DIR_MIRRORED = {
    '<': (0, 0), '^': (1, 0), '#': (2, 0),
    'v': (0, 1), '>': (1, 1),
}

DIR = DIR_MIRRORED if USE_MIRRORED_BACKUP_LAYOUT else DIR_STANDARD

MOVES = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}


# --------------------------------------------------
# DP des transitions
# --------------------------------------------------

def build_transition_costs(keypad, prev_cost):
    """
    prev_cost[a][b] = coût minimal pour faire appuyer b sur le keypad contrôleur
                      en sachant que son bras est sur a.

    Retourne:
    out[src][dst] = coût minimal pour déplacer le bras du keypad courant
                    de src à dst puis appuyer sur dst.
    """
    pos_to_btn = {pos: btn for btn, pos in keypad.items()}
    buttons = list(keypad.keys())
    controller_buttons = list(prev_cost.keys())
    INF = 10**30

    out = {src: {} for src in buttons}

    for src in buttons:
        # Quand un niveau supérieur finit d'émettre un bouton,
        # son bras termine toujours sur '#'
        start_state = (src, '#')

        dist = {start_state: 0}
        pq = [(0, src, '#')]

        while pq:
            cur_dist, cur_btn, last_controller_btn = heappop(pq)
            if cur_dist != dist.get((cur_btn, last_controller_btn), INF):
                continue

            x, y = keypad[cur_btn]

            for move_btn, (dx, dy) in MOVES.items():
                nx, ny = x + dx, y + dy
                if (nx, ny) not in pos_to_btn:
                    continue

                nxt_btn = pos_to_btn[(nx, ny)]
                nd = cur_dist + prev_cost[last_controller_btn][move_btn]
                state = (nxt_btn, move_btn)

                if nd < dist.get(state, INF):
                    dist[state] = nd
                    heappush(pq, (nd, nxt_btn, move_btn))

        # Pour "sélectionner" dst, il faut ensuite envoyer '#'
        for dst in buttons:
            best = INF
            for last_controller_btn in controller_buttons:
                d = dist.get((dst, last_controller_btn))
                if d is None:
                    continue
                best = min(best, d + prev_cost[last_controller_btn]['#'])
            out[src][dst] = best

    return out


def build_dir_costs(num_relays):
    """
    Construit les coûts pour une chaîne de num_relays keypads directionnels.
    Base: le joueur humain peut appuyer directement sur n'importe quel bouton -> coût 1.
    """
    dir_buttons = list(DIR.keys())

    # Base "humaine"
    cost = {a: {b: 1 for b in dir_buttons} for a in dir_buttons}

    for _ in range(num_relays):
        cost = build_transition_costs(DIR, cost)

    return cost


def total_complexity(codes, num_relays=25):
    dir_cost = build_dir_costs(num_relays)
    hex_cost = build_transition_costs(HEX, dir_cost)

    total = 0

    for code in codes:
        code = code.strip()
        if not code:
            continue

        presses = 0
        cur = '#'
        for ch in code:
            presses += hex_cost[cur][ch]
            cur = ch

        value = int(code[:-1], 16)
        if USE_PLUS_ONE:
            value += 1

        total += presses * value

    return total


def main():
    codes = [line.strip() for line in sys.stdin if line.strip()]
    print(total_complexity(codes, num_relays=25))


if __name__ == "__main__":
    main()