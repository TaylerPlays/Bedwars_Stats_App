from tkinter import *
import tkinter
from tkinter.font import BOLD
import tkinter.font
from dotenv import load_dotenv
from PIL import Image, ImageTk
import os
import requests
from io import BytesIO
from urllib.request import urlopen
import math
import decimal
import jizhi

HEIGHT = 600
WIDTH = 600
BASE = 10_000
GROWTH = 2_500
REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = REVERSE_PQ_PREFIX
GROWTH_DIVIDES_2 = 2 / GROWTH

app = Tk()
app.title("Tayler's Simple BW Stats")
#app.resizable(False, False)


def format_reponse(data,status):
    try:
        name = (data['player']['displayname'])
        fdeaths = (data['player']['stats']['Bedwars']['final_deaths_bedwars'])
        fkills = (data['player']['stats']['Bedwars']['final_kills_bedwars'])
        wins = (data['player']['stats']['Bedwars']["wins_bedwars"]) 
        losses = (data['player']['stats']['Bedwars']["losses_bedwars"])
        matches = (data['player']['stats']['Bedwars']['games_played_bedwars_1'])
        fkdr = fkills / fdeaths
        star = (data['player']['achievements']['bedwars_level'])
        exp = int(data["player"]["networkExp"])
        #recentlyplayed = (data['player']['mostRecentGameType'])
        expfinal = math.floor(1 + REVERSE_PQ_PREFIX + math.sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * exp))
        wlr = wins / losses
        global rank

        if "rank" in data["player"] and not data["player"]["rank"] == "NORMAL":
            rank = data["player"]["rank"]
        elif "monthlyPackageRank" in data["player"] and not data["player"]["monthlyPackageRank"] == "NONE":
            rank = data["player"]["monthlyPackageRank"]
        elif "newPackageRank" in data["player"]:
            rank = data["player"]["newPackageRank"]
        elif "packageRank" in data["player"]:
            rank = data["player"]["packageRank"]
        else:
            rank = None


        match rank:
            case "SUPERSTAR":
                rank = '[MVP++]'
            case "MVP_PLUS":
                rank = '[MVP+]'
            case "MVP":
                rank = '[MVP]'
            case "VIP_PLUS":
                rank = '[VIP+]'
            case "VIP":
                rank = '[VIP]'
            case "REGULAR":
                rank = '[Default]'
            case "YOUTUBER":
                rank = '[YouTube]'
            case "ADMIN":
                rank = "[Admin]"
            case "HELPER":
                rank = "[Helper]"

        status = response2.json()['session']['online']

        match status:
            case False:
                status = "Offline"
            case True:
                status = "Online"
                

        '''if recentlyplayed not in (data['player']):
            recentlyplayed = None'''

        d = decimal.Decimal(fkdr)
        e = decimal.Decimal(wlr)
        finalstr = 'Username: %s \nBedwars Star: %s \nHypixel Level: %s \nFKDR: %s \nFinal Kills: %s \nFinal Deaths: %s \nWLR: %s \nWins: %s \nLosses: %s \nTotal Matches Played: %s \nStatus: %s' % (rank +" "+ name,star,expfinal,round(d,3), fkills, fdeaths, round(e,3), wins, losses, matches, status)
    
    except:
        finalstr = 'There was an error retrieving \nthe information.'

    return finalstr


def get_stats(name):
    API_KEY = APIKEY
    response1 = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}')
    uuid = response1.json()['id']
    url = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
    response = requests.get(url)
    global response2
    response2 = requests.get(f"https://api.hypixel.net/status?key={API_KEY}&uuid={uuid}")
    global status
    status = response2.json()['session']['online']
    global data
    data = response.json()

    label['text'] = format_reponse(data,status)
    

Minecraftia = tkinter.font.Font( family = "Minecraftia", 
                                 
                                )

canvas = Canvas(app, height= HEIGHT, width= WIDTH)
canvas.pack()


background_img = PhotoImage(file = 'sky3.png')
background_label = Label(app, image = background_img)
background_label.place(x = 0, y = 0, relwidth=1, relheight=1)

frame = Frame(app, bg = '#000000', bd=5)
frame.place(relx=0.5 , rely = 0.1 ,relheight= 0.1, relwidth= 0.75, anchor='n')

entry = Entry(frame, font = ('Verdana', 18), foreground= "white", bg = "black", insertbackground= "white")
entry.place(relwidth=0.67, relheight= 1)

button = Button(frame, text = "Get Stats", font = ('Verdana', 12,'bold'), bg = 'black', foreground = 'white', activebackground = "White",command = lambda: get_stats(entry.get()))
button.place(relx = 0.7,relwidth=0.3, relheight=1)


lower_frame = Frame(app, bg ='#000000', bd=10)
lower_frame.place(relx =0.5, rely = 0.25, relwidth= 0.75, relheight= 0.6, anchor= 'n')


label = Label(lower_frame, font = ('Verdana', 18), anchor= 'nw', justify = 'left', bd = 4, background='black', foreground= 'white')
label.place(relwidth= 1, relheight=1)

#rank.tag_configure("red", foreground="red")

app.mainloop()

