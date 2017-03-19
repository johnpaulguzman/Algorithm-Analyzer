def linearSearch(alist, item):
    for i in range(0, len(alist)):
        if alist[i] == item:
            return i
    return -1

def f(n):
    x = range(0,n,1)
    linearSearch(x, n-1)