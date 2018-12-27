import threading
from passenger import * 

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