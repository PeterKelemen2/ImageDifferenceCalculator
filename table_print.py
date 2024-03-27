import debug


def print_table_line(*args):
    # Construct the line based on input arguments
    line = " | ".join(f"{str(arg):>{width}}" for arg, width in args)
    color = "blue"
    if type(args[0][0]) == int:
        if args[0][0] % 2 == 0:
            color = "magenta"
        debug.log(line, text_color=color)
    else:
        debug.log(line, text_color="magenta")
        debug.log(" " + "-" * len(line), text_color=color)


def stab_table_print(curr, total):
    if type(curr) == int:
        percent = f"{(curr * 100) // total}%"
        print_table_line((curr, 7), (total, 7), (percent, 10))
    else:
        print_table_line((curr, 7), (total, 7), ("Progress", 10))


def prepass_table_print(i, curr, first, delta):
    if type(curr) == int:
        print_table_line((i, 6), (curr, 22), (curr - first, 22), (delta, 22))
    else:
        print_table_line((i, 6), (curr, 22), (first, 22), (delta, 22))

# def stab_table_print(curr, total):
#     percent = str((curr * 100) // total) + "%"
#     curr_space = 4 - len(str(curr))
#     diff_space = 5 - len(str(total))
#     percent_space = 6 - len(percent)
#
#     line = (" | " + " " * curr_space + str(curr) +
#             " | " + " " * diff_space + str(total) +
#             " | " + " " * percent_space + str(percent) + " |")
#
#     color = "blue"
#     if curr % 2 == 0:
#         color = "magenta"
#     debug.log(line, text_color=color)
#
#
# def prepass_table_print(i, curr, first, delta):
#     # print(
#     #     f"[{i}] {curr} (Difference: {curr - first} | {delta})")
#
#     index_space = 4 - len(str(i))
#     curr_space = 22 - len(str(curr))
#     diff_space = 22 - len(str(curr - first))
#     delta_space = 22 - len(str(delta))
#
#     line = (" | " + " " * index_space + str(i) +
#             " | " + " " * curr_space + str(curr) +
#             " | " + " " * diff_space + str(curr - first) +
#             " | " + " " * delta_space + str(delta) + " |")
#
#     color = "blue"
#     if i % 2 == 0:
#         color = "magenta"
#     debug.log(line, text_color=color)
