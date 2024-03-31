import numpy as np
from pddl.pddl_plus import *
from pddl.nyx import nyx
import os
import math
import random
# from ray.rllib.policy.policy import Policy
#Need an added import for codalab competition submission?
#Post an issue to the github and we will work to get it added into the system!


#YOUR CODE HERE

#Load in your trained model and return the corresponding agent action based on the information provided in step()
class solution:
	#Add Variables required for solution
	
    def __init__(self):
        self.replan = True
        self.b1_actions = []
        # self.b2_actions = []
        # self.b3_actions = []
        self.n = 100 # number of actions b4 replan # need to set
        self.b1_full_speed = True # need to set
        # self.b2_full_speed = True  # need to set
        # self.b3_full_speed = True  # need to set
        self.b1_heading = 100  # set to wall 0 bearing
        # self.b2_heading = 90  # set to wall 0 bearing
        # self.b3_heading = 90  # set to wall 0 bearing
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
    def compute_action(self,agent_id:int, observation_normalized:list, observation:dict):

        if agent_id == 1:
            self.b1_heading = (observation[('wall_0_bearing')] + 360) % 360
            xb1 = observation[('wall_3_distance')]
            yb1 = observation[('wall_2_distance')]

            #adjust bearing
            if (len(self.b1_actions) == 1 or all(e == 4 for e in self.b1_actions[:5])) and ((4 <= self.b1_heading <= 86) or (94 <= self.b1_heading <= 176) or (184 <= self.b1_heading <= 266) or (276 <= self.b1_heading <= 356)):
                if 0 < self.b1_heading < 45 or 90 < self.b1_heading < 135 or 180 < self.b1_heading < 225 or 270 < self.b1_heading < 315:
                    return 2
                else:
                    return 6

            if self.replan:
                self.b1_actions = self.calc_actions(observation)[:self.n]
                self.replan = False
            elif len(self.b1_actions) == 1: # last action, need to replan next time
                self.replan = True
                return self.b1_actions[0]

            self.c += 1
            b1_current_action = self.b1_actions[0]
            self.b1_actions = self.b1_actions[1:]
            # print(b1_current_action, 'step', self.c)
            return b1_current_action

        if agent_id == 0:
            return 2
        if agent_id == 2:
            return 6

    def calc_actions(self, obs):
        backup_plan = []
        # Create PDDL Problem
        prob = self.create_pddl_problem(obs)
        self.pddl_p_to_file(prob, 'prob.pddl')

        # Run PDDL
        dir = os.path.dirname(os.path.realpath(__file__))+'/pddl/'
        try:
            # nyx.runner("./pddl/domain.pddl", "./pddl/prob.pddl", ['-v', 't:5', '-to:15', '-noplan', '-search:gbfs', 'custom_h:1'])
            # nyx.runner("./pddl/domain.pddl", "./pddl/nyx/prob_2.pddl", ['-v', 't:5', '-to:30', '-search:gbfs', 'custom_h:1'])
            plan_found = nyx.runner(dir+"domain.pddl", dir+"prob.pddl", ['-v', '-to:30', '-search:bfs'])
            if not plan_found:
                for _ in range (30):
                    backup_plan.append(4)
                for _ in range(self.steps_2_turn*4):
                    backup_plan.append(2)
                return backup_plan
        except Exception as e:
            print('no plan found, using default plan.', 'Error:', e)

        # Get actions from PDDL results
        plan_actions = self.extract_actions_from_plan_trace(dir+"plans/plan1_prob.pddl")
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


    def create_pddl_problem(self, obs):
        pddl_problem = PddlPlusProblem()
        pddl_problem.domain = 'mctf'
        pddl_problem.name = 'mctf-problem'
        pddl_problem.metric = 'minimize(total-time)'
        pddl_problem.objects = []
        pddl_problem.init = []
        pddl_problem.goal = []


        # objs
        pddl_problem.objects.append(['b1', 'blue'])
        pddl_problem.objects.append(['b2', 'red'])
        pddl_problem.objects.append(['b3', 'red'])
        pddl_problem.objects.append(['r1', 'red'])
        pddl_problem.objects.append(['r2', 'red'])
        pddl_problem.objects.append(['r3', 'red'])
        for i in range (1,8):
            for j in range (1,16):
                pddl_problem.objects.append(['cell'+str(j)+'_'+str(i), 'cell'])


        #calc positions
        xb1 = obs[('wall_3_distance')]
        yb1 = obs[('wall_2_distance')]
        xb2, yb2 = self.calc_abs_pos(xb1, yb1, obs, 'teammate_0')
        xb3, yb3 = self.calc_abs_pos(xb1, yb1, obs, 'teammate_1')
        xr1, yr1 = self.calc_abs_pos(xb1, yb1, obs, 'opponent_0')
        xr2, yr2 = self.calc_abs_pos(xb1, yb1, obs, 'opponent_1')
        xr3, yr3 = self.calc_abs_pos(xb1, yb1, obs, 'opponent_2')

        # init
        xc, yc = self.translate_coord_to_row_col(xb1, yb1)
        pddl_problem.init.append(['=', ['brow', 'b1'], yc])
        pddl_problem.init.append(['=', ['bcol', 'b1'], xc])
        # pddl_problem.init.append(['=', ['brow', 'b1'], 8]) #to trigger no plan found
        # pddl_problem.init.append(['=', ['bcol', 'b1'], 8])

        xc, yc = self.translate_coord_to_row_col(xb2, yb2)
        pddl_problem.init.append(['=', ['rrow', 'b2'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b2'], xc])
        xc, yc = self.translate_coord_to_row_col(xb3, yb3)
        pddl_problem.init.append(['=', ['rrow', 'b3'], yc])
        pddl_problem.init.append(['=', ['rcol', 'b3'], xc])

        xc, yc = self.translate_coord_to_row_col(xr1, yr1)
        pddl_problem.init.append(['=', ['rrow', 'r1'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r1'], xc])
        xc, yc = self.translate_coord_to_row_col(xr2, yr2)
        pddl_problem.init.append(['=', ['rrow', 'r2'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r2'], xc])
        xc, yc = self.translate_coord_to_row_col(xr3, yr3)
        pddl_problem.init.append(['=', ['rrow', 'r3'], yc])
        pddl_problem.init.append(['=', ['rcol', 'r3'], xc])

        pddl_problem.init.append(['=', ['rbrow'], '4'])
        pddl_problem.init.append(['=', ['rbcol'], '2'])
        pddl_problem.init.append(['=', ['bbrow'], '4'])
        pddl_problem.init.append(['=', ['bbcol'], '14'])

        has_flag = obs[('has_flag')]
        if has_flag:
            pddl_problem.init.append(['blue_has_flag', 'b1'])
        else:
            pddl_problem.init.append(['red_flag_at_red_base'])

        for i in range(1,8):
            for j in range(1,16):
                pddl_problem.init.append(['=', ['col', 'cell'+str(j)+'_'+str(i)], str(j)])
                pddl_problem.init.append(['=', ['row', 'cell' + str(j) + '_' + str(i)], str(i)])

        # pddl_problem.init.append(['=', ['x_base_blue'], '140'])
        # pddl_problem.init.append(['=', ['y_base_blue'], '40'])
        # pddl_problem.init.append(['=', ['x_base_red'], '20'])
        # pddl_problem.init.append(['=', ['y_base_red'], '40'])
        # pddl_problem.init.append(['=', ['r_agent'], '2'])
        # pddl_problem.init.append(['=', ['r_catch'], '10'])
        # pddl_problem.init.append(['=', ['r_collision'], '2.2'])
        # pddl_problem.init.append(['=', ['r_capture'], '10'])
        #
        # pddl_problem.init.append(['=', ['x_max'], '160'])
        # pddl_problem.init.append(['=', ['x_min'], '0'])
        # pddl_problem.init.append(['=', ['y_max'], '80'])
        # pddl_problem.init.append(['=', ['y_min'], '0'])
        # pddl_problem.init.append(['=', ['max_cooldown_time'], '30'])
        #
        # pddl_problem.init.append(['=', ['cooldown_time_blue', 'b1'], obs['tagging_cooldown']])
        # pddl_problem.init.append(['=', ['cooldown_time_blue', 'b2'], obs[('teammate_0', 'tagging_cooldown')]])
        # pddl_problem.init.append(['=', ['cooldown_time_blue', 'b3'], obs[('teammate_1', 'tagging_cooldown')]])
        # pddl_problem.init.append(['=', ['cooldown_time_red', 'r1'], obs[('opponent_0', 'tagging_cooldown')]])
        # pddl_problem.init.append(['=', ['cooldown_time_red', 'r2'], obs[('opponent_1', 'tagging_cooldown')]])
        # pddl_problem.init.append(['=', ['cooldown_time_red', 'r3'], obs[('opponent_2', 'tagging_cooldown')]])
        #
        # pddl_problem.init.append(['=', ['v_max'], '1.5'])
        #
        # pddl_problem.init.append(['=', ['score_blue'], obs['team_score']])
        # pddl_problem.init.append(['=', ['score_red'], obs['opponent_score']])
        #
        # pddl_problem.init.append(['ready'])
        # pddl_problem.init.append(['adjustable_handling'])
        # pddl_problem.init.append(['blue_flag_at_blue_base'])
        # pddl_problem.init.append(['red_flag_at_red_base'])


        # goal
        # # pddl_problem.goal.append(['pole_position'])
        # pddl_problem.goal.append(['not', ['total_failure']])
        # pddl_problem.goal.append(['=', ['brow', 'b1'], '4'])
        pddl_problem.goal.append(['>=', ['bcol', 'b1'], '9'])
        pddl_problem.goal.append(['blue_has_flag', 'b1'])
        pddl_problem.goal.append(['not', ['blue_collide', 'b1']])


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
