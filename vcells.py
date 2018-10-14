from math import sqrt
import numpy as np
from PIL import Image
from itertools import product
from tessellator import Tessellator
from util import top_of, right_of, bottom_of, left_of
from random import randint


class OriginalImage:
    def __init__(self, path):
        self._original_image = Image.open(path)
        self.image = Image.open(path)
        self.pixels = self.image.load()
        self.path = path

    @property
    def size(self):
        return self._original_image.size

    def clear_boundary(self):
        self.image = Image.open(self.path)
        self.pixels = self.image.load()

    def set_boundary(self, segment_list, color=(0, 255, 0)):
        self.clear_boundary()
        for segment in segment_list:
#             color = (randint(0, 255), 0, 0)
            for x, y in segment.edges:
                if (0 <= x < self.size[0]
                        and 0 <= y < self.size[1]):
                    self.pixels[x, y] = color

    def getpixel(self, pixel):
        return self._original_image.getpixel(pixel)

    def show(self):
        self.image.show()

    def calc_segment_color_centroid(self, segment):
        s = np.zeros_like(self._original_image.getpixel((0, 0)))
        for pixel in segment.pixels:
            s += np.array(self._original_image.getpixel(pixel))
        return s / len(segment.pixels)


class VCells:
    def __init__(self, path, cell_size, weight, radius=3):
        self.image = OriginalImage(path)
        self.tessellator = Tessellator(self.image.size, cell_size)
        self.weight = weight
        self.radius = radius

        N_omega_base = [p for p in product(range(-radius, radius+1),
                                           range(-radius, radius+1))
                        if p[0]**2 + p[1] ** 2 <= radius ** 2]

        self.pixels_in_N_omega = len(N_omega_base)
        self.N_omega = np.array(N_omega_base)

        for segment in self.tessellator.segment_list:
            c = self.image.calc_segment_color_centroid(segment)
            segment.color_centroid = c

        self.image.set_boundary(self.tessellator.segment_list)
        self.done = False

    def dist(self, pixel, segment):
        color_dist = np.linalg.norm(self.image.getpixel(pixel) -
                                    segment.color_centroid)

        N_omega_p = np.array(self.N_omega)
        N_omega_p[:, 0] += pixel[0]
        N_omega_p[:, 1] += pixel[1]

        seg_N_omega = [p for p in N_omega_p
                       if self.tessellator.pixel_map.get(tuple(p)) == segment.index]
        n_k_of_p = self.pixels_in_N_omega - len(seg_N_omega)
        return sqrt(color_dist**2 + 2 * self.weight * n_k_of_p)

    def iteration(self):
        self.done = True
        i = -1
        for pixel in self.tessellator.boundaries:
            neighbors = self.tessellator.pixel_map.get_neighbors(pixel)
            min_neighbor_index = np.array(
                [self.dist(pixel, self.tessellator.segment_list[n])
                 for n in neighbors]
            ).argmin()
            min_neighbor = neighbors[min_neighbor_index]

            current_segment_index = self.tessellator.pixel_map.get(pixel)

            if min_neighbor != current_segment_index and min_neighbor != -1:
                i += 1
#                 print(pixel, "move:", current_segment_index, "->", min_neighbor, min_neighbor_index)
                self.done = False

                self.tessellator.pixel_map.set(pixel, min_neighbor)

                c_seg = self.tessellator.segment_list[current_segment_index]
                c_seg.remove(pixel)
                c_seg_c = self.image.calc_segment_color_centroid(c_seg)
                c_seg.color_centroid = c_seg_c

                n_seg = self.tessellator.segment_list[min_neighbor]
                n_seg.add(pixel, edge=True)
                n_seg_c = self.image.calc_segment_color_centroid(c_seg)
                n_seg.color_centroid = n_seg_c

                if min_neighbor_index == 0:
                    n_seg.remove_edge(top_of(pixel))
                    c_seg.add(bottom_of(pixel), edge=True, body=False)
                elif min_neighbor_index == 1:
                    n_seg.remove_edge(right_of(pixel))
                    c_seg.add(left_of(pixel), edge=True, body=False)
                elif min_neighbor_index == 2:
                    n_seg.remove_edge(bottom_of(pixel))
                    c_seg.add(top_of(pixel), edge=True, body=False)
                elif min_neighbor_index == 3:
                    n_seg.remove_edge(left_of(pixel))
                    c_seg.add(right_of(pixel), edge=True, body=False)

    def set_boundary(self):
        self.image.clear_boundary()
        self.image.set_boundary(self.tessellator.segment_list)

    def run(self, num_iter):
        for _ in range(num_iter):
            self.iteration()
            self.set_boundary()
#             self.image.show()
            if self.done:
                return


def run():
    vcells = VCells("sample.bmp", 15, 100)
#     vcells = VCells("image_small.png", 10, 300)
    try:
        vcells.run(10000)
    except KeyboardInterrupt:
        vcells.set_boundary()
    vcells.image.show()


if __name__ == "__main__":
    run()
