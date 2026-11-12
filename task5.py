

def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order


print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
print("add_item.__defaults__       =", add_item.__defaults__)
print("-> the default list is created once at def-time and keeps growing.\n")


# parameters
def bill(item, qty=1, *, price):
    return f"{qty} x {item} @ {price}"


print(bill("Tea", 2, price=10), "|", bill(price=15, item="Vada"))


# multiple return values
def total_with_gst(prices, rate=0.05):
    total = sum(prices)
    gst = round(total * rate, 2)
    return total, gst


t, g = total_with_gst([10, 15, 20])
print("total, gst =", t, g)

# three customers independent
for cust, things in enumerate([["Tea", "Vada"], ["Coffee"], ["Dosa", "Tea", "Idli"]], 1):
    o = None
    for th in things:
        o = add_item(th, o)
    print(f"customer {cust}:", o)

# scope
x = "global"


def local_demo():
    x = "local"
    return x


def global_demo():
    global x
    x = "changed by global_demo"


def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        return count
    inner()
    inner()
    return count


print(local_demo(), "|", x)
global_demo()
print(x, "| nonlocal count =", outer())


# Alternative: closure
def make_order():
    order = []

    def add(item):
        order.append(item)
        return list(order)
    return add


c1, c2 = make_order(), make_order()
print("closure:", c1("Tea"), c2("Vada"), c1("Idli"))