from ..syntax.state import State
from ..syntax import constants


def external_function(input_state: State) -> State:

    if constants.SEMANTIC_ATTACHMENT_ID == 1:
        pass

    else:
        print("no semantic attachment ID specified...")
        pass

    return input_state