from command import Command
import numpy as np
from buttons import Buttons
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

class Bot:

    def __init__(self):
        #< - v + < - v - v + > - > + Y
        self.fire_code=["<","!<","v+<","!v+!<","v","!v","v+>","!v+!>",">+Y","!>+!Y"]
        self.exe_code = 0
        self.start_fire=True
        self.remaining_code=[]
        self.my_command = Command()
        self.buttn = Buttons()
        self.model = joblib.load('./decision_tree_model.pkl')

    def fight(self,current_game_state,player):

        if player == "1":
            x_diff = current_game_state.player1.x_coord - current_game_state.player2.x_coord
            y_diff = current_game_state.player1.y_coord - current_game_state.player2.y_coord

            d = {
                'health 1': [float(current_game_state.player2.health)/100.0], 
                'is_jumping 1':[int(current_game_state.player2.is_jumping)], 
                'is_crouching 1':[int(current_game_state.player2.is_crouching)], 
                'is_player_in_move 1':[int(current_game_state.player2.is_player_in_move)], 
                'player_id 2':[int(current_game_state.player1.player_id)], 
                'health 2':[float(current_game_state.player1.health)/100.0], 
                'is_jumping 2':[int(current_game_state.player1.is_jumping)],
                'is_crouching 2':[int(current_game_state.player1.is_crouching)], 
                'is_player_in_move 2':[int(current_game_state.player1.is_player_in_move)],        
                'x_coord_diff':[abs(float(x_diff)/100.0)],
                'y_coord_diff':[abs(float(y_diff))]
            }
            x = pd.DataFrame(d)
            y = int(self.model.predict(x)[0])

            binary_str = format(int(bin(y)[2:]), '010')

            self.buttn.up = bool(int(binary_str[0]))
            self.buttn.down = bool(int(binary_str[1]))
            self.buttn.right = bool(int(binary_str[2]))
            self.buttn.left = bool(int(binary_str[3]))
            self.buttn.select = False
            self.buttn.start = False
            self.buttn.Y = bool(int(binary_str[4]))
            self.buttn.B = bool(int(binary_str[5]))
            self.buttn.X = bool(int(binary_str[6]))
            self.buttn.A = bool(int(binary_str[7]))
            self.buttn.L = bool(int(binary_str[8]))
            self.buttn.R = bool(int(binary_str[9]))

            self.my_command.player_buttons=self.buttn

        else:
            x_diff = current_game_state.player1.x_coord - current_game_state.player2.x_coord
            y_diff = current_game_state.player1.y_coord - current_game_state.player2.y_coord

            d = {
                'health 1': [float(current_game_state.player1.health)/100.0], 
                'is_jumping 1':[int(current_game_state.player1.is_jumping)], 
                'is_crouching 1':[int(current_game_state.player1.is_crouching)], 
                'is_player_in_move 1':[int(current_game_state.player1.is_player_in_move)], 
                'player_id 2':[int(current_game_state.player2.player_id)], 
                'health 2':[float(current_game_state.player2.health)/100.0], 
                'is_jumping 2':[int(current_game_state.player2.is_jumping)],
                'is_crouching 2':[int(current_game_state.player2.is_crouching)], 
                'is_player_in_move 2':[int(current_game_state.player2.is_player_in_move)],        
                'x_coord_diff':[abs(float(x_diff)/100.0)],
                'y_coord_diff':[abs(float(y_diff))]
            }
            x = pd.DataFrame(d)
            y = int(self.model.predict(x)[0])

            binary_str = format(int(bin(y)[2:]), '010')

            self.buttn.up = bool(int(binary_str[0]))
            self.buttn.down = bool(int(binary_str[1]))
            self.buttn.right = bool(int(binary_str[2]))
            self.buttn.left = bool(int(binary_str[3]))
            self.buttn.select = False
            self.buttn.start = False
            self.buttn.Y = bool(int(binary_str[4]))
            self.buttn.B = bool(int(binary_str[5]))
            self.buttn.X = bool(int(binary_str[6]))
            self.buttn.A = bool(int(binary_str[7]))
            self.buttn.L = bool(int(binary_str[8]))
            self.buttn.R = bool(int(binary_str[9]))

            self.my_command.player2_buttons=self.buttn
        return self.my_command


    def run_command( self , com , player   ):

        if self.exe_code-1==len(self.fire_code):
            self.exe_code=0
            self.start_fire=False
            print ("compelete")
            #exit()
            # print ( "left:",player.player_buttons.left )
            # print ( "right:",player.player_buttons.right )
            # print ( "up:",player.player_buttons.up )
            # print ( "down:",player.player_buttons.down )
            # print ( "Y:",player.player_buttons.Y )

        elif len(self.remaining_code)==0 :

            self.fire_code=com
            #self.my_command=Command()
            self.exe_code+=1

            self.remaining_code=self.fire_code[0:]

        else:
            self.exe_code+=1
            if self.remaining_code[0]=="v+<":
                self.buttn.down=True
                self.buttn.left=True
                print("v+<")
            elif self.remaining_code[0]=="!v+!<":
                self.buttn.down=False
                self.buttn.left=False
                print("!v+!<")
            elif self.remaining_code[0]=="v+>":
                self.buttn.down=True
                self.buttn.right=True
                print("v+>")
            elif self.remaining_code[0]=="!v+!>":
                self.buttn.down=False
                self.buttn.right=False
                print("!v+!>")

            elif self.remaining_code[0]==">+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.right=True
                print(">+Y")
            elif self.remaining_code[0]=="!>+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.right=False
                print("!>+!Y")

            elif self.remaining_code[0]=="<+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.left=True
                print("<+Y")
            elif self.remaining_code[0]=="!<+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.left=False
                print("!<+!Y")

            elif self.remaining_code[0]== ">+^+L" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print(">+^+L")
            elif self.remaining_code[0]== "!>+!^+!L" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.L= False #not (player.player_buttons.L)
                print("!>+!^+!L")

            elif self.remaining_code[0]== ">+^+Y" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print(">+^+Y")
            elif self.remaining_code[0]== "!>+!^+!Y" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.Y= False #not (player.player_buttons.L)
                print("!>+!^+!Y")


            elif self.remaining_code[0]== ">+^+R" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print(">+^+R")
            elif self.remaining_code[0]== "!>+!^+!R" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.R= False #ot (player.player_buttons.R)
                print("!>+!^+!R")

            elif self.remaining_code[0]== ">+^+A" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print(">+^+A")
            elif self.remaining_code[0]== "!>+!^+!A" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.A= False #not (player.player_buttons.A)
                print("!>+!^+!A")

            elif self.remaining_code[0]== ">+^+B" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print(">+^+B")
            elif self.remaining_code[0]== "!>+!^+!B" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.B= False #not (player.player_buttons.A)
                print("!>+!^+!B")

            elif self.remaining_code[0]== "<+^+L" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print("<+^+L")
            elif self.remaining_code[0]== "!<+!^+!L" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.L= False  #not (player.player_buttons.Y)
                print("!<+!^+!L")

            elif self.remaining_code[0]== "<+^+Y" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print("<+^+Y")
            elif self.remaining_code[0]== "!<+!^+!Y" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.Y= False  #not (player.player_buttons.Y)
                print("!<+!^+!Y")

            elif self.remaining_code[0]== "<+^+R" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print("<+^+R")
            elif self.remaining_code[0]== "!<+!^+!R" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!<+!^+!R")

            elif self.remaining_code[0]== "<+^+A" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print("<+^+A")
            elif self.remaining_code[0]== "!<+!^+!A" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.A= False  #not (player.player_buttons.Y)
                print("!<+!^+!A")

            elif self.remaining_code[0]== "<+^+B" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print("<+^+B")
            elif self.remaining_code[0]== "!<+!^+!B" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.B= False  #not (player.player_buttons.Y)
                print("!<+!^+!B")

            elif self.remaining_code[0]== "v+R" :
                self.buttn.down=True
                self.buttn.R= not (player.player_buttons.R)
                print("v+R")
            elif self.remaining_code[0]== "!v+!R" :
                self.buttn.down=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!v+!R")

            else:
                if self.remaining_code[0] =="v" :
                    self.buttn.down=True
                    print ( "down" )
                elif self.remaining_code[0] =="!v":
                    self.buttn.down=False
                    print ( "Not down" )
                elif self.remaining_code[0] =="<" :
                    print ( "left" )
                    self.buttn.left=True
                elif self.remaining_code[0] =="!<" :
                    print ( "Not left" )
                    self.buttn.left=False
                elif self.remaining_code[0] ==">" :
                    print ( "right" )
                    self.buttn.right=True
                elif self.remaining_code[0] =="!>" :
                    print ( "Not right" )
                    self.buttn.right=False

                elif self.remaining_code[0] =="^" :
                    print ( "up" )
                    self.buttn.up=True
                elif self.remaining_code[0] =="!^" :
                    print ( "Not up" )
                    self.buttn.up=False
            self.remaining_code=self.remaining_code[1:]
        return
