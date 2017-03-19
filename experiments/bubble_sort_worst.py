def bubble_sort(items):
    """ Implementation of bubble sort """
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]  

def f(n): #bubble sort worst case
    x = range(n,0,-1) #range(first element, last element+1, step between)
    bubble_sort(x)