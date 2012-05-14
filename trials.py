#!/usr/bin/env python
import sys
import os
import os.path
from optparse import Values
import mapgen
from mapgen import format
from mapgen import Enum, CLASS, AI, SOCIETY, MAPSIZE, MAP_DIMS, CLASS_ANY

def get_ordered_trials():
   return sorted(TRIALS,key=lambda e: e['order'])

TRIALS = [ {
'title':"You're Just a Commoner",
'desc':"""Don't feel so bad, not everyone can be good at everything.  Defeat one Knight-level AI on a large map.""",
'classes': [CLASS_ANY]*2,
'levels': [AI.HUMAN, AI.KNIGHT],
'map_size': MAPSIZE.LARGE,
'society': SOCIETY.Random,
'order': 1
   }, {
'title':"Three Years' War",
'desc':"""Better hurry, three years isn't much time.
Defeat one Count-level AI on a small map in less than 35 turns.""",
'classes': [ [CLASS.TrollKing,CLASS.Witch,CLASS.Necromancer], CLASS_ANY ],
'levels': [AI.HUMAN, AI.COUNT],
'map_size': MAPSIZE.SMALL,
'society': SOCIETY.Random,
'order': 9
   },{
'title':"A Little Disagreement",
'desc':"Small people, huge wars.  Defeat one Count-level AI on a small map.",
'sets': {'A':[CLASS.Burgmeister, CLASS.DWARF_QUEEN]},
'classes': 'A'*2,
'levels': [0, AI.COUNT],
'map_size': MAPSIZE.SMALL,
'society': SOCIETY.Random,
'order': 2
   }, {
'title':"Eye for an Eye Justice",
'desc':"You thought you were so special because you were the only one. Guess again.  Defeat one Count-level AI on a small map.",
'classes': [[CLASS.PALE_ONE]]*2,
'levels': [0,AI.COUNT],
'map_size': MAPSIZE.SMALL,
'society': SOCIETY.Random,
'order': 3
   }, {
'title':"A Part of the Tribe",
'desc':"Everyone should be a part of the tribe, whether they want to be or not.  Defeat one Count-level AI on a large map.",
'sets' : {'A': list(set(CLASS_ANY) - 
                 set([CLASS.BAKEMONO, CLASS.PRIEST_KING, CLASS.BARBARIAN])) },
'classes': [ [CLASS.BAKEMONO, CLASS.PRIEST_KING, CLASS.BARBARIAN], 'A' ],
'levels': [0, AI.COUNT],
'map_size': MAPSIZE.LARGE,
'society': SOCIETY.DarkAges,
'order': 5
   }, {
'title':"The Justice League",
'desc':'''The forces of light are... rather undependable.
Ally yourself with 3 Jester level AI against 4 allied Knight-level AI on a huge map.''',
'sets': {'A': [CLASS.Baron, CLASS.Barbarian, CLASS.Senator, CLASS.Druid, 
               CLASS.Burgmeister, CLASS.Warlock, CLASS.Enchanter, 
               CLASS.DwarfQueen],
         'B': [CLASS.Necromancer, CLASS.Demonologist, CLASS.Witch,
               CLASS.HighPriestess, CLASS.Bakemono, CLASS.PALE_ONE, 
               CLASS.PriestKing, CLASS.TrollKing, CLASS.HighCultist] },
'classes': 4*'A'+4*'B',
'levels': [0]+3*[AI.Jester]+4*[AI.Knight],
'teams': [1]*4+[2]*4,
'map_size': MAPSIZE.Large,
'society': SOCIETY.FallenEmpire,
'options': {'Common cause': True, 'Cluster start': True},
'order': 4
}, {
'title':'The Legions of Doom',
'desc':'''The most egotistical alliance ever seen.
Ally yourself with 3 Jester level AI against 4 allied Baron-level AI on a huge map.''',
'sets': {'A': [CLASS.Baron, CLASS.Barbarian, CLASS.Senator, CLASS.Druid, 
               CLASS.Burgmeister, CLASS.Warlock, CLASS.Enchanter, 
               CLASS.DwarfQueen],
         'B': [CLASS.Necromancer, CLASS.Demonologist, CLASS.Witch,
               CLASS.HighPriestess, CLASS.Bakemono, CLASS.PALE_ONE, 
               CLASS.PriestKing, CLASS.TrollKing, CLASS.HighCultist] },
'classes': 'B'*4+4*'A',
'teams': [1]*4+[2]*4,
'levels': [0]+3*[AI.Jester]+4*[AI.Baron],
'map_size': MAPSIZE.Huge,
'society': SOCIETY.DawnofaNewEmpire,
'options': {'Common cause': False, 'Cluster start': True},
'order': 8
}, {
'title':'Flawless Victory',
'quote':('''"May the lightning of your glory be seen and the thunders of your onset heard from east to west, and be ye the avengers of noble blood."''',
         "William of Normandy"),
'desc':"""Defeat two allied Count-level AI on a huge map during the Dark Ages without losing a single commander.""",
'classes': [CLASS.Baron, CLASS.DwarfQueen, CLASS.Barbarian],
'levels': [0, AI.Count, AI.Count],
'teams': [1,2,2],
'map_size': MAPSIZE.Huge,
'society': SOCIETY.DarkAges,
'options': {'Common cause': True, 'Cluster start': False},
'order': 10
}, {
'title':'Running the Gauntlet',
'desc':'''The CoE3-class sampler... with a serious catch (contributed by BandC).
Play 17 games with each sequential class (start with Baron, then Necromancer, Demonologist, etc.) vs. 3 random Jester-level AI (not allied). If you lose a game, you have to start the challenge from the beginning. In other words, you must win the game with these settings for every single class without losing a single game.
Player class: Play each class sequentially (but if you lose twice, you have to start from the beginning of the list)
AI class: Three random non-allied classes
AI level: Jester''',
'map_size': MAPSIZE.Tiny,
'society': SOCIETY.Random,
'classes': [],
'levels': [],
'teams': [],
'order': 11
}, {
'title':'Squeezed In',
'desc':"""Feel the pressure (taken from gp1628's game variations).
Playing multiplayer, you and one human ally must beat two teams, each consisting of three Knight-level AI players. Both human players will receive a point for winning.""",
'classes': [ CLASS_ANY, CLASS_ANY, CLASS.Necromancer, CLASS.Demonologist, CLASS.Witch, CLASS.HighPriestess, CLASS.PriestKing, CLASS.HighCultist],
'levels': 2*[AI.Human]+6*[AI.Knight],
'teams' : 2*[1]+3*[2]+3*[3],
'map_size': MAPSIZE.Small,
'society': SOCIETY.Monarchy,
'options': {'Common cause': True, 'Cluster start': True },
'order': 13
}, {
'title':'Anti-Progress',
'quote': ('"We do not ride on the railroad; it rides upon us."',
          "Henry David Thoreau"),
'desc':"""Defeat 2 allied Knight-level AI on a large map with the society set as Dawn of a New Empire""",
'classes': [ [CLASS.Necromancer, CLASS.Demonologist, CLASS.Druid, 
              CLASS.Bakemono, CLASS.HighCultist],
             CLASS.Baron, CLASS.Senator],
'levels': [0, AI.Knight, AI.Knight],
'teams': [1,2,2],
'map_size': MAPSIZE.Small,
'society': SOCIETY.DawnofaNewEmpire,
'options': {'Common cause': True, 'Cluster start': False},
'order': 7
}, {
'title':'The Witch Hunter',
'desc':'''Make the land safe for your citizens. Why? So you get more taxes.
Defeat 3 allied Knight-level AI on a huge map with the society set to Empire.''',
'classes': [CLASS.Baron, CLASS.Witch, CLASS.Necromancer, CLASS.Demonologist],
'levels': [0] + [AI.Knight]*3,
'teams': [1]+3*[2],
'map_size': MAPSIZE.Small,
'society': SOCIETY.Empire,  
'options': {'Common cause': True, 'Cluster start': False},
'order': 12
}, {
'title':'Sorceror in the Middle',
'desc':'''Put a stop to all the commotion outside so you can go back to your mountain and go to sleep.
Defeat all Marquis-level AI, which consists of two AI teams, on a huge map with society set to Monarchy.''',
'sets': { 'A': [CLASS.Baron, CLASS.Senator, CLASS.Barbarian, CLASS.TrollKing],
          'B': [CLASS.Witch, CLASS.HighPriestess, CLASS.PriestKing] },
'classes': [ CLASS.Bakemono, 'A', 'A', 'A', 'A', 'B', 'B', 'B'],
'levels': [0] + 7*[AI.Marquis],
'teams': [1]+4*[2]+3*[3],
'map_size': MAPSIZE.Large,
'society': SOCIETY.Monarchy,
'options': {'Common cause': True, 'Cluster start': True},
'order': 14
}, {
'title':'Something Nasty is Brewing',
'quote': ('''"All that the witch-finder doth is to fleece the country of their money, and therefore rides and goes to townes to have imployment, and promiseth them faire promises, and it may be doth nothing for it, and possesseth many men that they have so many wizzards and so many witches in their towne, and so hartens them on to entertaine him."''',"The Discovery of Witches by Matthew Hopkins"),
'desc': '''Defeat five allied Jester-level AI on a large map during the Monarchy without your ally being defeated. Since the witch hunt was just proclaimed, you will need to rush to your ally's aid.''',
'classes': [CLASS.Witch,CLASS.Witch,CLASS.DwarfQueen,CLASS.Burgmeister,
            CLASS.Senator,CLASS.Druid,CLASS.Warlock],
'levels': [AI.Human]+6*[AI.Jester],
'teams': [1,1]+5*[2],
'options': {'Common cause': False, 'Cluster start': False},
'map_size': MAPSIZE.Large,
'society': SOCIETY.Monarchy,
'order': 15
}, {
'title':'Bring Out Your Dead',
'desc':'''So many dealings with the mindless is sure to drive you insane.
Defeat an alliance between a Jester-level Baron, a Butler-level Druid, and a Knight-level Senator.''',
'classes':[CLASS.NECROMANCER, CLASS.BARON, CLASS.DRUID, CLASS.SENATOR],
'levels': [0, AI.Jester, AI.Butler, AI.Knight],
'teams': [1]+3*[2],
'options':{'Common cause': False, 'Cluster start': False},
'map_size': MAPSIZE.Large,
'society': SOCIETY.FallenEmpire,
'order': 6
}, {
'title':'Save the Peons',
'desc':''' Your serfs are apt to complain, but now that they have started disappearing regularly you've determined that maybe there is something to their bickering...
Defeat five allied Butler-level AI on a large map.''',
'sets': {'A': [CLASS.Demonologist, CLASS.HighPriestess, CLASS.Bakemono,
               CLASS.PriestKing, CLASS.HighCultist] },
'classes': [CLASS.Baron, 'A', 'A', 'A', 'A', 'A'],
'levels': [0] + [AI.Butler]*5,
'teams': [1] + 5*[2],
'map_size': MAPSIZE.Large,
'society': SOCIETY.Agricultural,
'options': {'Cluster start': False, 'Common cause': False},
'order': 16
}, {
'title':'Political Tribulations',
'desc':'''In order to get reelected, you'll have to be alive.
The scenario can be downloaded from this post.''',
'classes': [CLASS.Senator, CLASS.Necromancer],
'levels': [0, AI.Butler],
'options':{'map url': 'http://ubuntuone.com/3w4a250e89binJ1tqeMfws'},
'order': 23
}, {
'title':'Seven Levels of Hell',
'desc':'''Defeat seven random AI enemies (no enemy demonologist) ranging in levels from Jester to Duke''',
'sets' : {
   'A': list(set(CLASS_ANY)-set([CLASS.Demonologist])),
   'B': [AI.Jester,AI.Butler,AI.Knight,AI.Baron,AI.Count,AI.Marquis,AI.Duke] 
  },
'classes': [CLASS.Demonologist]+7*['A'],
'levels': [0]+7*['B'],
'map_size': MAPSIZE.Large,
'society': SOCIETY.FallenEmpire,
'order': 17
}, {      
'title':'Curses!',
'quote': ('''"Sweet love, I see, changing his property,
Turns to the sourest and most deadly hate:
Again uncurse their souls; their peace is made
With heads, and not with hands; those whom you curse
Have felt the worst of death's destroying wound
And lie full low, graved in the hollow ground."''',
         "William Shakespeare's King Richard the Second"),
'desc': '''Defeat four allied AI enemies (one Duke and three Counts) on a large map with a random society.''',
'classes': [CLASS.HighPriestess, CLASS.Demonologist, CLASS.Bakemono, CLASS.PriestKing, CLASS.HighCultist],
'levels': [AI.Human, AI.Duke] + 3*[AI.Count],
'options': { 'Common cause': True, 'Clustered start': False }, 
'teams': [1]+4*[2],
'map_size' : MAPSIZE.Small,
'society' : SOCIETY.Random,
'order': 18,
}, {
'title':'Disposing of a Despot',
'quote': ('''"The Goths were now, on every side, surrounded and pursued by the Roman arms. The flower of their troops had perished in the long siege of Philippopolis, and the exhausted country could no longer afford subsistence for the remaining multitude of licentious barbarians. Reduced to this extremity, the Goths would gladly have purchased, by the surrender of all their booty and prisoners, the permission of an undisturbed retreat. But the emperor, confident of victory, and resolving, by the chastisement of these invaders, to strike a salutary terror into the nations of the North, refused to listen to any terms of accommodation. The high-spirited barbarians preferred death to slavery."''', "Edward Gibbon's History of the Decline and Fall Of the Roman Empire"),
'desc': """Defeat an Emperor-level AI Senator during the Empire society on an enormous map.""",
'classes': [CLASS.Barbarian, CLASS.Senator],
'levels': [0, AI.Emperor],
'map_size': MAPSIZE.Small,
'society': SOCIETY.Empire,
'order': 22
}, {
'title':'Homelands',
'desc':'''You've decided it's time to redraw the borders (scenario by hunter).
Please read the introduction to this scenario, written by its author, which you can access by clicking here. This scenario can be downloaded by clicking here (note that it will be easier to right-click the link and save the file).''',
'desc url':'http://dl.dropbox.com/u/2108541/Homelands%20Readme.txt',
'classes':[CLASS.Baron, CLASS.Witch, CLASS.Burgmeister, CLASS.Warlock, CLASS.HighCultist, CLASS.PriestKing, CLASS.Barbarian, CLASS.DwarfQueen],
'levels': [0] + 2*[AI.Butler]+5*[AI.Knight],
'options':{'map url': 'http://dl.dropbox.com/u/2108541/Homelands8.coem'},
'order': 20 
}, {
'title':'An Absolute Bash',
'desc':""" Roam the countryside wreaking havoc. But that will make you a lot of enemies...
Defeat 5 allied classes on a large map with the society set to agricultural.""",
'sets': {'A' : list(set(CLASS_ANY)- set([CLASS.TrollKing, CLASS.Baron, 
                  CLASS.Witch, CLASS.Burgmeister ])) },
'classes':[ CLASS.TrollKing, CLASS.Baron, CLASS.Witch, CLASS.Burgmeister, 'A' ],
'levels': [0] + 4*[AI.Knight],
'teams': [1] + 4*[2],
'map_size': MAPSIZE.Small,
'society': SOCIETY.Agricultural,
'options': {'Common cause': False, 'Cluster start': False},
'order': 21
} , {
'title':'One Against the World',
'desc':'''Ever feel like the whole world is out to get you?
Hold at least 5 enemy citadels for at least a year of the 7 allied Jester-level AI on a large map using any class.''',
'sets': { 'A': CLASS_ANY },
'classes': [CLASS.PlayerChoice]+7*['A'],
'levels': [0] + 7*[AI.Jester],
'teams': [1] + 7*[2],
'society': SOCIETY.Random,
'map_size': MAPSIZE.Large,
'options': {'Common cause': True, 'Cluster start': False },
'order': 19
}
]

