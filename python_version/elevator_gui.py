from tkinter import *
from PIL import Image, ImageTk
import random, time, threading
import datetime as date
import math

FLOOR_NUM = 6
TOP_FLOOR = FLOOR_NUM - 1
BOTTOM_FLOOR = 0
UP = 0
DOWN = 1


class app(Tk):

    def __init__(self, *args, **kwargs):
        # TK 初始化
        Tk.__init__(self, *args, **kwargs)
        self.title("Elevator")
        self.geometry("1100x720")
        #用frame裝其他視窗
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #設定圖片
        self.image = []
        self.img = Image.open("image/up.gif")
        self.up_image = ImageTk.PhotoImage(self.img)
        self.img2 = Image.open("image/down.gif")
        self.down_image = ImageTk.PhotoImage(self.img2)
        self.img3 = Image.open("image/student.png")
        self.student_image = ImageTk.PhotoImage(self.img3)
        self.img4 = Image.open("image/elevator.png")
        self.elevator_image = ImageTk.PhotoImage(self.img4)
        self.img5 = Image.open("image/professor.png")
        self.professor_image = ImageTk.PhotoImage(self.img5)
        self.img6 = Image.open("image/background.png")
        self.background_image = ImageTk.PhotoImage(self.img6)
        self.image.append(self.up_image)
        self.image.append(self.down_image)
        self.image.append(self.student_image)
        self.image.append(self.elevator_image)
        self.image.append(self.professor_image)
        self.image.append(self.background_image) 
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            #視窗創建
            frame = F(container, self,self.image)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    

        
class StartPage(Frame):

    def __init__(self, parent, controller,image):
        Frame.__init__(self,parent)

        background_label = Label(self,image=image[5])
        background_label.place(x=0,y=0)

        label = Label(self, text="OS FINAL PROJECT", font=("Verdana", 50),bg='orange')
        label.place(x=250,y=50)

        button = Button(self, text="DEMO",font=("Verdana", 30),width=10,bg='orange',
                            command=lambda: controller.show_frame(PageOne))
        button.place(x=450,y=370)

        button2 = Button(self, text="EXIT",font=("Verdana", 30),width=10,bg='orange',
                            command=lambda: controller.show_frame(PageTwo))
        button2.place(x=450,y=470)

#############################################################################################################

class PageOne(Frame):

    def __init__(self, parent, controller,image):
        Frame.__init__(self, parent,bg="orange")
        canvas = Canvas(self, width= 800, height=720, bd=0, highlightthickness=0, bg="gray")
        canvas.pack(side = LEFT)
        # 每一層樓要上樓或是下樓的人數(還沒有進電梯)
        up_down_text = [[] for i in range(6)]
        # 一定要是 gif 圖片才能顯示()
        
        up_image = image[0]
        down_image = image[1]
        
        for i in range(6) :
            canvas.create_rectangle(0, i * 120, 350, (i + 1) * 120, fill='white')
            canvas.create_image(25, i * 120 + 10, image=up_image, anchor=NW)
            canvas.create_image(172, i * 120 + 20, image=down_image, anchor=NW)
            canvas.create_text(18, 20 + i * 120, text=str(6 - i), font=("Comic Sans", 20))
            up_down_text[5 - i] = [canvas.create_text(130, i * 120 + 60, text="0", font=("Comic Sans", 50)), canvas.create_text(275, i * 120 + 60, text="0", font=("Comic Sans", 50))]
            canvas.create_rectangle(450, i * 120, 800, (i + 1) * 120, fill='white')
        
        text = StringVar() 

        down_sign = Label(self, text= "▼", bg="#424135",fg="gray", font=("Comic Sans", 50), borderwidth=0, relief="solid")
        floor = Label(self, text= "1", bg="#424135",fg="yellow", font=("Local baseball park", 50), textvariable=text, borderwidth=0, relief="solid")
        up_sign = Label(self, text= "▲", bg="#424135",fg="gray", font=("Comic Sans", 50), borderwidth=0, relief="solid")
        
        up_down_sign = []
        up_down_sign.append(down_sign)
        up_down_sign.append(up_sign)

        line = Label(self, text="", bg = 'black')

        left = Frame(self, bg="orange")
        right = Frame(self, bg="orange")
        left.place(x=800, y=38, width=150, height=420)
        right.place(x=950, y=38, width=150, height=420)

        floor_num = [None for i in range(6)]
        for i in range(3) :
            num = Label(left, text=str(i + 1 + i * 1), font=("Local baseball park", 40), borderwidth = 3, relief="solid")
            num.pack(side=TOP, padx=20, pady=20, ipadx=35, ipady=20)
            floor_num[2 * i] = num
        for i in range(3) :
            num = Label(right, text=str(i + 2 + i * 1), font=("Local baseball park", 40), borderwidth = 3, relief="solid")
            num.pack(side=TOP, padx=20, pady=20, ipadx=35, ipady=20)
            floor_num[2 * i + 1] = num
        line.place(x=800, y=479, width=300, height=3)
        down_sign.place(x=845,y=550,width=70,height=100)
        floor.place(x=915, y=550, width=70, height=100)
        up_sign.place(x=985,y=550,width=70,height=100)

        # main porgram
        elevator = Elevator(canvas, self, text, floor_num, up_down_text, image,up_down_sign)
        threads = []
        threads.append(threading.Thread(target=elevator.execute))
        threads.append(threading.Thread(target=create_passenger, args=(elevator,)))
        def start_thread(threads):
            threads[0].start()
            threads[1].start()
        
        # end of main program
        Button(self,text='Start',font=(20) ,width=20,command=lambda: start_thread(threads)).pack()
        
        Button(self, text="Back to Home",width=20,command=lambda: controller.show_frame(StartPage)).pack(side=BOTTOM)

