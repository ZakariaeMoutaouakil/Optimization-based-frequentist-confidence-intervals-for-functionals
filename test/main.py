from test.comparator_formula import comparator_formula
from test.generate_random_tuple import generate_random_tuple
from test.inequality import inequality
from test.majorization import majorization

m = 5
p1 = 0.9
q = 0.1
num = 1000000
assert q < 1 / m, "q must be less than 1 / m"
for i in range(num):
    p = generate_random_tuple(m)
    print("p:", p)
    bool1 = inequality(p, p1, q)
    print("p_[2] >= q:", bool1)
    p_ = comparator_formula(p1, q, m)
    print("sum(p_):", sum(p_))
    print("p_:", p_)
    bool2 = majorization(p_, p)
    print("p majorizes p_:", bool2)
    print(bool1, bool2)
    assert bool1 == bool2, f"Test failed at iteration {p}"

print("Test passed!")
