import math

class Vector:
    def __init__(self, components):
        self.components = components

    def set(self, index, value):
        self.components[index] = value

    def __add__(self, other):
        total = Vector([0] * len(self.components))
        for i in range(len(self.components)):
            total.set(i, self.components[i] + other.components[i])
        return total

    def __sub__(self, other):
        diff = Vector([0] * len(self.components))
        for i in range(len(self.components)):
            diff.set(i, self.components[i] - other.components[i])
        return diff

    def __mul__(self, other):
        v = Vector([0] * len(self.components))
        for i in range(len(self.components)):
            v.set(i, self.components[i] * other)
        return v

    def scale(self, factor, copy=False):
        if copy:
            v = Vector([0] * len(self.components))
            for i in range(len(self.components)):
                v.set(i, self.components[i] * factor)
            return v
        else:
            for i in range(len(self.components)):
                self.set(i, self.components[i] * factor)
            return self

    def norm(self):
        return math.sqrt(self.norm_squared())

    def norm_squared(self):
        total = 0
        for i in self.components:
            total += i * i
        return total

    def __str__(self):
        return str(self.components)




def zero(dim):
    return Vector([0] * dim)