def choose(c,sets):
   if isinstance(c,str) and sets.has_key(c):
      s = sets[c]
      v = mapgen.choose(s)
      s.remove(v)
      return v
   return mapgen.choose(c)

def pick_players(classes, levels, teams=None,sets=None):
   '''
   Returns an array of tuple (class, ai-level (0=human), team)
   '''
   if teams is None: teams = range(1,1+len(classes))
   if sets is None: sets = {}
   players = range(1,1+len(classes))
   sets = dict(sets) #shallow copy
   return [(i,choose(c,sets), choose(l,sets), t) 
           for i, c, l, t in zip(players, classes, levels, teams)]

def trialgen(trial, mapdir, rungame):
   mapname = format("trial{0}",trial['order'])
   mapgen.options.filename = os.path.join(mapdir, format("{0}.coem",mapname)) 
   mapgen.options.debug = options.debug
   map_url = trial.get('options',{}).get('map url',None)
   if not map_url:
      mapdim = MAP_DIMS[trial['map_size']]

   if options.mapgen:
      if map_url:
         cmd = format("curl -o {0} {1}",mapgen.options.filename,
            trial['options']['map url'])
         print cmd
         os.system(cmd)
      else:
         mapgen.options.basic = True
         mapgen.options.mapwidth = mapdim[0]
         mapgen.options.mapheight = mapdim[1]
         mapgen.mapgen()

   title = format("Trial By Fire {0}: {1}",trial['order'], trial["title"])
   output = ['',title, '-'*len(title)] 
   if trial.has_key('quote'):
      for line in trial['quote'][0].split('\n'):
         output.append( line)
      output.append('\t- ' + trial['quote'][1])
      output.append('')

   output.extend(trial['desc'].split('\n'))

   mapfile = None
   if not map_url:
      output.append( format("Map Size: {0} ({1}x{2})",
            MAPSIZE[trial['map_size']],mapdim[0], mapdim[1]))
      output.append( format("Society: {0} ({1})",SOCIETY[trial["society"]], 
                  trial['society']))
      optmap = {True: 'On', False: 'Off'}
      for k,v in trial.get('options',{}).iteritems():
         output.append(format("{0}: {1}",k,optmap[v]))

      if options.mapgen:
         mapfile = open(mapgen.options.filename,'a')
         mapfile.write('\n')
         mapfile.write( format('mapdescr "{0}"\n',
           '^'.join(map(lambda s: s.replace("\n","^").replace('"',"'"),output)) 
            ))

      players = pick_players(trial['classes'],trial['levels'],
                         trial.get('teams',None),trial.get('sets',None))
      if len(players):
         output.append('')
         output.append('Player\tTeam\tAI\tClass')
      for i, c, l, t in players:         
         output.append( format("{0}\t{1}\t{2}\t{3}", i,t,AI[l],CLASS[c]))
         if mapfile:
            mapfile.write( format("fixedplayer {0} {1} {2} {3} {4}\n",
               i, c, max(t,0), min(l,1), l))
      if mapfile: mapfile.close()
   
   for line in output: print line

   if mapfile: 
      print "Map saved at:", mapgen.options.filename
      cmd_options = [ format("-p {0}",mapname), format("--loadmap={0}",mapname)]
      if trial.has_key('society'): 
         cmd_options.append( format("--society={0}",trial["society"]))
      if trial.has_key('options'):
         if trial['options'].get('Common cause',False) == True:
            cmd_options.append('--commoncause')
         if trial['options'].get('Cluster start',False) == True:
            cmd_options.append('--clusterstart')
      cmd = format("./run_coe3 {0}"," ".join(cmd_options))
      print cmd
      if rungame: os.system(cmd)

