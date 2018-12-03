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
require "./passenger.rb"

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
