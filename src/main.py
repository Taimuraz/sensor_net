from tkinter import *
from enum import Enum
from math import sqrt
import random


class DrawingMode(Enum):
    NONE = 0
    BS = 1
    F = 2
    T = 3


class Node:
    id = 0
    x = 0
    y = 0
    type = 'bs'

    def __init__(self, id=0, x=0, y=0, node_type='bs'):
        self.x = x
        self.y = y
        self.id = id
        self.node_type = node_type

    def __repr__(self):
        return 'id={} x={}, y={}, type={}'.format(self.id, self.x, self.y, self.node_type)


class MainView:

    def __init__(self, master, minimal_distance=0, width=1024, height=700):
        self.bs_color = 'blue'
        self.f_color = 'green'
        self.t_color = 'red'
        self.node_radius = 15
        self.minimal_distance = minimal_distance
        self.mode = DrawingMode.NONE
        self.nodes = []
        self.node_id = 0
        master.resizable(width=False, height=False)
        master.geometry('{}x{}'.format(width, height))
        menu_frame = Frame(master)
        menu_frame.pack(side=RIGHT, anchor='n')

        self.btn_bs = Button(menu_frame, text="Добавить БС")
        self.btn_bs.pack(fill=X)

        self.btn_f = Button(menu_frame, text="Добавить Ф узел")
        self.btn_f.pack(fill=X)

        self.label_wdgt = Label(menu_frame, text="Число T узлов")
        self.label_wdgt.pack(fill=X)

        self.entry_widg = Entry(menu_frame)
        self.entry_widg.insert(0, '9')
        self.entry_widg.pack(fill=X)

        self.btn_t = Button(menu_frame, text="Сгенерировать Т узлы")
        self.btn_t.pack(fill=X)

        self.btn_clean = Button(menu_frame, text="Очистить поле")
        self.btn_clean.pack(fill=X)

        self.btn_exit = Button(menu_frame, text="Выход", fg="red", command=menu_frame.quit)
        self.btn_exit.pack(fill=X)

        self.canvas = Canvas(master, height=height)
        self.canvas.pack(fill=X)

        self.canvas.bind('<Button-1>', self.onCanvasClick)
        self.btn_bs.bind('<Button-1>', self.onButtonClick)
        self.btn_t.bind('<Button-1>', self.onButtonClick)
        self.btn_f.bind('<Button-1>', self.onButtonClick)
        self.btn_clean.bind('<Button-1>', self.onButtonClick)

    def isValidDistance(self, x, y):
        result = True
        critical_distance = self.minimal_distance + 2 * self.node_radius
        for node in self.nodes:
            distance = sqrt((x - node.x) ** 2 + (y - node.y) ** 2)
            if distance < critical_distance:
                result = False
        return result

    def drawCircle(self, x, y, node_color, node_type):
        make_step = True
        if node_type == 'bs':
            if self.isBsAdded():
                make_step = False

        if make_step:
            if self.isValidDistance(x, y):
                self.node_id += 1
                self.nodes.append(Node(self.node_id, x, y, node_type))
                self.canvas.create_oval([x - self.node_radius, y - self.node_radius],
                                        [x + self.node_radius, y + self.node_radius], fill=node_color)
        print(self.nodes)

    def isBsAdded(self):
        result = False
        for node in self.nodes:
            if node.type == 'bs':
                result = True
        return result

    def onCanvasClick(self, event):
        x = event.x
        y = event.y
        if self.mode == DrawingMode.BS:
            self.drawCircle(x, y, self.bs_color, 'bs')
        elif self.mode == DrawingMode.F:
            self.drawCircle(x, y, self.f_color, 'f')

    def btnRelief(self, btn):
        if btn['relief'] == 'raised':
            btn['relief'] = SUNKEN
        else:
            btn['relief'] = RAISED

    def cleanCanvas(self):
        self.canvas.delete('all')
        del self.nodes[:]

    def generateT(self):
        for i in range(int(self.entry_widg.get())):
            x = random.uniform(0, 500)
            y = random.uniform(0, 500)
            self.drawCircle(x, y, 'yellow', 't')

    def onButtonClick(self, event):
        btn_name = str(event.widget).split('!')[2]
        if btn_name == 'button':
            self.mode = DrawingMode.BS
        elif btn_name == 'button2':
            self.mode = DrawingMode.F
        elif btn_name == 'button3':
            self.generateT()
        elif btn_name == 'button4':
            self.cleanCanvas()


root = Tk()
canv = Canvas(root, width=30, height=30)
canv.pack()
app = MainView(root, minimal_distance=20)

root.mainloop()
root.destroy()  # optional; see description below
