(define (domain mctf)

  (:requirements :typing :fluents :time :negative-preconditions)

  (:types blue red)

  (:predicates
    (ready) (total_failure) 
    (adjustable_heading) ;; ensure agents only choose a single heading per time step (to reduce state space)
    (tagged_blue ?b - blue) (tagged_red ?r - red) (has_flag_blue ?b - blue) (has_flag_red ?r - red)
    (blue_flag_at_blue_base) (red_flag_at_red_base)
  )

  (:functions
    ;; time discretization (max sim update) = 0.1s
    ;; max_time = 360s
    ;; 
    (x_b ?b - blue) (y_b ?b - blue) (v_b ?b - blue) (heading ?b - blue) ;; blue agent numeric vars
    (x_r ?r - red) (y_r ?r - red) (v_r ?r - red) (heading_r ?r - red) ;; red agent numeric vars
    (x_base_blue) (y_base_blue) (x_base_red) (y_base_red) ;; coordinates for each team's flag base BLUE HOME=[120,40], RED HOME=[40,20]
    (x_max) (x_min) (y_max) (y_min) ;; global numeric vars: size of world in meters =[160, 80]
    (r_agent) (r_catch) (r_collision) (r_capture) ;; agent_radius = 2m, catch_radius = 10m, collision_radius = 2.2m, (flag)capture_radius = 10m [need to verify, could be 7 or 8m as well]
    (max_cooldown_time) ;; cooldown after tagging someone = 30s, 
    (cooldown_time_blue ?b - blue) (cooldown_time_red ?r - red)
    (v_max) ;; max_speed = 1.5m/s
    (score_blue) (score_red) 
    (game_time)
  )


  ; (:event e1
  ;     :parameters ()
  ;     :precondition (and (ready) (not (total_failure)))
  ;     :effect (and
  ;       
  ;     )
  ; )

  ; (:process p1
  ;   :parameters ()
  ;   :precondition (and (ready) (not (total_failure)))
  ;   :effect (and
  ;     
  ;   )
  ; )

  ; (:action a1
  ;   :parameters ()
  ;   :precondition (and (ready) (not (total_failure)))
  ;   :effect (and 
  ;     
  ;   )
  ; )

  (:process time_keeping
    :parameters ()
    :precondition (and (ready) (not (total_failure)))
    :effect (and
        (increase (elapsed_time) (* #t 1))
    )
  )

  (:process update_position
    :parameters (?b - blue)
    :precondition (and (ready) (not (total_failure)))
    :effect (and
        (increase (x_b ?b) (* #t (* (@cos (heading ?b)) (v_b))) )
        (increase (y_b ?b) (* #t (* (@sin (heading ?b)) (v_b))) )
    )
  )

  (:event reset_heading
      :parameters ()
      :precondition (and (ready) (not (total_failure)) (not (adjustable_heading)) )
      :effect (and
        (adjustable_heading)
      )
  )

  ; (:action half_speed
  ;   :parameters (?b - blue)
  ;   :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (= (v_b ?b) (v_max)) )
  ;   :effect (and 
  ;     (assign (v_b ?b) (/ (v_max) 2.0))
  ;   )
  ; )

  ; (:action full_speed
  ;   :parameters (?b - blue)
  ;   :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (= (v_b ?b) (/ (v_max) 2.0)) )
  ;   :effect (and 
  ;     (assign (v_b ?b) (/ (v_max) 2.0))
  ;   )
  ; )

  ; (:action heading_-135
  ;   :parameters (?b - blue)
  ;   :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) -135.0)) (adjustable_heading) )
  ;   :effect (and 
  ;     (assign (heading ?b) -135.0)
  ;     (not (adjustable_heading))
  ;   )
  ; )

  (:action heading_-90
    :parameters (?b - blue)
    :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) -90.0)) (adjustable_heading) )
    :effect (and 
      (assign (heading ?b) -90.0)
      (not (adjustable_heading))
    )
  )

  ; (:action heading_-45
  ;   :parameters (?b - blue)
  ;   :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) -45.0)) (adjustable_heading) )
  ;   :effect (and 
  ;     (assign (heading ?b) -45.0)
  ;     (not (adjustable_heading))
  ;   )
  ; )

  (:action heading_0
    :parameters (?b - blue)
    :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) 0.0)) (adjustable_heading) )
    :effect (and 
      (assign (heading ?b) 0.0)
      (not (adjustable_heading))
    )
  )

  ; (:action heading_45
  ;   :parameters (?b - blue)
  ;   :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) 45.0)) (adjustable_heading) )
  ;   :effect (and 
  ;     (assign (heading ?b) 45.0)
  ;     (not (adjustable_heading))
  ;   )
  ; )

  (:action heading_90
    :parameters (?b - blue)
    :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) 90.0)) (adjustable_heading) )
    :effect (and 
      (assign (heading ?b) 90.0)
      (not (adjustable_heading))
    )
  )

  ; (:action heading_135
  ;   :parameters (?b - blue)
  ;   :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) 135.0)) (adjustable_heading) )
  ;   :effect (and 
  ;     (assign (heading ?b) 135.0)
  ;     (not (adjustable_heading))
  ;   )
  ; )

  (:action heading_180
    :parameters (?b - blue)
    :precondition (and (not (tagged_blue ?b)) (not (total_failure)) (not (= (heading ?b) 180.0)) (adjustable_heading) )
    :effect (and 
      (assign (heading ?b) 180.0)
      (not (adjustable_heading))
    )
  )

  (:event out_of_bounds
    :parameters (?b - blue)
    :precondition (or (> (x_b ?b) (x_max)) (< (x_b ?b) (x_min)) (> (y_b ?b) (y_max)) (< (y_b ?b) (y_min)))
    :effect (and (total_failure))
  )

  (:event blue_tagged_by_red
    :parameters (?b - blue ?r - red)
    :precondition (and (< (x_b ?b) (/ (x_max) 2)) (<= (cooldown_time_red ?r) 0.0) (not (tagged_blue ?b))
      (< (^ (+ (^ (- (x_b ?b) (x_r ?r)) 2.0) (^ (- (y_b ?b) (y_r ?r)) 2.0)) 0.5) (r_catch))
    )
    :effect (and (tagged_blue ?b) 
      (assign (cooldown_time_red ?r) (max_cooldown_time))
    )
  )

  (:event red_tagged_by_blue
    :parameters (?b - blue ?r - red)
    :precondition (and (> (x_r ?r) (/ (x_max) 2)) (<= (cooldown_time_blue ?b) 0.0) (not (tagged_red ?r))
      (< (^ (+ (^ (- (x_b ?b) (x_r ?r)) 2.0) (^ (- (y_b ?b) (y_r ?r)) 2.0)) 0.5) (r_catch))
    )
    :effect (and (tagged_red ?r) 
      (assign (cooldown_time_blue ?b) (max_cooldown_time))
    )
  )

  (:process cooldown_red
    :parameters (?r - red)
    :precondition (and (> (cooldown_time_red ?r) 0.0) )
    :effect (and (decrease (cooldown_time_red ?r) (* #t 1.0)) ) 
  )

  (:process cooldown_blue
    :parameters (?b - blue)
    :precondition (and (> (cooldown_time_blue ?b) 0.0) )
    :effect (and (decrease (cooldown_time_blue ?b) (* #t 1.0)) ) 
  )

  (:event blue_captured_the_red_flag
    :parameters (?b - blue)
    :precondition (and (not (has_red_flag ?b)) (red_flag_at_red_base)
      (< (^ (+ (^ (- (x_b ?b) (x_base_red)) 2.0) (^ (- (y_b ?b) (y_base_red)) 2.0)) 0.5) (r_capture))
    )
    :effect (and (not (red_flag_at_red_base)) (has_red_flag ?b)) 
  )

  (:event red_captured_the_blue_flag
    :parameters (?r - red)
    :precondition (and (not (has_blue_flag ?r)) (blue_flag_at_blue_base)
      (< (^ (+ (^ (- (x_r ?r) (x_base_blue)) 2.0) (^ (- (y_r ?r) (y_base_blue)) 2.0)) 0.5) (r_capture))
    )
    :effect (and (not (blue_flag_at_blue_base)) (has_blue_flag ?r))
  )

  (:event untag_blue
    :parameters (?b - blue)
    :precondition (and (tagged_blue ?b) 
      (< (^ (+ (^ (- (x_b ?b) (x_base_blue)) 2.0) (^ (- (y_b ?b) (y_base_blue)) 2.0)) 0.5) (r_capture)) 
    )
    :effect (and (not (tagged_blue ?b)) ) 
  )

  (:process untag_red
    :parameters (?r - red)
    :precondition (and (tagged_red ?r) 
      (< (^ (+ (^ (- (x_r ?r) (x_base_red)) 2.0) (^ (- (y_r ?r) (y_base_red)) 2.0)) 0.5) (r_capture))
    )
    :effect (and (not (tagged_red ?r)) )
  )

  (:event blue_scores
    :parameters (?b - blue)
    :precondition (and (has_red_flag ?b) (> (x_b ?b) (/ (x_max) 2)) )
    :effect (and (increase (score_blue) 1.0))
  )

  (:event red_scores
    :parameters (?r - red)
    :precondition (and (has_blue_flag ?r) (< (x_r ?r) (/ (x_max) 2)))
    :effect (and (increase (score_red) 1.0))
  )

  (:event times_up
    :parameters ()
    :precondition (and (>= (elapsed_time) (game_time)))
    :effect (and (game_end))
  )


)
