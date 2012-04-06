import sys
sys.path.insert(0,"../..")
import flask
from trials import TRIALS, pick_players
from mapgen import AI,CLASS,SOCIETY,MAPSIZE
import copy
app = flask.Flask(__name__)

@app.route('/')
@app.route('/trials')
def show_trial_list():
   return flask.render_template('trials.html', trials=TRIALS)

@app.route('/trial/<int:num>')
def show_trial(num):
   trial = copy.deepcopy(TRIALS[num-1])
   players = pick_players(trial['classes'],trial['levels'],
                   trial.get('teams',None),trial.get('sets',None))
   return flask.render_template('trial.html', trial=trial, players=players,
         AI=AI, CLASS=CLASS, SOCIETY=SOCIETY, MAPSIZE=MAPSIZE)

if __name__ == '__main__':
   app.run(debug=True)


