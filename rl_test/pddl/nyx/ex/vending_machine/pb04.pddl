(define (problem vendingmachine-problem)
(:domain vending-machine)
(:objects )
(:init (= (vel) 0)
	(= (acc) 0)
	(= (dist) 0)
	(lightsensorstatus)
	(= (lightsensorposn) 1)
	(= (trayposition) 2)
	(= (counted) 0)
	(slotopen)
)
(:goal (and (= (counted) 12) (finished)))
(:metric minimize (total-time))) 
