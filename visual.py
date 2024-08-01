from common import Vec2, SVI, Stack
from svscript import OPCODES
from typing import Any



class NoVar:
    def __repr__(self) -> str: return "<NoVar>"

def run_visualizer(svi: SVI):
    import pygame
    ip: int = 0
    step: int = 0
    stack: Stack = Stack()
    vars: list[Any] = []
    output: str = ""
    line: str = ""

    usesVars: bool = svi["useVars"]
    varCount: int = svi["vars"]
    if usesVars and varCount > -1: vars = [NoVar() for _ in range(varCount)]
    usesOutput: bool = svi["useOutput"]
    usesLine: bool = svi["useLine"]
    instructions: list[dict[str, tuple[int, int, str] | tuple[int, int] | tuple[int, str] | tuple[int]]] = svi["instructions"]

    pygame.init()

    # creating a screen
    screenxy = Vec2(1000, 800)
    screen = pygame.display.set_mode(screenxy.lit())  # passing width and height

    stack_offset = screenxy.y - (22 + ((varCount + usesOutput + usesLine) * 24))

    # title and icon
    pygame.display.set_caption('Stack Visualizer')

    clock = pygame.time.Clock()

    pygame.font.init() # initiate font
    mainfont = pygame.font.Font('freesansbold.ttf', 20)

    waiting_for_input = False

    to_str = lambda value, is_str: (f"'{value}'" if len(value) == 1 else f'"{value}"') if is_str else f"{value}"

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_SPACE and waiting_for_input and ip < len(instructions):
                    step += 1
                    waiting_for_input = False

        if not waiting_for_input and ip < len(instructions):
            for i in instructions[ip:]:
                match i[0]:
                    # nop
                    case 0: pass
                    # end
                    case 1:
                        ip = len(instructions) - 1
                    # wait
                    case 2:
                        waiting_for_input = True
                        ip += 1
                        break
                    # push
                    case 3:
                        if i[1] == OPCODES["push"][1]['v']:
                            stack.push(vars[i[2]])
                        else:
                            stack.push(to_str(i[2], i[1] == 0))
                    # pop
                    case 4:
                        v = stack.pop()
                        if i[1] == 1: output = v
                        elif i[1] == 2: vars[i[2]] = v
                        del v
                    # line
                    case 5:
                        line = i[1]
                ip += 1
                if ip >= len(instructions): break

        pygame.draw.line(screen, (150, 150, 150), (5, stack_offset - 8), (100, stack_offset - 8), 3)
        # `stack.__dict__["_Stack__stack"]` allows me to get the private field `__stack` from the Stack class
        stack_height = 0
        for i, c in enumerate(stack.__dict__["_Stack__stack"]):
            screen.blit(mainfont.render(f"{i}: {c}", True, (255, 255, 255)),
                        (9,
                         ((stack_offset - 28) - (i * 20)) - 2)
                        )
            stack_height = (i + 1) * 20

        if stack_height > 0:
            pygame.draw.line(screen, (150, 150, 150), (5, (stack_offset - 8)), (5, (stack_offset - 16) - stack_height), 3)
            pygame.draw.line(screen, (150, 150, 150), (5, (stack_offset - 16) - stack_height), (100, (stack_offset - 16) - stack_height), 3)
        
        if usesOutput:
            screen.blit(mainfont.render(f"output: {output}", True, (255, 255, 255)), (5, screenxy.y - 22))
        
        if usesLine:
            screen.blit(mainfont.render(f"current line: {line}", True, (255, 255, 255)), (5, screenxy.y - (50 if usesOutput else 22)))
        
        if usesVars:
            for i, v in enumerate(vars):
                screen.blit(mainfont.render(f"v{i}: {v}", True, (255, 255, 255)), (5, (screenxy.y - {1: 46, 2: 72}.get(usesOutput + usesLine, 22)) - (i * 24)))

        clock.tick(60)

        pygame.display.update()