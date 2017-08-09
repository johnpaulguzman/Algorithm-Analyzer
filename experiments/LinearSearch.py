def linearSearch(alist, item):
    for i in range(0, len(alist)):
        if alist[i] == item:
            return i
    return -1

def f(n):
    linearSearch(range(n), n-1)