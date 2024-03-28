from typing import Union, List, Callable, Optional, Iterator

from . import JIT
from ..syntax import constants
from ..syntax.action import Action
from ..syntax.event import Event
from ..syntax.process import Process
from ..syntax.state import State

Happening = Union[Action, Process, Event]


class PreconditionsTree:

    def __init__(self):
        self.root = PreconditionsNode()

    def add_happening(self, happening: Happening):
        self.root.add_preconditions(iter(happening.preconditions), happening)

    def get_applicable(self, state: State) -> List[Happening]:
        return list(self.root.get_applicable(state))

    def iter(self) -> Iterator[Happening]:
        return self.root.iter()


class PreconditionsNode:

    def __init__(self, expression: Optional[str] = None):
        self.objects = []
        self.children = []
        self._function = None
        self._function_code = None
        self.expression = expression

    @property
    def function(self) -> Callable:
        if self._function is None and self.expression is not None:
            self._function_code, self._function = JIT.compile_expression([self.expression], name='precondition')
        return self._function

    def add_preconditions(self, preconditions: Iterator[str], obj: Happening):
        try:
            precondition = next(preconditions)
        except StopIteration:
            self.objects.append(obj)
            return

        match = None
        for child in self.children:
            if precondition == child.expression:
                match = child
                break
        else:
            match = PreconditionsNode(precondition)
            self.children.append(match)
        match.add_preconditions(preconditions, obj)

    def get_applicable(self, state: State) -> Iterator[Happening]:
        if self.function is not None and not self.function(state, constants):
            return
        yield from self.objects
        for child in self.children:
            yield from child.get_applicable(state)

    def iter(self) -> Iterator[Happening]:
        yield from self.objects
        for child in self.children:
            yield from child.iter()
