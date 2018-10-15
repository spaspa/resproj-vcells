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


def dist_2_neighbors_of(pixel):
    yield (pixel[0] - 3, pixel[1])
    yield (pixel[0] - 2, pixel[1] - 2)
    yield (pixel[0] - 2, pixel[1] - 1)
    yield (pixel[0] - 2, pixel[1])
    yield (pixel[0] - 1, pixel[1] - 2)
    yield (pixel[0] - 1, pixel[1] - 1)
    yield (pixel[0] - 1, pixel[1])
    yield (pixel[0], pixel[1] - 3)
    yield (pixel[0], pixel[1] - 2)
    yield (pixel[0], pixel[1] - 1)
    yield (pixel[0], pixel[1])
    yield (pixel[0], pixel[1] + 3)
    yield (pixel[0], pixel[1] + 2)
    yield (pixel[0], pixel[1] + 1)
    yield (pixel[0], pixel[1])
    yield (pixel[0] + 1, pixel[1] + 2)
    yield (pixel[0] + 1, pixel[1] + 1)
    yield (pixel[0] + 1, pixel[1])
    yield (pixel[0] + 2, pixel[1] + 2)
    yield (pixel[0] + 2, pixel[1] + 1)
    yield (pixel[0] + 2, pixel[1])
    yield (pixel[0] + 3, pixel[1])
    raise StopIteration
