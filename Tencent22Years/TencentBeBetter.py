import turtle as t
from math import *

pen = t.Turtle()


def ellipse(m, n, a):
    """描绘椭圆"""
    t.goto(m, n)
    t.setheading(0)
    t.pd()              # 画笔落下
    t.begin_fill()
    b = a / 5
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a = a + b
            t.lt(3)
            t.fd(a)
        else:
            a = a - b
            t.lt(3)
            t.fd(a)     # 向前
    t.end_fill()
    t.pu()      # 画笔抬起
    return


t.screensize(400, 400, 'white')
t.pensize(4)
t.pencolor('black')
t.speed(0)
t.ht()
t.pu()
# 头部轮廓
t.goto(150, 100)
t.setheading(90)
t.pd()
t.fillcolor('black')
t.begin_fill()
t.circle(200, 180)
t.lt(60)
t.circle(400, 60)
t.end_fill()
# 围脖
t.fillcolor('red')
t.pensize(3)
t.begin_fill()
t.rt(60)
t.circle(-60, 60)
t.rt(60)
t.circle(-460, 60)
position1 = t.pos()
t.rt(60)
t.circle(-60, 60)
t.rt(60)
t.circle(400, 60)
t.end_fill()
t.pu()

# 眼睛
t.pencolor('white')
t.fillcolor('white')
ellipse(0, 130, 0.5)
ellipse(-100, 130, 0.5)
t.pencolor('black')
t.fillcolor('black')
ellipse(-10, 160, 0.18)
ellipse(-90, 160, 0.18)

# 嘴
t.goto(-180, 98)
t.pd()
t.pencolor('orange')
t.fillcolor('orange')
t.pd()
t.setheading(30)
t.begin_fill()
t.circle(-260, 60)
t.rt(120)
t.circle(-260, 60)
t.end_fill()
t.pu()
# 微笑
t.goto(-150, 99)
t.setheading(-30)
t.fillcolor('black')
t.begin_fill()
t.circle(200, 60)
t.rt(150)
t.circle(-115.47, 120)
t.end_fill()
t.pu()

# t.done()
t.goto(-50, -100)
t.color('skyblue')
t.write('Tencent 腾讯', font=('Arial', 36), align='center')
t.color('darkorange')
t.goto(-50, -150)
t.write('22 Year Be Better!!', font=('Arial', 28), align='center')
t.ht()

t.done()
