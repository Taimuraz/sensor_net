from tkinter import *
from enum import Enum


class DrawingMode(Enum):
    NONE = 0
    BS = 1
    F = 2
    T = 3


class MainView:
    def __init__(self, master, width=1024, height=700):
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

        self.canvas = Canvas(master, bg='green', height=height)
        self.canvas.pack(fill=X)

        self.canvas.bind('<Button-1>', self.onCanvasClick)
        self.btn_bs.bind('<Button-1>', self.onButtonClick)
        self.btn_t.bind('<Button-1>', self.onButtonClick)
        self.btn_f.bind('<Button-1>', self.onButtonClick)

    def onCanvasClick(self, event):
        x = event.x
        y = event.y
        r = 30
        self.canvas.create_oval([x - r, y - r], [x + r, y + r], fill='blue')

        if self.mode == DrawingMode.BS:
            pass
        elif self.mode == DrawingMode.F:
            pass
        elif self.mode == DrawingMode.T:
            pass

    def btnRelief(self, btn):
        if btn['relief'] == 'raised':
            btn['relief'] = SUNKEN
        else:
            btn['relief'] = RAISED

    def onButtonClick(self, event):
        btn_name = str(event.widget).split('!')[2]
        print(btn_name)
        self.btnRelief(self.btn_bs)
        # if btn_name == 'botton':


root = Tk()
canv = Canvas(root, width=30, height=30)
canv.pack()
app = MainView(root)

root.mainloop()
root.destroy()  # optional; see description below
