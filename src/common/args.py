import sys
return_args = {}

def get_format_args():
    global return_args
    args = sys.argv[1:]
    current_key = None

    for arg in args:
        if arg.startswith("--"):
            current_key = arg[2:]
        elif current_key:
            return_args[current_key] = arg
            current_key = None

    return return_args

def asArg(key):
    return return_args.get(key)

def getArg(key):
    return return_args[key]

def getArgs():
    return return_args