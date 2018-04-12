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
    node_type = 'bs'

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
        self.achivable_radius = 150
        self.minimal_distance = minimal_distance
        self.mode = DrawingMode.NONE
        self.nodes = []
        self.node_id = 0
        self.x_min = 10000
        self.x_max = 0
        self.y_min = 10000
        self.y_max = 0
        self.adjacency_map = []  # словарь смежности графа.
        self.message_time = 0  # время передачи сообщения

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
        self.entry_widg.insert(0, '4')
        self.entry_widg.pack(fill=X)

        self.btn_t = Button(menu_frame, text="Сгенерировать Т узлы")
        self.btn_t.pack(fill=X)

        self.label_time = Label(menu_frame, text="Время передачи сообщения")
        self.label_time.pack(fill=X)

        self.entry_time = Entry(menu_frame)
        self.entry_time.insert(0, '3')
        self.entry_time.pack(fill=X)

        self.btn_path = Button(menu_frame, text="Определить кратчайшие пути")
        self.btn_path.pack(fill=X)

        self.btn_clean = Button(menu_frame, text="Очистить поле")
        self.btn_clean.pack(fill=X)

        self.btn_exit = Button(menu_frame, text="Выход", fg="red", command=menu_frame.quit)
        self.btn_exit.pack(fill=X)

        self.canvas = Canvas(master, height=height, background='white')
        self.canvas.pack(fill=X)

        self.canvas.bind('<Button-1>', self.onCanvasClick)
        self.btn_bs.bind('<Button-1>', self.onButtonClick)
        self.btn_t.bind('<Button-1>', self.onButtonClick)
        self.btn_f.bind('<Button-1>', self.onButtonClick)
        self.btn_clean.bind('<Button-1>', self.onButtonClick)
        self.btn_path.bind('<Button-1>', self.onButtonClick)

    def isValidDistance(self, x, y):
        result = True
        critical_distance = self.minimal_distance + 2 * self.node_radius
        for node in self.nodes:
            distance = sqrt((x - node.x) ** 2 + (y - node.y) ** 2)
            if distance < critical_distance:
                result = False
        return result

    def defineBounds(self, x, y):
        if x < self.x_min: self.x_min = x
        if x > self.x_max: self.x_max = x
        if y < self.y_min: self.y_min = y
        if y > self.y_max: self.y_max = y

    def isBsAdded(self):
        result = False
        for node in self.nodes:
            if node.node_type == 'bs':
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
        self.x_min = 10000
        self.x_max = 0
        self.y_min = 10000
        self.y_max = 0

    def drawCircle(self, x, y, node_color, node_type):
        make_step = True
        if node_type == 'bs':
            if self.isBsAdded():
                make_step = False

        if make_step:
            if self.isValidDistance(x, y):
                self.nodes.append(Node(id=self.node_id, x=x, y=y, node_type=node_type))
                self.defineBounds(x, y)
                self.canvas.create_text(x + self.node_radius, y - self.node_radius, text=str(self.node_id))
                self.node_id += 1
                self.canvas.create_oval([x - self.node_radius, y - self.node_radius],
                                        [x + self.node_radius, y + self.node_radius],
                                        fill=node_color)
            else:
                return False
        return True
        # print(self.y_min,"  ",self.y_max)

    def drawLine(self, x0, y0, x1, y1, color='black', width=1.0):
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def getAchivableNodes(self, current_node):
        res = []
        for node in self.nodes:
            if node.id != current_node.id:
                distance = sqrt((current_node.x - node.x) ** 2 + (current_node.y - node.y) ** 2)
                if distance <= self.achivable_radius:
                    res.append(node)
        return res

    def generateEdges(self):
        tmp_list = []
        self.achivable_radius = max(self.x_max - self.x_min,
                                    self.y_max - self.y_min) / 2  # максимальное расстояние между узлами делим пополам.
        for i in range(len(self.nodes)):  # это и есть радиус досигаемости
            neighbours = self.getAchivableNodes(self.nodes[i])
            for neighbour_node in neighbours:
                self.drawLine(self.nodes[i].x, self.nodes[i].y, neighbour_node.x, neighbour_node.y)
                tmp_list.append(neighbour_node.id)
            self.adjacency_map.append(tmp_list.copy())
            tmp_list.clear()

    def generateT(self):
        iter = 0
        for i in range(int(self.entry_widg.get())):
            x = random.uniform(self.x_min, self.x_max)
            y = random.uniform(self.y_min, self.y_max)
            res = self.drawCircle(x, y, 'yellow', 't')
            if res == False:
                while res != True:
                    x = random.uniform(self.x_min, self.x_max)
                    y = random.uniform(self.y_min, self.y_max)
                    res = self.drawCircle(x, y, 'yellow', 't')
                    if iter > 1000: break
                    iter += 1
        self.generateEdges()

    def onButtonClick(self, event):
        btn_name = str(event.widget).split('!')[2]
        if btn_name == 'button':
            self.mode = DrawingMode.BS
        elif btn_name == 'button2':
            self.mode = DrawingMode.F
        elif btn_name == 'button3':
            self.generateT()
        elif btn_name == 'button4':
            self.createPathways()
        elif btn_name == 'button5':
            self.cleanCanvas()

    def getMinimalPath(self, pathways):
        min = 1000
        result = []
        for path in pathways:
            if len(path) < min:
                min = len(path)
                result = path
        return result

    def createPathways(self):
        self.message_time = int(self.entry_time.get())
        bs_node = self.nodes[0]
        f_nodes = []
        for node in self.nodes:
            if node.node_type == 'f':
                f_nodes.append(node)

        # search path ==========================
        for f_node in f_nodes:
            p = PathSearcher(adj_list=self.adjacency_map, start_node=bs_node.id, target_node=f_node.id)
            pathways = p.getMinimalPathways(max_path_length=self.message_time)
            print("id = ", f_node.id, "================================= ")
            for path in pathways:
                print(path)
            # ====================== draw minimal pathways
            for path in pathways:
                for i in range(len(path) - 1):
                    self.drawLine(self.nodes[path[i]].x, self.nodes[path[i]].y, self.nodes[path[i + 1]].x,
                                  self.nodes[path[i + 1]].y, color='red', width=3.0)


