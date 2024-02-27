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
        pass
	#Given an observation return a valid action agent_id is agent that needs an action, observation space is the current normalized observation space for the specific agent
    def compute_action(self,agent_id:int, observation_normalized:list, observation:dict):
        action = self.calc_actions(observation)

        if str(action).__contains__("dummy"):
            action = 1
        else:
            action = 2

        return action
        # if agent_id == 0 or agent_id == 3:
        #     return self.policy_one.compute_single_action(observation_normalized)[0]
        # elif agent_id == 1 or agent_id == 4:
        #     return self.policy_two.compute_single_action(observation_normalized)[0]
        # else:
        #     return self.policy_three.compute_single_action(observation_normalized)[0]

    def calc_actions(self, obs):
        # Create PDDL Problem
        # prob = self.create_pddl_problem(self, obs)
        # self.pddl_p_to_file(prob)

        # Run PDDL
        # plan, explored_states = nyx.runner("pddl/domain.pddl", "pddl/prob.pddl", ['-v', '-to:100', '-noplan', '-search:gbfs', '-custom_heuristic:42'])

        # Get actions from PDDL results
        plan_actions = self.extract_actions_from_plan_trace("pddl/plans/plan1_prob.pddl")

        # plan_actions = [1,2,3]
        plan_action = plan_actions[0] # or n step
        return plan_action

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
                if "move" or "fire" in line: # or "fly_east" in line or "fly_north" in line or "fly_south" in line or "time-passing" in line or "fire_missile_at_ammo_storage" in line:
                    action_name = (line.split(':')[1].split('[')[0]) #this is parsing the plan_capstone_prob.pddl (taking out the time)
                    # print (str(action_angle_time) + "\n")

                    plan_actions.append(TimedAction(action_name, 0.0))
                if "syntax error" in line:
                    plan_actions.append(TimedAction("syntax error", 0.0))
                    break

                if "0 goals found" in line:

                    break

        return  plan_actions


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
