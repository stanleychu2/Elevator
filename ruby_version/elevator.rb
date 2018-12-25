FLOOR_NUM = 6
TOP_FLOOR = FLOOR_NUM - 1
BOTTOM_FLOOR = 0
UP = 0
DOWN = 1

class Elevator
	attr_accessor :command
	
	def initialize()
		@floor_call = Array.new(FLOOR_NUM){[]}
		@car_call = []
		@current_floor = 0
		@direction = 0
		@destination = 0
		@mutex = Mutex.new
	end

	def excute
		loop do
			# 檢查現在這個樓層有沒有人需要上車
			pickup()
			deliver_passenger()
			display_elevator # 可以在稍作修改位置？
			sleep(1)
			# 移動電梯達到樓層
			while(@current_floor != @destination)
				@direction = (@destination > @current_floor ? UP : DOWN)
				@current_floor += (@direction == UP ? 1 : -1)
				# 每到一層查看有無人要上車、下車，接著繼續送客更改目的地
				pickup()
				getoff()
				display_elevator()
				deliver_passenger()
				sleep(1)
			end
		end
	end

	def add_command(command)
		@mutex.synchronize {
			@floor_call[command.from] << command
		}
	end

	def pickup
		@mutex.synchronize {
			if !@floor_call[@current_floor].empty?
				# 防止 destination 被其中一個人更改導致 @current_floor == tempt 這個條件到達樓層時無法進入電梯
				tempt = @destination
				for i in (0...@floor_call[@current_floor].size)
					# puts @floor_call[@current_floor].size.to_s + " ~~~ " +  @current_floor.to_s + " " + @direction.to_s + " " + @floor_call[@current_floor][i].from.to_s + " "  + @floor_call[@current_floor][i].direction.to_s
					# 在到達目的地的途中且方向相同才可以被接上車，或是剛好到達目的地把你接上車
					if((@direction == @floor_call[@current_floor][i].direction && @current_floor == @floor_call[@current_floor][i].from) || (@current_floor == tempt && @car_call.empty?) || @current_floor == TOP_FLOOR || @current_floor == BOTTOM_FLOOR)
						# 當電梯是空的時候，第一個進來的人決定電梯的方向
						@direction = @floor_call[@current_floor][i].direction if @car_call.empty?
						# 到達後告訴電梯想要去哪一個樓層
						to = rand(@floor_call[@current_floor][i].direction == UP ? (@floor_call[@current_floor][i].from + 1)..TOP_FLOOR : BOTTOM_FLOOR..(@floor_call[@current_floor][i].from - 1))
						command = CarCall.new(to)
						@car_call << command
						puts "從 #{@current_floor} 樓要到 #{to} 樓的人上車"
						# 現在新上車的人的目的地比電梯現在的目的地還近且同方向先執行它
						if((@direction == UP && @destination > command.to) || (@direction == DOWN && @destination < command.to))
							@destination = command.to
						end
						@floor_call[@current_floor][i] = nil
						# 電梯剛好到他的目標樓層把人送完，可以直接送這個新進來的人
						if(@destination == @current_floor && @car_call.empty?)
							@destination = command.to
						end
					end
				end
				# 將接起來的人從 floor 的清單裡清除，他已經到達電梯裡了
				@floor_call[@current_floor].delete(nil)
			end
		}
	end

	def getoff
		@mutex.synchronize {
			for i in (0...@car_call.size)
				if(@car_call[i].to == @current_floor)
					@car_call[i] = nil
					puts "有一個人在 #{@current_floor} 樓下車"
				end
			end
			@car_call.delete(nil)
		}
	end

	def deliver_passenger
		@mutex.synchronize {
			# 到達目前目的地，車廂裡還有人先執行車廂裡的人要去的地方
			if(@current_floor == @destination && !@car_call.empty?)
				@destination = @car_call[0].to
				@car_call.each do |command|
					if((@direction == UP && command.to < @destination) || (@direction == DOWN && command.to > @destination))
						@destination = command.to
					end
				end
			# 車廂裡沒有人去載還未上車的乘客，依照他們上車的時間決定
			elsif(@current_floor == @destination && @car_call.empty? && !floor_call_empty?)
				# 挑選一個乘客之後檢查他是不是最先按電梯的人
				for i in @floor_call
					if(i.size > 0)
						tempt = i[0]
						break
					end
				end
				@floor_call.each do |floor|
					floor.each do |command|
						if(command.time < tempt.time)
							tempt = command
						end
					end
				end
				@destination = tempt.from
			end
			# puts "目前目標樓層 #{@destination}"
		}
	end

	def display_elevator
		@mutex.synchronize {
			# puts("main: #{Thread.list[0].status}\npassengger: #{Thread.list[1].status}\nelevator: #{Thread.list[2].status}")
			puts "目前目標樓層: #{@destination}"
			puts @car_call.inspect
			puts("------------------------------------------")
			for i in BOTTOM_FLOOR..TOP_FLOOR
				print(i == @current_floor ? "== " : i.to_s + " ")
			end
			puts(@direction == 0 ? "\n--->" : "\n<---")
			puts("------------------------------------------")
			puts("")
		}
	end

	def floor_call_empty?
		
		for i in @floor_call
			if(i.size > 0)
				return false
			end
		end

		return true
	end
end