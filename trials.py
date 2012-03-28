#!/usr/bin/env python
import sys
import os
import os.path
from optparse import Values
import mapgen

class Enum(object): 
   def __init__(self, tuples):
      if isinstance(tuples,list) and isinstance(tuples[0],str):
         tuples = zip(range(len(tuples)),tuples)
      self.strs = dict(tuples)
      for val, name in tuples:
         setattr(self,name.upper().replace(" ","_"), val)
         setattr(self,name.replace(" ",""), val)

   def __getitem__(self,key):
      try:
         if isinstance(key,int): return self.strs[key]
         else: raise ValueError()
      except KeyError: 
         raise ValueError()

   def __iter__(self):
      return self.strs.iteritems()

   def __repr__(self):
      return "Enum({0})".format(list(self))



CLASS = Enum([
   (1, "Baron"),
   (2, "Necromancer"),
   (3, "Demonologist"),
   (4, "Witch"),
   (5, "Priestess"),
   (6, "Bakemono"),
   (7, "Barbarian"),
   (8, "Senator"),
   (9, "Pale One"),
   (10, "Druid"),
   (11, "Hoburg"),
   (12, "Warlock"),
   (13, "Priest King"),
   (14, "Troll King"),
   (15, "Enchanter"),
   (19, "High Cultist"),
   (20, "Dwarf Queen")
   ])

AI = Enum([ 
   (0, "Human"),
   (1, "Piss Boy"), # -25%
   (2, "Jester"),   # 0%
   (3, "Butler"),   # 25%
   (4, "Knight"),   # 50%
   (5, "Baron"),    # 75%
   (6, "Count"),    # 100%
   (7, "Marquis"),  # 150%
   (8, "Duke"),     # 200%
   (9, "King"),     # 300%
   (10, "Emperor")  # 500%   
 ])

SOCIETY = Enum([
   (0, "Random"),
   (1, "Dark Ages"),
   (2, "Agricultural"),
   (3, "Empire"),
   (4, "Fallen Empire"),
   (5, "Monarchy"),
   (6, "Dawn of a New Empire")
 ])

MAPSIZE = Enum(["Tiny", "Small", "Large", "Huge", "Enormous"])
   
MAP_DIMS = [ (30, 20), (40, 28), (50, 36), (60, 44), (70, 52) ]

CLASS_ANY = [i for i,v in CLASS] 

def choose_class(c,sets):
   if isinstance(c,str) and sets.has_key(c):
      s = sets[c]
      v = mapgen.choose(s)
      s.remove(v)
      return v
   return mapgen.choose(c)

def pick_classes(classes, levels, teams=None,sets=None):
   '''
   Returns an array of tuple (class, ai-level (0=human), team)
   '''
   if teams is None: teams = range(1,1+len(classes))
   if sets is None: sets = {}
   sets = dict(sets) #shallow copy
   return [(choose_class(c,sets), l, t) 
           for c, l, t in map(None, classes, levels, teams)]



   
