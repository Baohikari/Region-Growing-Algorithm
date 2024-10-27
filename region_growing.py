import cv2
import numpy as np
import itertools

class Stack():
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        return self.items.pop() if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0

class RegionGrowing():
    def __init__(self, img_path, threshold):
        self.image = cv2.imread(img_path, 1).astype('int')
        self.h, self.w, _ = self.image.shape
        self.passed_by = np.zeros((self.h, self.w), np.double)
        self.current_region = 0
        self.segs = np.zeros((self.h, self.w, 3), dtype='uint8')
        self.stack = Stack()
        self.threshold = float(threshold)

    def get_neighbors(self, x0, y0):
        return [
            (x, y)
            for i, j in itertools.product((-1, 0, 1), repeat=2)
            if (i, j) != (0, 0) and self.boundaries(x := x0 + i, y := y0 + j)
        ]

    def boundaries(self, x, y):
        return 0 <= x < self.h and 0 <= y < self.w

    def apply_region_growing(self, seeds):
        for seed in seeds:
            x0, y0 = seed
            if self.passed_by[x0, y0] == 0:
                self.current_region += 1
                self.passed_by[x0, y0] = self.current_region
                self.stack.push((x0, y0))

                while not self.stack.is_empty():
                    x, y = self.stack.pop()
                    self.bfs(x, y)

        self.color_pixels()

    def bfs(self, x0, y0):
        region_num = self.passed_by[x0, y0]
        neighbors = self.get_neighbors(x0, y0)

        for x, y in neighbors:
            if self.passed_by[x, y] == 0 and self.distance(x, y, x0, y0) < self.threshold:
                self.passed_by[x, y] = region_num
                self.stack.push((x, y))

    def distance(self, x, y, x0, y0):
        return np.linalg.norm(self.image[x0, y0] - self.image[x, y])

    def color_pixels(self):
        for i in range(self.h):
            for j in range(self.w):
                val = self.passed_by[i][j]
                self.segs[i][j] = (255, 255, 255) if (val == 0) else (val * 35, val * 90, val * 30)

    def get_segmented_image(self):
        return self.segs
