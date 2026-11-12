

def separate_ifs(units, ration_card, has_80):
    """Buggy style: independent ifs can fire more than once."""
    result = []
    if units <= 100:
        result.append("full")
    if 101 <= units <= 200 and ration_card:
        result.append("partial")
    if units > 200 and has_80:
        result.append("senior")
    if units > 100 and has_80:          # overlapping rule a developer might add
        result.append("senior-extra")
    return result or ["none"]


def chained(units, ration_card, has_80):
    """Correct style: exactly one decision."""
    if units <= 100:
        return "full"
    elif 101 <= units <= 200:
        return "partial" if ration_card else "none"
    elif has_80:
        return "senior"
    else:
        return "none"


# Alternative 1: table of (upper limit, decision) searched in a loop
SLABS = [(100, "full"), (200, "partial-if-card"), (float("inf"), "senior-only")]


def slab_lookup(units, ration_card, has_80):
    for limit, label in SLABS:                      # O(k) per decision
        if units <= limit:
            if label == "full":
                return "full"
            if label == "partial-if-card":
                return "partial" if ration_card else "none"
            return "senior" if has_80 else "none"


# Alternative 2: match-case (Python 3.10+)
def match_case(units, ration_card, has_80):
    match units:
        case u if u <= 100:
            return "full"
        case u if u <= 200:
            return "partial" if ration_card else "none"
        case _:
            return "senior" if has_80 else "none"


# Eight households incl. every boundary: (units, ration_card, has_80)
cases = [(50, False, False), (100, False, False), (101, True, False),
         (101, False, False), (200, True, False), (201, False, True),
         (201, False, False), (350, True, True)]
predicted = ["full", "full", "partial", "none", "partial", "senior", "none", "senior"]

print(f"{'units':>5} {'card':>5} {'80+':>5} | {'separate-ifs':<22} {'if-elif':<8} {'pred':<8} ok")
for (u, rc, s), p in zip(cases, predicted):
    a, b = separate_ifs(u, rc, s), chained(u, rc, s)
    assert b == slab_lookup(u, rc, s) == match_case(u, rc, s)
    print(f"{u:>5} {str(rc):>5} {str(s):>5} | {str(a):<22} {b:<8} {p:<8} {b == p}")

print("\nDesign decision: flat if-elif with combined Boolean conditions is easier to")
print("read/change than nested ifs: each slab is one line, and a new slab is one new elif.")