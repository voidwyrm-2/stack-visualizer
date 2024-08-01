import sys
import os
from svscript import interpret
from visual import run_visualizer



USAGE = "stack-visualizer [-h|--help] [SVScript file]"
def main():
    args = sys.argv[1:]
    if len({"-h", "--help"} & set(args)):
        print(f"usage: {USAGE}")
        return
    elif len(args) != 1:
        print(f"usage: {USAGE}")
        return
    elif ((False if args[0].rsplit(os.path.extsep, 1)[1] == "svs" else True) if len(args[0].rsplit(os.path.extsep, 1)) > 1 else False) and os.path.isfile(args[0]) == False:
        print(f"file '{args[0]}' is not a SVScript file")
        return
    elif not os.path.exists(f"scripts/{args[0].removeprefix("/") if args[0].startswith("/") else args[0].removeprefix("\\") if args[0].startswith("\\") else args[0]}"):
        print(f"file '{f"scripts/{args[0].removeprefix("/") if args[0].startswith("/") else args[0].removeprefix("\\") if args[0].startswith("\\") else args[0]}"}' does not exist")
        return
    
    with open(f"scripts/{args[0].removeprefix("/") if args[0].startswith("/") else args[0].removeprefix("\\") if args[0].startswith("\\") else args[0]}", "r") as f:
        content = f.read()
    
    res, err = interpret(content)
    if err: print(err); return
    run_visualizer(res)



if __name__ == "__main__":
    main()