class PathSearcher:
    def __init__(self, adj_list, start_node, target_node):
        self.adj_list = adj_list
        self.start_node = start_node
        self.target_node = target_node
        self.visited = [False] * len(self.adj_list)
        self.level = [-1] * len(self.adj_list) # уровни вершин
        self.pathways = []
        self.path = []


    def getAllPathways(self, curr_node):
        self.visited[curr_node] = True
        self.path.append(curr_node)

        if curr_node == self.target_node:
            self.pathways.append(self.path.copy())
        else:
            for node in self.adj_list[curr_node]:
                if not self.visited[node]:
                    self.getAllPathways(node)
        self.visited[curr_node] = False
        self.path.pop()

    def getMinimalPathways(self, max_path_length):
        result = []
        self.getAllPathways(self.start_node)

        for path in self.pathways:
           if len(path) - 1 <= max_path_length:
               result.append(path)
        return result

if __name__ == '__main__':
    # adj = [
    #     # список смежности
    #     [1, 3, 5],  # 0
    #     [0, 4, 5],  # 1
    #     [4, 5],  # 2
    #     [0, 4, 5],  # 3
    #     [1, 2, 3],  # 4
    #     [0, 1, 2, 3]  # 5
    # ]
    #
    # p = PathSearcher(adj_list=adj, start_node=0, target_node=5)
    # p.getMinimalPathways()

    root = Tk()
    canv = Canvas(root, width=30, height=30)
    canv.pack()
    app = MainView(root, minimal_distance=10)

    # # test purposes
    # app.drawCircle(150, 200, 'blue', 'bs')
    # app.drawCircle(200, 300, 'green', 'f')
    # app.drawCircle(500, 300, 'green', 'f')
    # app.drawCircle(400, 100, 'green', 'f')
    # app.generateT()
    # # for node in app.adjacency_map:
    # #     print(node)
    # app.createPathways()

    root.mainloop()
    root.destroy()  # optional; see description below
