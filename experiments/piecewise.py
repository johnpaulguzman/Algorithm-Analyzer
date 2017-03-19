def f(x):
    loops = 0
    if x<100:
        loops = x*5
    else:
        if x<200:
            loops = x*10
        else:
            if x<300:
                loops = x*15
            else:
                loops = x*20
    for i in xrange(loops):
        t=0