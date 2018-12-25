class Passenger
	attr_accessor :i , :start , :from
	def initialize(app,from,direction,floor_position,start)
		static_dir = File.expand_path(File.join(__FILE__, ".."))
		@start =start
		@from = from
		@app = app
		@i = @app.image File.join(static_dir, "1.jpg") , left:@start,top:floor_position[from]+25
	end
end

def show_floor(y,floor_position)	
	@position = 5 if y==floor_position[5]
	@position = 4 if y==floor_position[4]
	@position = 3 if y==floor_position[3]
	@position = 2 if y==floor_position[2]
	@position = 1 if y==floor_position[1]
	@current_floor.replace @position
end


floor_position = [0,442,332,222,112,2]
direction = 1
@current_floor = nil

Shoes.app(title:"elevator", width: 1000, height: 556, resizable: false){
	background "#EEC".."#996", curve: 5, margin: 2
#=========================================================

stack left:0 ,top:0 ,width:800 ,height:556 do 
	border black,strokewidth: 3

#=========================================================    

for k in (1..5)
	@f = rect 2,floor_position[k],348,110,fill:white,strokewidth:2,stroke:black
	@f = rect 452,floor_position[k],348,110,fill:white,strokewidth:2,stroke:black
end

#=========================================================
px = 5
p1 = Passenger.new(self,3,1,floor_position,px)
p1.i
@anim2 = animate(24) do
		if(p1.start>348)
			p1.i.toggle
			p1.start = 348
			@anim2.stop
		end
		p1.i.move(p1.start+=2,floor_position[p1.from])
end
#=========================================================    

@e = rect 350,442,100,110,fill:gray, strokewidth:3,stroke:black 
y=442
@position = 1
@anim = animate(24) do	
	if(@floor > @position)
		direction = 1
	end
	if(@floor < @position)
		direction = -1
	end			
	if(@floor == @position)
		@anim.stop
	end
	@e.move(350, y+=-2*direction) 
	show_floor(y,floor_position)
end

end

#==========================================================   

stack left:800,top:0,width:200,height:330 do           
	border black,strokewidth: 3
	flow left:75, top:50,width:50 do
		%w[5 4 3 2 1 ].each do |btn|
			button btn, width: 50, height: 50 do
				case btn
				when '5'
					@floor = 5
					@anim.start
				when '4'
					@floor = 4
					@anim.start
				when '3'
					@floor = 3
					@anim.start
				when '2'
					@floor = 2
					@anim.start
				when '1'
					@floor = 1 
					@anim.start 			
				end

			end
		end
	end  
end
stack left:800, top:330,width:200 ,height:226 do
	border black,strokewidth: 3
	@o = rect 50, 50, 100, 100, fill: yellow, strokewidth: 3, stroke: white
	@current_floor = para "#{@position}" ,left:85,top:75,size:30
	stack do
	end
end
}