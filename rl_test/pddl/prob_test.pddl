(define(problem mctf-problem)
(:domain mctf)
(:objects b1 - blue b2 - blue b3 - blue r1 - red r2 - red r3 - red )
(:init 	(= (x_b b1)  106.82444763183594)
	(= (y_b b1)  20.0)
	(= (x_b b2)  107.41303151713913)
	(= (y_b b2)  43.20799168716924)
	(= (x_b b3)  107.41303291435514)
	(= (y_b b3)  56.792003280998806)
	(= (x_b r1)  49.917597146183084)
	(= (y_b r1)  27.7442545874658)
	(= (x_b r2)  52.62277651052458)
	(= (y_b r2)  36.64146310651967)
	(= (x_b r3)  51.51119766392731)
	(= (y_b r3)  54.239209582328556)
	(= (v_b b1)  1.5)
	(= (v_b b2)  1.5)
	(= (v_b b3)  1.5)
	(= (v_r r1)  1.5)
	(= (v_r r2)  1.5)
	(= (v_r r3)  1.5)
	(= (bearing b1)  90.0)
	(= (bearing b2)  61.370567321777344)
	(= (bearing b3)  118.62944030761719)
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