default_options = {
   'version': '0.1',
   'debug': False,
   'mapdir': './coe3.app/Contents/Resources/maps',
   'rungame': False,
   'mapgen': True,
   'list_trials': False
   }
options = Values(default_options) 

def print_columns(ncols, keyL):
   rows = len(keyL) // ncols
   if len(keyL) % ncols: rows += 1
   fmts = [ "%2d) %-" + str(max([ len(keyL[j]) 
               for j in range(i*rows,(i+1)*rows) if j < len(keyL)])) +"s "
               for i in range(ncols) ]
   for cols in zip(*[range(i*rows,(i+1)*rows) for i in range(ncols)]):
      for i, k in enumerate(cols):
         if k < len(keyL) :
            print fmts[i]  % (1+k, keyL[k]),
      print ""       

def trials_main():
   from optparse import OptionParser, OptionGroup
   description='''Conquest of Elysium 3 - Trial By Fire scenario map generator.
Default values for options given in parentheses.'''

   global options
   parser = OptionParser(description=description, version=options.version)
   parser.set_defaults(**default_options)
   parser.add_option("--debug",action="store_true",dest="debug",
         help="Really verbose output")
   parser.add_option("-d","--mapdir",dest="mapdir", help="Game map directory")
   parser.add_option("-r","--rungame",action="store_true",dest="rungame",
         help="Run game with the selected trial")
   parser.add_option("--nomap",action="store_false",dest="mapgen",
         help="Just show selected trial description")
   parser.add_option("--list",action="store_true",dest="list_trials",
         help="List trials titles")

   (options, args) = parser.parse_args()

   trials = get_ordered_trials()

   if options.list_trials:
      print_columns(2, [t['title'] for t in trials])
      return

   arg = None
   if len(args) > 0:
      arg = args[0]
   interactive = len(args) == 0
   doloop = True
   while doloop:
      if interactive:
         print_columns(2, [t['title'] for t in trials])
         try:
            arg = raw_input(format("Enter Trial [1-{0}]: ",len(trials)))
         except KeyboardInterrupt:
            print ''
            break
      else:
         doloop = False

      try:
         num = int(arg)
         if num < 0 or num > len(trials): raise IndexError
         doloop = False
      except:
         print format("\n*** Input must be a number between 1 and {0}\n",
               len(trials))
         continue

      trialgen(trials[num-1], options.mapdir, options.rungame)


if __name__ == '__main__':
   trials_main()

