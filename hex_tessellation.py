from math import (
    ceil, floor, sin, tan, pi
)
from PIL import Image


def draw(image, x, y, color):
    if 0 <= x < width and 0 <= y < height:
        pixels[x, y] = color


def generate_horizontal_pixels(y, x1, x2):
    return [(x, y) for x in range(floor(x1), ceil(x2+1))]


#   p2 p3
# p1     p4
#   p6 p5
def generate_hexagon_vertexes(size, p1=(0, 0)):
    h = size * sin(pi/3)
    p2 = (p1[0] + ceil(size/2), ceil(p1[1] - h))
    p6 = (p1[0] + ceil(size/2), ceil(p1[1] + h))
    p4 = (p1[0] + 2*size, p1[1])
    p3 = (p4[0] - ceil(size/2), ceil(p4[1] - h))
    p5 = (p4[0] - ceil(size/2), ceil(p4[1] + h))
    return p2, p3, p4, p5, p6


def generate_hexagon_pixels(size, p1=(0, 0), edges=False):
    result = []
    p2, p3, p4, p5, p6 = generate_hexagon_vertexes(size, p1)
    result.extend(generate_horizontal_pixels(p1[1], p1[0], p4[0]))

    for y in range(p2[1] - 1, p1[1]):
        dy = y - p2[1]
        dx = dy / tan(pi/3)
        result.extend(generate_horizontal_pixels(y, p2[0] - dx, p3[0] + dx))
        if y != p2[1] - 1:
            result.extend(
                generate_horizontal_pixels(p1[1]*2 - y, p2[0]-dx, p3[0]+dx)
            )

    return result


def generate_hexagon_edges(size, p1=(0, 0)):
    result = []
    p2, p3, p4, p5, p6 = generate_hexagon_vertexes(size, p1)
    result.extend(generate_horizontal_pixels(p2[1], p2[0], p3[0]))
    result.extend(generate_horizontal_pixels(p6[1], p6[0], p5[0]))
    # 左端はp1の1ピクセル左
    result.append((p1[0] - 1, p1[1]))
    # 右端はp4の1ピクセル左
    result.append((p4[0] - 1, p4[1]))

    for y in range(p2[1] - 1, p1[1]):
        dy = y - p2[1]
        dx = dy / tan(pi/3)
        result.append((p2[0] - dx - 1, y))
        result.append((p3[0] + dx, y))
        if y != p2[1] - 1:
            result.append((p2[0] - dx - 1, p1[1]*2 - y))
            result.append((p3[0] + dx, p1[1]*2 - y))

    return result


def hex_generator(img_width, img_height, size, edges=False):
    h = size * sin(pi/3)
    origin = [10, 100]
    for i in range(ceil(img_width / size)):
        for j in range(ceil(img_height / size)):
            if edges:
                yield generate_hexagon_edges(size, origin)
            else:
                yield generate_hexagon_pixels(size, origin)
            raise StopIteration
            p6_prev_y = ceil(origin[1] + h)
            origin[1] = ceil(p6_prev_y + h)
        origin[0] = ceil(origin[0] + size * 3/2) + 1
        origin[1] = 0 if i % 2 == 0 else ceil(h)


width = 640
height = 640
size = 20

image = Image.new('RGB', (width, height))
pixels = image.load()

for i, hex_pixels in enumerate(hex_generator(width, height, size, True)):
    for x, y in hex_pixels:
        if i < 256:
            color = (255 - 20*i, 0, 255)
        elif 256 <= i < 512:
            color = (0, i - 256, 255)
        else:
            color = (0, 255, 255 - i*20 + 512)

        if 0 <= x < width and 0 <= y < height:
            if (pixels[x, y] != (0, 0, 0)):
                pixels[x, y] = (255, 0, 0)
            else:
                pixels[x, y] = color

image.show()
