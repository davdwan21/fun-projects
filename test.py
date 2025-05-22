from tabulate import tabulate

icons = tabulate(["P", "E", "#", "-", "M", "T"], tablefmt="grid")

print(icons)