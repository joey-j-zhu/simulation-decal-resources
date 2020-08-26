from tkinter import Tk, Canvas, Frame, BOTH
import Grid
import time
import math


g = Grid.test_case()

SPACE = 8
AMP = 1
STEP = 0.05

root = Tk()
canvas = Canvas(root, width=1024, height=1024)
canvas.pack()

def c(r, g, b, check_cap=False):
    if check_cap:
        return '#%02x%02x%02x' % (max(min(int(r), 255), 0), max(min(int(g), 255), 0), max(min(int(b), 255), 0))
    else:
        return '#%02x%02x%02x' % (r, g, b)

while True:
    for i in range(3):
        g.step(STEP)
    canvas.delete("all")
    for y in range(g.y_size):
        for x in range(g.x_size):
        # color = hex(math.floor(min(255, AMP * g.get(x, y).state_pos)))
        # color *= 3
            color = c(g.get(x, y).state_pos * AMP * -1,
                      g.get(x, y).state_pos * AMP,
                      g.get(x, y).state_pos * AMP * 2,

                      True)

            canvas.create_rectangle(x * SPACE, y * SPACE, x * SPACE + SPACE, y * SPACE + SPACE,
                                        fill=color, outline="")
    canvas.update()
    #time.sleep(0.05)