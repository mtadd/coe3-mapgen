#!/usr/bin/env python

#
# Graphs score files from coe3
#

# Note:  Launch coe3 with something like the following script.  The --gamelog is important
#
# +++++++++++++
#/bin/bash
#SCORE_LOCATION=/home/richard/.coe3/score
#SCORE=scores-`date +%Y%m%d-%H%M`.txt
#/opt/coe3_linux/coe3_amd64 -dd --rename --showallies --autosave=LastTurn --gamelog=${SCORE_LOCATION}/${SCORE} --battlereports
# +++++++++++++
# Note:  the date stuff prevents re-running of coe3 from writing over old score data.

# ----------------------
#  CHANGE THIS to where your score data (--gamelog) puts data
#   *****  IMPORTANT:  This directory should be cleaned out before every new game.  ****

#Score_Data_Dir = '/Users/mtadd/.coe3/'

# ----------------------

VERSION = ' $Id: coe3-graph-score.py,v 1.2 2012/03/10 03:22:39 richard Exp $ '

colorL = ['red', 'blue', 'green', '#CCCC00', 'purple', 'cyan', 'brown', '0.7', '0.5', '0.3']

score_data = []
  # [  [turn number, season number, [{playerA}, {playerB}, ...] ]  ] each turn is one list entry
  #     {playerX}:    [Name:<name>, type:<human | ai>, .....

def turn_exists(turn):                 # return true if turn already exists in score_data
   for turnL in score_data:            #   also used in add_line_to_data to get turn entry
      if turnL[0] == turn:
         return turnL
   return 0

def data_dump_test():
   print '-' * 20
   score_data.sort()
   for i in score_data:
      print i
   
def add_line_to_data(turn, fileLine):  # add a player line as a dectionary to a turn in score_data
   global score_data
   lineL = fileLine.split(', ')        # split up the line on commas
   turnIndex = score_data.index(turn_exists(turn)) # the score_data index of the current turn list entry
   playerD = {}
   for i in lineL:
      if r_keyNum.search(i):
         playerD[r_keyNum.search(i).group(1)] = r_keyNum.search(i).group(2)
      elif i.find('Name') == 0:
         playerD['Name'] = i[5:]
      elif i.find('Class') == 0:
         playerD['Class'] = i[6:]
      elif i.find('Human') == 0:
         playerD['type'] = 'Human'
      elif i.find('AI') == 0:
         playerD['type'] = 'AI'
      elif i.find('Dead') == 0:
         playerD['type'] = 'Dead'
      else:
         print 'ERROR in add_line_to_data:  no match for:  %s' % (i)
   score_data[turnIndex][2].append(playerD)

def getdata(score_file_time):
   global score_data
   new_score_file_time=time.time()
   if len(sys.argv) > 1:
      score_fileL = sys.argv[1:]
   else:
      score_fileL = glob.glob("*.log")
   for sf in score_fileL:
      print "Reading game log", sf
      if os.stat(sf).st_mtime > score_file_time:  # time newer than last read
         fileL = open(sf, 'r').readlines()
         add_turn = 0                  # if > 0 adding that turn number data
         for line in fileL:
            if r_turn.search(line):    # this is a 'turn' line
               turn =   int(r_turn.search(line).group('turnNum'))
               season = int(r_turn.search(line).group('season'))
               if turn_exists(turn):   # ignore turn if already exists
                  add_turn = 0         # if > 0 adding that turn number data
                  # print "Turn %d already exists, ignoring" % (turn)
               else:
                  add_turn = 1         # add next player lines to this turn
                  score_data.append([turn,season,[]])
               continue                # don't need more processing for this file line
            if add_turn and line.find('Player ') == 0:   # this is a player line
               add_line_to_data(turn, line)  
               continue
            else:
               add_turn = 0            # assume end of turn
   score_data.sort()
   return new_score_file_time

