def f(n):
    if(n<=5):
        return 1
    else:
        return f(n-1)+f(n-2)+f(n-3)+f(n-4)