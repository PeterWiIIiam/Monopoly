"""
 *****************************************************************************
   FILE:            game.py

   AUTHOR:          Xingyu He

   ASSIGNMENT:      Final Project

   DATE:            Nov 3 2017

   DESCRIPTION:     This is a monopoly game.

 *****************************************************************************
"""

from cs110graphics import *
import random
import json

monopoly_data = json.load(open("monopoly.json"))
street_names = ['MEDITERRANEAN AVENUE', 'COMMUNITY CHEST','BALTIC AVENUE',
                'INCOME TAX', 'READING RAILROAD','ORIENTAL AVENUE',
                'CHANCE','VERMONT AVENUE', 'CONNECTICUT AVENUE',
                'JUST VISITING', 'ST.CHARLES PLACE', 'ELECTRIC COMPANY', 
                'STATES AVENUE','VIRGINIA AVENUE','PENNSYLVANIA RAILROAD',
                'ST.JAMES PLACE', 'COMMUNITY CHEST','TENNESSEE AVENUE',
                'NEW YORK AVENUE', 'FREE PARKING', 'KENTUCKY AVENUE', 
                'CHANCE', 'INDIANA AVENUE', 'ILLINOIS AVENUE',
                'B&O RAILROAD','ATLANTIC AVENUE', 'VENTNOR AVENUE', 
                'WATER WORKS','MARVIN GARDENS', 'GO TO JAIL',
                'PACIFIC AVENUE', 'NORTH CAROLINA AVENUE', 'COMMUNITY CHEST', 
                'PENNSYLVANIA AVENUE','SHORT LINE', 'CHANCE',
                'PARK PLACE','LUXURY TAX', 'BROADWALK', 'GO']

loc_dict = {}

class InfoCard(EventHandler):
    """docstring for InfoCard"""
    def __init__(self, win, game):

        EventHandler.__init__(self)

        self._win = win
        self._game = game
        self._body = Rectangle(win, 300, 500, (900, 277))
        self._title = ""
        self._title_rect = Rectangle(win, 250, 100, (900, 100))
        self._title_text = Text(win, "", 12,(900, 100))
        self._line_1 = Text(win, "", 12, (900, 180+30*0))
        self._line_2 = Text(win, "", 12, (900, 180+30*1))
        self._line_3 = Text(win, "", 12, (900, 180+30*2))
        self._line_4 = Text(win, "", 12, (900, 180+30*3))
        self._line_5 = Text(win, "", 12, (900, 180+30*4))
        self._line_6 = Text(win, "", 12, (900, 180+30*5))
        self._line_7 = Text(win, "", 12, (900, 180+30*6))
        self._line_8 = Text(win, "", 12, (900, 180+30*7))
        self._line_9 = Text(win, "", 12, (900, 180+30*8))
        self._line_10 = Text(win, "", 12, (900, 180+30*9))


        self._btn = ""
        self._btn_rect = Rectangle(win, 250, 23, (900, 500))
        self._btn_text = Text(win, self._btn, 12, (900, 500))
        self.deactivate_btn()
        self._btn_rect.add_handler(self)
        self._btn_text.add_handler(self)

        self._parts = [self._body, self._title_rect, self._title_text, self._line_1,
                        self._line_2,self._line_3,self._line_4,self._line_5,
                        self._line_6,self._line_7,self._line_8,self._line_9,
                        self._line_10, self._btn_rect, self._btn_text]
        self.addTo()

    def addTo(self):
        for part in self._parts:
            self._win.add(part)

    def clear_text_lines(self):
        for i in range(3,len(self._parts)):
            self._parts[i].set_text("")

    def reveal_chest_chance(self):
        if self._title == "CHANCE" or "COMMUNITY CHEST":
            options = propertyInfor['options']
            luck_num = random.randint(1, len(options))

            self._line_1.set_text(options[str(luck_num)])

    def handle_mouse_release(self, _):

        if self._btn == "BUY":
            self._game.buy_property()
            print('buy property')

        if self._btn == "MORTGAGE":
            self._game.mortgage_property()
            print('mortgage property')

    def activate_buy_btn(self):

        self._btn = 'BUY'
        self._btn_text.set_text(self._btn)
        self._btn_rect.set_depth(0)
        self._btn_text.set_depth(0)
        self._btn_rect.set_fill_color('green')

    def activate_mortgage_btn(self):

        self._btn = 'MORTGAGE'
        self._btn_text.set_text(self._btn)
        self._btn_rect.set_depth(0)
        self._btn_text.set_depth(0)
        self._btn_rect.set_fill_color('red')

    def deactivate_btn(self):

        self._btn_rect.set_depth(100)
        self._btn_text.set_depth(100)
        self._btn_rect.set_fill_color('grey')

    def update(self, section):
        self._title = section.get_name()
        propertyInfor = section.get_section_info()

        self._title_text.set_text(self._title)

        bgcolor = propertyInfor["color"]
        self._title_rect.set_fill_color(bgcolor)

        if self._title in ["CHANCE", "COMMUNITY CHEST", "GO", "GO TO JAIL",
                            "FREE PARKING", "LUXURY TAX", "INCOME TAX",
                            "JUST VISITING"]:
            self.clear_text_lines()
            self._line_1.set_text(propertyInfor["function"])

            return

        rent = propertyInfor['rent']
        self._line_1.set_text("RENT $%s"%rent)

        rent_1_house = propertyInfor['rent 1 house']
        self._line_2.set_text("With 1 House $%s"%rent_1_house)

        rent_2_house = propertyInfor['rent 2 house']
        self._line_3.set_text("With 2 Houses $%s"%rent_2_house)

        rent_3_house = propertyInfor['rent 3 house']
        self._line_4.set_text("With 3 Houses $%s"%rent_3_house)

        rent_4_house = propertyInfor['rent 4 house']
        self._line_5.set_text("With 4 Houses $%s"%rent_4_house)

        rent_1_hotel = propertyInfor['rent 1 hotel']
        self._line_6.set_text("With 1 Hotel $%s"%rent_1_hotel)

        mortgage_value = propertyInfor['mortgage value']
        self._line_7.set_text('Mortgage Value $%s'%mortgage_value)


        #set up btn
        if self._title in self._game._curr_player._properties:

            self.activate_mortgage_btn()

        elif self._title == self._game._curr_player.current_property():

            self.activate_buy_btn()

        else:

            self.deactivate_btn()   

    def current_display(self):
        return self._title_text
        

