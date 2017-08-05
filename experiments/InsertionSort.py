def insertion_sort(items):
    for i in range(1, len(items)):
        j = i
        while j > 0 and items[j] < items[j-1]:
            items[j],items[j-1] = items[j-1],items[j]
            j -= 1

def f(n): #insertion sort worst case
    x = range(n,0,-1)
    insertion_sort(x)