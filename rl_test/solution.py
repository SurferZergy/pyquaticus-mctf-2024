import numpy as np
from pddl.pddl_plus import *
from pddl.nyx import nyx
import os
import math
import random
import copy
from itertools import groupby
# from ray.rllib.policy.policy import Policy
#Need an added import for codalab competition submission?
#Post an issue to the github and we will work to get it added into the system!


#YOUR CODE HERE

#Load in your trained model and return the corresponding agent action based on the information provided in step()
class solution:
	#Add Variables required for solution

    def __init__(self):
        self.replan_b1 = True
        # self.replan_b0 = True
        # self.replan_b2 = True
        self.b1_actions = []
        # self.b0_actions = []
        # self.b2_actions = []
        self.n = 100 # number of actions b4 replan # need to set
        self.default_n = 100
        self.heuristic = 5
        self.b1_full_speed = True # need to set
        # self.b0_full_speed = True  # need to set
        # self.b2_full_speed = True  # need to set
        self.b1_heading = 100  # set to wall 0 bearing
        # self.b0_heading = 90  # set to wall 0 bearing
        # self.b2_heading = 90  # set to wall 0 bearing
        # self.curr_time = 0.0
        # self.time_inc = 0.1
        # self.noop = False
        # self.tmp = []
        self.steps_2_turn = 132//3
        self.steps_2_move_1_cell = 200//3
        self.c = 0
        # for _ in range(self.steps_2_turn):
        #     self.tmp.append(2) #up
        # # for _ in range (self.steps_2_turn):
        # #     self.tmp.append(6) #left
        # for _ in range(130):
        #     self.tmp.append(4) #keep going
        # for _ in range(self.steps_2_turn * 2):
        #     self.tmp.append(6) #turn around
        # for _ in range(self.steps_2_move_1_cell * 2):
        #     self.tmp.append(4)


    def calculate_new_point(self, x1, y1, distance, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        x2 = x1 + distance * math.cos(angle_radians)
        y2 = y1 + distance * math.sin(angle_radians)
        return x2, y2

	#Given an observation return a valid action agent_id is agent that needs an action, observation space is the current normalized observation space for the specific agent
    def compute_action(self,agent_id:int, observation_normalized:list, observation:dict, full_observation:dict):

        if agent_id == 1 or agent_id == 4:

            self.b1_heading = (observation[('wall_0_bearing')] + 360) % 360

            if agent_id == 4:
                self.b1_heading = (observation[('wall_2_bearing')] + 360) % 360
            # xb1 = observation[('wall_3_distance')]
            # yb1 = observation[('wall_2_distance')]

            #adjust bearing
            if (len(self.b1_actions) == 1 or all(e == 4 for e in self.b1_actions[:5])) and ((4 <= self.b1_heading <= 86) or (94 <= self.b1_heading <= 176) or (184 <= self.b1_heading <= 266) or (276 <= self.b1_heading <= 356)):
                if 0 < self.b1_heading < 45 or 90 < self.b1_heading < 135 or 180 < self.b1_heading < 225 or 270 < self.b1_heading < 315:
                    return 2
                else:
                    return 6

            if self.replan_b1:
                # self.b1_actions = self.calc_actions(observation, agent_id)[:self.n]
                temp_b1_actions = self.calc_actions(full_observation, agent_id)
                duplicate_actions = [sum(1 for _ in group) for _, group in groupby(temp_b1_actions)]
                self.n = min(self.default_n, duplicate_actions[0])
                self.b1_actions = temp_b1_actions[:self.n]
                self.replan_b1 = False
            elif len(self.b1_actions) == 1: # last action, need to replan next time
                self.replan_b1 = True
                return self.b1_actions[0]
            # else:
            #     self.replan_b1 = True
            #     return 2

            self.c += 1
            b1_current_action = self.b1_actions[0]
            self.b1_actions = self.b1_actions[1:]
            # print(b1_current_action, 'step', self.c)
            return b1_current_action

        if agent_id == 0 or agent_id == 5:
            return 2

        if agent_id == 2 or agent_id == 3:
            return 6

    def calc_actions(self, obs, ag_id):
        backup_plan = []
        # Create PDDL Problem

        prob = None

        if ag_id == 4:
            prob = self.create_pddl_problem_red(obs)
        elif ag_id == 1:
            prob = self.create_pddl_problem_blue(obs)

        self.pddl_p_to_file(prob, 'prob_{}.pddl'.format(ag_id))

        # Run PDDL
        dir = os.path.dirname(os.path.realpath(__file__))+'/pddl/'
        try:
            # nyx.runner("./pddl/domain.pddl", "./pddl/prob.pddl", ['-v', 't:5', '-to:15', '-noplan', '-search:gbfs', 'custom_h:1'])
            # nyx.runner("./pddl/domain.pddl", "./pddl/nyx/prob_2.pddl", ['-v', 't:5', '-to:30', '-search:gbfs', 'custom_h:1'])

            if ag_id == 4:
                self.heuristic = 6
            elif ag_id == 1:
                self.heuristic = 5

            plan_found = nyx.runner(dir+"domain.pddl", dir+"prob_{}.pddl".format(ag_id), ['-v', '-to:30', '-search:gbfs', '-custom_h:{}'.format(self.heuristic)])
            if not plan_found:
                for _ in range (30):
                    backup_plan.append(4)
                for _ in range(self.steps_2_turn*4):
                    backup_plan.append(2)
                return backup_plan
        except Exception as e:
            print('no plan found, using default plan.', 'Error:', e)

        # Get actions from PDDL results
        plan_actions = self.extract_actions_from_plan_trace(dir+"plans/plan1_prob_{}.pddl".format(ag_id))
        # plan_actions = self.extract_actions_from_plan_trace("./pddl/plans/test_plan.pddl")

        # Convert actions to discrete
        b1_plan_actions_num = self.convert_actions(plan_actions)

        # plan_actions = [1,2,3]
        # plan_action = plan_actions[0] # or n step
        return b1_plan_actions_num

    def extract_actions_from_plan_trace(self, plane_trace_file: str):
        plan_actions = PddlPlusPlan()
        lines_list = open(plane_trace_file).readlines()
        with open(plane_trace_file) as plan_trace_file:
            for i, line in enumerate(plan_trace_file):
                # print(str(i) + " =====> " + str(line))
                if "No Plan Found!" in line:
                    plan_actions.append(TimedAction("out of memory", 1.0))
                    # if the planner ran out of memory:
                    # change the goal to killing a single pig to make the problem easier and try again with one fewer pig
                    return plan_actions
                if "blue_move" in line:
                    action_name = (line.split(':')[1].split('[')[0])
                    action_time_step = float(line.split(':')[0])
                    ta = TimedAction(action_name, action_time_step)
                    plan_actions.append(ta)
                if "syntax error" in line:
                    plan_actions.append(TimedAction("syntax error", 0.0))
                    break

                if "0 goals found" in line:

                    break

        return plan_actions


    def create_pddl_problem_blue(self, obs):
        pddl_problem = PddlPlusProblem()
        pddl_problem.domain = 'mctf'
        pddl_problem.name = 'mctf-problem'
        pddl_problem.metric = 'minimize(total-time)'
        pddl_problem.objects = []
        pddl_problem.init = []
        pddl_problem.goal = []

        # objs
        pddl_problem.objects.append(['b1', 'blue'])
        pddl_problem.objects.append(['b0', 'red'])
        pddl_problem.objects.append(['b2', 'red'])
        pddl_problem.objects.append(['r0', 'red'])
        pddl_problem.objects.append(['r1', 'red'])
        pddl_problem.objects.append(['r2', 'red'])

        #calc positions
        xb1 = obs[1][('wall_3_distance')]
        yb1 = obs[1][('wall_2_distance')]
        xb0 = obs[0][('wall_3_distance')]
        yb0 = obs[0][('wall_2_distance')]
        xb2 = obs[2][('wall_3_distance')]
        yb2 = obs[2][('wall_2_distance')]
        xr0 = obs[3][('wall_1_distance')]
        yr0 = obs[3][('wall_0_distance')]
        xr1 = obs[4][('wall_1_distance')]
        yr1 = obs[4][('wall_0_distance')]
        xr2 = obs[5][('wall_1_distance')]
        yr2 = obs[5][('wall_0_distance')]

        # init
        xc, yc = self.translate_coord_to_row_col(xb1, yb1)
        pddl_problem.init.append(['=', ['brow', 'b1'], yc])
        pddl_problem.init.append(['=', ['bcol', 'b1'], xc])
        # pddl_problem.init.append(['=', ['brow', 'b1'], 8]) #to trigger no plan found
        # pddl_problem.init.append(['=', ['bcol', 'b1'], 8])

        xc, yc = self.translate_coord_to_row_col(xb0, yb0)
        pddl_problem.init.append(['=', ['rrow', 'b0'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b0'], xc])
        xc, yc = self.translate_coord_to_row_col(xb2, yb2)
        pddl_problem.init.append(['=', ['rrow', 'b2'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b2'], xc])

        xc, yc = self.translate_coord_to_row_col(xr1, yr1)
        pddl_problem.init.append(['=', ['rrow', 'r1'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r1'], xc])
        xc, yc = self.translate_coord_to_row_col(xr2, yr2)
        pddl_problem.init.append(['=', ['rrow', 'r2'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r2'], xc])
        xc, yc = self.translate_coord_to_row_col(xr0, yr0)
        pddl_problem.init.append(['=', ['rrow', 'r0'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r0'], xc])

        pddl_problem.init.append(['=', ['rbrow'], '4'])
        pddl_problem.init.append(['=', ['rbcol'], '2'])
        pddl_problem.init.append(['=', ['bbrow'], '4'])
        pddl_problem.init.append(['=', ['bbcol'], '14'])

        has_flag = obs[1][('has_flag')]
        if has_flag:
            pddl_problem.init.append(['blue_has_flag', 'b1'])
        else:
            pddl_problem.init.append(['red_flag_at_red_base'])

        if (obs[0][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'b0'])
        if (obs[2][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'b2'])
        if (obs[3][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'r0'])
        if (obs[4][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'r1'])
        if (obs[5][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'r2'])

        pddl_problem.goal.append(['>=', ['bcol', 'b1'], '9'])
        pddl_problem.goal.append(['blue_has_flag', 'b1'])
        pddl_problem.goal.append(['not', ['blue_collide', 'b1']])

        return pddl_problem

    def create_pddl_problem_red(self, obs):
        pddl_problem = PddlPlusProblem()
        pddl_problem.domain = 'mctf'
        pddl_problem.name = 'mctf-problem'
        pddl_problem.metric = 'minimize(total-time)'
        pddl_problem.objects = []
        pddl_problem.init = []
        pddl_problem.goal = []

        # objs
        pddl_problem.objects.append(['r4', 'blue'])
        pddl_problem.objects.append(['r3', 'red'])
        pddl_problem.objects.append(['r5', 'red'])
        pddl_problem.objects.append(['b0', 'red'])
        pddl_problem.objects.append(['b1', 'red'])
        pddl_problem.objects.append(['b2', 'red'])


        #calc positions
        xr4 = obs[4][('wall_1_distance')]
        yr4 = obs[4][('wall_0_distance')]
        xr3 = obs[3][('wall_1_distance')]
        yr3 = obs[3][('wall_0_distance')]
        xr5 = obs[5][('wall_1_distance')]
        yr5 = obs[5][('wall_0_distance')]
        xb0 = obs[0][('wall_3_distance')]
        yb0 = obs[0][('wall_2_distance')]
        xb1 = obs[1][('wall_3_distance')]
        yb1 = obs[1][('wall_2_distance')]
        xb2 = obs[2][('wall_3_distance')]
        yb2 = obs[2][('wall_2_distance')]
        # xr2, yb2 = self.calc_abs_pos(xb1, yb1, obs[1], 'teammate_0')
        # xb3, yb3 = self.calc_abs_pos(xb1, yb1, obs[1], 'teammate_1')
        # xr1, yr1 = self.calc_abs_pos(xb1, yb1, obs[1], 'opponent_0')
        # xr2, yr2 = self.calc_abs_pos(xb1, yb1, obs[1], 'opponent_1')
        # xr3, yr3 = self.calc_abs_pos(xb1, yb1, obs[1], 'opponent_2')

        # init
        xc, yc = self.translate_coord_to_row_col(xr4, yr4)
        pddl_problem.init.append(['=', ['brow', 'r4'], yc])
        pddl_problem.init.append(['=', ['bcol', 'r4'], xc])
        # pddl_problem.init.append(['=', ['brow', 'b1'], 8]) #to trigger no plan found
        # pddl_problem.init.append(['=', ['bcol', 'b1'], 8])

        xc, yc = self.translate_coord_to_row_col(xr3, yr3)
        pddl_problem.init.append(['=', ['rrow', 'r3'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r3'], xc])
        xc, yc = self.translate_coord_to_row_col(xr5, yr5)
        pddl_problem.init.append(['=', ['rrow', 'r5'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r5'], xc])

        xc, yc = self.translate_coord_to_row_col(xb0, yb0)
        pddl_problem.init.append(['=', ['rrow', 'b0'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b0'], xc])
        xc, yc = self.translate_coord_to_row_col(xb1, yb1)
        pddl_problem.init.append(['=', ['rrow', 'b1'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b1'], xc])
        xc, yc = self.translate_coord_to_row_col(xb2, yb2)
        pddl_problem.init.append(['=', ['rrow', 'b2'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b2'], xc])

        pddl_problem.init.append(['=', ['bbrow'], '4'])
        pddl_problem.init.append(['=', ['bbcol'], '2'])
        pddl_problem.init.append(['=', ['rbrow'], '4'])
        pddl_problem.init.append(['=', ['rbcol'], '14'])

        has_flag = obs[4][('has_flag')]
        if has_flag:
            pddl_problem.init.append(['blue_has_flag', 'r4'])
        else:
            pddl_problem.init.append(['red_flag_at_red_base'])

        if (obs[0][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'b0'])
        if (obs[1][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'b1'])
        if (obs[2][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'b2'])
        if (obs[3][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'r3'])
        if (obs[5][("is_tagged")]):
            pddl_problem.init.append(['red_tagged', 'r5'])


        pddl_problem.goal.append(['<=', ['bcol', 'r4'], '7'])
        pddl_problem.goal.append(['blue_has_flag', 'r4'])
        pddl_problem.goal.append(['not', ['blue_collide', 'r4']])

        return pddl_problem

    def translate_coord_to_row_col(self, xb1, yb1):
        xc = round(xb1 / 10)
        if xc > 15:
            xc = 15
        yc = round(yb1 / 10)
        if yc > 7:
            yc = 7
        return xc, yc

    def calc_abs_pos(self, xb1 , yb1, obs, agent):
        other_agent_dis = obs[(agent, 'distance')]
        wall_bearing = obs[('wall_1_bearing')] # needs to be the pos X axis
        other_agent_bearing_to_you = obs[(agent, 'bearing')]
        other_agent_bearing_to_xaxis = wall_bearing - other_agent_bearing_to_you
        # wall_bearing = self.convert_angle_to_pos_aka_clockwise(wall_bearing)
        # other_agent_bearing_to_you = self.convert_angle_to_pos_aka_clockwise(other_agent_bearing_to_you)
        # other_agent_bearing_to_xaxis = other_agent_bearing_to_you - wall_bearing
        return self.calculate_new_point(xb1, yb1, other_agent_dis, other_agent_bearing_to_xaxis)


    def pddl_p_to_file(self, pddl_problem: PddlPlusProblem, output_file_name):
        parse_utils = PddlParserUtils()

        # dir = "./pddl/"
        dir = os.path.dirname(os.path.realpath(__file__))+'/pddl/'
        output = os.path.join(dir, output_file_name)
        out_file = open(output, "w")
        out_file.write("(define(problem %s)\n" % pddl_problem.name)
        out_file.write("(:domain %s)\n" % pddl_problem.domain)

        # Print objects
        out_file.write("(:objects ")
        for object in pddl_problem.objects:
            out_file.write("%s - %s " % (object[0], object[1]))
        out_file.write(")\n")

        # Print init facts
        out_file.write("(:init ")
        for init_fact in pddl_problem.init:
            parse_utils.write_tokens(init_fact, out_file, prefix_str="\t", suffix_str="\n")
        out_file.write(")\n")

        out_file.write("(:goal (and ")
        for goal_fact in pddl_problem.goal:
            parse_utils.write_tokens(goal_fact, out_file, prefix_str=" ", suffix_str=" ")
        out_file.write("))\n")

        out_file.write("(:metric %s)\n" % pddl_problem.metric)

        out_file.write(")\n")
        out_file.close()

    def convert_actions(self, plan_actions):
        # self.curr_time = 0.0
        b1_plan_actions_num = []

        for n in range(len(plan_actions)):
            if plan_actions[n].action_name.__contains__("move-north"):
                if 60 <= self.b1_heading <= 120:  # heading west
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(2)
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if 150 <= self.b1_heading <= 210:  # heading south
                    for _ in range (self.steps_2_turn*3//2):
                        b1_plan_actions_num.append(2)
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if 240 <= self.b1_heading <= 300:  # heading east
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(6)
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if self.b1_heading <= 30 or self.b1_heading >= 300:  # heading north
                    for _ in range(self.steps_2_move_1_cell):
                        b1_plan_actions_num.append(4)
                self.b1_heading = 0 # after moving north, bearing is now changed
            if plan_actions[n].action_name.__contains__("move-south"):
                if 60 <= self.b1_heading <= 120:  # heading west
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(6)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if 150 <= self.b1_heading <= 210:  # heading south
                    for _ in range(self.steps_2_move_1_cell):
                        b1_plan_actions_num.append(4)
                if 240 <= self.b1_heading <= 300:  # heading east
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(2)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if self.b1_heading <= 30 or self.b1_heading >= 300:  # heading north
                    for _ in range(self.steps_2_turn * 2):
                        b1_plan_actions_num.append(2)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                self.b1_heading = 180 # after moving north, bearing is now changed
            if plan_actions[n].action_name.__contains__("move-west"):
                if 60 <= self.b1_heading <= 120:  # heading west
                    for _ in range(self.steps_2_move_1_cell):
                        b1_plan_actions_num.append(4)
                if 150 <= self.b1_heading <= 210:  # heading south
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(2)
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if 240 <= self.b1_heading <= 300:  # heading east
                    for _ in range(self.steps_2_turn*2):
                        b1_plan_actions_num.append(2)
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if self.b1_heading <= 30 or self.b1_heading >= 300:  # heading north
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(6)
                    for _ in range (self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                self.b1_heading = 90 # after moving north, bearing is now changed
            if plan_actions[n].action_name.__contains__("move-east"):
                if 60 <= self.b1_heading <= 120:  # heading west
                    for _ in range(self.steps_2_turn*3):
                        b1_plan_actions_num.append(2)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(6)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if 150 <= self.b1_heading <= 210:  # heading south
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(6)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                if 240 <= self.b1_heading <= 300:  # heading east
                    for _ in range(self.steps_2_move_1_cell):
                        b1_plan_actions_num.append(4)
                if self.b1_heading <= 30 or self.b1_heading >= 300:  # heading north
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(2)
                    for _ in range(self.steps_2_turn):
                        b1_plan_actions_num.append(4)
                self.b1_heading = 270 # after moving north, bearing is now changed


        # self.curr_time += self.time_inc
        # self.curr_time = round(self.curr_time, 5) # wtf, 0.3 becomes 0.30000000000000004, so we do this

        return b1_plan_actions_num


class PddlParserUtils:
    """
    A class with utility function to help parse PDDL files.
    """

    def tokenize(self, file_name: str) -> list:
        """ Converts the file in a list of tokens, considering space and newline as a delimiter,
                and considers each parenthesis as a token"""
        in_file = open(file_name, encoding='utf-8-sig')
        file_tokens = list()
        for line in in_file.readlines():
            if line.strip().startswith(";"):  # A comment line
                continue
            if ';' in line:
                line = line[:line.find(';')]  # strip away inline comment
            line_tokens = line.lower().replace("(", " ( ").replace(")", " ) ").split()
            for token in line_tokens:
                if len(token.strip()) == 0:
                    continue
                file_tokens.append(token)
        in_file.close()
        return file_tokens

    def read_from_tokens(self, tokens: list):
        """ A recursive function to create nodes in the parse tree"""
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF")
        token = tokens.pop(0)

        if token == '(':
            node = []
            while tokens[0] != ')':
                node.append(self.read_from_tokens(tokens))

            tokens.pop(0)  # pop off ')'
            return node
        elif token == ')':
            raise SyntaxError('unexpected )')
        else:
            return token  # A basic atom in the syntax tree

    def parse_syntax_tree(self, file_name: str) -> list():
        """ Accepts a file written in LISP and outputs a syntax tree, in the form of a list of lists (recursively) """

        tokens = self.tokenize(file_name)
        return self.read_from_tokens(tokens)

    def write_tokens(self, tokens: list, out_file, prefix_str="", suffix_str="\n"):
        """ A recursive function to create nodes in the parse tree"""

        out_file.write("%s(" % prefix_str)
        first_token = True
        for token in tokens:
            if type(token) is list:
                if len(token) < 3:
                    self.write_tokens(token, out_file, prefix_str=" ", suffix_str=" ")
                else:
                    self.write_tokens(token, out_file, prefix_str)
            else:
                if first_token == False:
                    out_file.write(" %s" % token)
                else:
                    out_file.write("%s" % token)
            first_token = False

        out_file.write(")%s" % suffix_str)

#END OF CODE SECTION