class Section(EventHandler):
    """This class represents each small section on the board."""

    def __init__(self, win, center, height, width, propertyName, infoCard, game): 
        EventHandler.__init__(self)

        cx = center[0]
        cy = center[1]
        self._section_info = monopoly_data[propertyName]
        self._game = game
        self._infoCard = infoCard
        self._propertyName = propertyName
        self._win = win
        self._rect = Rectangle(win, width, height, center)
        if height < width:
            self._color_rect = Rectangle(win, round(width/4), round(height), center)
            self._street_name = Text(win, propertyName, 6, (round(cx + width/3) , cy))
            self._cost = Text(win, str(self._section_info["cost"]), 10, (round(cx - width/3), cy))
        else:
            self._color_rect = Rectangle(win, round(width), round(height/4), center)
            self._street_name = Text(win, propertyName, 6, (cx, round(cy - width/3)))
            self._cost = Text(win, str(self._section_info["cost"]), 10, (cx, round(cy+width/3)))

        self._color_rect.set_fill_color(self._section_info["color"])

        self._parts = [self._rect, self._color_rect, self._street_name, self._cost]
        self.addTo()

    def addTo(self):
        for part in self._parts:
            self._win.add(part)
            part.add_handler(self)

    def get_name(self):

        return self._propertyName

    def get_section_info(self):

        return self._section_info

    def handle_mouse_release(self, _):

        self._infoCard.update(self)



