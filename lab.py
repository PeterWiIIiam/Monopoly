import json
from cs110graphics import *
monopoly_data = json.load(open("monopoly.json"))
print (monopoly_data)
options = monopoly_data['CHANCE']['options']
print(options)
print(len(options))
print(options[str(2)])

# def program(win):
#     win.set_height(1600)
#     win.set_width(1600)

#     rect1 = Rectangle(win)
#     win.add(rect1)

# def main():
#     StartGraphicsSystem(program)