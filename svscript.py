from common import SVI, gen_opcodes



OPCODES = gen_opcodes([
    "nop",
    "end",
    "wait",
    ("push", [
        's',
        'i',
        'b',
        'v'
    ]),
    ("pop", [
        'n',
        'o',
        'v'
    ]),
    "line"
])



def interpret(code: str) -> tuple[SVI, None | str]:
    out: SVI = {
        "useVars": False,
        "vars": -1,
        "useOutput": False,
        "useLine": False,
        "instructions": []
    }
    in_program = False
    in_block_comment = False

    for i, l in enumerate(code.split("\n")):
        err = lambda msg = None: f"error on line {i + 1}" if msg is None else f"error on line {i + 1}: {msg}"
        l = l.strip()
        if "./" in l:
            if not in_block_comment:
                return {}, err("unexpected './'")
            l = l.split("./", 1)[1].strip()
            in_block_comment = False

        if l.startswith("//") or l == "" or in_block_comment: continue
        elif "/." in l and not in_block_comment:
            l = l.split("/.", 1)[0].strip()
            in_block_comment = True
        
        ins: tuple[int, int, str] | tuple[int, int] | tuple[int, str] | tuple[int] = None

        if l.startswith('@'):
            l = l.removeprefix('@')
            if in_program:
                return {}, err("directives can only be used at the top of the file, before any other code")
            elif l == "useVars":
                out["useVars"] = True
            elif l.startswith("vars"):
                try:
                    vcount = int(l.removeprefix("vars").strip())
                    out["vars"] = vcount
                except Exception:
                    return {}, err("expected whole number as input for directive 'vars'")
            elif l == "useOutput":
                out["useOutput"] = True
            elif l == "useLine":
                out["useLine"] = True
            else:
                return {}, err(f"unknown directive '{l}'")
            continue

        in_program = True

        if l == "nop":
            ins = (OPCODES["nop"],)

        elif l == "end":
            ins = (OPCODES["end"],)
            
        elif l == "wait":
            ins = (OPCODES["wait"],)

        elif l.startswith("push."):
            ins = (OPCODES["push"][0],)
            mode = l.split('.', 1)[1]
            param = None if len(mode.split(" ", 1)) == 1 else mode.split(" ", 1)[1].strip()
            mode = mode.split(" ", 1)[0].strip()
            match mode:
                case 's':
                    try:
                        param = eval(param)
                        if not isinstance(param, str): raise Exception()
                    except Exception:
                        return {}, err("expected string input for instruction 'push.s'")
                    ins += (OPCODES["push"][1]['s'], param)
                case 'n':
                    try:
                        param = eval(param)
                        if not isinstance(param, (int, float)): raise Exception()
                    except Exception:
                        return {}, err("expected number input for instruction 'push.n'")
                    ins += (OPCODES["push"][1]['n'], param)
                case 'b':
                    try:
                        param = eval(param)
                        if not isinstance(param, bool): raise Exception()
                    except Exception:
                        return {}, err("expected boolean input for instruction 'push.b'")
                    ins += (OPCODES["push"][1]['b'], param)
                case other:
                    if mode.isdigit():
                        ins += (OPCODES["push"][1]['v'], int(mode))
                    else:
                        return err(f"unknown operand '{mode}' for instruction 'push'")

        elif l.startswith("pop."):
            ins = (OPCODES["pop"][0],)
            mode = l.split('.', 1)[1]
            param = None if len(mode.split(" ", 1)) == 1 else mode.split(" ", 1)[1].strip()
            if param is not None:
                return {}, err("instruction 'pop' does not take input")
            mode = mode.split(" ", 1)[0].strip()
            match mode:
                case 'n':
                    ins += (OPCODES["pop"][1]['n'],)
                case 'o':
                    ins += (OPCODES["pop"][1]['o'],)
                case other:
                    if mode.isdigit():
                        ins += (OPCODES["pop"][1]['v'], int(mode))
                    else:
                        return err(f"unknown operand '{mode}' for instruction 'pop'")
        
        elif l.startswith("line"):
            ins = (OPCODES["line"],)
            param = l.removeprefix("line").strip()
            try:
                result = eval(param)
                if not isinstance(result, str): raise Exception()
            except Exception:
                return {}, err("expected string input for instruction 'line'")
            ins += (result,)

        else:
            return {}, err(f"unknown instruction '{l.split(' ', 1)[0]}'")
        
        if ins is not None: out["instructions"].append(ins)

    if out["vars"] == -1 and out["useVars"]:
        return {}, err(f"directive 'vars' must be given when 'useVars' is set to true")
    elif out["vars"] == 0 and out["useVars"]:
        return {}, err(f"directive 'vars' cannot be 0")

    return out, None