(define (problem handcoded_game)
(:domain mctf)
(:objects
b1 b2 b3 - blue
r1 r2 r3 - red
)
(:init
    ; functions
    ; locations
    (= (x_b b1) 120.0)
    (= (x_b b2) 120.0)
    (= (x_b b3) 120.0)
    (= (y_b b1) 20.0)
    (= (y_b b2) 40.0)
    (= (y_b b3) 60.0)
    (= (x_r r1) 40.0)
    (= (x_r r2) 40.0)
    (= (x_r r3) 40.0)
    (= (y_r r1) 20.0)
    (= (y_r r2) 40.0)
    (= (y_r r3) 60.0)
    ; environment limits
    (= (x_max) 160.0)
    (= (x_min) 0.0)
    (= (y_max) 80.0)
    (= (y_min) 0.0)
    ; times to the best of my understanding
    (= (max_cooldown_time) 30.0)    ; this seems a little higher as compared to the video shown
    (= (cooldown_time_blue b1) 0.0)
    (= (cooldown_time_blue b2) 0.0)
    (= (cooldown_time_blue b3) 0.0)
    (= (cooldown_time_red r1) 0.0)
    (= (cooldown_time_red r2) 0.0)
    (= (cooldown_time_red r3) 0.0)
    (= (v_max) 1.5)
    (= (score_blue) 0.0)
    (= (score_red) 0.0)
    (= (game_time) 0.0)
    ; predicates
    (ready)
    (adjustable_handling)
)

; initial value that we might want to check
(:goal (and (>= (score_blue) 1.0)))
;(:metric minimize(total-time))
)
