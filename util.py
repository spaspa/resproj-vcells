from numba import jit


@jit('i4(i4[:])')
def top_of(pixel):
    return pixel[0], pixel[1] - 1


@jit('i4(i4[:])')
def right_of(pixel):
    return pixel[0] + 1, pixel[1]


@jit('i4(i4[:])')
def left_of(pixel):
    return pixel[0] - 1, pixel[1]


@jit('i4(i4[:])')
def bottom_of(pixel):
    return pixel[0], pixel[1] + 1
