
from .syntax.state import State
from .syntax import constants as constants
import math


def dis_pts(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def heuristic_function(state):

    if constants.CUSTOM_HEURISTIC_ID == 0:

        if state.state_vars["['blue_has_flag', 'b1']"]:
            distance_to_blue_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['bbcol']"], state.state_vars["['bbrow']"]])
            return distance_to_blue_base

        else:
            distance_to_red_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['rbcol']"], state.state_vars["['rbrow']"]])
            return distance_to_red_base

    elif constants.CUSTOM_HEURISTIC_ID == 3:

        if state.state_vars["['blue_has_flag', 'b1']"]:
            distance_to_blue_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['bbcol']"], state.state_vars["['bbrow']"]])
            return distance_to_blue_base

        else:
            distance_to_red_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['rbcol']"], state.state_vars["['rbrow']"]])
            distance_to_red_agents = (math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                                           [state.state_vars["['rcol', 'r0']"], state.state_vars["['rrow', 'r0']"]]) + \
                                                math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                                          [state.state_vars["['rcol', 'r1']"], state.state_vars["['rrow', 'r1']"]]) + \
                                                math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                                           [state.state_vars["['rcol', 'r2']"], state.state_vars["['rrow', 'r2']"]]))/3


            return distance_to_red_base/distance_to_red_agents

    elif constants.CUSTOM_HEURISTIC_ID == 4:

        if state.state_vars["['blue_has_flag', 'b1']"]:
            distance_to_blue_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['bbcol']"], state.state_vars["['bbrow']"]])
            return distance_to_blue_base

        else:
            distance_to_red_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['rbcol']"], state.state_vars["['rbrow']"]])
            distance_to_red_agents = (math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                                           [state.state_vars["['rcol', 'r0']"], state.state_vars["['rrow', 'r0']"]]) + \
                                                math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                                          [state.state_vars["['rcol', 'r1']"], state.state_vars["['rrow', 'r1']"]]) + \
                                                math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                                           [state.state_vars["['rcol', 'r2']"], state.state_vars["['rrow', 'r2']"]]))/3

            if (state.state_vars["['bcol', 'b1']"] >= 7):
                distance_to_red_agents = 1


            return distance_to_red_base/distance_to_red_agents

    elif constants.CUSTOM_HEURISTIC_ID == 5:

        if state.state_vars["['blue_has_flag', 'b1']"]:
            distance_to_scrimmage_line = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [8, state.state_vars["['rbrow']"]])
            # distance_to_scrimmage_line = math.dist([state.state_vars["['bcol', 'b1']"]], [8])

            distance_to_red_agents = (math.dist(
                [state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                [state.state_vars["['rcol', 'r0']"], state.state_vars["['rrow', 'r0']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                          [state.state_vars["['rcol', 'r1']"], state.state_vars["['rrow', 'r1']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                          [state.state_vars["['rcol', 'r2']"], state.state_vars["['rrow', 'r2']"]])) / 3

            return distance_to_scrimmage_line/distance_to_red_agents

        else:
            distance_to_red_base = math.dist([state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                             [state.state_vars["['rbcol']"], state.state_vars["['rbrow']"]])
            distance_to_red_agents = (math.dist(
                [state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                [state.state_vars["['rcol', 'r0']"], state.state_vars["['rrow', 'r0']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                          [state.state_vars["['rcol', 'r1']"], state.state_vars["['rrow', 'r1']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'b1']"], state.state_vars["['brow', 'b1']"]],
                                          [state.state_vars["['rcol', 'r2']"], state.state_vars["['rrow', 'r2']"]])) / 3

            if (state.state_vars["['bcol', 'b1']"] >= 7):
                distance_to_red_agents = 1

            return distance_to_red_base / distance_to_red_agents

    elif constants.CUSTOM_HEURISTIC_ID == 6:

        if state.state_vars["['blue_has_flag', 'r4']"]:
            distance_to_scrimmage_line = math.dist([state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                                             [8, state.state_vars["['rbrow']"]])

            distance_to_red_agents = (math.dist(
                [state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                [state.state_vars["['rcol', 'b0']"], state.state_vars["['rrow', 'b0']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                                          [state.state_vars["['rcol', 'b1']"], state.state_vars["['rrow', 'b1']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                                          [state.state_vars["['rcol', 'b2']"], state.state_vars["['rrow', 'b2']"]])) / 3

            return distance_to_scrimmage_line/distance_to_red_agents

        else:
            distance_to_red_base = math.dist([state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                                             [state.state_vars["['rbcol']"], state.state_vars["['rbrow']"]])
            distance_to_red_agents = (math.dist(
                [state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                [state.state_vars["['rcol', 'b0']"], state.state_vars["['rrow', 'b0']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                                          [state.state_vars["['rcol', 'b1']"], state.state_vars["['rrow', 'b1']"]]) + \
                                      math.dist(
                                          [state.state_vars["['bcol', 'r4']"], state.state_vars["['brow', 'r4']"]],
                                          [state.state_vars["['rcol', 'b2']"], state.state_vars["['rrow', 'b2']"]])) / 3

            if (state.state_vars["['bcol', 'r4']"] <= 9):
                distance_to_red_agents = 1

            return distance_to_red_base / distance_to_red_agents

    elif constants.CUSTOM_HEURISTIC_ID == 1:
        COLLISION_DIS = 4.2
        xb1 = state.state_vars["['x_b', 'b1']"]
        yb1 = state.state_vars["['y_b', 'b1']"]
        xb2 = state.state_vars["['x_b', 'b2']"]
        yb2 = state.state_vars["['y_b', 'b2']"]
        xb3 = state.state_vars["['x_b', 'b3']"]
        yb3 = state.state_vars["['y_b', 'b3']"]
        xr1 = state.state_vars["['x_b', 'r1']"]
        yr1 = state.state_vars["['y_b', 'r1']"]
        xr2 = state.state_vars["['x_b', 'r2']"]
        yr2 = state.state_vars["['y_b', 'r2']"]
        xr3 = state.state_vars["['x_b', 'r3']"]
        yr3 = state.state_vars["['y_b', 'r3']"]
        bb1 = state.state_vars["['bearing', 'b1']"]
        bb2 = state.state_vars["['bearing', 'b2']"]
        bb3 = state.state_vars["['bearing', 'b3']"]
        # print(xb1,yb1)
        # print(state.state_vars["['turn_rate', 'b1']"], state.state_vars["['v_b', 'b1']"])
        # print(bb1)

        heuristic_score = 0
        if state.state_vars["['score_blue']"] > state.state_vars["['score_red']"]:
            # print(state.state_vars["['score_blue']"])
            return 0
        if state.state_vars["['has_red_flag', 'b1']"] or state.state_vars["['has_red_flag', 'b2']"] or state.state_vars["['has_red_flag', 'b3']"]:
            # print('has_red_flag')
            # print(state.state_vars["['has_red_flag', 'b1']"],state.state_vars["['has_red_flag', 'b2']"],state.state_vars["['has_red_flag', 'b3']"], xb1,yb1,xb2,yb2,xb3,yb3)
            return 3
        if state.state_vars["['tagged_blue', 'b1']"] or state.state_vars["['tagged_blue', 'b2']"] or state.state_vars["['tagged_blue', 'b3']"] :
            heuristic_score += 100
        if state.state_vars["['score_red']"] > state.state_vars["['score_blue']"]:
            heuristic_score += 700
        if dis_pts(xb1,yb1,xb2,yb2) <= COLLISION_DIS or dis_pts(xb1,yb1,xb3,yb3) <= COLLISION_DIS or dis_pts(xb2,yb2,xb3,yb3) <= COLLISION_DIS or dis_pts(xb1,yb1,xr1,yr1) <= COLLISION_DIS or dis_pts(xb1,yb1,xr2,yr2) <= COLLISION_DIS or dis_pts(xb1,yb1,xr3,yr3) <= COLLISION_DIS or dis_pts(xb2,yb2,xr1,yr1) <= COLLISION_DIS or dis_pts(xb2,yb2,xr2,yr2) <= COLLISION_DIS or dis_pts(xb2,yb2,xr3,yr3) <= COLLISION_DIS or dis_pts(xb3,yb3,xr1,yr1) <= COLLISION_DIS or dis_pts(xb3,yb3,xr2,yr2) <= COLLISION_DIS or dis_pts(xb3,yb3,xr3,yr3) <= COLLISION_DIS:
            heuristic_score += 500
        # if state.time < 20 and (bb1 < 1 or bb2 < 1 or bb3 < 1):
        #     heuristic_score += 30
        if heuristic_score != 0:
            pass
        #     print(heuristic_score)
        dis = dis_pts(state.state_vars["['x_base_red']"], state.state_vars["['y_base_red']"], xb1, yb1)
        # print(dis)
        # print(state.state_vars["['turn_rate', 'b1']"])
        return heuristic_score

    if constants.CUSTOM_HEURISTIC_ID == 2: #single agent test
        bb1 = state.state_vars["['bearing', 'b1']"]
        xb1 = state.state_vars["['x_b', 'b1']"]
        yb1 = state.state_vars["['y_b', 'b1']"]
        dis = dis_pts(state.state_vars["['x_base_red']"], state.state_vars["['y_base_red']"], xb1, yb1)
        print(xb1,yb1,state.state_vars["['x_base_red']"], state.state_vars["['y_base_red']"], dis, state.state_vars["['turn_rate', 'b1']"], bb1)

        if state.state_vars["['has_red_flag', 'b1']"]:
            print("has_red_flag")
            return 0
        if state.time < 20 and (bb1 < 1):
            return 10000
        if state.state_vars["['turn_rate', 'b1']"] == 0:
            return 100
        else:
            return 5
        # xb1 = state.state_vars["['x_b', 'b1']"]
        # yb1 = state.state_vars["['y_b', 'b1']"]
        # dis = dis_pts(state.state_vars["['x_base_red']"], state.state_vars["['y_base_red']"], xb1, yb1)
        # print(dis)
        return dis
