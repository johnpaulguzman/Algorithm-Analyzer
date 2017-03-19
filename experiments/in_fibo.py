def f(n):
    fibo(n)
    
def fibo(na):
    if(na<=2):
        return 1
    else:
        return fibo(na-1) + fibo(na-2)