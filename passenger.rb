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