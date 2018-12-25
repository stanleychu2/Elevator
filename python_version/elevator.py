#!/usr/local/bin/python3

import random, time, threading
import datetime as date
import math
from tkinter import *

FLOOR_NUM = 6
TOP_FLOOR = FLOOR_NUM - 1
BOTTOM_FLOOR = 0
UP = 0
DOWN = 1

class FloorCall() :
	def __init__(self, source, direction) :
		self.time = date.datetime.now()
		self.source = source
		self.direction = direction

class CarCall() :
	def __init__(self, to) :
		self.to = to

class Elevator():
	def __init__(self):
		self.floor_call = [[] for i in range(6)]
		self.car_call = []
		self.current_floor = 0
		self.direction = 0
		self.destination = 0
		self.mutex = threading.Lock()

	def execute(self):
		while(True) :
			self.pickup()
			self.deliver_passenger()
			self.display_elevator()
			time.sleep(1)
			while(self.current_floor != self.destination) :
				self.direction = (UP if self.destination > self.current_floor else DOWN)
				self.current_floor += (1 if self.direction == UP else -1)
				# 每到一層查看有無人要上車、下車，接著繼續送客更改目的地
				self.pickup()
				self.getoff()
				self.display_elevator()
				self.deliver_passenger()
				time.sleep(1) 

	def pickup(self) :
		self.mutex.acquire()
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
					self.car_call.append(command)
					print("從 {} 樓要到 {} 樓的人上車".format(self.current_floor, to))
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

	def getoff(self) :
		self.mutex.acquire()
		for i in range(0, len(self.car_call)) :
			if(self.car_call[i].to == self.current_floor) :
				self.car_call[i] = None
				print("有一個人在 {} 樓下車".format(self.current_floor))
		self.car_call[:] = (value for value in self.car_call if value != None)
		self.mutex.release()

	def add_command(self, command) :
		self.mutex.acquire()
		self.floor_call[command.source].append(command)
		self.mutex.release()

	def deliver_passenger(self) : 
		self.mutex.acquire()
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

	def display_elevator(self) :
		self.mutex.acquire()
		print("目前目標樓層: {}".format(self.destination))
		print(self.car_call_toString())
		print("------------------------------------------")
		for i in range(BOTTOM_FLOOR, TOP_FLOOR + 1) :
			print("== " if i == self.current_floor else str(i) + " ", end="")
		print("\n--->" if self.direction == 0 else "\n<---")
		print("------------------------------------------")
		print("")
		self.mutex.release()

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
		#source = random.randint(0, TOP_FLOOR)
		source = TOP_FLOOR-1
		direction = None

		if(source == BOTTOM_FLOOR) :
			direction = UP
		elif(source == TOP_FLOOR):
			direction = DOWN
		else:
			direction = random.randint(0, 1)
		print("有一個人在 {} 樓想要向{}".format(source, '上' if direction == UP else '下'))
		print("--->\n\n" if direction == UP else "<---\n\n")
		command = FloorCall(source, direction)
		elevator.add_command(command)
		time.sleep(poisson(4))

# main porgram
gui = Tk()
gui.configure(background = 'light green')
gui.geometry("500x300")
button = Button(gui, text='Stop', width=25, command=exit())
button.pack()

gui.mainloop()

elevator = Elevator()
threads = []
threads.append(threading.Thread(target = elevator.execute))
threads.append(threading.Thread(target = create_passenger, args = (elevator,)))
threads[0].start()
threads[1].start()

for i in threads:
	i.join()




# end of main program