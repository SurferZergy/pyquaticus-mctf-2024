import math
import sys
from collections import namedtuple
from typing import TextIO, Iterator

from PDDL import GroundedPDDLInstance
from syntax import constants
from syntax.action import Action
from syntax.state import State
from syntax.trace import Trace


class Plan(list):
    TrajectoryElement = namedtuple('TrajectoryElement', ['action', 'time'])

    def iter(self, ignore_time_passing: bool = False) -> Iterator[TrajectoryElement]:
        return filter(lambda item: not (item.action is constants.TIME_PASSING_ACTION and ignore_time_passing), self)

    def append_action(self, action: Action, time: float, expand_time_passing: bool = False):
        if expand_time_passing:
            self.pass_time(time)
        self.append(self.TrajectoryElement(action, time))

    def pass_time(self, time: float):
        current_time = 0.0 if len(self) == 0 else self[-1].time
        current_duration = 0.0 if len(self) == 0 else self[-1].action.duration
        current_time = round(current_time + current_duration, constants.NUMBER_PRECISION)

        if current_time < time:
            time_passing = constants.TIME_PASSING_ACTION
            delta = (time - current_time) / time_passing.duration
            num_actions = round(delta)

            if not math.isclose(delta, num_actions):
                raise RuntimeError('Could not expand plan with time-passing actions between t={} and t={}'.
                                   format(current_time, time))

            for a in range(num_actions):
                start_time = round(current_time + (a * time_passing.duration), constants.NUMBER_PRECISION)
                self.append(self.TrajectoryElement(time_passing, start_time))

    def simulate(self, init: State, grounded_pddl: GroundedPDDLInstance, double_events: bool = False) -> Trace:
        current_state = init
        trace = Trace(current_state)

        for item in self:
            if item.action.preconditions_func(current_state, constants):
                time = item.time

                if item.action.duration > 0:
                    time = round(time + item.action.duration, constants.NUMBER_PRECISION)

                    for happening_tree in [grounded_pddl.events, grounded_pddl.processes]:
                        for hp in happening_tree.get_applicable(current_state):
                            current_state = current_state.apply_happening(hp)
                            current_state.set_time(time)
                            trace.append(current_state)

                    if double_events or constants.DOUBLE_EVENT_CHECK:
                        for hp2 in grounded_pddl.events.get_applicable(current_state):
                            current_state = current_state.apply_happening(hp2)
                            current_state.set_time(time)
                            trace.append(current_state)

                current_state = current_state.apply_happening(item.action)
                current_state.set_time(time)
                trace.append(current_state)
            else:
                break
        else:
            trace.finished = True

        return trace

    def print(self, ignore_time_passing: bool = False, out: TextIO = sys.stdout):
        for item in self.iter(ignore_time_passing=ignore_time_passing):
            out.write("{:10.3f}:\t{}\t[{}]\n".format(item.time, item.action.grounded_name, item.action.duration))

    def to_file(self, plan_file: str, ignore_time_passing: bool = False):
        with open(plan_file, 'w') as f:
            self.print(ignore_time_passing=ignore_time_passing, out=f)

    @classmethod
    def from_file(cls, plan_file: str, grounded_pddl: GroundedPDDLInstance,
                  expand_time_passing: bool = False) -> 'Plan':
        plan = cls()

        action_lookup = {action.grounded_name: action for action in grounded_pddl.actions.iter()}

        with open(plan_file, 'r') as f:
            for line in f:
                line = line.strip().split(':')
                if line[0].replace('.', '', 1).isdigit():
                    time = float(line[0])
                    action_name, _ = line[1].split('[')
                    action = action_lookup[action_name.strip()]
                    plan.append_action(action, time, expand_time_passing=expand_time_passing)

        return plan

    @classmethod
    def from_trace(cls, trace: Trace) -> 'Plan':
        plan = cls()
        for state in trace.iter(extended=False):
            if state.predecessor_action:
                plan.append_action(state.predecessor_action, state.time)
        return plan
