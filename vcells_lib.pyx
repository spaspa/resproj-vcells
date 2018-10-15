import cython
import numpy as np
cimport numpy as np
from libc.math cimport sqrt

DTYPE_I = np.int32
ctypedef np.int32_t DTYPE_I_t

DTYPE_F = np.float64
ctypedef np.float64_t DTYPE_F_t

@cython.boundscheck(False)
def calc_seg_n_omega(int center_x,
                     int center_y,
                     np.ndarray[DTYPE_I_t, ndim=2] base_n_omega,
                     np.ndarray[DTYPE_I_t, ndim=2] raw_pixel_map,
                     int segment_index):
    cdef int w_max = raw_pixel_map.shape[0]
    cdef int h_max = raw_pixel_map.shape[1]
    cdef int n_omega_p_length = base_n_omega.shape[0]
    cdef int result = 0
    cdef int x, y, i

    for i in range(n_omega_p_length):
        x = base_n_omega[i, 0] + center_x
        y = base_n_omega[i, 1] + center_y
        if x < w_max and y < h_max and raw_pixel_map[x, y] == segment_index:
            result += 1

    return result


def dist(int pixel_x,
         int pixel_y,
         np.ndarray[DTYPE_F_t, ndim=1] segment_centroid,
         np.ndarray[DTYPE_I_t, ndim=2] base_n_omega,
         np.ndarray[DTYPE_I_t, ndim=2] raw_pixel_map,
         np.ndarray[DTYPE_I_t, ndim=3] raw_pixel,
         int segment_index,
         int pixels_in_N_omega,
         double weight):
    cdef double color_dist2 = ((segment_centroid[0] - raw_pixel[pixel_y, pixel_x, 0]) ** 2
                               + (segment_centroid[1] - raw_pixel[pixel_y, pixel_x, 1]) ** 2
                               + (segment_centroid[2] - raw_pixel[pixel_y, pixel_x, 2]) ** 2)

    cdef int pixels_seg_n_omega = calc_seg_n_omega(pixel_x,
                                                   pixel_y,
                                                   base_n_omega,
                                                   raw_pixel_map,
                                                   segment_index)

    cdef int n_k_of_p = pixels_in_N_omega - pixels_seg_n_omega

    cdef double result = sqrt(color_dist2 + 2 * weight * n_k_of_p)
    return result


def calc_color_centroid(np.ndarray[DTYPE_I_t, ndim=2] pixels,
                        np.ndarray[DTYPE_I_t, ndim=3] raw_pixel):
    cdef int size = pixels.shape[0]
    cdef int w = raw_pixel.shape[0]
    cdef int h = raw_pixel.shape[1]
    cdef int i, x, y
    cdef np.ndarray[DTYPE_F_t, ndim=1] result = np.zeros_like(raw_pixel[0, 0], dtype=DTYPE_F)

    for i in range(size):
        x = pixels[i, 0]
        y = pixels[i, 1]
        if x < w and y < h:
            result[0] += raw_pixel[y, x, 0]
            result[1] += raw_pixel[y, x, 1]
            result[2] += raw_pixel[y, x, 2]

    result[0] /=  size
    result[1] /=  size
    result[2] /=  size

    return result
