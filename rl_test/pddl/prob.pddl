(define(problem mctf-problem)
(:domain mctf)
(:objects b1 - blue b2 - red b3 - red r1 - red r2 - red r3 - red cell1_1 - cell cell2_1 - cell cell3_1 - cell cell4_1 - cell cell5_1 - cell cell6_1 - cell cell7_1 - cell cell8_1 - cell cell9_1 - cell cell10_1 - cell cell11_1 - cell cell12_1 - cell cell13_1 - cell cell14_1 - cell cell15_1 - cell cell1_2 - cell cell2_2 - cell cell3_2 - cell cell4_2 - cell cell5_2 - cell cell6_2 - cell cell7_2 - cell cell8_2 - cell cell9_2 - cell cell10_2 - cell cell11_2 - cell cell12_2 - cell cell13_2 - cell cell14_2 - cell cell15_2 - cell cell1_3 - cell cell2_3 - cell cell3_3 - cell cell4_3 - cell cell5_3 - cell cell6_3 - cell cell7_3 - cell cell8_3 - cell cell9_3 - cell cell10_3 - cell cell11_3 - cell cell12_3 - cell cell13_3 - cell cell14_3 - cell cell15_3 - cell cell1_4 - cell cell2_4 - cell cell3_4 - cell cell4_4 - cell cell5_4 - cell cell6_4 - cell cell7_4 - cell cell8_4 - cell cell9_4 - cell cell10_4 - cell cell11_4 - cell cell12_4 - cell cell13_4 - cell cell14_4 - cell cell15_4 - cell cell1_5 - cell cell2_5 - cell cell3_5 - cell cell4_5 - cell cell5_5 - cell cell6_5 - cell cell7_5 - cell cell8_5 - cell cell9_5 - cell cell10_5 - cell cell11_5 - cell cell12_5 - cell cell13_5 - cell cell14_5 - cell cell15_5 - cell cell1_6 - cell cell2_6 - cell cell3_6 - cell cell4_6 - cell cell5_6 - cell cell6_6 - cell cell7_6 - cell cell8_6 - cell cell9_6 - cell cell10_6 - cell cell11_6 - cell cell12_6 - cell cell13_6 - cell cell14_6 - cell cell15_6 - cell cell1_7 - cell cell2_7 - cell cell3_7 - cell cell4_7 - cell cell5_7 - cell cell6_7 - cell cell7_7 - cell cell8_7 - cell cell9_7 - cell cell10_7 - cell cell11_7 - cell cell12_7 - cell cell13_7 - cell cell14_7 - cell cell15_7 - cell )
(:init 	(= (brow b1)  6)
	(= (bcol b1)  10)
	(= (rrow b2)  2)
	(= (rcol b2)  12)
	(= (rrow b3)  6)
	(= (rcol b3)  12)
	(= (rrow r1)  5)
	(= (rcol r1)  7)
	(= (rrow r2)  4)
	(= (rcol r2)  5)
	(= (rrow r3)  3)
	(= (rcol r3)  9)
	(= (rbrow)  4)
	(= (rbcol)  2)
	(= (bbrow)  4)
	(= (bbcol)  14)
	(red_flag_at_red_base)
	(= (col cell1_1)  1)
	(= (row cell1_1)  1)
	(= (col cell2_1)  2)
	(= (row cell2_1)  1)
	(= (col cell3_1)  3)
	(= (row cell3_1)  1)
	(= (col cell4_1)  4)
	(= (row cell4_1)  1)
	(= (col cell5_1)  5)
	(= (row cell5_1)  1)
	(= (col cell6_1)  6)
	(= (row cell6_1)  1)
	(= (col cell7_1)  7)
	(= (row cell7_1)  1)
	(= (col cell8_1)  8)
	(= (row cell8_1)  1)
	(= (col cell9_1)  9)
	(= (row cell9_1)  1)
	(= (col cell10_1)  10)
	(= (row cell10_1)  1)
	(= (col cell11_1)  11)
	(= (row cell11_1)  1)
	(= (col cell12_1)  12)
	(= (row cell12_1)  1)
	(= (col cell13_1)  13)
	(= (row cell13_1)  1)
	(= (col cell14_1)  14)
	(= (row cell14_1)  1)
	(= (col cell15_1)  15)
	(= (row cell15_1)  1)
	(= (col cell1_2)  1)
	(= (row cell1_2)  2)
	(= (col cell2_2)  2)
	(= (row cell2_2)  2)
	(= (col cell3_2)  3)
	(= (row cell3_2)  2)
	(= (col cell4_2)  4)
	(= (row cell4_2)  2)
	(= (col cell5_2)  5)
	(= (row cell5_2)  2)
	(= (col cell6_2)  6)
	(= (row cell6_2)  2)
	(= (col cell7_2)  7)
	(= (row cell7_2)  2)
	(= (col cell8_2)  8)
	(= (row cell8_2)  2)
	(= (col cell9_2)  9)
	(= (row cell9_2)  2)
	(= (col cell10_2)  10)
	(= (row cell10_2)  2)
	(= (col cell11_2)  11)
	(= (row cell11_2)  2)
	(= (col cell12_2)  12)
	(= (row cell12_2)  2)
	(= (col cell13_2)  13)
	(= (row cell13_2)  2)
	(= (col cell14_2)  14)
	(= (row cell14_2)  2)
	(= (col cell15_2)  15)
	(= (row cell15_2)  2)
	(= (col cell1_3)  1)
	(= (row cell1_3)  3)
	(= (col cell2_3)  2)
	(= (row cell2_3)  3)
	(= (col cell3_3)  3)
	(= (row cell3_3)  3)
	(= (col cell4_3)  4)
	(= (row cell4_3)  3)
	(= (col cell5_3)  5)
	(= (row cell5_3)  3)
	(= (col cell6_3)  6)
	(= (row cell6_3)  3)
	(= (col cell7_3)  7)
	(= (row cell7_3)  3)
	(= (col cell8_3)  8)
	(= (row cell8_3)  3)
	(= (col cell9_3)  9)
	(= (row cell9_3)  3)
	(= (col cell10_3)  10)
	(= (row cell10_3)  3)
	(= (col cell11_3)  11)
	(= (row cell11_3)  3)
	(= (col cell12_3)  12)
	(= (row cell12_3)  3)
	(= (col cell13_3)  13)
	(= (row cell13_3)  3)
	(= (col cell14_3)  14)
	(= (row cell14_3)  3)
	(= (col cell15_3)  15)
	(= (row cell15_3)  3)
	(= (col cell1_4)  1)
	(= (row cell1_4)  4)
	(= (col cell2_4)  2)
	(= (row cell2_4)  4)
	(= (col cell3_4)  3)
	(= (row cell3_4)  4)
	(= (col cell4_4)  4)
	(= (row cell4_4)  4)
	(= (col cell5_4)  5)
	(= (row cell5_4)  4)
	(= (col cell6_4)  6)
	(= (row cell6_4)  4)
	(= (col cell7_4)  7)
	(= (row cell7_4)  4)
	(= (col cell8_4)  8)
	(= (row cell8_4)  4)
	(= (col cell9_4)  9)
	(= (row cell9_4)  4)
	(= (col cell10_4)  10)
	(= (row cell10_4)  4)
	(= (col cell11_4)  11)
	(= (row cell11_4)  4)
	(= (col cell12_4)  12)
	(= (row cell12_4)  4)
	(= (col cell13_4)  13)
	(= (row cell13_4)  4)
	(= (col cell14_4)  14)
	(= (row cell14_4)  4)
	(= (col cell15_4)  15)
	(= (row cell15_4)  4)
	(= (col cell1_5)  1)
	(= (row cell1_5)  5)
	(= (col cell2_5)  2)
	(= (row cell2_5)  5)
	(= (col cell3_5)  3)
	(= (row cell3_5)  5)
	(= (col cell4_5)  4)
	(= (row cell4_5)  5)
	(= (col cell5_5)  5)
	(= (row cell5_5)  5)
	(= (col cell6_5)  6)
	(= (row cell6_5)  5)
	(= (col cell7_5)  7)
	(= (row cell7_5)  5)
	(= (col cell8_5)  8)
	(= (row cell8_5)  5)
	(= (col cell9_5)  9)
	(= (row cell9_5)  5)
	(= (col cell10_5)  10)
	(= (row cell10_5)  5)
	(= (col cell11_5)  11)
	(= (row cell11_5)  5)
	(= (col cell12_5)  12)
	(= (row cell12_5)  5)
	(= (col cell13_5)  13)
	(= (row cell13_5)  5)
	(= (col cell14_5)  14)
	(= (row cell14_5)  5)
	(= (col cell15_5)  15)
	(= (row cell15_5)  5)
	(= (col cell1_6)  1)
	(= (row cell1_6)  6)
	(= (col cell2_6)  2)
	(= (row cell2_6)  6)
	(= (col cell3_6)  3)
	(= (row cell3_6)  6)
	(= (col cell4_6)  4)
	(= (row cell4_6)  6)
	(= (col cell5_6)  5)
	(= (row cell5_6)  6)
	(= (col cell6_6)  6)
	(= (row cell6_6)  6)
	(= (col cell7_6)  7)
	(= (row cell7_6)  6)
	(= (col cell8_6)  8)
	(= (row cell8_6)  6)
	(= (col cell9_6)  9)
	(= (row cell9_6)  6)
	(= (col cell10_6)  10)
	(= (row cell10_6)  6)
	(= (col cell11_6)  11)
	(= (row cell11_6)  6)
	(= (col cell12_6)  12)
	(= (row cell12_6)  6)
	(= (col cell13_6)  13)
	(= (row cell13_6)  6)
	(= (col cell14_6)  14)
	(= (row cell14_6)  6)
	(= (col cell15_6)  15)
	(= (row cell15_6)  6)
	(= (col cell1_7)  1)
	(= (row cell1_7)  7)
	(= (col cell2_7)  2)
	(= (row cell2_7)  7)
	(= (col cell3_7)  3)
	(= (row cell3_7)  7)
	(= (col cell4_7)  4)
	(= (row cell4_7)  7)
	(= (col cell5_7)  5)
	(= (row cell5_7)  7)
	(= (col cell6_7)  6)
	(= (row cell6_7)  7)
	(= (col cell7_7)  7)
	(= (row cell7_7)  7)
	(= (col cell8_7)  8)
	(= (row cell8_7)  7)
	(= (col cell9_7)  9)
	(= (row cell9_7)  7)
	(= (col cell10_7)  10)
	(= (row cell10_7)  7)
	(= (col cell11_7)  11)
	(= (row cell11_7)  7)
	(= (col cell12_7)  12)
	(= (row cell12_7)  7)
	(= (col cell13_7)  13)
	(= (row cell13_7)  7)
	(= (col cell14_7)  14)
	(= (row cell14_7)  7)
	(= (col cell15_7)  15)
	(= (row cell15_7)  7)
)
(:goal (and  (>= (bcol b1)  9)  (blue_has_flag b1)  (not (blue_collide b1) ) ))
(:metric minimize(total-time))
)