def get_keys():                        # create a list of keys (data types, ex, Iron)
   keyL = score_data[0][2][0].keys()   #   remove the non data related fields
   keyL.pop(keyL.index('Player'))
   keyL.pop(keyL.index('Name'))
   keyL.pop(keyL.index('type'))
   keyL.pop(keyL.index('Class'))
   return keyL

def print_columns(ncols, keyL):
   maxlen = str(max(map(len,keyL)))
   fmt = "  %2d %-" + maxlen + "s"
   rows = len(keyL) // ncols
   j = 0
   while j < len(keyL):
      for i in range(ncols):
         if j+i < len(keyL):
            print fmt % (j+i, keyL[j+i]),
      print ""       
      j += ncols 

def user_input(keyL, graphL):          # user input -- graphL holds last input for repeating
   print "enter number(s), space separated,  or <return> to keep last selection:"
   print_columns(4,keyL)
   userinL = raw_input('Enter numbers, space separated, or <return> to keep last selection: ')
   if userinL == 'q':
      return None
   userinL = userinL.split()
   inL = []
   if len(userinL) == 0:
      inL = graphL
   else:
      for i in userinL:
         inL.append(keyL[int(i)])
   return inL

def graph_it(graphL):
   for item in graphL:
      fig = plt.figure()
      ax = fig.add_subplot(111)
      numPlayers = len(score_data[0][2])  # assumes the number of players is constant
      playerNum = 0
      while playerNum < numPlayers:
         xL = []
         yL = []
         for turnL in score_data:
            xL.append(turnL[0])
            yL.append(int(turnL[2][playerNum][item]))
         labelText = score_data[0][2][playerNum]['Class'] + ': ' + score_data[0][2][playerNum]['Name']
         plt.plot(xL, yL, color = colorL[playerNum], label=labelText, linewidth=2.0)
         playerNum += 1
      #rescale y-axis min to 0
      axis = list(plt.axis())
      axis[2] = 0
      plt.axis(axis)

      from matplotlib.ticker import MultipleLocator
      #set major ticks to 12, minor to 3
      ax.xaxis.set_major_locator(MultipleLocator(12.0))
      ax.xaxis.set_minor_locator(MultipleLocator(3.0))
      
      ymax = axis[3]
      ytvals = [i*10**j for j in range(5) for i in [1,5]]
      ytdiffs = map(lambda n:abs(ymax/10.0-n),ytvals)
      ytick = ytvals[ytdiffs.index(min(ytdiffs))]
      ax.yaxis.set_major_locator(MultipleLocator(ytick))

      ax.xaxis.grid(True,which='both')
      #ax.yaxis.grid(True)

      #striping
      yTicks = ax.get_yticks()[:-1]
      xTicks = ax.get_xticks()
      if len(yTicks) >= 2:
         ax.barh(yTicks, [axis[1]]*len(yTicks), 
            height=(yTicks[1]-yTicks[0]), left=min(xTicks), 
            color=['#4c4040','#332a2b'])

      #legend placement and color
      plt.legend(loc=0)
      ax.get_legend().get_frame().set_facecolor('#61302C')
      ax.get_legend().get_frame().set_edgecolor('#89795F')
      for text in ax.get_legend().get_texts():
         text.set_color('#C3AC96')

      plt.title(item)
      plt.show()

def main():
   global score_data
   score_file_time = 0
   score_file_time = getdata(score_file_time)
   keyL = get_keys()
   keyL.sort()
   # data_dump_test()
   graphL = []
   graphL.append(keyL[0])              # initial 'saved' choice
   while(1):
      graphL = user_input(keyL, graphL)
      if graphL == None:
         break
      score_file_time = getdata(score_file_time)
      graph_it(graphL)

if __name__ == '__main__':
   import re, os, time, sys, readline, matplotlib.pyplot as plt
   import os.path, glob
   r_turn    = re.compile(r'^turn:\s+(?P<turnNum>\d+).+season\s+(?P<season>\d+)')
   r_keyNum  = re.compile(r'(\D+) (\d+)')
   main()

