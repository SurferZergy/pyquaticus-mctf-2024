(define(problem mctf-problem)
(:domain mctf)
(:objects b1 - blue)
(:init 	(= (x_b b1)  106.82444763183594)
	(= (y_b b1)  20.0)
	(= (v_b b1)  1.5)
	(= (bearing b1)  90.0)
	(= (x_base_blue)  140)
	(= (y_base_blue)  40)
	(= (x_base_red)  20)
	(= (y_base_red)  40)
	(= (r_agent)  2)
	(= (r_catch)  10)
	(= (r_collision)  2.2)
	(= (r_capture)  10)
	(= (x_max)  160)
	(= (x_min)  0)
	(= (y_max)  80)
	(= (y_min)  0)

	(= (v_max)  1.5)
	(= (score_blue)  0.0)

	(ready)
	(adjustable_handling)
	(blue_flag_at_blue_base)
	(red_flag_at_red_base)
)
;(:goal (and  (not (total_failure) )  (>= (score_blue)  1) ))
(:goal (and (not (total_failure)) (has_red_flag b1)))
(:metric minimize(total-time))
)
