def f(n):
    return ack(2, n)
    
def ack(m, n):
    if m==0:
        return n+1
    if n==0:
        return ack(m-1, 1)
    return ack(m-1, ack(m, n-1))