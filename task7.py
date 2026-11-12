"""A2 Q7 - Diagnose, redesign, validate.  Chosen program: Q6 naive recursion.

A. Diagnosis : work = number of calls; grows ~phi^n; same sub-problems repeated.
B. Objective : calls for n=30 below 100 (from ~2.7 million) and n=1000 without RecursionError.
C. Design    : exploit overlapping sub-problems (ways(n) depends only on the last two
               values). Use bottom-up iteration with two variables: O(n) time, O(1) space.
D. Prediction: naive calls ~ 2*ways(n)-1; iterative performs n-1 additions.
"""
import time
from functools import lru_cache

calls = 0


def naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return naive(n - 1) + naive(n - 2)


def iterative(n):
    adds = 0
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
        adds += 1
    return b, adds


@lru_cache(maxsize=None)
def memo(n):
    return 1 if n <= 1 else memo(n - 1) + memo(n - 2)


print(f"{'n':>3} {'naive calls':>12} {'predicted':>10} {'naive s':>9} {'iter adds':>10} {'iter s':>9}")
for n in (10, 20, 25, 30, 32):
    calls = 0
    t = time.perf_counter(); v = naive(n); tn = time.perf_counter() - t
    t = time.perf_counter(); w, adds = iterative(n); ti = time.perf_counter() - t
    assert v == w
    print(f"{n:>3} {calls:>12} {2*v-1:>10} {tn:>9.4f} {adds:>10} {ti:>9.6f}")

val, adds = iterative(1000)
print("\nn=1000 iterative adds:", adds, "digits:", len(str(val)))
memo.cache_clear()
try:
    memo(1000)
except RecursionError:
    print("memoised recursion at n=1000: RecursionError (default limit)")

print("\nF. Evaluation: objective met (calls 2.7M -> 29 additions). Cost: big ints grow")
print("(~209 digits at n=1000) so additions are not O(1) in bit terms. Naive code stays")
print("preferable only for teaching because it mirrors the definition exactly.")