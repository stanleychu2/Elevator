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
