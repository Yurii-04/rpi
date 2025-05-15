def f(x):
    if -2.4 <= x <= 5.7:
        return x ** 2
    else:
        return 4

test_values = [-3, -2.4, 0, 5.7, 6]
for x in test_values:
    print(f"f({x}) = {f(x)}")