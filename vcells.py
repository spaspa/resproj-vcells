from math import sqrt
import numpy as np
from PIL import Image
from itertools import product
from tessellator import Tessellator
from vcells_util import (
    top_of, right_of, bottom_of, left_of,
    direct_neighbors_of
)
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include()]})
from vcells_lib import dist, calc_color_centroid # noqa


class OriginalImage:
    def __init__(self, path):
        self._original_image = Image.open(path)
        self.raw_pixel = np.asarray(self._original_image, dtype=np.int32)
        self.image = Image.open(path)
        self.pixels = self.image.load()
        self.path = path
        self.animation_list = []

    @property
    def size(self):
        return self._original_image.size

    def clear_boundary(self):
        self.animation_list.append(self.image)
        self.image = Image.open(self.path)
        self.pixels = self.image.load()

    def set_boundary(self, segment_list, color=(0, 255, 0)):
        self.clear_boundary()
        for segment in segment_list:
            color = (0, segment.index, 0)
            for x, y in segment.edges:
                if (0 <= x < self.size[0]
                        and 0 <= y < self.size[1]):
                    self.pixels[x, y] = color

    def getpixel(self, pixel):
        return self._original_image.getpixel(pixel)

    def show(self):
        self.image.show()

    def save(self, path):
        self.image.save(path)

    def calc_segment_color_centroid(self, segment):
        conv = np.array(list(segment.pixels), dtype=np.int32)
        return calc_color_centroid(conv, self.raw_pixel)

    def save_animation(self, path):
        self._original_image.save(path,
                                  save_all=True,
                                  optimize=False,
                                  duration=200,
                                  loop=0,
                                  append_images=self.animation_list)


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
        self.N_omega = np.array(N_omega_base, dtype=np.int32)

        for segment in self.tessellator.segment_list:
            c = self.image.calc_segment_color_centroid(segment)
            segment.color_centroid = c

        self.image.set_boundary(self.tessellator.segment_list)
        self.done = False

    def get_segment_of(self, pixel):
        return self.tessellator.segment_list[
            self.tessellator.pixel_map.get(pixel)
        ]

    def iteration(self):
        self.done = True
        pixels_moved = 0
        w, h, _ = self.image.raw_pixel.shape
        for pixel in self.tessellator.boundaries:
            if pixel[0] >= w or pixel[1] >= h:
                continue
            neighbors = self.tessellator.pixel_map.get_neighbors(pixel)
            min_neighbor_index = np.array(
                [dist(pixel[0], pixel[1],
                      self.tessellator.segment_list[n].color_centroid,
                      self.N_omega,
                      self.tessellator.pixel_map.get_raw_pixel_map(),
                      self.image.raw_pixel,
                      self.tessellator.segment_list[n].index,
                      self.pixels_in_N_omega,
                      self.weight)
                 for n in neighbors]
            ).argmin()
            min_neighbor = neighbors[min_neighbor_index]

            current_segment_index = self.tessellator.pixel_map.get(pixel)

            if min_neighbor != current_segment_index and min_neighbor != -1:
                pixels_moved += 1
#                 print(pixel, "move:", current_segment_index, "->", min_neighbor, min_neighbor_index)
                self.done = False

                self.tessellator.pixel_map.set(pixel, min_neighbor)
                self.tessellator.pixel_map.set_around_neighbor_to(pixel, min_neighbor)

                c_seg = self.tessellator.segment_list[current_segment_index]
                c_seg.remove(pixel)

                if len(c_seg.pixels) != 0:
                    c_seg_c = self.image.calc_segment_color_centroid(c_seg)
                    c_seg.color_centroid = c_seg_c

                n_seg = self.tessellator.segment_list[min_neighbor]
                n_seg.add(pixel, edge=True)
                n_seg_c = self.image.calc_segment_color_centroid(n_seg)
                n_seg.color_centroid = n_seg_c

                for i, n in enumerate(direct_neighbors_of(pixel)):
                    seg = self.get_segment_of(n)
                    if self.tessellator.pixel_map.is_edge(n):
                        seg.add(n, edge=True, body=False)
#                         print("edge-", end="")
                    else:
                        seg.remove_edge(n)
#                         print("non-edge-", end="")
#                     print(f"pixel:{n} {i} of {pixel}\n"
#                           f"   {self.tessellator.pixel_map.get(top_of(n))}\n"
#                           f"{self.tessellator.pixel_map.get(left_of(n))}    {self.tessellator.pixel_map.get(right_of(n))}\n"
#                           f"   {self.tessellator.pixel_map.get(bottom_of(n))}\n")

        return pixels_moved

    def set_boundary(self):
        self.image.set_boundary(self.tessellator.segment_list)

    def run(self, num_iter):
        for i in range(num_iter):
            moved = self.iteration()
            print(f"iter {i}: {moved} pixel moved")
            self.set_boundary()
            if self.done:
                return


def run():
#     vcells = VCells("sample.bmp", 20, 500)
    vcells = VCells("image.png", 10, 100)
    try:
        vcells.run(100)
    except KeyboardInterrupt:
        vcells.set_boundary()
    vcells.image.save_animation("result.gif")
    vcells.image.show()


if __name__ == "__main__":
    run()
