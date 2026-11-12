
import io
import time

items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]


def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):
    return ";".join(parts) + ";"


def build_fstring_join(parts):
    return "".join([f"{p};" for p in parts])


def build_stringio(parts):
    buf = io.StringIO()
    for p in parts:
        buf.write(p)
        buf.write(";")
    return buf.getvalue()


def timed(fn, data):
    start = time.perf_counter()
    out = fn(data)
    return out, time.perf_counter() - start


# Required program (3 runs, average)
tp, tj = [], []
for _ in range(3):
    a, x = timed(build_plus, items)
    b, y = timed(build_join, items)
    tp.append(x)
    tj.append(y)
print("same text:", a == b, "| length:", len(b))
print(f"+= time: {sum(tp)/3:.4f} s   join time: {sum(tj)/3:.4f} s  (average of 3 runs)")

# Measurement at three sizes
print(f"\n{'lines':>8} {'+= (s)':>10} {'join (s)':>10} {'f-str+join':>11} {'StringIO':>10}")
for n in (1_000, 10_000, 200_000):
    data = items[:n]
    r = [timed(f, data) for f in (build_plus, build_join, build_fstring_join, build_stringio)]
    assert len({o for o, _ in r}) == 1
    print(f"{n:>8} {r[0][1]:>10.5f} {r[1][1]:>10.5f} {r[2][1]:>11.5f} {r[3][1]:>10.5f}")

print("\nNote: CPython can resize in place for += when the string has one reference,")
print("so it may look fast; but that is an implementation detail, not guaranteed")
print("(PyPy and other cases copy => O(n^2)), so join() remains the recommended practice.")