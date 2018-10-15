def top_of(pixel):
    return pixel[0], pixel[1] - 1


def right_of(pixel):
    return pixel[0] + 1, pixel[1]


def left_of(pixel):
    return pixel[0] - 1, pixel[1]


def bottom_of(pixel):
    return pixel[0], pixel[1] + 1


def direct_neighbors_of(pixel):
    yield (pixel[0], pixel[1] - 1)
    yield (pixel[0] + 1, pixel[1])
    yield (pixel[0], pixel[1] + 1)
    yield (pixel[0] - 1, pixel[1])
    raise StopIteration
