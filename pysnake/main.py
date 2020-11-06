import pyglet
from pyglet.shapes import Rectangle
from pyglet.window import key
from collections import namedtuple
from typing import List
from random import randint

class Window(pyglet.window.Window):
    """
    the gamewindow
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.dim = Point(10,10)
        self.box_count = Point(self.width//self.dim.x, self.height//self.dim.y)
        self.snake: List[Point] = [Point(5,5),Point(5,6)]
        self.dir = Point(1,0)
        self.place_foot()
        self.points = 0
        self.point_label = pyglet.text.Label(f"Points {self.points}", x=10,y=self.height-20)


    def on_key_press(self, symbol, modifiers):
        newdir = Point(0,0)
        if symbol == key.W:
            newdir = Point(0,1)
        elif symbol == key.D:
            newdir = Point(1,0)
        elif symbol == key.S:
            newdir = Point(0,-1)
        elif symbol == key.A:
            newdir = Point(-1,0)
        if newdir + self.dir != Point(0,0):
            self.dir = newdir
        
    def on_draw(self):
        self.clear()
        self.point_label.draw()
        for ele in self.snake:
            Rectangle(ele.x*self.dim.x,ele.y*self.dim.y,self.dim.x,self.dim.y).draw()
        if self.foot:
            Rectangle(self.foot.x*self.dim.x,self.foot.y*self.dim.y,self.dim.x,self.dim.y,color=(255,0,0)).draw()

    def update(self,*args,**kwargs):
        self.move_snake()

    def move_snake(self):
        new_ele = self.snake[-1]+self.dir
        if new_ele == self.snake[-2]:
            return
        
        # Border Collision
        if new_ele.x > self.box_count.x or new_ele.y > self.box_count.y:
            self.gameover()
            return

        # self collision
        for ele in self.snake:
            if ele == new_ele:
                self.gameover()
                return

        if not self.eat_foot():
            self.snake.pop(0)
        self.snake.append(self.snake[-1]+self.dir)

    def place_foot(self):
        while True:
            foot = Point(randint(0,self.box_count.x),randint(0,self.box_count.y))
            for ele in self.snake:
                if ele == foot:
                    break
            break
        self.foot = foot

    def eat_foot(self) -> bool:
        for ele in self.snake:
            if ele == self.foot:
                self.place_foot()
                self.points += 10
                self.point_label.text = f"Points {self.points}"
                self.on_draw()
                return True
        return False

    def gameover(self):
        self.close()

class Point(object):
    """
    Point things
    """
    def __init__(self, x, y) -> None:	
        self.x = x
        self.y = y

    def __add__(self, point_obj):
        return Point(self.x+point_obj.x,self.y+point_obj.y)

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

if __name__ == "__main__":
    win = Window(800,600)
    pyglet.clock.schedule_interval(win.update, 0.15)
    pyglet.app.run()
    