from elevator import *
from PIL import Image, ImageTk

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

app = app()
app.mainloop()
