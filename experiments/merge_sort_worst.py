def merge_sort(items):
    """ Implementation of mergesort """
    if len(items) > 1:
        mid = len(items) // 2        # Determine the midpoint and split
        left = items[0:mid]
        right = items[mid:]
        merge_sort(left)            # Sort left list in-place
        merge_sort(right)           # Sort right list in-place
        l = 0
        r = 0
        for i in range(len(items)):     # Merging the left and right list
            if l < len(left):
                lval = left[l]
            else:
                lval = None
            if r < len(right):
                rval = right[r]
            else:
                rval = None
            if (lval is not None and rval is not None and lval < rval) or rval is None:
                items[i] = lval
                l += 1
            else:
                items[i] = rval
                r += 1

def f(n): #merge sort worst case
    x = range(n,0,-1) #range(first element, last element+1, step between)
    merge_sort(x)