"""A2 Q3 - Vehicle registration number validator (no regex)."""
import re


def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234'"""
    return text.strip().replace(" ", "").replace("-", "").upper()


def is_valid(reg):
    """2 letters, 2 digits, 1 or 2 letters, 4 digits."""
    if len(reg) not in (9, 10):
        return False
    return (reg[:2].isalpha() and reg[2:4].isdigit()
            and reg[4:-4].isalpha() and reg[-4:].isdigit())


def format_receipt(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234' (valid numbers only)."""
    if not is_valid(reg):
        raise ValueError(f"invalid number {reg!r}")
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])


def is_valid_regex(reg):
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg) is not None


for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

print()
tests = ["tn 09 ab 1234", "TN-09-AB-1234", "Tn09Ab1234", "KA-01-M-0007",
         "T1 09 AB 1234", "TN 09 AB 123"]
for t in tests:                     # last two should be rejected
    r = normalise(t)
    ok = is_valid(r)
    assert ok == is_valid_regex(r)
    print(f"{t!r:18} -> {r:11} {ok!s:5}", format_receipt(r) if ok else "rejected")

print("\nSlicing:")
for s in ("TN09AB1234", "KA01M0007"):
    print(f"{s} len={len(s)}  s[-4:]={s[-4:]!r}  s[4:-4]={s[4:-4]!r}")

t = "tn09"
u = t.upper()
print("\nImmutability: text.upper() returns a NEW string; text is still", t, "and result is", u)