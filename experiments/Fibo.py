def f(n):
    fibo(n)
    
def fibo(n):
    if(n<=2):
        return 1
    else:
        return fibo(n-1) + fibo(n-2)