##########################################################################################


class PageTwo(Frame):

    def __init__(self, parent, controller,image):
        
        Frame.__init__(self, parent,bg ="orange")

        background_label = Label(self,image=image[5])
        background_label.place(x=0,y=0)

        label = Label(self, text="THANK YOU", font=("Verdana", 60),bg='orange')
        label.pack(padx=10,pady=200)
        
#############################  elevator logic ############################################
class FloorCall() :

    def __init__(self, source, direction) :
        self.time = date.datetime.now()
        self.source = source
        self.direction = direction
 
class CarCall() :

    def __init__(self, to) :
        self.to = to

class Elevator():

    def __init__(self, canvas, root, text, floor_num, up_down_text,image,up_down_sign):
        self.floor_call = [[] for i in range(6)]
        self.car_call = []
        self.current_floor = 0
        self.direction = 0
        self.destination = 0
        self.mutex = threading.Lock()
        self.root = root
        self.canvas = canvas
        self.image = canvas.create_image(350, 595,image=image[3],anchor=NW)
        self.text = text
        self.floor_num = floor_num
        self.up_down_text = up_down_text
        self.student_image = image[2]
        self.professor_image = image[4]
        self.down_sign = up_down_sign[0]
        self.up_sign = up_down_sign[1]
        text.set("1")

    def execute(self):
        while(True) :
            print("第一次")
            self.pickup()
            self.deliver_passenger()
            self.display_elevator()
            print("sleep 1 one")
            time.sleep(1)
            while(self.current_floor != self.destination) :
                self.direction = (UP if self.destination > self.current_floor else DOWN)
                self.current_floor += (1 if self.direction == UP else -1)
                #position = canvas.coords(self.image)
                print("anim start")
                plus = -2 if self.direction == UP else 2
                for i in range(60):
                    self.canvas.move(self.image,0,plus)               
                    self.root.update()
                    time.sleep(0.025)
                
                #self.canvas.move(self.image, 0, -120 if self.direction == UP else 120)
                #self.root.update()

                self.down_sign.config(fg='yellow' if self.direction == DOWN else 'gray')
                self.text.set(str(self.current_floor + 1))
                self.up_sign.config(fg='yellow' if self.direction == UP else 'gray')
                print("anim end")
                # 每到一層查看有無人要上車、下車，接著繼續送客更改目的地
                print("第二次")
                self.pickup()
                self.getoff()
                self.display_elevator()
                self.deliver_passenger()
                print("sleep 1 two")
                time.sleep(1) 

    def pickup(self) :
        self.mutex.acquire()
        print("pickup start")
        if(self.floor_call[self.current_floor]) :
            tempt = self.destination
            for i in range(len(self.floor_call[self.current_floor])) : 
                if((self.direction == self.floor_call[self.current_floor][i].direction and self.current_floor == self.floor_call[self.current_floor][i].source) or (self.current_floor == tempt and not self.car_call) or self.current_floor == TOP_FLOOR or self.current_floor == BOTTOM_FLOOR) :
                    # 當電梯是空的時候，第一個進來的人決定電梯的方向
                    if(not self.car_call) :
                        self.direction = self.floor_call[self.current_floor][i].direction
                    # 到達後告訴電梯想要去哪一個樓層
                    to = random.randint(self.floor_call[self.current_floor][i].source + 1, TOP_FLOOR) if self.floor_call[self.current_floor][i].direction == UP else random.randint(BOTTOM_FLOOR, self.floor_call[self.current_floor][i].source - 1)
                    command = CarCall(to)
                    #time.sleep(1)
                    self.car_call.append(command)
                    self.floor_num[to].config(bg="yellow")
                    #time.sleep(1)
                    print("從 {} 樓要到 {} 樓的人上車".format(self.current_floor, to))
                    # 進電梯之後外面等待的人便少一
                    new_num = int(self.canvas.itemconfig(self.up_down_text[self.current_floor][self.floor_call[self.current_floor][i].direction])["text"][4]) -1
                    self.canvas.itemconfig(self.up_down_text[self.current_floor][self.floor_call[self.current_floor][i].direction], text=str(new_num))
                    # 現在新上車的人的目的地比電梯現在的目的地還近且同方向先執行它
                    if((self.direction == UP and self.destination > command.to) or (self.direction == DOWN and self.destination < command.to)) :
                        self.destination = command.to
                    self.floor_call[self.current_floor][i] = None
                    # 電梯剛好到他的目標樓層把人送完，可以直接送這個新進來的人
                    if(self.destination == self.current_floor and not self.car_call) :
                        self.destination = command.to
            # 將接起來的人從 floor 的清單裡清除，他已經到達電梯裡了
            self.floor_call[self.current_floor][:] = (value for value in self.floor_call[self.current_floor] if value != None)
        self.mutex.release()
        print("pickup end")

    def getoff(self) :
        self.mutex.acquire()
        print("getoff start")
        for i in range(0, len(self.car_call)) :
            if(self.car_call[i].to == self.current_floor) :
                self.car_call[i] = None
                print("有一個人在 {} 樓下車".format(self.current_floor)) 
                #使用thread來產生乘客動畫(避免影響電梯運作)
                time.sleep(0.5)        
                t = threading.Thread(target= passenger_anim, args= (self,self.current_floor,self.student_image if random.randint(0,1) == 0 else self.professor_image))
                t.start()

        self.car_call[:] = (value for value in self.car_call if value != None)
        self.floor_num[self.current_floor].config(bg="white")
        self.mutex.release()
        print("getoff end")

    def add_command(self, command, source, direction) :
        self.mutex.acquire()
        print("add_command start")
        print("有一個人在 {} 樓想要向{}".format(source, '上' if direction == UP else '下'))
        print("--->\n\n" if direction == UP else "<---\n\n")
        self.floor_call[command.source].append(command)
        self.mutex.release()
        print("add_command end")

    def deliver_passenger(self) :
        self.mutex.acquire()
        print("deliver_passenger start")
        # 到達目前目的地，車廂裡還有人先執行車廂裡的人要去的地方
        if(self.current_floor == self.destination and self.car_call) :
            self.destination = self.car_call[0].to
            for command in self.car_call :
                if((self.direction == UP and command.to < self.destination) or (self.direction == DOWN and command.to > self.destination)) :
                    self.destination = command.to
        # 車廂裡沒有人去載還未上車的乘客，依照他們上車的時間決定
        elif(self.current_floor == self.destination and not self.car_call and not self.floor_call_empty()) :
            # 挑選一個乘客之後檢查他是不是最先按電梯的人
            for i in self.floor_call :
                if(len(i) > 0) :
                    tempt = i[0]
                    break
            for floor in self.floor_call :
                for command in floor :
                    if(command.time < tempt.time):
                        tempt = command
            self.destination = tempt.source
            # puts "目前目標樓層 #{@destination}"
        self.mutex.release()
        print("deliver_passenger end")

    def display_elevator(self) :
        self.mutex.acquire()
        print("display_elevator start")
        print("目前目標樓層: {}".format(self.destination))
        print(self.car_call_toString())
        print("------------------------------------------")
        for i in range(BOTTOM_FLOOR, TOP_FLOOR + 1) :
            print("== " if i == self.current_floor else str(i) + " ", end="")
        print("\n--->" if self.direction == 0 else "\n<---")
        print("------------------------------------------")
        print("")
        self.mutex.release()
        print("display_elevator end")

    def floor_call_empty(self) :
        for i in self.floor_call : 
            if(len(i) > 0):
                return False

        return True

    def car_call_toString(self) :
        text = "["
        for i in self.car_call :
            text += str(i.to) + ", "

        return text + "]"

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
#################################################################################################################

app = app()
app.mainloop()