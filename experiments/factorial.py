def f(n):
    if n==0:
        return 1
    else:
        for i in range(0, n):
            f(n-1)