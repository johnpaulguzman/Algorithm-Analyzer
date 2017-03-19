def f(n): 
    big_nested_sum=0
    for i in range(0 ,n):
        for j in range(0, i):
            for k in range(0, j):
                big_nested_sum+=k