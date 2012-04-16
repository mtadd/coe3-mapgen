#!/home/mtadd/bin/python
from constants import render_template
import cgi
import copy
from trials import pick_players, get_ordered_trials
from mapgen import format, CLASS, AI, SOCIETY, MAPSIZE, MAP_DIMS

form = cgi.FieldStorage()

def web_get(url):
   import urllib
   return urllib.urlopen(url).read()

COLORS = [ (22,90,18), (90,27,18), (18,40,90), (90,88,18), 
           (18,77,90), (90,18,86), (90,63,18), (49,18,90) ]

def player_color(player):
   color = COLORS[player-1]
   return format('rgb({0},{1},{2})',*color)

def player_block(player):
   color = player_color(player)
   return format('<div class="colorblock" style="outline-color: {0}; background-color: {1}" temp="{2}" ></div>',color,color,player)

try:
   trials = get_ordered_trials()
   num = int(form.getvalue("t"))
   trial = copy.deepcopy(trials[num-1])
   players = pick_players(trial['classes'],trial['levels'],
                   trial.get('teams',None),trial.get('sets',None))
   if trial.has_key('desc url'):
      trial['descurl'] = web_get(trial['desc url'])

   render_template('trial.html', trial=trial, players=players,
         COLORS=COLORS, AI=AI, CLASS=CLASS, SOCIETY=SOCIETY, MAPSIZE=MAPSIZE,
         OPTMAP = {True: 'On', False: 'Off'})
except IndexError:
   render_template('trials.html',trials=trials,error=
         'Value ("t") must be a number between 1 and ' + str(len(trials)))
except ValueError:
   render_template('trials.html',trials=trials,error=
         'Value ("t") must be a number between 1 and ' + str(len(trials)))

