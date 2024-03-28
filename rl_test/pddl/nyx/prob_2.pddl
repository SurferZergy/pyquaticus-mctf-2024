(define(problem mctf-problem)
(:domain mctf)
(:objects b1 - blue b2 - blue b3 - blue r1 - red r2 - red r3 - red )
(:init 	(= (x_b b1)  116.42444610595703)
	(= (y_b b1)  20.0)
	(= (x_b b2)  116.46170939952971)
	(= (y_b b2)  40.19063944209504)
	(= (x_b b3)  116.46170110714502)
	(= (y_b b3)  59.809365960069286)
	(= (x_b r1)  43.40730974020859)
	(= (y_b r1)  20.870368953582986)
	(= (x_b r2)  43.53801193853823)
	(= (y_b r2)  39.667596012708294)
	(= (x_b r3)  43.47748456908539)
	(= (y_b r3)  59.3786807908937)
	(= (v_b b1)  1.5)
	(= (v_b b2)  1.4999998807907104)
	(= (v_b b3)  1.4999998807907104)
	(= (v_r r1)  1.5)
	(= (v_r r2)  1.4999998807907104)
	(= (v_r r3)  1.5)
	(= (bearing b1)  90.00000762939453)
	(= (bearing b2)  83.79302215576172)
	(= (bearing b3)  96.20697784423828)
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
;(:goal (and  (not (total_failure) )  (has_red_flag b1) ))
(:goal (and  (not (total_failure) )  (>= (score_blue)  1) ))
(:metric minimize(total-time))
)
