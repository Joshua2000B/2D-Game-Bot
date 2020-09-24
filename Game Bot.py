#https://discordpy.readthedocs.io/en/latest/api.html
#API for Discord.py

import discord
import asyncio
from datetime import *
import random

SIZE_X, SIZE_Y = 10,10

COLORS = ["<:yellowcrew:758756327693615124>","<:whitecrew:758756327395819521>","<:redcrew:758756327689420800>","<:pinkcrew:758756327715110943>","<:orangecrew:758756296421277787>","<:limecrew:758756265480028241>","<:greencrew:758756252708241468>","<:cyancrew:758756242276614184>","<:browncrew:758756235687886879>","<:bluecrew:758756229773393960>","<:blackcrew:758756223268159548>"]
#COLORS = ["<:fred:687444771056254986>"]

class Game:
    def __init__(self,users):
        self.area = [[0 for x in range(SIZE_X)] for x in range(SIZE_Y)]
        self.players = {}
        for player in users:
            if(player not in self.players):
                while(True):
                    coords = [random.randint(0,SIZE_X-1),random.randint(0,SIZE_Y-1)]
                    self.players[player] = coords
                    if(self.area[coords[1]][coords[0]] == 0):
                        break
        self.colors = {}
        i = 0
        use_colors = COLORS.copy()
        random.shuffle(use_colors)
        for player in self.players:
            self.colors[player] = use_colors[i]
            i += 1

    def user_is_playing(self,user_id):
        return user_id in self.players

    def move_player_up(self,user_id):
        if(self.players[user_id][0] == 0):
            return
        else:
            self.players[user_id][0] -= 1

    def generate_board(self):
        output = ""
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                if(self.area[y][x] == 0):
                    good = False
                    for player in self.players:
                        if(self.players[player][0] == x and self.players[player][1] == y):
                            output += self.colors[player]
                            good = True
                            break
                    if(not good):
                        output += "⬛️"
                    #check for players
                elif(self.area[y][x] == 1):
                    output += "⬜️"
            output += "\n"
        return output



class MyClient(discord.Client):

    def __init__(self,**args):
        discord.Client.__init__(self)
        self.current_games = {}

    
    #ON MESSAGE
    async def on_message(self,message):
        #print(datetime.now(),":",message.content)
        if(message.content.startswith("/")):
            await self.process_commands(message)
            



    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here
        if(command == "/start"):
            await self.start_game(message)
        elif(command == "/up"):
            await self.up(message)

    async def start_game(self,message):
        if(message.author in self.current_games):
            return
        mentions = [x.id for x in message.mentions] + [message.author.id]
        print("Mentions:",mentions)
        self.current_games[message.author] = [Game(mentions),True]
        board = await message.channel.send(self.current_games[message.author][0].generate_board())
        #loop = False
        while(self.current_games[message.author][1]):
            await asyncio.sleep(1)
            await board.edit(content=self.current_games[message.author][0].generate_board())
        del(self.current_games[message.author])
            
    async def up(self,message):
        active_game = None
        for game in self.current_games:
            if(self.current_games[game][0].user_is_playing(message.author.id)):
                active_game = self.current_games[game][0]
                break
        if(active_game == None):
            return
        active_game.move_player_up(message.author.id)


    #WHEN READY
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name = "game"))
        print("Successfully set Bot's game status")


    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Starting Bot")
bot = MyClient()
file = open("TOKEN.txt",'r')
TOKEN = file.read()
#print(TOKEN)
bot.run(TOKEN)