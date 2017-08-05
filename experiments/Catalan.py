def f(n): 
    if n <=0:
        return 1 
    res = 0 
    for i in range(n):
        res += f(i) * f(n-i-1)
    return res