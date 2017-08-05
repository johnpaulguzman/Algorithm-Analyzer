def f(n): 
    big_nested_sum=0
    for i in range(n):
        for j in range(i):
            for k in range(j):
                big_nested_sum+=k