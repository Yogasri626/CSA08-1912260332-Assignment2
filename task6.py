
import sys
from functools import lru_cache

calls = 0


def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_loop(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b if n >= 1 else 1


calls = 0; print("naive:", ways_naive(25), "calls =", calls)
ways_memo.cache_clear()
calls = 0; print("memo :", ways_memo(25), "calls =", calls)

print("\nBy hand n=1..6 -> 1,2,3,5,8,13 ; program:", [ways_loop(n) for n in range(1, 7)])

print("\nCall counts:")
print(f"{'n':>3} {'naive':>10} {'memo':>6}")
for n in (10, 20, 25, 30):
    calls = 0; ways_naive(n); cn = calls
    ways_memo.cache_clear(); calls = 0; ways_memo(n); cm = calls
    print(f"{n:>3} {cn:>10} {cm:>6}")

print("\nrecursion limit:", sys.getrecursionlimit())
ways_memo.cache_clear()
try:
    print(ways_memo(1000))
except RecursionError as e:
    print("RecursionError:", e)

# deployment: both approaches
ways_memo.cache_clear()
sys.setrecursionlimit(5000)
print("memo n=1000 with raised limit, digits:", len(str(ways_memo(1000))))
sys.setrecursionlimit(1000)
print("loop n=1000 matches:", ways_loop(1000) == ways_memo(1000))
print("Decision: loop version (O(n) time, O(1) extra space, no limit problem).")

# call tree for n=5
def tree(n, depth=0):
    print("  " * depth + f"ways({n})")
    if n > 1:
        tree(n - 1, depth + 1)
        tree(n - 2, depth + 1)

print("\nCall tree n=5:")
tree(5)