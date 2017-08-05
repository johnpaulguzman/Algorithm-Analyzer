def f(n):
    nm1=1
    nm2=0
    for i in range(n-1):
        temp=nm1+nm2
        nm2=nm1
        nm1=temp
    return nm1