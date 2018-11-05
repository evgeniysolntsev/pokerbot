from termcolor import colored


def print_error(error):
    print(colored("\t\tError message : {}".format(error), "red"))
    exit(-1)
