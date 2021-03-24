import random
import sys
import time
import argparse

class Player:
    def __init__(self,name,total=0):
        self.name = name
        self.total = total
    def newTotal(self, newPoint):
        self.total = self.total + newPoint
    def decision(self, game_total=0):
        roll = input("Would you like to roll? r = roll, h = pass" + "\n")
        return roll
class KeepingScore: 
    def addtototalscore(self,rolled_value,total=0):
        total = total + rolled_value
        return total
    #cant access temptotal to pass onto ComputerPlayer(Player) because theres no _init_ method.
    def addtotempscore(self,rolled_value,temptotal=0):
        temptotal = temptotal + rolled_value
        return temptotal
class Game:
    def _int_(self,player,total=0):
        self.player = player
        self.total = total
    def Switchplayer(self,name):
        print("Switching players")
        return 2 if name == 1 else 1
    def currentplayer(self,player):
        #.name is accessed from the Player class that is initialized in line 33.
        print("It is currently %s turn" % (player.name))
    def CurrentScore(self, player):
        print("%s, your current score is %s." % \
        (player.name,player.total))
    def GameOver(self,player,win_points):
        score = player.total
        if score >= win_points:
            print("%s has won." % (player.name))
            print("Restart to play again.")
            sys.exit()


class ComputerPlayer(Player):
    #game_total doesn't exist in the Player class, its supposed to represent turn total.
    #KeepingScore has addtotempscore for this. But KeepingScore has no _init_ function so no values can be passed
    #when you do ComputerPlayer(name)
    def decision(self, game_total):
        #total from Player class
        limit = 100 - self.total
        #the computer will hold at the lesser of 25 and 100 - x. Meaning it will set to whether is smaller.
        limit = 25 if limit > 25 else limit
        #if turn total is smaller than the limit, keep rolling. 
        #Player score could be 100 - 0, so turn total must keep going up till 25.
        if (game_total < limit):
            roll = 'r'
            rolling = 'rolling'
        #Player score could be 100 - 90, meaning the computer won't do as many rolls.
        else:
            #limit could be set to 10, meaning turn total can't go above 10.
            roll = 'h'
            rolling = 'passing'
        return roll
class PlayerFactory:
    def getPlayer(self, player_type, name):
        if player_type == 'h':
            return Player(name)
        if player_type == 'c':
            return ComputerPlayer(name)
class TimedGameProxy:
    def __init__(self, timestamp = 0):
        self.timestamp = timestamp
    def timeCheck(self, timestamp):
        if (self.timestamp == 0 or self.timestamp > time.time() ):
            pass
        else:
            print("GAME OVER")
            print("Your time is up!")
            sys.exit() 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    player1 = parser.add_argument("--player1", help='enter player type: "c" -computer, "h" -human', type=str)
    player2 = parser.add_argument("--player2", help='enter player type: "c" -computer, "h" -human', type=str)
    timed = parser.add_argument("--timed", help='for timed game enter y', type=str)
    args = parser.parse_args()

    factory = PlayerFactory()
    score = KeepingScore()
    game = Game()

    players = { 1: factory.getPlayer(args.player1,'Player 1'),
                2: factory.getPlayer(args.player2,'Player 2')}

    if args.timed=='y':
        timestamp = time.time() + 60
    else:
        timestamp = 0

    p = TimedGameProxy(timestamp)

    current_player = 1
    addingtempscore = 0

    game.currentplayer(players[current_player])

    while players[current_player].total < 100:
        #decision = input("Type r to roll or h to hold and pass on the turn:" + "\n")   
        #You have to pass the turn value somehow to ComputerPlayer(Player)
        decision = players[current_player].decision(addingtempscore)

        if decision == "r":
            rolled_value = random.randrange(1, 7)
            print(rolled_value)
            if rolled_value == 1:
                current_player = game.Switchplayer(current_player)
                game.CurrentScore(players[current_player])
                addingtempscore = 0
                p.timeCheck(timestamp)
            else:
                tempscore = score.addtotempscore(rolled_value)
                addingtempscore = tempscore + addingtempscore
                print("Your turn total is: " + str(addingtempscore))
                game.GameOver(players[current_player], 100)
                p.timeCheck(timestamp)
        elif decision == "h":
            p.timeCheck(timestamp)
            totalscore = score.addtototalscore(addingtempscore)
            #each key in the players dictonary has its own total instanced when the newtotal method is called.
            players[current_player].newTotal(totalscore)
            print("You've added " + str(totalscore) + " to your total score")
            current_player = game.Switchplayer(current_player)
            game.CurrentScore(players[current_player])
            addingtempscore = 0
        else:
            print("enter r - to roll or h - to pass")

        p.timeCheck(timestamp)