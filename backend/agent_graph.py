from typing import TypedDict

class State(TypedDict):
    input: str
    output: str

def process_input(state: State):
    return {"output": f"Processato: {state['input']}"}