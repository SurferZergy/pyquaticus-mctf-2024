import argparse
import math
import sys
import os
import copy
import os.path
import pyquaticus
from pyquaticus import pyquaticus_v0
from pyquaticus.base_policies.base_attack import BaseAttacker
from pyquaticus.base_policies.base_defend import BaseDefender
from pyquaticus.base_policies.base_combined import Heuristic_CTF_Agent
from pyquaticus.envs.pyquaticus import Team
from collections import OrderedDict
from pyquaticus.config import config_dict_std, ACTION_MAP

#Update this to the path of your solution.py file or ensure its on the same level as this (competition_test.py) script
from solution_wiktor_domain import solution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test against the evaluation used on the submission platform (3v3)')
    parser.add_argument('--render', help='Enable rendering', action='store_true')
    args = parser.parse_args()
    RENDER_MODE = 'human' if args.render else None #set to 'human' if you want rendered output
    RENDER_MODE = 'human'

    config_dict = config_dict_std
    config_dict["max_time"] = 600.0
    config_dict["max_score"] = 100


    easy_score = 0
    medium_score = 0
    hidden_score = 0

    step = 0
    #RED side Competition Easy Defender and Attacker vs Submission (Blue Side)
    env = pyquaticus_v0.PyQuaticusEnv(team_size=3, config_dict=config_dict,render_mode=RENDER_MODE)
    term_g = {0:False,1:False}
    truncated_g = {0:False,1:False}
    term = term_g
    trunc = truncated_g
    obs = env.reset()
    temp_score = env.game_score
    sol = solution()
    H_one = BaseDefender(3, Team.RED_TEAM, mode='competition_easy')
    H_two = BaseAttacker(4, Team.RED_TEAM, mode='competition_easy')
    H_three = BaseAttacker(5, Team.RED_TEAM, mode='competition_easy')

    prev_x = None
    curr_x = env.players[0].pos[0]
    error_x = 9999
    real_dx = 0
    est_dx = 0

    prev_y = None
    curr_y = env.players[0].pos[0]
    error_y = 9999
    real_dy = 0
    est_dy = 0

    headings = []

    while True:
        new_obs = {}
        #Get normalized observation (for heuristic approaches)
        for k in obs:
            new_obs[k] = env.agent_obs_normalizer.unnormalized(obs[k])
        zero = sol.compute_action(0,obs[0], new_obs[0])
        one = sol.compute_action(1,obs[1],new_obs[1])
        two = sol.compute_action(2,obs[2],new_obs[2])
        three = H_one.compute_action(new_obs)
        four = H_two.compute_action(new_obs)
        five = H_three.compute_action(new_obs)

        curr_x = copy.copy(env.players[0].pos[0])
        curr_y = copy.copy(env.players[0].pos[1])
        if prev_x is not None:
            error_x = (1.5/2 * 0.1 * math.sin(math.radians(env.players[0].heading))) - (curr_x - prev_x)
            real_dx = (curr_x - prev_x)
            est_dx = (1.5/2 * 0.1 * math.sin(math.radians(env.players[0].heading)))
            error_y = (1.5/2 * 0.1 * math.cos(math.radians(env.players[0].heading))) - (curr_y - prev_y)
            real_dy = (curr_y - prev_y)
            est_dy = (1.5/2 * 0.1 * math.cos(math.radians(env.players[0].heading)))
        # print("{}. {}, {} :: \t\treal_dx={}, est_dx={} :: \t\treal_dy={}, est_dy={}".format(env.players[0].pos[0], env.players[0].pos[1], env.players[0].heading, real_dx, est_dx, real_dy, est_dy))
        
        obs, reward, term, trunc, info = env.step({0:zero,1:one, 2:two, 3:three, 4:four, 5:five})

        headings.append(env.players[0].heading)

        if len(headings) % 10 == 0:
            # print(len(headings))
            sum_d_heading = 0
            sub_headings = headings[-10:]
            for ix in range(0,9):
                sum_d_heading += abs(sub_headings[ix+1]) - abs(sub_headings[ix])
            # print("AVG HEADING: {} \t :: \t {}".format(sum_d_heading/len(sub_headings), sub_headings))

        prev_x = copy.copy(curr_x)
        prev_y = copy.copy(curr_y)

        # print(env.players[0].heading)
        k =  list(term.keys())
        step += 1
        if term[k[0]] == True or trunc[k[0]]==True:
            break
    for k in env.game_score:
        temp_score[k] += env.game_score[k]
    env.close()
    easy_score = temp_score['blue_captures'] - temp_score['red_captures'] - temp_score['blue_collisions']
    print("Easy Detailed Results: ", temp_score)
    print("Final Easy Score: ", easy_score)

    step = 0
    #RED side Competition Medium Defender and Attacker vs Submission (Blue Side)
    env = pyquaticus_v0.PyQuaticusEnv(team_size=3, config_dict=config_dict,render_mode=RENDER_MODE)
    term_g = {0:False,1:False}
    truncated_g = {0:False,1:False}
    term = term_g
    trunc = truncated_g
    obs = env.reset()
    temp_score = env.game_score
    sol = solution()
    H_one = BaseDefender(3, Team.RED_TEAM, mode='competition_medium')
    H_two = BaseAttacker(4, Team.RED_TEAM, mode='competition_medium')
    H_three = BaseAttacker(5, Team.RED_TEAM, mode='competition_medium')
    while True:
        new_obs = {}
        #Get normalized observation (for heuristic approaches)
        for k in obs:
            new_obs[k] = env.agent_obs_normalizer.unnormalized(obs[k])
        zero = sol.compute_action(0,obs[0], new_obs[0])
        one = sol.compute_action(1,obs[1],new_obs[1])
        two = sol.compute_action(2,obs[2],new_obs[2])
        three = H_one.compute_action(new_obs)
        four = H_two.compute_action(new_obs)
        five = H_three.compute_action(new_obs)
        
        obs, reward, term, trunc, info = env.step({0:zero,1:one, 2:two, 3:three, 4:four, 5:five})
        k =  list(term.keys())
        step += 1
        if term[k[0]] == True or trunc[k[0]]==True:
            break
    for k in env.game_score:
        temp_score[k] += env.game_score[k]
    env.close()
    print("Medium Detailed Results: ", temp_score)
    medium_score += temp_score['red_captures'] - temp_score['blue_captures'] - temp_score['blue_collisions']
    print("Final Medium Score: ", medium_score)
