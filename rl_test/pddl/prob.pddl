(define(problem mctf-problem)
(:domain mctf)
(:objects b1 - blue b2 - blue b3 - blue r1 - red r2 - red r3 - red )
(:init 	(= (x_b b1)  120.0)
	(= (y_b b1)  20.0)
	(= (x_b b2)  120.0)
	(= (y_b b2)  40.0)
	(= (x_b b3)  120.0)
	(= (y_b b3)  60.0)
	(= (x_b r1)  40.0)
	(= (y_b r1)  20.0)
	(= (x_b r2)  40.0)
	(= (y_b r2)  40.0)
	(= (x_b r3)  40.0)
	(= (y_b r3)  60.0)
	(= (v_b b1)  0.0)
	(= (v_b b2)  0.0)
	(= (v_b b3)  0.0)
	(= (v_r r1)  0.0)
	(= (v_r r2)  0.0)
	(= (v_r r3)  0.0)
	(= (heading_b b1)  -90)
	(= (heading_b b2)  -90)
	(= (heading_b b3)  -90)
	(= (heading_r r1)  90)
	(= (heading_r r2)  90)
	(= (heading_r r3)  90)
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
	(= (max_cooldown_time)  30)
	(= (cooldown_time_blue b1)  30.0)
	(= (cooldown_time_blue b2)  30.0)
	(= (cooldown_time_blue b3)  30.0)
	(= (cooldown_time_red r1)  30.0)
	(= (cooldown_time_red r2)  30.0)
	(= (cooldown_time_red r3)  30.0)
	(= (v_max)  1.5)
	(= (score_blue)  0.0)
	(= (score_red)  0.0)
	(ready)
	(adjustable_handling)
	(blue_flag_at_blue_base)
	(red_flag_at_red_base)
)
(:goal (and  (not (total_failure) )  (>= (score_blue)  1) ))
(:metric minimize(total-time))
)
