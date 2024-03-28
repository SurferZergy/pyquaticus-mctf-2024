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
        self.b2_actions = []
        self.b3_actions = []
        self.n = 500 # number of actions b4 replan # need to set
        self.b1_full_speed = True # need to set
        self.b2_full_speed = True  # need to set
        self.b3_full_speed = True  # need to set
        self.b1_heading = 90  # set to wall 0 bearing
        self.b2_heading = 90  # set to wall 0 bearing
        self.b3_heading = 90  # set to wall 0 bearing
        self.curr_time = 0.0
        self.time_inc = 0.1
        # self.noop = False
        self.tmp = []
        self.steps_2_turn = 130
        self.steps_2_move_1_cell = 200
        self.c = 0
        for _ in range(self.steps_2_turn):
            self.tmp.append(2) #up
        for _ in range (self.steps_2_turn):
            self.tmp.append(6) #left
        for _ in range(self.steps_2_move_1_cell*2):
            self.tmp.append(4) #keep going
        for _ in range(self.steps_2_turn * 2):
            self.tmp.append(6) #turn around
        for _ in range(self.steps_2_move_1_cell * 2):
            self.tmp.append(4)

    def convert_angle_to_pos_aka_clockwise(self, a):
        if a < 0:
            a += 360
        return a

    def calculate_new_point(self, x1, y1, distance, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        x2 = x1 + distance * math.cos(angle_radians)
        y2 = y1 + distance * math.sin(angle_radians)
        return x2, y2

	#Given an observation return a valid action agent_id is agent that needs an action, observation space is the current normalized observation space for the specific agent
    def compute_action(self,agent_id:int, observation_normalized:list, observation:dict):
        if agent_id == 0:
            self.b1_heading = (observation[('wall_0_bearing')] +360) %360
        xb1 = observation[('wall_3_distance')]
        yb1 = observation[('wall_2_distance')]
        print(xb1,yb1,self.b1_heading)

        if 60 <= self.b1_heading <=120: #heading west
            print('w')
        if 150 <= self.b1_heading <= 210:  # heading south
            print('s')
        if 240 <= self.b1_heading <= 300:  # heading east
            print('e')
        if self.b1_heading <=30 or self.b1_heading >=300:  # heading north
            print('n')

        a = self.tmp[0]
        self.tmp = self.tmp[1:]
        self.tmp.append(4)
        # print('a', a)
        return 2

        # if agent_id == 0:
        #     b1wzb = observation[('wall_0_bearing')]
        #
        #     xb1 = observation[('wall_3_distance')]
        #     yb1 = observation[('wall_2_distance')]
        #     other_agent_dis = observation[('teammate_0', 'distance')]
        #     wall_bearing = observation[('wall_1_bearing')]
        #     other_agent_bearing_to_you = observation[('teammate_0', 'bearing')]
        #     wall_bearing = self.convert_angle_to_pos_aka_clockwise(wall_bearing)
        #     other_agent_bearing_to_you = self.convert_angle_to_pos_aka_clockwise(other_agent_bearing_to_you)
        #     other_agent_bearing_to_xaxis = abs(other_agent_bearing_to_you - wall_bearing)
        #     xb2, yb2 = self.calculate_new_point(xb1, yb1, other_agent_dis, other_agent_bearing_to_xaxis)
        #     print('b1w0b', b1wzb)
        #     b = observation[('teammate_0', 'bearing')]
        #     print('b', b)
        #     rh = (360-observation[('teammate_0', 'relative_heading')]) % 360
        #     print('rh', rh)
        #     answer = (abs(b) + b1wzb) - rh
        #     print('answer', answer)
        #     print('yb2', yb2,'yb1', yb1)
        #     if yb2 < yb1:
        #         b2wzb = 180 - answer
        #     else:
        #         b2wzb = answer
        #     print('b2w0b', b2wzb)

            # b2_wall_0_bearing = (180 - (observation[('wall_0_bearing')]+observation[('teammate_0', 'bearing')])) + observation[('teammate_0', 'relative_heading')]
            # b3_wall_0_bearing = (180 - (observation[('wall_0_bearing')]+observation[('teammate_1', 'bearing')])) + observation[('teammate_1', 'relative_heading')]

            # print('b2 calc',b2_wall_0_bearing, 'b3 calc', b3_wall_0_bearing)
            #
            # print('b1 real x', observation[('wall_2_distance')])
            # print('b2 real y', observation[('wall_3_distance')])
            #
            # print('b1 wall 0', observation[('wall_0_bearing')])
            # print('b1 wall 2', observation[('wall_2_bearing')])


            # print('bb', observation[('teammate_0', 'bearing')])
            # xb2, yb2 = self.calculate_new_point(observation[('wall_3_distance')], observation[('wall_2_distance')], observation[('teammate_0', 'distance')], abs(observation[('teammate_0', 'bearing')]))
            #
            # self.b1_abs_loc = (observation[('wall_3_distance')], observation[('wall_2_distance')])
            # self.b1_heading = observation[('wall_0_bearing')]

            # print('b1 wb', observation[('wall_3_bearing')], 'ob', observation[('teammate_0', 'bearing')])
            # xb1 = observation[('wall_3_distance')]
            # yb1 = observation[('wall_2_distance')]
            # other_agent_dis = observation[('teammate_0', 'distance')]
            # print('b1 loc', xb1, yb1)
            # print('d', other_agent_dis)
            # wall_bearing = observation[('wall_1_bearing')]
            # print('maybe neg wall b', wall_bearing)
            # other_agent_bearing_to_you = observation[('teammate_0', 'bearing')]
            # print('maybe neg orh', other_agent_bearing_to_you)
            # wall_bearing = self.convert_angle_to_pos_aka_clockwise(wall_bearing)
            # print('pos wall b', wall_bearing)
            # other_agent_bearing_to_you = self.convert_angle_to_pos_aka_clockwise(other_agent_bearing_to_you)
            # print('pos orh', other_agent_bearing_to_you)
            # other_agent_bearing_to_xaxis = abs(other_agent_bearing_to_you - wall_bearing)
            # print('other_agent_bearing_to_xaxis', other_agent_bearing_to_xaxis)
            # xb2, yb2 = self.calculate_new_point(xb1, yb1, other_agent_dis, other_agent_bearing_to_xaxis)
            # print('xb2', xb2, 'yb2', yb2)
        if agent_id == 0:
            self.b1_heading = observation[('wall_0_bearing')]
        elif agent_id == 1:
            self.b2_heading = observation[('wall_0_bearing')]
        elif agent_id == 2:
            self.b3_heading = observation[('wall_0_bearing')]

        # print(self.b1_heading, self.b2_heading, self.b3_heading)

        # if agent_id == 0:
        #     return 7
        # elif agent_id == 1:
        #     if random.random() > 0.5:
        #         return 3
        #     else:
        #         return 5
        # elif agent_id == 2:
        #     return 6

        if self.replan:
            self.b1_actions, self.b2_actions,self.b3_actions = self.calc_actions(observation)[:self.n]
            self.b1_actions = self.b1_actions[:self.n]
            # print('b1 a', self.b1_actions)
            self.b2_actions = self.b2_actions[:self.n]
            self.b3_actions = self.b3_actions[:self.n]
            self.replan = False
        elif len(self.b1_actions) == 1 and len(self.b3_actions) == 1 and len(self.b2_actions) == 1: # last action, need to replan next time
                if agent_id == 0:
                    return self.b1_actions[0]
                if agent_id == 1:
                    return self.b2_actions[0]
                if agent_id == 2:
                    self.replan = True # agent_id=2 is always last one processed, so here we set replan to true after returning last action
                    return self.b3_actions[0]

        if agent_id == 0:
            b1_current_action = self.b1_actions[0]
            self.b1_actions = self.b1_actions[1:]
            return b1_current_action
        if agent_id == 1:
            b2_current_action = self.b2_actions[0]
            self.b2_actions = self.b2_actions[1:]
            return b2_current_action
        if agent_id == 2:
            b3_current_action = self.b3_actions[0]
            self.b3_actions = self.b3_actions[1:]
            return b3_current_action

    def calc_actions(self, obs):
        # Create PDDL Problem
        prob = self.create_pddl_problem(obs)
        self.pddl_p_to_file(prob, 'prob.pddl')

        # Run PDDL
        try:
            # nyx.runner("./pddl/domain.pddl", "./pddl/prob.pddl", ['-v', 't:5', '-to:15', '-noplan', '-search:gbfs', 'custom_h:1'])
            # nyx.runner("./pddl/domain.pddl", "./pddl/nyx/prob_2.pddl", ['-v', 't:5', '-to:30', '-search:gbfs', 'custom_h:1'])
            nyx.runner("./pddl/domain.pddl", "./pddl/prob.pddl",['-v', 't:5', '-to:30', '-search:gbfs', 'custom_h:1'])
        except Exception as e:
            print('no plan found, using default plan.', 'Error:', e)

        # Get actions from PDDL results
        # plan_actions = self.extract_actions_from_plan_trace("pddl/plans/plan1_prob.pddl")
        plan_actions = self.extract_actions_from_plan_trace("./pddl/nyx/plans/plan1_prob_2.pddl")

        # Convert actions to discrete
        b1_plan_actions_num, b2_plan_actions_num, b3_plan_actions_num = self.convert_actions(plan_actions,50)

        # plan_actions = [1,2,3]
        # plan_action = plan_actions[0] # or n step
        return b1_plan_actions_num, b2_plan_actions_num, b3_plan_actions_num

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
                if "straight_ahead" or "clockwise_90_full_speed" in line:
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
        pddl_problem.objects.append(['b2', 'blue'])
        pddl_problem.objects.append(['b3', 'blue'])
        pddl_problem.objects.append(['r1', 'red'])
        pddl_problem.objects.append(['r2', 'red'])
        pddl_problem.objects.append(['r3', 'red'])

        #calc positions
        xb1 = obs[('wall_3_distance')]
        yb1 = obs[('wall_2_distance')]
        xb2, yb2 = self.calc_abs_pos(xb1, yb1, obs, 'teammate_0')
        xb3, yb3 = self.calc_abs_pos(xb1, yb1, obs, 'teammate_1')
        xr1, yr1 = self.calc_abs_pos(xb1, yb1, obs, 'opponent_0')
        xr2, yr2 = self.calc_abs_pos(xb1, yb1, obs, 'opponent_1')
        xr3, yr3 = self.calc_abs_pos(xb1, yb1, obs, 'opponent_2')

        # init
        pddl_problem.init.append(['=', ['x_b', 'b1'], xb1])
        pddl_problem.init.append(['=', ['y_b', 'b1'], yb1])
        pddl_problem.init.append(['=', ['x_b', 'b2'], xb2])
        pddl_problem.init.append(['=', ['y_b', 'b2'], yb2])
        pddl_problem.init.append(['=', ['x_b', 'b3'], xb3])
        pddl_problem.init.append(['=', ['y_b', 'b3'], yb3])

        pddl_problem.init.append(['=', ['x_b', 'r1'], xr1])
        pddl_problem.init.append(['=', ['y_b', 'r1'], yr1])
        pddl_problem.init.append(['=', ['x_b', 'r2'], xr2])
        pddl_problem.init.append(['=', ['y_b', 'r2'], yr2])
        pddl_problem.init.append(['=', ['x_b', 'r3'], xr3])
        pddl_problem.init.append(['=', ['y_b', 'r3'], yr3])

        # pddl_problem.init.append(['=', ['v_b', 'b1'], obs['speed']])
        # pddl_problem.init.append(['=', ['v_b', 'b2'], obs[('teammate_0', 'speed')]])
        # pddl_problem.init.append(['=', ['v_b', 'b3'], obs[('teammate_1', 'speed')]])
        # pddl_problem.init.append(['=', ['v_r', 'r1'], obs[('opponent_0', 'speed')]])
        # pddl_problem.init.append(['=', ['v_r', 'r2'], obs[('opponent_1', 'speed')]])
        # pddl_problem.init.append(['=', ['v_r', 'r3'], obs[('opponent_2', 'speed')]])

        # Assume speed is 1.5 so we can plan
        pddl_problem.init.append(['=', ['v_b', 'b1'], '1.5'])
        pddl_problem.init.append(['=', ['v_b', 'b2'], '1.5'])
        pddl_problem.init.append(['=', ['v_b', 'b3'], '1.5'])
        pddl_problem.init.append(['=', ['v_r', 'r1'], '1.5'])
        pddl_problem.init.append(['=', ['v_r', 'r2'], '1.5'])
        pddl_problem.init.append(['=', ['v_r', 'r3'], '1.5'])

        pddl_problem.init.append(['=', ['bearing', 'b1'], self.b1_heading])
        pddl_problem.init.append(['=', ['bearing', 'b2'], self.b2_heading])
        pddl_problem.init.append(['=', ['bearing', 'b3'], self.b3_heading])
        # pddl_problem.init.append(['=', ['heading_r', 'r1'], players[3].heading])
        # pddl_problem.init.append(['=', ['heading_r', 'r2'], players[4].heading])
        # pddl_problem.init.append(['=', ['heading_r', 'r3'], players[5].heading])

        # b2_wall_0_bearing = (180 - (obs[('wall_0_bearing')]+obs[('teammate_0', 'bearing')])) + obs[('teammate_0', 'relative_heading')]
        # print(b2_wall_0_bearing)

        pddl_problem.init.append(['=', ['x_base_blue'], '140'])
        pddl_problem.init.append(['=', ['y_base_blue'], '40'])
        pddl_problem.init.append(['=', ['x_base_red'], '20'])
        pddl_problem.init.append(['=', ['y_base_red'], '40'])
        pddl_problem.init.append(['=', ['r_agent'], '2'])
        pddl_problem.init.append(['=', ['r_catch'], '10'])
        pddl_problem.init.append(['=', ['r_collision'], '2.2'])
        pddl_problem.init.append(['=', ['r_capture'], '10'])

        pddl_problem.init.append(['=', ['x_max'], '160'])
        pddl_problem.init.append(['=', ['x_min'], '0'])
        pddl_problem.init.append(['=', ['y_max'], '80'])
        pddl_problem.init.append(['=', ['y_min'], '0'])
        pddl_problem.init.append(['=', ['max_cooldown_time'], '30'])

        pddl_problem.init.append(['=', ['cooldown_time_blue', 'b1'], obs['tagging_cooldown']])
        pddl_problem.init.append(['=', ['cooldown_time_blue', 'b2'], obs[('teammate_0', 'tagging_cooldown')]])
        pddl_problem.init.append(['=', ['cooldown_time_blue', 'b3'], obs[('teammate_1', 'tagging_cooldown')]])
        pddl_problem.init.append(['=', ['cooldown_time_red', 'r1'], obs[('opponent_0', 'tagging_cooldown')]])
        pddl_problem.init.append(['=', ['cooldown_time_red', 'r2'], obs[('opponent_1', 'tagging_cooldown')]])
        pddl_problem.init.append(['=', ['cooldown_time_red', 'r3'], obs[('opponent_2', 'tagging_cooldown')]])

        pddl_problem.init.append(['=', ['v_max'], '1.5'])

        pddl_problem.init.append(['=', ['score_blue'], obs['team_score']])
        pddl_problem.init.append(['=', ['score_red'], obs['opponent_score']])

        pddl_problem.init.append(['ready'])
        pddl_problem.init.append(['adjustable_handling'])
        pddl_problem.init.append(['blue_flag_at_blue_base'])
        pddl_problem.init.append(['red_flag_at_red_base'])


        # goal
        # # pddl_problem.goal.append(['pole_position'])
        pddl_problem.goal.append(['not', ['total_failure']])
        pddl_problem.goal.append(['>=', ['score_blue'], '1'])


        return pddl_problem

    def calc_abs_pos(self, xb1 , yb1, obs, agent):
        other_agent_dis = obs[(agent, 'distance')]
        wall_bearing = obs[('wall_1_bearing')] # needs to be the pos X axis
        other_agent_bearing_to_you = obs[(agent, 'bearing')]
        wall_bearing = self.convert_angle_to_pos_aka_clockwise(wall_bearing)
        other_agent_bearing_to_you = self.convert_angle_to_pos_aka_clockwise(other_agent_bearing_to_you)
        other_agent_bearing_to_xaxis = abs(other_agent_bearing_to_you - wall_bearing)
        return self.calculate_new_point(xb1, yb1, other_agent_dis, other_agent_bearing_to_xaxis)


    def pddl_p_to_file(self, pddl_problem: PddlPlusProblem, output_file_name):
        parse_utils = PddlParserUtils()

        dir = "./pddl/"
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

    def convert_actions(self, plan_actions, tdm=1):
        self.curr_time = 0.0
        b1_plan_actions_num = []
        b2_plan_actions_num = []
        b3_plan_actions_num = []

        for n in range(len(plan_actions)):
            if plan_actions[n].action_name.__contains__("advance-time"):
                for _ in range(tdm):
                    b1_plan_actions_num.append(4)
                    b2_plan_actions_num.append(4)
                    b3_plan_actions_num.append(4)
            if plan_actions[n].action_name.__contains__("straight_ahead") and plan_actions[n].action_name.__contains__("b1"):
                for _ in range(tdm):
                    b1_plan_actions_num.append(4)
            if plan_actions[n].action_name.__contains__("straight_ahead") and plan_actions[n].action_name.__contains__("b2"):
                for _ in range(tdm):
                    b2_plan_actions_num.append(4)
            if plan_actions[n].action_name.__contains__("straight_ahead") and plan_actions[n].action_name.__contains__("b3"):
                for _ in range(tdm):
                    b3_plan_actions_num.append(4)
            if plan_actions[n].action_name.__contains__("turn_clockwise_90_full_speed") and plan_actions[n].action_name.__contains__("b1"):
                for _ in range(tdm):
                    b1_plan_actions_num.append(2)
            if plan_actions[n].action_name.__contains__("turn_clockwise_90_full_speed") and plan_actions[n].action_name.__contains__("b2"):
                for _ in range(tdm):
                    b2_plan_actions_num.append(2)
            if plan_actions[n].action_name.__contains__("turn_clockwise_90_full_speed") and plan_actions[n].action_name.__contains__("b3"):
                for _ in range(tdm):
                    b3_plan_actions_num.append(2)
            if plan_actions[n].action_name.__contains__("turn_counter_clockwise_90_full_speed") and plan_actions[n].action_name.__contains__("b1"):
                for _ in range(tdm):
                    b1_plan_actions_num.append(6)
            if plan_actions[n].action_name.__contains__("turn_counter_clockwise_90_full_speed") and plan_actions[n].action_name.__contains__("b2"):
                for _ in range(tdm):
                    b2_plan_actions_num.append(6)
            if plan_actions[n].action_name.__contains__("turn_counter_clockwise_90_full_speed") and plan_actions[n].action_name.__contains__("b3"):
                for _ in range(tdm):
                    b3_plan_actions_num.append(6)

        self.curr_time += self.time_inc
        self.curr_time = round(self.curr_time, 5) # wtf, 0.3 becomes 0.30000000000000004, so we do this

        return b1_plan_actions_num, b2_plan_actions_num, b3_plan_actions_num


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
