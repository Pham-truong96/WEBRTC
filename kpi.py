import math 


def KPIresolution(t):
    e = 2.718
    return 0.003 * e**(0.064*t) + 2.498

def KPIfps(fps):
    if fps >=30:
        return 5
    if fps <=2:
        return 1
    return 1.07504 * math.log(3.42171*fps)
