from typing import Any



class Vec2:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
    
    def lit(self) -> tuple[int, int]:
        return self.x, self.y


class Stack:
    def __init__(self, initial_list: list[Any] = []):
        self.__stack: list[Any] = initial_list.copy() if len(initial_list) > 0 else []
    
    def __len__(self) -> int:
        raise NotImplementedError()
        #return len(self.__stack)

    def __check_stack(self):
        "Throws an IndexError if the stack is empty"
        if len(self.__stack) == 0:
            raise IndexError("Stack is empty")
    
    def push(self, value: Any):
        "Pushes a value to the stack"
        self.__stack.append(value)
    
    def pop(self) -> Any:
        "Pops a value off the stack"
        self.__check_stack()
        return self.__stack.pop()
    
    def peek(self) -> Any:
        "Returns the top value of the stack without popping"
        self.__check_stack()
        return self.__stack[-1]
    
    def copy(self):
        "Copies the current stack instance into a new object"
        return Stack(self.__stack)


SVI = dict[str, bool | list[tuple[int, int, Any] | tuple[int, int] | tuple[int, Any] | tuple[int]]]


#iota = object()
def gen_opcodes(opcodes: list[str | tuple[str, list[str]]]) -> dict[str, int | tuple[int, dict[str, int]]]:
    out: dict[str, int | tuple[int, dict[str, int]]] = {}
    for i, o in enumerate(opcodes):
        if isinstance(o, str):
            out[o] = i
        else:
            iout: dict[str, int] = {} # inner out
            for ii, io in enumerate(o[1]):
                iout[io] = ii
            out[o[0]] = (i, iout)
    return out