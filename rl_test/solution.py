import numpy as np
from pddl.pddl_plus import *
from pddl.nyx import nyx
import os
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
        self.n = 3 # number of actions b4 replan # need to set
        self.b1_full_speed = True # need to
        self.b2_full_speed = True  # need to set
        self.b3_full_speed = True  # need to set
        self.b1_heading = -135 # need to set
        self.b2_heading = -135  # need to set
        self.b3_heading = -135  # need to set
        self.curr_time = 0.0
        self.time_inc = 0.1
        # self.noop = False

	#Given an observation return a valid action agent_id is agent that needs an action, observation space is the current normalized observation space for the specific agent
    def compute_action(self,agent_id:int, observation_normalized:list, observation:dict):
        if self.replan:
            self.b1_actions, self.b2_actions,self.b3_actions = self.calc_actions(observation)[:self.n]
            self.replan = False
        elif len(self.b1_actions) == 1: # last action, need to replan next time
                self.replan = True
                if agent_id == 0:
                    return self.b1_actions[0]
                if agent_id == 1:
                    return self.b2_actions[0]
                if agent_id == 2:
                    return self.b3_actions[0]

        b1_current_action = self.b1_actions[0]
        self.b1_actions = self.b1_actions[1:]
        b2_current_action = self.b2_actions[0]
        self.b2_actions = self.b2_actions[1:]
        b3_current_action = self.b3_actions[0]
        self.b3_actions = self.b3_actions[1:]

        if agent_id == 0:
            return b1_current_action
        if agent_id == 1:
            return b2_current_action
        if agent_id == 2:
            return b3_current_action

    def calc_actions(self, obs):
        # Create PDDL Problem
        # prob = self.create_pddl_problem(self, obs)
        # self.pddl_p_to_file(prob)

        # Run PDDL
        # plan, explored_states = nyx.runner("pddl/domain.pddl", "pddl/prob.pddl", ['-v', '-to:100', '-noplan', '-search:gbfs', '-custom_heuristic:42'])

        # Get actions from PDDL results
        plan_actions = self.extract_actions_from_plan_trace("pddl/plans/plan1_prob.pddl")

        # Convert actions to discrete
        b1_plan_actions_num, b2_plan_actions_num, b3_plan_actions_num = self.convert_actions(plan_actions)

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
                if "heading" or "speed" in line:
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
        pddl_problem.domain = 'acq'
        pddl_problem.name = 'acq-problem'
        pddl_problem.metric = self.metric
        pddl_problem.objects = []
        pddl_problem.init = []
        pddl_problem.goal = []


        # objs
        obs_theta = round(observation_array[2], 5)
        obs_theta_dot = round(observation_array[3], 5)
        obs_x = round(observation_array[0], 5)
        obs_x_dot = round(observation_array[1], 5)

        # A dictionary with global problem parameters
        problem_params = dict()

        # Add constants fluents
        for numeric_fluent in self.constant_numeric_fluents:
            pddl_problem.init.append(['=', [numeric_fluent], round(self.constant_numeric_fluents[numeric_fluent],
                                                                   CartPoleMetaModel.PLANNER_PRECISION)])  # TODO
        for boolean_fluent in self.constant_boolean_fluents:
            if self.constant_boolean_fluents[boolean_fluent]:
                pddl_problem.init.append([boolean_fluent])
            # else:
            # pddl_problem.init.append(['not',[boolean_fluent]])

        # MAIN COMPONENTS: X and THETA + derivatives
        pddl_problem.init.append(['=', ['x'], round(obs_x, CartPoleMetaModel.PLANNER_PRECISION)])
        pddl_problem.init.append(['=', ['x_dot'], round(obs_x_dot, CartPoleMetaModel.PLANNER_PRECISION)])
        pddl_problem.init.append(['=', ['theta'], round(obs_theta, CartPoleMetaModel.PLANNER_PRECISION)])
        pddl_problem.init.append(['=', ['theta_dot'], round(obs_theta_dot, CartPoleMetaModel.PLANNER_PRECISION)])
        pddl_problem.init.append(
            ['=', ['F'], round(self.constant_numeric_fluents['force_mag'], CartPoleMetaModel.PLANNER_PRECISION)])

        calc_temp = (self.constant_numeric_fluents['force_mag'] + (self.constant_numeric_fluents['m_pole'] *
                                                                   self.constant_numeric_fluents['l_pole']) *
                     obs_theta_dot ** 2 * math.sin(obs_theta)) / (
                                self.constant_numeric_fluents['m_cart'] + self.constant_numeric_fluents['m_pole'])
        calc_theta_ddot = (self.constant_numeric_fluents['gravity'] * math.sin(obs_theta) - math.cos(
            obs_theta) * calc_temp) / (self.constant_numeric_fluents['l_pole'] * (
                    4.0 / 3.0 - self.constant_numeric_fluents['m_pole'] * math.cos(obs_theta) ** 2 / (
                        self.constant_numeric_fluents['m_cart'] + self.constant_numeric_fluents['m_pole'])))
        calc_x_ddot = calc_temp - (self.constant_numeric_fluents['m_pole'] * self.constant_numeric_fluents[
            'l_pole']) * calc_theta_ddot * math.cos(obs_theta) / (
                                  self.constant_numeric_fluents['m_cart'] + self.constant_numeric_fluents['m_pole'])

        pddl_problem.init.append(['=', ['x_ddot'], round(calc_x_ddot, CartPoleMetaModel.PLANNER_PRECISION)])
        pddl_problem.init.append(['=', ['theta_ddot'], round(calc_theta_ddot, CartPoleMetaModel.PLANNER_PRECISION)])

        # Add goal
        # pddl_problem.goal.append(['pole_position'])
        pddl_problem.goal.append(['not', ['total_failure']])
        pddl_problem.goal.append(['=', ['elapsed_time'], ['time_limit']])


        return pddl_problem


    def pddl_p_to_file(self, pddl_problem: PddlPlusProblem, output_file_name):
        parse_utils = PddlParserUtils()

        out_file = open(output_file_name, "w")
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
        b1_plan_actions_num = []
        b2_plan_actions_num = []
        b3_plan_actions_num = []

        actual_a_at_curr_time = self.preprocess_plan(plan_actions)

        while len(actual_a_at_curr_time) > 0:
            # actual_a_at_curr_time = self.preprocess_plan(plan_actions)
            for n in range(len(actual_a_at_curr_time)):
                if actual_a_at_curr_time[n].action_name.__contains__("full_speed") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_full_speed = True
                if actual_a_at_curr_time[n].action_name.__contains__("half_speed") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_full_speed = False
                if actual_a_at_curr_time[n].action_name.__contains__("full_speed") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_full_speed = True
                if actual_a_at_curr_time[n].action_name.__contains__("half_speed") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_full_speed = False
                if actual_a_at_curr_time[n].action_name.__contains__("full_speed") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_full_speed = True
                if actual_a_at_curr_time[n].action_name.__contains__("half_speed") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_full_speed = False
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-135") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = -135
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-90") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = -90
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-45") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = -45
                if actual_a_at_curr_time[n].action_name.__contains__("heading_0") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = 0
                if actual_a_at_curr_time[n].action_name.__contains__("heading_45") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = 45
                if actual_a_at_curr_time[n].action_name.__contains__("heading_90") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = 90
                if actual_a_at_curr_time[n].action_name.__contains__("heading_135") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = 135
                if actual_a_at_curr_time[n].action_name.__contains__("heading_180") and actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    self.b1_heading = 180
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-135") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = -135
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-90") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = -90
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-45") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = -45
                if actual_a_at_curr_time[n].action_name.__contains__("heading_0") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = 0
                if actual_a_at_curr_time[n].action_name.__contains__("heading_45") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = 45
                if actual_a_at_curr_time[n].action_name.__contains__("heading_90") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = 90
                if actual_a_at_curr_time[n].action_name.__contains__("heading_135") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = 135
                if actual_a_at_curr_time[n].action_name.__contains__("heading_180") and actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    self.b2_heading = 180
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-135") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = -135
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-90") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = -90
                if actual_a_at_curr_time[n].action_name.__contains__("heading_-45") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = -45
                if actual_a_at_curr_time[n].action_name.__contains__("heading_0") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = 0
                if actual_a_at_curr_time[n].action_name.__contains__("heading_45") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = 45
                if actual_a_at_curr_time[n].action_name.__contains__("heading_90") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = 90
                if actual_a_at_curr_time[n].action_name.__contains__("heading_135") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = 135
                if actual_a_at_curr_time[n].action_name.__contains__("heading_180") and actual_a_at_curr_time[n].action_name.__contains__("b3"):
                    self.b3_heading = 180

                if actual_a_at_curr_time[n].action_name.__contains__("b1"):
                    if self.b1_full_speed:
                        heading_to_action = {180: 0, 135: 1, 90: 2, 45: 3, 0: 4, -45: 5, -90: 6, -135: 7}
                    else:
                        heading_to_action = {180: 8, 135: 9, 90: 10, 45: 11, 0: 12, -45: 13, -90: 14, -135: 15}
                    if self.b1_heading in heading_to_action:
                        b1_plan_actions_num.append(heading_to_action[self.b1_heading])
                elif actual_a_at_curr_time[n].action_name.__contains__("b2"):
                    if self.b2_full_speed:
                        heading_to_action = {180: 0, 135: 1, 90: 2, 45: 3, 0: 4, -45: 5, -90: 6, -135: 7}
                    else:
                        heading_to_action = {180: 8, 135: 9, 90: 10, 45: 11, 0: 12, -45: 13, -90: 14, -135: 15}
                    if self.b2_heading in heading_to_action:
                        b2_plan_actions_num.append(heading_to_action[self.b2_heading])
                else:
                    if self.b3_full_speed:
                        heading_to_action = {180: 0, 135: 1, 90: 2, 45: 3, 0: 4, -45: 5, -90: 6, -135: 7}
                    else:
                        heading_to_action = {180: 8, 135: 9, 90: 10, 45: 11, 0: 12, -45: 13, -90: 14, -135: 15}
                    if self.b3_heading in heading_to_action:
                        b3_plan_actions_num.append(heading_to_action[self.b3_heading])

            self.curr_time += self.time_inc
            self.curr_time = round(self.curr_time, 5) # wtf, 0.3 becomes 0.30000000000000004, so we do this

            actual_a_at_curr_time = self.preprocess_plan(plan_actions)

        return b1_plan_actions_num, b2_plan_actions_num, b3_plan_actions_num
        #     # if plan_actions[0].__contains__("noop"):
        #     #     self.noop = True
        #
        #     # if self.noop:
        #     #     plan_actions_num.append(16)

    def preprocess_plan(self, plan_actions):
        actual_a_at_curr_time = []
        list_a_at_curr_time = [a for a in plan_actions if a.start_at == self.curr_time]
        # combine speed and heading actions into one action
        b1_speed_related_a = [element for element in list_a_at_curr_time if
                              "b1" in element.action_name and "speed" in element.action_name]
        b1_heading_related_a = [element for element in list_a_at_curr_time if
                                "b1" in element.action_name and "heading" in element.action_name]
        if len(b1_heading_related_a) == 1 and len(b1_speed_related_a) == 1:
            s = (b1_speed_related_a[0].action_name + "+" + b1_heading_related_a[0].action_name)
            actual_a_at_curr_time.append(TimedAction(s, self.curr_time))
        elif len(b1_heading_related_a) == 1 and len(b1_speed_related_a) == 0:
            actual_a_at_curr_time.append(TimedAction(b1_heading_related_a[0].action_name, self.curr_time))
        elif len(b1_heading_related_a) == 0 and len(b1_speed_related_a) == 1:
            actual_a_at_curr_time.append(TimedAction(b1_speed_related_a[0].action_name, self.curr_time))
        else:
            pass

        b2_speed_related_a = [element for element in list_a_at_curr_time if
                              "b2" in element.action_name and "speed" in element.action_name]
        b2_heading_related_a = [element for element in list_a_at_curr_time if
                                "b2" in element.action_name and "heading" in element.action_name]
        if len(b2_heading_related_a) == 1 and len(b2_speed_related_a) == 1:
            s = (b2_speed_related_a[0].action_name + "+" + b2_heading_related_a[0].action_name)
            actual_a_at_curr_time.append(TimedAction(s, self.curr_time))
        elif len(b2_heading_related_a) == 1 and len(b2_speed_related_a) == 0:
            actual_a_at_curr_time.append(TimedAction(b2_heading_related_a[0].action_name, self.curr_time))
        elif len(b2_heading_related_a) == 0 and len(b2_speed_related_a) == 1:
            actual_a_at_curr_time.append(TimedAction(b2_speed_related_a[0].action_name, self.curr_time))
        else:
            pass

        b3_speed_related_a = [element for element in list_a_at_curr_time if
                              "b3" in element.action_name and "speed" in element.action_name]
        b3_heading_related_a = [element for element in list_a_at_curr_time if
                                "b3" in element.action_name and "heading" in element.action_name]
        if len(b3_heading_related_a) == 1 and len(b3_speed_related_a) == 1:
            s = (b3_speed_related_a[0].action_name + "+" + b3_heading_related_a[0].action_name)
            actual_a_at_curr_time.append(TimedAction(s, self.curr_time))
        elif len(b3_heading_related_a) == 1 and len(b3_speed_related_a) == 0:
            actual_a_at_curr_time.append(TimedAction(b3_heading_related_a[0].action_name, self.curr_time))
        elif len(b3_heading_related_a) == 0 and len(b3_speed_related_a) == 1:
            actual_a_at_curr_time.append(TimedAction(b3_speed_related_a[0].action_name, self.curr_time))
        else:
            pass

        return actual_a_at_curr_time


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