class Game(object):
    """This class represents the game."""

    def __init__(self, win, player_num):

        #set info card
        self._infoCard = InfoCard(win,self)

        #set the board.
        originX = 100
        originY = 575

        self._board = []
        self._longerSide = 80
        self._shorterSide = 55

        self._board_length = self._shorterSide * 9 + self._longerSide
        self._average_length = (self._shorterSide + self._longerSide)/2

        upperleftCorner = (originX,  
                            round(originY - self._board_length + 
                                self._average_length))
        upperrightCorner = (round(originX + self._board_length),
                            round(originY - self._board_length + 
                                self._average_length))
        lowerrightCorner = (round(originX + self._board_length),
                            round(originY + (self._longerSide + 
                                self._shorterSide) / 2))
        lowerleftCorner = (originX,
                            round(originY + (self._longerSide + 
                                self._shorterSide) / 2))


        self._first_column = []
        for i in range(9):

            loc = (originX, originY - i * self._shorterSide)

            section = Section(win, loc, 
                            self._shorterSide, 
                            self._longerSide, 
                            street_names[i], 
                            self._infoCard,
                            self)
            self._first_column.append(section)
            loc_dict[i + 1] = loc

        self._square1 = Section(win, upperleftCorner, self._longerSide,
                        self._longerSide, street_names[9], 
                        self._infoCard, self)
        loc_dict[10] = upperleftCorner
        self._first_column.append(self._square1)
        self._board.append(self._first_column)


        self._first_row = []
        for i in range(9):

            loc = (originX + i * self._shorterSide + 
                        round(self._average_length),
                        originY - self._board_length + 
                        round(self._average_length))

            section = Section(win, loc, 
                        self._longerSide, 
                        self._shorterSide,street_names[i+10], 
                        self._infoCard,
                        self)
            self._first_row.append(section)
            loc_dict[i + 11] = loc

        self._square2 = Section(win, upperrightCorner, 
                                self._longerSide,
                                self._longerSide, 
                                street_names[19], 
                                self._infoCard,
                                self)
        loc_dict[20] = upperrightCorner
        self._first_row.append(self._square2)
        self._board.append(self._first_row)


        self._second_column = []
        for i in range(9):

            loc = (round(originX + 
                        self._board_length), 
                        originY - 8 * 
                        self._shorterSide + 
                        i * self._shorterSide)

            section = Section(win, loc, 
                        self._shorterSide, 
                        self._longerSide, 
                        street_names[i+20], 
                        self._infoCard,
                        self)
            self._second_column.append(section)
            loc_dict[i + 21] = loc

        self._square3 = Section(win, lowerrightCorner, 
                                self._longerSide,
                                self._longerSide, 
                                street_names[29], 
                                self._infoCard,
                                self)
        loc_dict[30] = lowerrightCorner
        self._first_row.append(self._square3)
        self._board.append(self._second_column)


        self._second_row = []
        for i in range(9):

            loc =  (round(originX + 
                        8 * self._shorterSide + 
                        self._average_length - 
                        i * self._shorterSide), 
                        round(originY + 
                        (self._average_length)))

            section = Section(win, loc, 
                            self._longerSide, 
                            self._shorterSide, 
                            street_names[i+30], 
                            self._infoCard,
                            self)
            self._second_row.append(section)
            loc_dict[i + 31] = loc

        self._square4 = Section(win, lowerleftCorner, 
                                self._longerSide,
                                self._longerSide, 
                                street_names[39], 
                                self._infoCard,
                                self)
        loc_dict[0] = lowerleftCorner
        self._first_row.append(self._square4)
        self._board.append(self._second_row)


        #set the dice.
        self._die1 = Die(win, self, 50, (360, 200), "white", "black")
        self._die2 = Die(win, self, 50, (440, 200), "white", "black")

        #initialize players
        self._players = []
        # for i in range(player_num):

        player1 = Player(win, self)
        self._players.append(player1)
        self._curr_player = self._players[0]


    def turn(self):
        player_index = self._players.index(self._curr_player)
        self._curr_player = self._players[(player_index + 1)%len(self._players)]


    def buy_property(self):

        propertyName = self._infoCard._title
        cost = monopoly_data[propertyName]["cost"]
        self._curr_player.buy_property(propertyName, -cost)

    def mortgage_property(self):

        propertyName = self._infoCard._title
        loan = monopoly_data[propertyName]['mortgage value']
        print(loan)
        self._curr_player.mortgage_property(propertyName, loan)


