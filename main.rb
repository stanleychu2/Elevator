#!/usr/local/bin/ruby

=begin

shared memory : 
- 電梯裡的乘客
- 每一個樓層的乘客
- 電梯的方向
- 電梯現在所處樓層

Thread :
- 乘客產生
- 電梯啟動

=end

require "./elevator.rb"
require "./call.rb"

def create_passenger(elevator)
	loop do
		# puts("main: #{Thread.list[0].status}\npassengger: #{Thread.list[1].status}\nelevator: #{Thread.list[2].status}")
		from = rand(FLOOR_NUM)
		direction = nil 

		if(from == BOTTOM_FLOOR)
			direction = UP
		elsif(from == TOP_FLOOR)
			direction = DOWN
		else
			direction = rand(2)
		end
		puts("有一個人在 #{from} 樓想要向#{(direction == UP ? '上' : '下')}")
		puts(direction == UP ? "--->\n\n" : "<---\n\n")
		command = FloorCall.new(from, direction)
		elevator.add_command(command)
		sleep(rand(8) + 1)
		# sleep(3)
	end
end

# main porgram
elevator = Elevator.new
threads = []
threads << Thread.new {create_passenger(elevator)}
threads << Thread.new {elevator.excute()}
# 防止主程式結束後所有的 threas 跟著終止
for i in threads
	i.join()
end
# end of main program
