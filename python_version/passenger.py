import random
from call import *
import time, math
from tkinter import *

FLOOR_NUM = 6
TOP_FLOOR = FLOOR_NUM - 1
BOTTOM_FLOOR = 0
UP = 0
DOWN = 1

def poisson(mean) :
    l = math.exp(-mean)
    k = 0
    p = 1.0

    while(True) :
        p = p * random.random()
        k += 1
        if(p <= l) :
            break

    return k - 1 

def create_passenger(elevator):
    while(True) :
        source = random.randint(0, TOP_FLOOR)
        direction = None

        if(source == BOTTOM_FLOOR) :
            direction = UP
        elif(source == TOP_FLOOR):
            direction = DOWN
        else:
            direction = random.randint(0, 1)
        command = FloorCall(source, direction)
        elevator.add_command(command, source, direction)
        # 在某一層產生一個乘客那個樓層那個方向的乘客 + 1
        new_num = int(elevator.canvas.itemconfig(elevator.up_down_text[source][direction])["text"][4]) + 1
        elevator.canvas.itemconfig(elevator.up_down_text[source][direction], text=str(new_num))
        print("sleep possion")
        time.sleep(poisson(5))
        
def passenger_anim(elevator,floor,passenger):
        a = elevator.canvas.create_image(455,(5-floor)*120+50,image=passenger,anchor=NW)
        print("passenger_anim")
        time.sleep(0.25)
        for i in range(70):  
            elevator.canvas.move(a,5,0)
            time.sleep(0.25)
        elevator.canvas.delete(a)