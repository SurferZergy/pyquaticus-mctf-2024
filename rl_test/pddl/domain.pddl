(define (domain mctf)

    (:requirements :typing :fluents :negative-preconditions)
    (:types cell blue red)

    (:predicates
        (blue_collide ?b - blue)
        (blue_has_flag ?b - blue)
        (red_flag_at_red_base)
    )
    (:functions
        (row ?c - cell)
        (col ?c - cell)
        (brow ?b - blue)
        (bcol ?b - blue)
        (rbrow)
        (rbcol)
        (bbrow)
        (bbcol)
        (rrow ?r - red)
        (rcol ?r - red)
        ; (blue_score)
        ; (red_score)
        )

    (:action blue_move-north
        ; :parameters (?b - blue ?to - cell ?r - red)
        :parameters (?b - blue ?to - cell)
        :precondition (and
            (= (bcol ?b) (col ?to))
            (= (- (brow ?b) (row ?to)) -1)
            (not (= (brow ?b) 2))
            (not (= (bcol ?b) 12))
            (not (= (brow ?b) 6))
            (not (= (bcol ?b) 12))
            ; (<= (+ (^ (^ (- (brow ?b) (rrow ?r)) 2) 0.5) (^ (^ (- (bcol ?b) (rcol ?r)) 2) 0.5)) 1)
        )
        :effect (and
            (assign (brow ?b) (row ?to))
        )
    )

    (:action blue_move-south
        ; :parameters (?b - blue ?to - cell ?r - red)
        :parameters (?b - blue ?to - cell)
        :precondition (and
            (= (bcol ?b) (col ?to))
            (= (- (brow ?b) (row ?to)) 1)
            (not (= (brow ?b) 2))
            (not (= (bcol ?b) 12))
            (not (= (brow ?b) 6))
            (not (= (bcol ?b) 12))
            ; (<= (+ (^ (^ (- (brow ?b) (rrow ?r)) 2) 0.5) (^ (^ (- (bcol ?b) (rcol ?r)) 2) 0.5)) 1)
        )
        :effect (and
            (assign (brow ?b) (row ?to))
        )
    )

    (:action blue_move-east
        ; :parameters (?b - blue ?to - cell ?r - red)
        :parameters (?b - blue ?to - cell)
        :precondition (and
            (= (brow ?b) (row ?to))
            (= (- (bcol ?b) (col ?to)) -1)
            (not (= (brow ?b) 2))
            (not (= (bcol ?b) 12))
            (not (= (brow ?b) 6))
            (not (= (bcol ?b) 12))
            ; (<= (+ (^ (^ (- (row ?to) (rrow ?r)) 2) 0.5) (^ (^ (- (col ?to) (rcol ?r)) 2) 0.5)) 1)
        )
        :effect (and
            (assign (bcol ?b) (col ?to))
        )
    )

    (:action blue_move-west
        ; :parameters (?b - blue ?to - cell ?r - red)
        :parameters (?b - blue ?to - cell)
        :precondition (and
            (= (brow ?b) (row ?to))
            (= (- (bcol ?b) (col ?to)) 1)
            ; (<= (+ (^ (^ (- (brow ?b) (rrow ?r)) 2) 0.5) (^ (^ (- (bcol ?b) (rcol ?r)) 2) 0.5)) 1)
        )
        :effect (and
            (assign (bcol ?b) (col ?to))
        )
    )

    ; (:event blue_scores
    ;     :parameters (?b - blue)
    ;     :precondition (and
    ;         (blue_has_flag ?b)
    ;         (= (bbrow) (brow ?b))
    ;         (= (bbcol) (bcol ?b))
    ;     )

    ;     :effect(and
    ;         (increase (blue_score) 1)
    ;         (not (blue_has_flag ?b))
    ;         (red_flag_at_red_base)
    ;     )
    ; )

    (:event blue_grabs_flag
        :parameters (?b - blue)
        :precondition (and
            (red_flag_at_red_base)
            (= (rbrow) (brow ?b))
            (= (rbcol) (bcol ?b))
        )

        :effect(and
            (blue_has_flag ?b)
            (not (red_flag_at_red_base))
        )
    )

    (:event blue_collide_r
        :parameters (?b - blue ?r - red)
        :precondition (and
            (= (rrow ?r) (brow ?b))
            (= (rcol ?r) (bcol ?b))
        )
        :effect(and
            (blue_collide ?b)
            (red_flag_at_red_base)
        )
    )

    (:event blue_collide_b_1
        :parameters (?b - blue)
        :precondition (and
            (= (brow ?b) 2)
            (= (bcol ?b) 12)
        )
        :effect(and
            (blue_collide ?b)
            (red_flag_at_red_base)
        )
    )

    (:event blue_collide_b_2
        :parameters (?b - blue)
        :precondition (and
            (= (brow ?b) 6)
            (= (bcol ?b) 12)
        )
        :effect(and
            (blue_collide ?b)
            (red_flag_at_red_base)
        )
    )
)