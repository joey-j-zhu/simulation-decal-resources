import Vector
import math
SPEED = 1
DAMP = 1

class Grid2D:
    def __init__(self, initial_value, x_size, y_size, x_length, y_length):
        self.x_size, self.y_size = x_size, y_size
        self.x_spacing, self.y_spacing = x_length / self.x_size, y_length / self.y_size
        #self.components = [[eval(initial_value)] * x_size] * y_size
        self.components = []
        for y in range(y_size):
            temp = []
            for x in range(x_size):
                cell = eval(initial_value)
                cell.place(Vector.Vector([x * self.x_spacing - x_length / 2, y * self.y_spacing - y_length / 2]))
                temp.append(cell)
            self.components.append(temp)

        self.fields = []
        self.t = 0
        self.function = lambda: 0

    def get(self, x, y):
        return self.components[y][x]

    def add_field(self, field):
        self.fields.append(field)

    #Set the function for each grid cell to evaluate to go the next step in the simulation. Variables native to the
    #Grid class will be in scope, but remember that the Cell object is calling the function.
    def set_particle_function(self, func):
        self.function = func

    def step(self, h):
        sys = self
        func = self.function
        for y in range(self.y_size):
            for x in range(self.x_size):
                #Actual non-state position of the particle
                p = self.components[y][x].real_position
                self.function(self.components[y][x], self, x, y, p, self.t)

        for y in range(self.y_size):
            for x in range(self.x_size):
                self.components[y][x].step(h)
        self.t += h

    def set(self, value, x, y):
        self.components[y][x] = value

    def ker(self, kernel, *index, wrap=True):
        assert len(index) == 2
        x_offset = len(kernel) // 2
        y_offset = len(kernel[0]) // 2
        total = 0
        for y_ in range(len(kernel)):
            for x_ in range(len(kernel[0])):
                #x = (index[0] - x_offset + x_) % self.x_size
                #y = (index[1] - y_offset + y_) % self.y_size
                x, y = index[0] - x_offset + x_, index[1] - y_offset + y_

                if y < 0 or y >= self.y_size or x < 0 or x >= self.x_size:
                    0
                else:
                    total += kernel[y_][x_] * self.get(x, y).state_pos

        return total


def laplacian():
        return [[0.25, 0.5, 0.25],
                [0.5, -3, 0.5],
                [0.25, 0.5, 0.25]]

def nine_point():
    return [[0, 0, -3/120, 0, 0],
            [0, 8/120, 56/120, 8/120, 0],
            [-3/120, 56/120, 476/120, 56/120, -3/120],
            [0, 8/120, 56/120, 8/120, 0],
            [0, 0, -3/120, 0, 0]]

class Cell:
    def __init__(self, state_type):
        self.state_pos = eval(state_type)
        self.state_vel = eval(state_type)
        self.stage_pos = None
        self.stage_vel = None

    def place(self, pos):
        self.real_position = pos

    def manual_set(self, pos, vel):
        self.state_pos = pos
        self.state_vel = vel

    def manual_adjust(self, pos, vel):
        self.state_pos += pos
        self.state_vel += vel

    def stage_change(self, pos, vel):
        self.stage_pos, self.stage_vel = pos, vel

    def step(self, h):
        self.state_pos += self.stage_pos * h
        self.state_vel += self.stage_vel * h

#Implementations for different general PDEs
def wave_eq(self, sys, x, y, p, t):
    change = 0
    for f in sys.fields:
        change += f(p, t)
    self.stage_change(self.state_vel,
                      SPEED * sys.ker(laplacian(), x, y) + change)

def heat_eq(self, sys, x, y, p, t):
    change = 0
    for f in sys.fields:
        change += f(p, t)
    self.stage_change(SPEED * sys.ker(laplacian(), x, y) + change, 0)


#Define a field that takes in position and time as arguments. This particular function creates a binary orbit between
#a positive and negative source.

#q = width of source
#a = radius of orbit
#f = frequency of orbit
#n = amplitude of source

def orbit_source(q, a, f, n, f2):
    def field_func(p, t):
        def atan_deriv(r):
            return n * q * q / (q * q + r.norm_squared())
        return atan_deriv(p - Vector.Vector([a * math.cos(f * t), a * math.sin(f * t)])) - \
               atan_deriv(p - Vector.Vector([a * -math.cos(f * t), a * -math.sin(f * t)]))
    return field_func

#test_case is a particular simulation to be exported into the render, with resolution SIZE x SIZE. Edit and tweak
#the simulation here.
SIZE = 128
def test_case():
    g = Grid2D("Cell('0')", SIZE, SIZE, SIZE, SIZE)
    g.set_particle_function(heat_eq)
    g.add_field(orbit_source(3, 8, 1, 500, 2))
    g.add_field(orbit_source(3, 16, 2, -500, 2))
    return g


