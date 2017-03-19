def f(n):#4n
    nm1=1
    nm2=0
    for i in range (0,n-1):
        temp=nm1+nm2
        nm2=nm1
        nm1=temp
    return nm1