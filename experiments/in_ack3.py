def f(n):
    return ack(3, n)
    
def ack(ma, na):
    if ma==0:
        return na+1
    if na==0:
        return ack(ma-1, 1)
    return ack(ma-1, ack(ma, na-1))