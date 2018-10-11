from math import (
    ceil, floor, sin, tan, pi
)
from PIL import Image
import numpy as np
from random import randint


class PixelMap:
    def __init__(self, image_size):
        self._pixel_map = np.zeros(image_size)

    def set(self, pixel, superpixel_id):
        if (superpixel_id == 0):
            raise ValueError('superpixel id should not be zero')
        shape = self._pixel_map.shape
        if 0 <= pixel[0] < shape[0] and 0 <= pixel[1] < shape[1]:
            self._pixel_map[pixel] = superpixel_id

    def get(self, pixel):
        shape = self._pixel_map.shape
        if 0 <= pixel[0] < shape[0] and 0 <= pixel[1] < shape[1]:
            return self._pixel_map[pixel]
        return None


class Superpixel:
    def __init__(self):
        self.pixels = set()
        self.edges = set()

    def add(self, pixel, edge=False):
        if edge:
            self.edges.add(pixel)
        self.pixels.add(pixel)


class Tessellator:
    def __init__(self, image_size, cell_size):
        self.superpixel_list = []
        self.pixel_map = PixelMap(image_size)
        self.image_width = image_size[0]
        self.image_height = image_size[1]
        self.cell_size = cell_size
        self.tessellate()

    #   p2 p3
    # p1     p4
    #   p6 p5
    def generate_hexagon_vertexes(self, p1=(0, 0)):
        size = self.cell_size
        h = size * sin(pi/3)
        p2 = (p1[0] + ceil(size/2), ceil(p1[1] - h))
        p6 = (p1[0] + ceil(size/2), ceil(p1[1] + h))
        p4 = (p1[0] + 2*size, p1[1])
        p3 = (p4[0] - ceil(size/2), ceil(p4[1] - h))
        p5 = (p4[0] - ceil(size/2), ceil(p4[1] + h))
        return p2, p3, p4, p5, p6

    def generate_hexagon_pixels(self, p1):
        self.superpixel_list.append(Superpixel())

        def generate_body(y, x1, x2):
            return ((x, y) for x in range(floor(x1), ceil(x2)))

        def append_pixel(pixel, edge=False):
            superpixel = self.superpixel_list[-1]
            superpixel_id = len(self.superpixel_list)
            if self.pixel_map.get(pixel):
                # If the pixel is already assigned to a superpixel,
                # move the pixel to the right.
                pixel = (pixel[0] + 1, pixel[1])
            superpixel.add(pixel, edge)
            self.pixel_map.set(pixel, superpixel_id)

        p2, p3, p4, p5, p6 = self.generate_hexagon_vertexes(p1)

        # upper and lower edge
        for p in generate_body(p2[1] - 1, p2[0] - 1, p3[0]):
            append_pixel(p, edge=True)
        for p in generate_body(p6[1] - 1, p6[0] - 1, p5[0]):
            append_pixel(p, edge=True)

        append_pixel((p1[0] - 1, p1[1]), edge=True)
        append_pixel((p4[0] - 1, p4[1]), edge=True)
        body_pixels_middle = generate_body(p1[1], p1[0] - 1, p4[0] - 1)
        for pixel in body_pixels_middle:
            append_pixel(pixel)

        for y in range(p2[1], p1[1]):
            dy = y - p2[1]
            dx = dy / tan(pi/3)
            append_pixel((floor(p2[0] - dx - 1), y), edge=True)
            append_pixel((floor(p3[0] + dx), y), edge=True)
            body_pixels_upper = generate_body(y,
                                              floor(p2[0] - dx - 1),
                                              floor(p3[0] + dx))
            for pixel in body_pixels_upper:
                append_pixel(pixel)
            if y != p2[1]:
                append_pixel((floor(p2[0] - dx - 1), p1[1]*2 - y), edge=True)
                append_pixel((floor(p3[0] + dx), p1[1]*2 - y), edge=True)
                body_pixels_lower = generate_body(p1[1]*2 - y,
                                                  floor(p2[0] - dx - 1),
                                                  floor(p3[0] + dx))
                for pixel in body_pixels_lower:
                    append_pixel(pixel)

    def tessellate(self):
        h = self.cell_size * sin(pi/3)
        origin = [-self.cell_size, ceil(h)]
        for i in range(ceil(self.image_width / self.cell_size)):
            for j in range(ceil(self.image_height / self.cell_size)):
                self.generate_hexagon_pixels(origin)
                p6_prev_y = ceil(origin[1] + h)
                origin[1] = ceil(p6_prev_y + h)
            origin[0] = ceil(origin[0] + self.cell_size * 3/2) + 1
            origin[1] = 0 if i % 2 == 0 else ceil(h)


def run():
    width = 640
    height = 640
    size = 20

    image = Image.new('RGB', (width, height))
    pixels = image.load()
    tessellator = Tessellator((width, height), size)

    for i, superpixel in enumerate(tessellator.superpixel_list):
        if i < 256:
            color = (255 - i, 0, 255)
        elif 256 <= i < 512:
            color = (0, i - 256, 255)
        else:
            color = (0, 255, 255 - i + 512)
        c = randint(0, 255)
        color = (c, c, 255)

        for x, y in superpixel.pixels:
            if 0 <= x < width and 0 <= y < height:
                if (pixels[x, y] != (0, 0, 0)):
                    pixels[x, y] = (255, 0, 0)
                else:
                    pixels[x, y] = color

    image.show()


if __name__ == "__main__":
    run()
