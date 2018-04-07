from tkinter import *
from enum import Enum


class DrawingMode(Enum):
    NONE = 0
    BS = 1
    F = 2
    T = 3


class MainView:
    def __init__(self, master, width=1024, height=700):
        self.bs_color = 'blue'
        self.f_color = 'green'
        self.t_color = 'red'
        self.bs_radius = 40
        self.f_radius = 30
        self.t_radius = 20
        self.mode = DrawingMode.NONE

        master.resizable(width=False, height=False)
        master.geometry('{}x{}'.format(width, height))

        menu_frame = Frame(master)
        menu_frame.pack(side=RIGHT, anchor='n')

        self.btn_bs = Button(menu_frame, text="БС")
        self.btn_bs.pack(fill=X)

        self.btn_f = Button(menu_frame, text="Ф узел")
        self.btn_f.pack(fill=X)

        self.btn_t = Button(menu_frame, text="Т узел")
        self.btn_t.pack(fill=X)

        self.btn_exit = Button(menu_frame, text="Выход", fg="red", command=menu_frame.quit)
        self.btn_exit.pack(fill=X)

        self.canvas = Canvas(master, height=height)
        self.canvas.pack(fill=X)

        self.canvas.bind('<Button-1>', self.onCanvasClick)
        self.btn_bs.bind('<Button-1>', self.onButtonClick)
        self.btn_t.bind('<Button-1>', self.onButtonClick)
        self.btn_f.bind('<Button-1>', self.onButtonClick)

    def onCanvasClick(self, event):
        x = event.x
        y = event.y

        if self.mode == DrawingMode.BS:
            self.canvas.create_oval([x - self.bs_radius, y - self.bs_radius], [x + self.bs_radius, y + self.bs_radius],
                                    fill=self.bs_color)

        elif self.mode == DrawingMode.F:
            self.canvas.create_oval([x - self.f_radius, y - self.f_radius], [x + self.f_radius, y + self.f_radius],
                                    fill=self.f_color)

        elif self.mode == DrawingMode.T:
            self.canvas.create_oval([x - self.t_radius, y - self.t_radius], [x + self.t_radius, y + self.t_radius],
                                    fill=self.t_color)

    def btnRelief(self, btn):
        if btn['relief'] == 'raised':
            btn['relief'] = SUNKEN
        else:
            btn['relief'] = RAISED

    def onButtonClick(self, event):
        btn_name = str(event.widget).split('!')[2]
        if btn_name == 'button':
            self.mode = DrawingMode.BS
        elif btn_name == 'button2':
            self.mode = DrawingMode.F
        elif btn_name == 'button3':
            self.mode = DrawingMode.T


root = Tk()
canv = Canvas(root, width=30, height=30)
canv.pack()
app = MainView(root)

root.mainloop()
root.destroy()  # optional; see description below
