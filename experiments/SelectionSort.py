def selection_sort(lst):
    for slot in range(len(lst)-1,0,-1):
        max_idx=0
        for idx in range(1,slot+1):
            if lst[idx]>lst[max_idx]:
                max_idx = idx
        lst[slot], lst[max_idx] = lst[max_idx], lst[slot]

def f(n): #selection sort worst case
    selection_sort(range(n))