TRIALS = [ {
'title':"You're Just a Commoner",
'desc':"Don't feel so bad, not everyone can be good at everything. Defeat one Knight-level AI on a large map.",
'classes': [CLASS_ANY]*2,
'levels': [AI.HUMAN, AI.KNIGHT],
'map_size': MAPSIZE.LARGE,
'society': SOCIETY.Random
   }, {
'title':"A Little Disagreement",
'desc':"Small people, huge wars.  Defeat one Count-level AI on a small map.",
'sets': {'A':[CLASS.HOBURG, CLASS.DWARF_QUEEN]},
'classes': 'A'*2,
'levels': [0, AI.COUNT],
'map_size': MAPSIZE.SMALL,
'society': SOCIETY.Random
   }, {
'title':"Eye for an Eye Justice",
'desc':"You thought you were so special because you were the only one. Guess again.  Defeat one Count-level AI on a small map.",
'classes': [[CLASS.PALE_ONE]]*2,
'levels': [0,AI.COUNT],
'map_size': MAPSIZE.SMALL,
'society': SOCIETY.Random
   }, {
'title':"A Part of the Tribe",
'desc':"Everyone should be a part of the tribe, whether they want to be or not.  Defeat one Count-level AI on a large map.",
'sets' : {'A': list(set(CLASS_ANY) - 
                 set([CLASS.BAKEMONO, CLASS.PRIEST_KING, CLASS.BARBARIAN])) },
'classes': [ [CLASS.BAKEMONO, CLASS.PRIEST_KING, CLASS.BARBARIAN], 'A' ],
'levels': [0, AI.COUNT],
'map_size': MAPSIZE.LARGE,
'society': SOCIETY.DarkAges
   }, {
'title':"The Justice League",
'desc':'''The forces of light are... rather undependable.
Ally yourself with 3 Jester level AI against 4 allied Knight-level AI on a huge map.''',
'sets': {'A': [CLASS.Baron, CLASS.Barbarian, CLASS.Senator, CLASS.Druid, 
               CLASS.Hoburg, CLASS.Warlock, CLASS.Enchanter, 
               CLASS.DwarfQueen],
         'B': [CLASS.Necromancer, CLASS.Demonologist, CLASS.Witch,
               CLASS.Priestess, CLASS.Bakemono, CLASS.PALE_ONE, 
               CLASS.PriestKing, CLASS.TrollKing, CLASS.HighCultist] },
'classes': 4*'A'+4*'B',
'levels': [0]+3*[AI.Jester]+4*[AI.Knight],
'teams': [1]*4+[2]*4,
'map_size': MAPSIZE.Huge,
'society': SOCIETY.FallenEmpire,
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'The Legions of Doom',
'desc':'''The most egotistical alliance ever seen.
Ally yourself with 3 Jester level AI against 4 allied Baron-level AI on a huge map.''',
'sets': {'A': [CLASS.Baron, CLASS.Barbarian, CLASS.Senator, CLASS.Druid, 
               CLASS.Hoburg, CLASS.Warlock, CLASS.Enchanter, 
               CLASS.DwarfQueen],
         'B': [CLASS.Necromancer, CLASS.Demonologist, CLASS.Witch,
               CLASS.Priestess, CLASS.Bakemono, CLASS.PALE_ONE, 
               CLASS.PriestKing, CLASS.TrollKing, CLASS.HighCultist] },
'classes': 'B'*4+4*'A',
'teams': [1]*4+[2]*4,
'levels': [0]+3*[AI.Jester]+4*[AI.Baron],
'map_size': MAPSIZE.Huge,
'society': SOCIETY.DawnofaNewEmpire,
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'Flawless Victory',
'desc':"""May the lightning of your glory be seen and the thunders of your onset heard from east to west, and be ye the avengers of noble blood." - William of Normandy
Defeat two allied Count-level AI on a huge map during the Dark Ages without losing a single commander.""",
'classes': [CLASS.Baron, CLASS.DwarfQueen, CLASS.Barbarian],
'levels': [0, AI.Count, AI.Count],
'teams': [1,2,2],
'map_size': MAPSIZE.Huge,
'society': SOCIETY.DarkAges,
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'Anti-Progress',
'desc':"""We do not ride on the railroad; it rides upon us" - Henry David Thoreau
Defeat 2 allied Knight-level AI on a large map with the society set as Dawn of a New Empire""",
'classes': [ [CLASS.Necromancer, CLASS.Demonologist, CLASS.Druid, 
              CLASS.Bakemono, CLASS.HighCultist],
             CLASS.Baron, CLASS.Senator],
'levels': [0, AI.Knight, AI.Knight],
'teams': [1,2,2],
'society': SOCIETY.DawnofaNewEmpire,
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'The Witch Hunter',
'desc':'''Make the land safe for your citizens. Why? So you get more taxes.
Defeat 3 allied Knight-level AI on a huge map with the society set to Empire.''',
'classes': [CLASS.Baron, CLASS.Witch, CLASS.Necromancer, CLASS.Demonologist],
'levels': [0] + [AI.Knight]*3,
'teams': [1]+3*[2],
'map_size': MAPSIZE.Large,
'society': SOCIETY.Empire,  
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'Sorcerer in the Middle',
'desc':'''Put a stop to all the commotion outside so you can go back to your mountain and go to sleep.
Defeat all Marquis-level AI, which consists of two AI teams, on a huge map with society set to Monarchy.''',
'sets': { 'A': [CLASS.Baron, CLASS.Senator, CLASS.Barbarian, CLASS.TrollKing],
          'B': [CLASS.Witch, CLASS.Priestess, CLASS.PriestKing] },
'classes': [ CLASS.Bakemono, 'A', 'A', 'A', 'A', 'B', 'B', 'B'],
'levels': [0] + 7*[AI.Marquis],
'teams': [1]+4*[2]+3*[3],
'map_size': MAPSIZE.Huge,
'society': SOCIETY.Monarchy,
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'Save the Peons',
'desc':''' Your serfs are apt to complain, but now that they have started disappearing regularly you've determined that maybe there is something to their bickering...
Defeat five allied Butler-level AI on a large map.''',
'sets': {'A': [CLASS.Demonologist, CLASS.Priestess, CLASS.Bakemono,
               CLASS.PriestKing, CLASS.HighCultist] },
'classes': [CLASS.Baron, 'A', 'A', 'A', 'A', 'A'],
'levels': [0] + [AI.Butler]*5,
'teams': [1] + 5*[2],
'map_size': MAPSIZE.Large,
'society': SOCIETY.Agricultural
}, {
'title':'Political Tribulations',
'desc':'''In order to get reelected, you'll have to be alive.
The scenario can be downloaded from this post.''',
'classes': [CLASS.Senator, CLASS.Necromancer],
'levels': [0, AI.Knight],
'options':{'Map URL': 'http://ubuntuone.com/3w4a250e89binJ1tqeMfws'}
}, {
'title':'Disposing of a Despot',
'desc':"""The Goths were now, on every side, surrounded and pursued by the Roman arms. The flower of their troops had perished in the long siege of Philippopolis, and the exhausted country could no longer afford subsistence for the remaining multitude of licentious barbarians. Reduced to this extremity, the Goths would gladly have purchased, by the surrender of all their booty and prisoners, the permission of an undisturbed retreat. But the emperor, confident of victory, and resolving, by the chastisement of these invaders, to strike a salutary terror into the nations of the North, refused to listen to any terms of accommodation. The high-spirited barbarians preferred death to slavery." - Edward Gibbon's History of the Decline and Fall Of the Roman Empire
Defeat an Emperor-level AI Senator during the Empire society on an enormous map.""",
'classes': [CLASS.Barbarian, CLASS.Senator],
'levels': [0, AI.Emperor],
'map_size': MAPSIZE.Enormous,
'society': SOCIETY.Empire
}, {
'title':'An Absolute Bash',
'desc':""" Roam the countryside wreaking havoc. But that will make you a lot of enemies...
Defeat 5 allied classes on a large map with the society set to agricultural.""",
'sets': {'A' : list(set(CLASS_ANY)- set([CLASS.TrollKing, CLASS.Baron, 
                  CLASS.Witch, CLASS.Senator, CLASS.Hoburg ])) },
'classes':[ CLASS.TrollKing, CLASS.Baron, CLASS.Witch, CLASS.Senator, 
            CLASS.Hoburg, 'A' ],
'levels': [0] + 5*[AI.Knight],
'teams': [1] + 5*[2],
'map_size': MAPSIZE.Large,
'society': SOCIETY.Agricultural,
'options': {'Common cause': 'Off', 'Clustered start': 'On'}
}, {
'title':'One Against the World',
'desc':""" Ever feel like the whole world is out to get you?
Defeat 7 allied Jester-level AI on an enormous map using any class.""",
'sets': { 'A': CLASS_ANY },
'classes': 'A'*8,
'levels': [0] + 7*[AI.Jester],
'teams': [1] + 7*[2],
'society': SOCIETY.Random,
'options': {'Common cause': 'Off', 'Clustered start': 'On',
            'Player Class': 'Choose Any'}
}
]

