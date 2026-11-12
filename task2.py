"""A2 Q2 - OTP attempts: while, for, break/continue/pass, loop-else, recursion."""


def make_inputs(seq):
    it = iter(seq)
    return lambda: next(it, "")


def otp_while(get_input, otp="4321", max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        entry = get_input().strip()
        if entry == "":
            continue                    # blank does NOT count (counter not touched)
        attempts += 1                   # counted only after a non-blank entry
        if entry == otp:
            return "verified"
        else:
            pass                        # placeholder: could log the wrong try
    return "LOCKED 30 min"


def otp_for(get_input, otp="4321", max_attempts=3):
    for _ in range(max_attempts):
        entry = get_input().strip()
        while entry == "":              # blank: ask again, attempt not used
            entry = get_input().strip()
        if entry == otp:
            break
    else:                               # loop-else: runs only if no break
        return "LOCKED 30 min"
    return "verified"


def otp_changed(get_input, security_ok, otp="4321", base=3, extra=2):
    """Changed condition: +2 attempts if the security question is correct."""
    limit, granted = base, False
    attempts = 0
    while attempts < limit:
        entry = get_input().strip()
        if not entry:
            continue
        attempts += 1
        if entry == otp:
            return "verified"
        if attempts == base and not granted and security_ok():
            limit += extra
            granted = True
    return "LOCKED 30 min"


def otp_recursive(get_input, otp="4321", left=3):
    if left == 0:
        return "LOCKED 30 min"
    entry = get_input().strip()
    if entry == "":
        return otp_recursive(get_input, otp, left)      # blank: same attempts left
    if entry == otp:
        return "verified"
    return otp_recursive(get_input, otp, left - 1)


scenarios = {
    "right on 2nd": ["1111", "4321"],
    "blank then right": ["", "4321"],
    "three wrong": ["1", "2", "3"],
    "blanks + 3 wrong": ["", "1", "", "2", "3"],
}
for name, seq in scenarios.items():
    print(f"{name:18} while={otp_while(make_inputs(seq)):14} "
          f"for={otp_for(make_inputs(seq)):14} rec={otp_recursive(make_inputs(seq))}")

print("changed, 5 wrong, sec-question OK :", otp_changed(make_inputs(list("12345")), lambda: True))
print("changed, 3 wrong, sec-question bad:", otp_changed(make_inputs(list("123")), lambda: False))
print("changed, 4th try right (sec OK)   :", otp_changed(make_inputs(["1", "2", "3", "4321"]), lambda: True))

print("\nBug if counter updated BEFORE the blank check: blank entries use up attempts,")
print("so a customer who presses Enter 3 times is locked out unfairly.")