def quick_sort(items):
    if len(items) > 1:
        pivot_index = 0
        smaller_items = []
        larger_items = []
        for i, val in enumerate(items):
            if i != pivot_index:
                if val < items[pivot_index]:
                    smaller_items.append(val)
                else:
                    larger_items.append(val)
        quick_sort(smaller_items)
        quick_sort(larger_items)
        items[:] = (smaller_items+
            [items[pivot_index]]+larger_items)

def f(n): #quick_sort sort worst case
    quick_sort(range(n,0,-1))