def trialgen(idx, mapdir, rungame):
   trial = TRIALS[idx]
    
   print trial['title']
   print '-'*len(trial['title'])
   print trial['desc']

   i = 1
   print '\nPlayer\tTeam\tAI\tClass'
   
   players = pick_classes(trial['classes'],trial['levels'],
                      trial.get('teams',None),trial.get('sets',None))
   for c, l, t in players:
      print '{0}\t{1}\t{2}\t{3}'.format(
               i,t,AI[l],CLASS[c])
      i += 1
   print '='
   mapdim = MAP_DIMS[trial['map_size']]
   print 'Map Size: {0} ({1}x{2})'.format(
         MAPSIZE[trial['map_size']],mapdim[0], mapdim[1])
   print 'Society:', SOCIETY[trial['society']]
   for k,v in trial.get('options',{}).iteritems():
      print "{0}: {1}".format(k,v)

   mapname = 'trial{0}'.format(idx+1)
   mapgen.options.filename = os.path.join(options.mapdir,
         '{0}.coem'.format(mapname)) 
   mapgen.options.basic = True
   mapgen.options.mapwidth = mapdim[0]
   mapgen.options.mapheight = mapdim[1]
   mapgen.mapgen()

   f = open(mapgen.options.filename,'a')
   f.write('\n')
  
   f.write( 'mapdescr "{0}^^{1}"\n'.format(trial['title'],
      trial['desc'].replace('\n','^').replace('"',"'")))
   i = 1
   for c, l, t in players:
      f.write( 'fixedplayer {0} {1} {2} {3} {4}\n'.format(
         i, c, t if t > 0 else 0, 0 if l == 0 else 1, l))
      i += 1 
   f.close()
   
   if rungame:
      cmd = './run_coe3 -p {0} --loadmap={0} --society={1}'.format(
         mapname, trial['society'])
      print cmd
      os.system(cmd)

   
   

default_options = {
   'version': '0.1',
   'mapdir': './coe3.app/Contents/Resources/maps',
   'rungame': False
   }
options = Values(default_options) 

def trials_main():
   from optparse import OptionParser, OptionGroup
   description='''Conquest of Elysium 3 - Trial By Fire scenario map generator.
Default values for options given in parentheses.'''

   global options
   parser = OptionParser(description=description, version=options.version)
   parser.set_defaults(**default_options)
   parser.add_option("-d","--mapdir",dest="mapdir", help="Game map directory")
   parser.add_option("-r","--rungame",action="store_true",dest="rungame")

   (options, args) = parser.parse_args()

   arg = args[0] if len(args) > 0 else None
   if arg is None:
      for i, trial in enumerate(TRIALS):
         print '{0}) {1}'.format(1+i,trial['title'])
      arg = raw_input('Enter Trial [1-{0}]: '.format(len(TRIALS)))
   i = int(arg)-1
   
   trialgen(i, options.mapdir, options.rungame)

   


if __name__ == '__main__':
   trials_main()

