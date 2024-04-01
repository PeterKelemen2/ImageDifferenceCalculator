import debug


def print_table_line(*args):
    # Construct the line based on input arguments
    line = " | ".join(f"{str(arg):>{width}}" for arg, width in args)
    color = "blue"
    if type(args[0][0]) == int:
        if args[0][0] % 2 == 0:
            color = "magenta"
        debug.log("| " + line + " |", text_color=color)
    else:
        debug.log("|" + "-" * (len(line) + 2) + "|", text_color=color)
        debug.log("| " + line + " |", text_color="magenta")
        debug.log("|" + "-" * (len(line) + 2) + "|", text_color=color)


def stab_table_print(curr, total):
    if type(curr) == int:
        percent = f"{(curr * 100) // total}%"
        print_table_line((curr, 7), (total, 7), (percent, 10))
    else:
        print_table_line((curr, 7), (total, 7), ("Progress", 10))


def prepass_table_print(i, curr, delta):
    if type(curr) == int:
        print_table_line((i, 6), (curr, 22), (delta, 22))
    else:
        print_table_line((i, 6), (curr, 22), (delta, 22))