class Die(EventHandler):
    # class variable
    SIDES = 6
    POSITIONS = [None,
                 [(0, 0), None, None, None, None, None],
                 [(-.25, .25), (.25, -.25), None, None, None, None],
                 [(-.25, .25), (.25, -.25), (0, 0), None, None, None],
                 [(-.25, .25), (.25, -.25), (.25, .25), (-.25, -.25), None, None],
                 [(-.25, .25), (.25, -.25), (.25, .25), (-.25, -.25), (0,0), None],
                 [(-.25, .25), (.25, -.25), (.25, .25), (-.25, -.25), (-.25, 0), (.25, 0)]]
    
    def __init__(self, win, game, width=25, center=(200, 200),
                 bgcolor='red', fgcolor='white'):

        EventHandler.__init__(self)

        self._game = game
        self._value = 1
        self._square = Rectangle(win, width, width, center)
        self._square.set_fill_color(bgcolor)
        self._square.set_depth(20)
        self._square.add_handler(self)
        self._center = center
        self._width = width 
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(win, round(width / 20), center)
            pip.set_fill_color(fgcolor)
            pip.set_border_color(fgcolor)
            pip.set_depth(20)
            self._pips.append(pip)

        self.addTo(win)

    def addTo(self, win):
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
            pip.add_handler(self)
            
    def roll(self):
        self._value = random.randrange(Die.SIDES) + 1
        self._update()

    def get_value(self):
        pass

    def _update(self):
        """ private method.  make the appearance of this die match its value """
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].set_depth(25)
            else:
                self._pips[i].set_depth(15)
                dx, dy = positions[i]
                self._pips[i].move_to((round(cx + dx * self._width),
                                       round(cy + dy * self._width)))

    def handle_mouse_release(self, _):
        self.roll()
        self._game._curr_player.move_to(self._value)


class Player(object):
    """This class represent a player in the game."""

    def __init__(self, win, game, character="player1.png"):

        self._game = game
        self._win = win
        self._body = Image(win, character, 30, 30, (100, 642))
        self._capital_display = Rectangle(win, 250, 23, (900, 650))

        self._name = "Player 1"
        self._name_text = Text(win, self._name, 10, (900, 620))

        self._mortgage_text = Text(win, "", 10, (900, 710))
        self._mortgaged_properties = ['MORTGAGED PROPERTIES: ']

        self._property_text = Text(win, "", 10, (900, 680))
        self._properties = ['OWNED PROPERTIES: ']

        self._capital = 1000
        self._wealth_text = Text(win, str(self._capital), 12, (900, 650))
        self._loc = 0
        self._curr_property = ""
        self._parts = [self._body, self._capital_display, self._wealth_text,
                        self._property_text, self._mortgage_text, self._name_text]
        self.current_property()
        self.addTo()


    def addTo(self):

        for body in self._parts:
            self._win.add(body)

    def move_to(self, loc):

        self._loc += loc

        self._body.move_to(loc_dict[self._loc])

        self.current_property()

    def current_property(self):

        self._curr_property = street_names[self._loc - 1]
        return self._curr_property

    def capital_transaction(self, delta_capital):

        self._capital += delta_capital
        self._wealth_text.set_text(str(self._capital))
        print(self._capital)

    def buy_property(self, delta_property, delta_capital):

        if delta_property in self._properties or\
            -delta_capital > self._capital:
            return 
        else:
            self._properties.append(delta_property)
            self.capital_transaction(delta_capital)
            self._property_text.set_text(str(self._properties))
            # self._game._infoCard.activate_mortgage_btn()

            if delta_property in self._mortgaged_properties:
                self._mortgaged_properties.remove(delta_property)


    def mortgage_property(self, delta_property, delta_capital):

        print(delta_property)
        print(self._properties)

        self._mortgaged_properties.append(delta_property)
        self._properties.remove(delta_property)
        self.capital_transaction(delta_capital)
        self._mortgage_text.set_text(str(self._mortgaged_properties))
        self._property_text.set_text(str(self._properties))


def program(win):
    # change this as you see fit!

    win.set_height(1600)
    win.set_width(1600)

    game = Game(win, 2)
    print(loc_dict)



def main():
    StartGraphicsSystem(program)

if __name__ == "__main__":
    main()
