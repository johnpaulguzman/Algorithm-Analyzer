def merge_sort(items):
    if len(items) > 1:
        mid = len(items) // 2
        left = items[0:mid]
        right = items[mid:]
        merge_sort(left)
        merge_sort(right)
        l = 0
        r = 0
        for i in range(len(items)):
            if l < len(left):
                lval = left[l]
            else:
                lval = None
            if r < len(right):
                rval = right[r]
            else:
                rval = None
            if ((lval is not None and 
                 rval is not None and lval < rval) or 
                 rval is None):
                items[i] = lval
                l += 1
            else:
                items[i] = rval
                r += 1

def f(n): #merge sort worst case
    merge_sort(range(n,0,-1))