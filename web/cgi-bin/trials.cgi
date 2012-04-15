#!/home/mtadd/bin/python
from constants import render_template
from trials import get_ordered_trials

render_template('trials.html',trials=get_ordered_trials())
