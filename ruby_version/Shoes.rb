FLOOR_NUM = 6
TOP_FLOOR = FLOOR_NUM
BOTTOM_FLOOR = 1
UP = 0
DOWN = 1

class FloorCall
    attr_accessor :from, :direction, :time

    def initialize(from, direction)
        @time = Time.now
        @from = from
        @direction = direction
    end
end

class CarCall
    attr_accessor :to
    
    def initialize(to)
        @to = to
    end
end

class Passenger < Shoes::Widget 
    
    def initialize(opts = {}) 
        @prom = opts[:stack]
        @prom.append do
            @text = para ""
        end 
    end 

    def poisson(mean)   
        l = Math.exp(-mean)
        k = 0
        p = 1.0

        loop do
            p = p * rand
            k += 1
            if p <= l
                break           
            end
        end

        return k - 1
    end

    def create(elevator)
        from = rand(FLOOR_NUM) + 1
        direction = nil 

        if(from == BOTTOM_FLOOR)
            direction = UP
        elsif(from == TOP_FLOOR)
            direction = DOWN
        else
            direction = rand(2)
        end
        # 普法松隨機變數以 4 為平均去產生客人等待時間
        number = poisson(4)
        @text.text = "有一個人在 #{from} 樓想要向#{(direction == UP ? '上' : '下')}\n#{direction == UP ? "--->" : "<---"}\n#{number} 秒之後更新"
        command = FloorCall.new(from, direction)
        elevator.add_command(command)
        timer(number) {self.create(elevator)} 
    end 

end

class Elevator < Shoes::Widget
    attr_accessor :command
    
    def initialize(stack, current_floor_text)
        @image = rect(350, 603, 100, 120, fill: gray, strokewidth: 2, stroke: black)
        @debug = para "1", left: 350, top: 500
        stack.app do
        stack.append do 
            @image
            @debug
            @anim
        end
    end
        # 0 樓不會用到所以要 + 1
        @floor_call = Array.new(FLOOR_NUM + 1){[]}
        @car_call = []
        @current_floor = 1
        @direction = 0
        @destination = 1
        @mutex = Mutex.new
        @anim_stopped = true
        @y_coordinate = 603
        @current_floor_text = current_floor_text
        @anim = nil
    end

    def excute
        loop do
            # 移動電梯達到樓層
            # while(@current_floor != @destination)
            #     @direction = (@destination > @current_floor ? UP : DOWN)
            #     @current_floor += (@direction == UP ? 1 : -1)
            #     # 每到一層查看有無人要上車、下車，接著繼續送客更改目的地
            #     pickup()
            #     getoff()
            #     display_elevator()
            #     deliver_passenger()
            #     sleep(1)
            # end
            if @anim_stopped
                pickup()
                deliver_passenger() 
            end
            while(@current_floor != @destination)
                if(@anim_stopped)
                    @anim_stopped = false
                    @direction = (@destination > @current_floor ?  UP : DOWN)
                    @anim = animate(48) do |frame|
                        # 調數字比較有效果控制快慢
                        @image.move(350, @y_coordinate += -3 * (@direction == UP ? 1 : -1))
                        @debug.text = "#{@destination} #{frame}"
                        arrive_floor(@y_coordinate)
                    end
                end

                # if @current_floor == @destination 
                #     @debug.text = "Stop"
                #     @anim.remove
                #     @anim_stopped = true
                # end
            end
        end
    end

    def arrive_floor(y)
        @current_floor = 6 if y == 3
        @current_floor = 5 if y == 123
        @current_floor = 4 if y == 243
        @current_floor = 3 if y == 363
        @current_floor = 2 if y == 483
        @current_floor = 1 if y == 603
        @current_floor_text.replace(@current_floor)
                if @current_floor == @destination 
                    @debug.text = "Stop"
                    @anim.remove
                    @anim_stopped = true
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
                        # puts "從 #{@current_floor} 樓要到 #{to} 樓的人上車"
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
                    # puts "有一個人在 #{@current_floor} 樓下車"
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

    def floor_call_empty?
        
        for i in @floor_call
            if(i.size > 0)
                return false
            end
        end

        return true
    end
end

Shoes.app(title:"Elevator", width: 1000, height: 722, resizable: false) do
    background("#EEC".."#996", margin: 2)
    #=========================================================

    column_1 = stack(left:0, top:0, width: 800, height: 722) do 
        border(black, strokewidth: 3)

        #=========================================================    

        for k in (1..6)
            rect(2, (6 - k) * 120 + 2, 348, 120, fill: white, strokewidth: 2, stroke: black)
            para "上 : #{0}  下 : #{0}", left: 50, top: (6 - k) * 120 + 45 
            rect(450, (6 - k) * 120 + 2, 348, 120, fill: white, strokewidth: 2, stroke: black)
        end

        #=========================================================

        # static_dir = File.expand_path(File.join(__FILE__, ".."))
        # image(File.join(static_dir, "1.jpg"), left: 2, top: 452)

        #=========================================================
    end

    #==========================================================   

    stack(left: 800, top: 0, width: 200, height: 436) do           
        border(black,strokewidth: 3)
        flow(left: 75, top: 30, width: 50) do
            %w[6 5 4 3 2 1].each do |btn|
                button(btn, width: 50, height: 60) do
                    case btn
                        when '6'
                            @floor = 6
                        when '5'
                            @floor = 5
                        when '4'
                            @floor = 4
                        when '3'
                            @floor = 3
                        when '2'
                            @floor = 2
                        when '1'
                            @floor = 1             
                    end
                end
            end
        end  
    end

    stack(left: 800, top: 436, width: 200, height: 286) do
        border(black,strokewidth: 3)
        @o = rect(50, 63, 100, 100, fill: yellow, strokewidth: 3, stroke: white)
        @current_floor_text = para("1", left: 85, top: 88, size: 30)
    end

    @elevator = elevator(column_1, @current_floor_text)
    @client = passenger({top: 50, left: 20, width: 200, stack: column_1}) 
    button "Start" do
        @a = Thread.new { @client.create(@elevator) }
        @b = Thread.new { @elevator.excute() }
    end
    button "Exit" do
        Thread.kill(@a)
        Thread.kill(@b)
        exit
    end
end 
