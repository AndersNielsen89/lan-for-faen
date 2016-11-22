"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from SteamGameCompare import app
from steamapi import core, user
core.APIConnection(api_key="C1A3F48B1D60C30171651AB68A669F19") 

@app.route('/')
@app.route('/<name>')
def home(name=None):
    users = [76561197962013969,76561197969414635,76561197963030643,76561197979558339,76561198026530137,76561197971343484]
    """Renders the home page."""
    name = "76561197992266681"
    content = [] # meta data of the users
    names = [] # names of users
    common_games = [] # a list of all games
    user_games = {} # Games a specific user has in his lib
    try:
        for name in users:
            try:
                steam_user = user.SteamUser(userid=int(name))
            except ValueError: # Not an ID, but a vanity URL.
                steam_user = user.SteamUser(userurl=name)
            name = steam_user.name
            #content = "Your real name is {0}. You have {1} friends and {2} games.".format(steam_user.name,
            #                                                                            len(steam_user.friends),
            #                                                                            len(steam_user.games))
            
            img = steam_user.avatar
            user_info = {"avatar": img, "name": name, "lastgame": steam_user.currently_playing}
            #common_games.append({ name: steam_user.games})
            games = [game.name for game in steam_user.games]
            common_games += games
            user_games[name] = games
            names.append(name)
            content.append(user_info)
        mutual_games, blamelist = find_mutual_games(names,common_games, user_games)
        return render_template('index.html', names=names, content=content, img=img, commongames = mutual_games, blamelist=blamelist)
    except Exception as ex:
    # We might not have permission to the user's friends list or games, so just carry on with a blank message.
        return render_template('index.html', name=name)

def find_mutual_games(names, all_games, user_games):
    mutual_games = {}
    unique_games = set(all_games)
    blame_games = {}
    for game in unique_games:
        occurence = all_games.count(game)
        mutual_games[game]= occurence
        if occurence < 6: 
            blame_games[game] = blame(game, user_games)
    mutual_games_sorted = sorted(mutual_games.items(), key=lambda x:x[1], reverse=True)
    return mutual_games_sorted, blame_games

def blame(game, user_games):
    blame_list = []
    for user in user_games:
        if game not in user_games[user]:
            blame_list.append(user)
    return blame_list
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
