#!/usr/bin/env python
import types
import random
from optparse import Values

T_PLAIN = 0
T_SEA = 69
T_COAST = 65 
T_MOUNTAIN = 12 
T_HIGH_MOUNTAIN = 71
T_HILL1 = 73
T_HILL2 = 74
T_FOREST = 2
T_ANCIENT_FOREST = 4
T_SWAMP = 107
T_RANDOM = 35
T_RANDOM_RARE = 99
T_LAKE1 = 10
T_LAKE2 = 11

TA_FORESTS = (2,4)
TA_MOUNTAINS = (12,71)
TA_HILLS = (73,74)
TA_LAKES = (10,11)
TA_BRIDGES = (48, 49, 168, 169, 178, 179, 186, 187)

COASTS = [
 (TA_LAKES, ['.','.','.', '.','c','.', '.','.','.']),
 (56, ['c.', 'c', '#c', '.', 'c', '#c', 'c.', 'c', 'c#']),
 (57, ['c#', 'c', 'c.', '#c', 'c', '.', 'c#', 'c', 'c.']),
 (58, ['c.', '.', 'c.', 'c', 'c', 'c', 'c#', '#c', 'c#']),
 (59, ['c#', 'c#', 'c#', 'c', 'c', 'c', 'c.', '.', 'c.']),
 (60, ['c.', '.', 'c.', '.', 'c', 'c', 'c.', 'c', '#c']),
 (61, ['c.', '.', 'c.', 'c', 'c', '.', 'c#', 'c', 'c.']),
 (62, ['c.', 'c', 'c#', '.', 'c', 'c', 'c.', '.', 'c.']),
 (63, ['c#', 'c', 'c.', 'c', 'c', '.', 'c.', '.', 'c.']),
 (64, ['.', 'c', '#c', 'c', 'c', 'c#', 'c#', 'c#', 'c#']),
 (65, ['c.', '~', 'c.', 'c.', 'c', 'c.', 'c#', 'c#', 'c#']),
 (66, ['#c', 'c', '.', '#c', 'c', 'c', '#c', '#c', 'c#']),
 (67, ['c#', 'c#', 'c#', '#c', 'c', 'c', 'c#', 'c', '.']),
 (68, ['c#', '#c', '#c', 'c', 'c', '#c', '.', 'c', '#c']),
# (75, ['c.', 'c', '#c', '.', 'c', '#c', 'c.', 'c', 'c#']),
# (76, ['#c', 'c', 'c.', '#c', 'c', '.', 'c#', 'c', 'c.']),
# (77, ['c.', '.', 'c.', 'c', 'c', 'c', '#c', '#', '#c']),
# (78, ['c#', '#c', '#c', 'c', 'c', 'c', 'c.', '.', 'c.']),
# (79, ['c.', 'c', '#c', '.', 'c', '#c', 'c.', 'c', 'c#']),
# (80, ['#c', 'c', '.', 'c#', 'c', '.', 'c#', 'c', 'c.']),
# (81, ['c.', '.', 'c.', 'c', 'c', 'c', '#c', '#', '#']),
# (82, ['#c', '#', '#c', 'c', 'c', 'c', 'c.', '.', 'c.']),
 (108, ['c.', '.', 'c.', 'c', 'c', 'c', 'c.', '.', 'c.']),
 (109, ['c.', 'c', 'c.', '.', 'c', '.', 'c.', 'c', 'c.']),
 (139, ['c.', '.', 'c.', 'c', 'c', '.', 'c.', '.', 'c.']),
 (140, ['c.', '.', 'c.', '.', 'c', 'c', 'c.', '.', 'c.']),
 (141, ['c.', 'c', 'c.', '.', 'c', '.', 'c.', '.', 'c.']),
 (142, ['c.', '.', 'c.', '.', 'c', '.', 'c.', 'c', 'c.']),
 (143, ['.', 'c', '.', 'c', 'c', 'c', 'c#', '#c', 'c#']),
 (144, ['c#', 'c#', '#c', 'c', 'c', 'c', '.', 'c', '.']),
 (145, ['.', 'c', 'c#', 'c', 'c', 'c#', '.', 'c', 'c#']),
 (146, ['c#', 'c', '.', 'c#', 'c', 'c', '#c', 'c', '.']),
 (147, ['.', 'c', 'c#', 'c', 'c', 'c', 'c#', 'c', '.']),
 (148, ['c#', 'c', '.', 'c', 'c', 'c', '.', 'c', 'c#']),
 (149, ['c.', 'c', '.', '.', 'c', 'c', 'c.', 'c', '#c']),
 (150, ['c.', 'c', '#c', '.', 'c', 'c', 'c.', 'c', '.']),
 (151, ['.', 'c', '.c', 'c', 'c', '.', '#c', 'c', 'c.']),
 (152, ['#c', 'c', 'c.', 'c', 'c', '.', '.', 'c', 'c.'])
] 

RIVERS = [
(40, {'...~~~..~': 3, '..~~~~...': 2, '...~~~...': 4, '~..~~~..~': 1, '~..~~~...': 1, '...~~~..~': 1, '~..~~~...': 1, '...~~~~..': 2}),
(41, {'..~~~~...': 1, '....~~...': 1, '..~~~~~..': 2, '~..~~~..~': 1, '..~~~~~..': 1, '~..~~~...': 1, '...~~~...': 1, '...~~~...': 7, '...~~~~..': 2}),
(42, {'.~~.~..~.': 4, '~~.~~....': 1, '.~..~....': 1, '~~..~..~.': 1, '.~.~~.~~.': 1, '.~~.~~...': 1, '.~..~..~~': 3, '.~..~..~.': 1, '~~.~~.~~.': 2, '.~..~..~.': 1, '.~..~....': 1, '.~..~..~.': 16, '....~..~.': 1, '.~~.~~.~~': 1, '....~..~.': 1, '~~.~~.~~.': 1, '.~..~....': 1, '.~..~....': 1, '.~..~.~~.': 1}),
(43, {'.~..~.~~.': 4, '....~..~.': 1, '~~..~..~.': 3, '....~..~~': 1, '.~..~..~.': 1, '.~~.~~~~~': 1, '~~.~~.~~~': 1, '.~.~~.~~.': 1, '~~~.~~.~~': 2, '.~..~..~.': 1, '.~..~..~.': 11, '~~..~.~~.': 1, '.~~.~..~.': 1, '.~..~....': 1, '.~~.~..~.': 2, '~~..~..~.': 1, '.~~.~....': 1, '.~..~....': 1, '.~..~..~~': 2, '.~..~....': 1}),
(44, {'.~.~~.~..': 1, '.~.~~....': 4, '.~.~~....': 1, '.~.~~....': 1, '.~~~~~...': 1}),
(45, {'.~..~~...': 1, '....~~..~': 1, '~~.~~~...': 1, '.~..~~...': 3, '.~..~~...': 1, '.~..~~..~': 2, '~~..~~...': 1, '~~..~~...': 1}),
(46, {'~.~~~~.~~': 1, '....~..~~': 1, '....~..~.': 1, '...~~..~.': 5, '....~..~.': 1, '...~~..~~': 2, '~..~~....': 1, '~..~~..~.': 1, '..~~~~.~~': 1, '...~~..~.': 1}),
(47, {'..~.~~.~.': 1, '....~~.~.': 1, '....~~.~.': 8}),
(48, {'...~~~..~': 1, '..~~~~...': 1, '...~~~...': 1, '~..~~~...': 2, '...~~~..~': 1, '...~~~~..': 1}),
(49, {'.~..~..~.': 5, '.~..~....': 1, '.~..~..~.': 1, '....~..~.': 2, '.~..~..~.': 1, '~~..~..~.': 1, '.~~.~..~.': 1, '.~~.~....': 1, '.~..~.~~.': 3}),
(52, {'...~~....': 1, '...~~.~..': 1})
] 


RESOURCES = [
# test       prob  Terrain:weight pairs
 (T_PLAIN,     10,{5:2,6:2,7:2,8:1,9:1,17:1,18:1}),
 (TA_HILLS,    10,[14,105]),
 (TA_MOUNTAINS,10,{14:2,15:2,33:1,34:1,101:1,102:1}),
 (56,          10,{75:2,79:1}),
 (57,          10,{76:2,80:1}),
 (58,          10,{77:2,81:1}),
 (59,          10,{78:2,82:1})
]


def is_coastal(t):
   return (56<=t<=68 or 75<=t<=82 or 139<=t<=152 
          or 198<=t<=201 or t in [108, 109])

def is_coastal_village(t):
   return 75<=t<=82

def is_land(t):
   return not (t==T_SEA or is_coastal(t))

def is_hill(t):
   return t in TA_HILLS

def is_river(t): #include bridges
   return 40 <= t <= 55 or 170 <= t <= 189 or t == 195

TERRAIN_STR = [
   (T_SEA,              '#'),
   (is_coastal_village, '+'),
   (is_coastal,         'c'),
   (is_river,           '~'),
   (is_hill,            'n'),
   (T_HIGH_MOUNTAIN,    'M'),
   (T_MOUNTAIN,         '^'),
   (T_PLAIN,            '.'),
   (T_FOREST,           'f'),
   (T_ANCIENT_FOREST,   'F'),
   (T_RANDOM,           '?'),
   (T_RANDOM_RARE,      '!'),
   (lambda t: True,     '+')
   ]


def terrain_to_str(t):
   for test, ch in TERRAIN_STR:
      if test_terrain(t,test): 
         return ch
   raise ValueError('Invalid terrain code: ' + repr(t))

def test_terrain(terrain,test):
   if isinstance(test,tuple) or isinstance(test,list):
      return terrain in test
   elif isinstance(test,int):
      return terrain == test
   elif isinstance(test,types.FunctionType):
      return test(terrain)
   else:
      raise ValueError("test_terrain test arg invalid: " + repr(test))

def choose(arg):
   if isinstance(arg,tuple) or isinstance(arg,list):
      return random.choice(arg)
   elif isinstance(arg,dict):
      r = random.randrange(sum(arg.values()))
      for k,v in arg.iteritems():
         if r < v: 
            return choose(k)
         r -= v
   elif isinstance(arg,int):
      return arg
   else:
      raise ValueError("choose: arg invalid: " + repr(arg))

class MapGen(object):
   def __init__(self,width,height):
      self.width = width
      self.height = height
      self.initmap()

   def initmap(self):
      self.map = [[T_SEA for i in range(self.height)] 
                         for j in range(self.width)]

   def itermap(self):
      for x in range(self.width):
         for y in range(self.height):
            yield x,y,self.map[x][y]

   def in_range(self,x,y):
      return 0 <= x < self.width and 0 <= y < self.height
      
   def R(self, x, y, terrain, dist=1, bounded=False):
      cnt = 0
      for i in range(x-dist,x+dist+1):
         for j in range(y-dist,y+dist+1):
            if not self.in_range(i,j):
               if not bounded:
                  cnt += 1
            else:
               if test_terrain(self.map[i][j],terrain):
                  cnt += 1
      return cnt
      
   def seed(self,prob,terr,mask=lambda x,y,t: is_land(t)):
      count = 0
      for x,y,t in self.itermap():
         if mask and not mask(x,y,t): continue
         if random.randrange(100) < prob:
            nt = terr() if isinstance(terr,types.FunctionType) else choose(terr)
            if nt != t:
               self.map[x][y] = nt
               count += 1
      return count
   
   def mask_radius(self,radius):
       cx, cy = self.width/2.0, self.height/2.0
       return lambda x,y,t: is_land(t) and (x-cx)**2+(y-cy)**2 <= radius**2
    
   def mask_border(self,b):
      return lambda x,y,t: b<=x< self.width-b and b<=y<=self.height-b

   def cellular_automata(self,steps,kernel,actions,
                         seed=None,mask=None,name=None):
      if steps == 0: return
      if options.debug and name: print 'Cellular Automata', name
      if seed: 
         self.seed(seed[0],seed[1],mask)
         if options.debug:
            print 'Seed'
            print self
      for step in range(steps):
         nmap = eval(repr(self.map))
         for x,y,t in self.itermap():
            if mask and not mask(x,y,t): continue
            val = sum(map(lambda a: a[2]*self.R(x,y,a[0],a[1]),kernel))
            for r, terrain in actions:
               if val >= r:
                  nmap[x][y] = choose(terrain)
                  break
         self.map = nmap
         if options.debug:
            print 'Step',step+1
            print self

   def flood_fill(self,x,y,target,replace):
      queue = [(x,y)]
      while len(queue):
         x,y = queue.pop()
         if test_terrain(self.map[x][y], target):
            self.map[x][y] = replace
            queue.extend([(x+i,y+j) for i,j in [(-1,0),(0,1),(1,0),(0,-1)]
                          if self.in_range(x+i,y+j)])
         
   def is_contiguous(self,terr):
      T_PLACEHOLDER = -1
      for x,y,t in self.itermap():
         if test_terrain(t,terr):
            self.flood_fill(x,y,terr,T_PLACEHOLDER)
            break
      ret = 0 == [t for _,_,t in self.itermap()].count(terr)
      self.seed(100,terr,lambda x,y,t: t == T_PLACEHOLDER)
      return ret


   def shape_land(self,prob,border,repeat=1,r=5):
      it = 0
      while True:
         it += 1
         if options.verbose:
            print "Shaping land iteration", it
         self.initmap()
         self.cellular_automata( 
            name = 'Land',
            seed = (prob,T_PLAIN),
            mask = self.mask_border(border),
            steps = repeat,
            kernel = [(T_SEA,1,1)],
            actions = [(r,T_SEA), (0,T_PLAIN)]
            )

         # ensure all land contiguous
         if not (options.big_islands or self.is_contiguous(T_PLAIN)):
            continue

         # ensure no inland seas
         if not options.inland_seas:
            for x,y,t in self.itermap():
               if test_terrain(t,T_SEA):
                  self.flood_fill(x,y,T_SEA,-1)
                  break
            self.seed(100,T_PLAIN,lambda x,y,t: t == T_SEA)
            self.seed(100,T_SEA,lambda x,y,t: t == -1)
         break

   def clear_land(self,mask=None):
      if mask is None:
         self.seed(100,T_PLAIN)
      else:
         self.seed(100,T_PLAIN,mask=mask)
        
   def raise_mountains(self,repeat=3,prob=40):
      if repeat == 0: return
      self.cellular_automata( **{
         'steps': repeat,
         'mask': lambda x,y,t: is_land(t),
         'seed': (prob,{TA_HILLS:3,T_MOUNTAIN:1}),
         'kernel': [(TA_HILLS,1,1),
                    (T_MOUNTAIN,1,1),
                    (T_HIGH_MOUNTAIN,1,2)],
         'actions': [(options.highmountr,{T_MOUNTAIN:3,T_HIGH_MOUNTAIN:1}),
                     (options.hillr,TA_HILLS),
                     (0,T_PLAIN)]
         })
      self.seed(5,TA_HILLS,lambda x,y,t: t == T_PLAIN)

   def plant_forests(self,repeat=2,prob=43):
      if repeat == 0: return
      self.cellular_automata( **{
         'steps': repeat,
         'mask': lambda x,y,t: t in [T_PLAIN,T_FOREST,T_ANCIENT_FOREST],
         'seed': (prob,T_FOREST),
         'kernel': [(TA_FORESTS,1,1)],
         'actions': [(9,TA_FORESTS),
                     (7,{T_FOREST:4,T_ANCIENT_FOREST:1}),
                     (5,T_FOREST),
                     (0,T_PLAIN)]
         })
      self.seed(5,T_FOREST,lambda x,y,t: t == T_PLAIN)

   def basic_terrain(self):
      self.cellular_automata( 
            name = 'Mountains',
            steps = options.hillsteps,
            mask = lambda x,y,t: is_land(t),
            seed = (options.hillprob,T_MOUNTAIN),
            kernel = [(TA_MOUNTAINS,1,1)],
            actions = [(options.highmountr,T_HIGH_MOUNTAIN),
                       (options.hillr,T_MOUNTAIN), (0,T_PLAIN)] )
      self.cellular_automata(
            name = 'Forests',
            steps = options.treesteps,
            mask = lambda x,y,t: t in [T_PLAIN,T_FOREST],
            seed = (options.treeprob,T_FOREST),
            kernel = [(T_FOREST,1,1)],
            actions = [(options.treer,T_FOREST), (0,T_PLAIN)] )

   def place_resources(self,prob=10):
      for x,y,t in self.itermap():
         for test, prob, choices in RESOURCES:
            if test_terrain(t,test) and random.randrange(100) < prob:
               self.map[x][y] = choose(choices)

   def mark_coastline(self):
      #Ensure every sea terrain bordering land is converted to coastline
      for x,y,t in self.itermap():
         if t == T_SEA and self.R(x,y,T_PLAIN,bounded=True) >= 1:
            self.map[x][y] = T_COAST

   def sanitize_coastline(self,max_iterations=10):
      """
      Ensure we have selects for all coastlines marked on this map.
      If not, replace bad squares with appropriate land terrain.
      """
      iteration = 1
      while iteration < max_iterations:
         self.mark_coastline()
         bad_coasts = 0
         for x,y,t in self.itermap():
            if not is_coastal(t): continue
            c = self._select_coast(x,y)
            if c is None:
               self.map[x][y] = T_PLAIN
               bad_coasts += 1
         if bad_coasts > 0:
            if options.verbose:
               print "Reshaping {0} coast.".format(bad_coasts)
         else:
            break
      
   def create_coastline(self):
      self.sanitize_coastline()
      for x,y,t in self.itermap():
         if not is_coastal(t): continue
         t = self._select_coast(x,y)
         if t is not None:
            self.map[x][y] = choose(t)
         else:
            rng = [(x+i,y+j) for j in range(-1,2) for i in range(-1,2)]
            print 'Warning - missing tile for coast:', ''.join(
               map(lambda n: terrain_to_str(self.map[n[0]][n[1]]),rng))
            
   def _select_coast(self,x,y):
      rng = [(x+i,y+j) for j in range(-1,2) for i in range(-1,2)]
      for t, neighbors in COASTS:
         if all(map( lambda x,y,n: not self.in_range(x,y) or
                        terrain_to_str(self.map[x][y]) in n, 
            [i[0] for i in rng], [i[1] for i in rng], neighbors)):
            return t
      return None 

   def clear_coast(self):
      #Convert all coastline to sea
      for x,y,t in self.itermap():
         if is_coastal(t):
            self.map[x][y] = T_SEA

   def to_coem(self,filename="map.coem"):
      f = open(filename,'w')
      f.write("# Created by MapGen.py v{0}\n".format(options.version))
      f.write("\n#options {0}\n".format(options))
      for y in range(self.height):
         f.write("\n#  ")
         for x in range(self.width):
            f.write(terrain_to_str(self.map[x][y]))

      f.write("\nmapsize {0} {1}\n".format(self.width,self.height))
      for y in range(self.height):
         f.write("terrainrow {0} ".format(y))
         for x in range(self.width):
            f.write("{0},".format(self.map[x][y]))
         f.write("\n")

      if options.basic:
         f.write("addfancyterrain\n")
      f.close()

   @staticmethod
   def from_coem(filename):
      rows = {}
      f = open(filename,'r')
      for line in f.readlines():
         line = line.rstrip()
         if line.startswith("mapsize"):
            toks = line.split(" ")
            m = MapGen(int(toks[1]), int(toks[2]))
         elif line.startswith("terrainrow"):
            toks = line.split(" ")
            idx = int(toks[1])
            if toks[2][-1] == ',':
               toks[2] = toks[2][:-1]
            rows[idx] = map(int,toks[2].split(","))
      m.map = [[ rows[y][x] for y in range(m.height)] for x in range(m.width)] 
      f.close()
      return m
         
   def __str__(self):
      transposed = [[self.map[x][y] for x in range(self.width)] 
                     for y in range(self.height)]
      return '\n'.join(map(lambda n: ''.join(map(terrain_to_str,n)),transposed))

def scan_terrains(files, clear_mask, test):
   hist = {}
   for f in files: 
      print f
      m = MapGen.from_coem(f)
      m.clear_land(clear_mask)
      print m
      for x,y,terr in m.itermap():
         if test(terr):
            key = ''.join([ ''.join([ terrain_to_str(m.map[x+i][y+j]) 
                  for i in range(-1,2)]) for j in range(-1,2)])
            z = hist.get(key,{})
            z[terr] = 1 + z.get(terr,0)
            hist[key] = z 
   tiles = {}
   for k, v in hist.iteritems():
      for t in v.keys():
         z = tiles.get(t,{})
         z[k] = v[t]
         tiles[t] = z
   res = {}
   for t,v in tiles.iteritems():
      re = [ ''.join(list(set([k[i] for k in v.keys()]))) for i in range(9) ]
      res[t] = re 
   return hist, tiles, res

def print_scan(hist, tiles, res):
   print 'Hist:'
   for k in hist: print k, hist[k] 
   print 'Tiles:'
   for k in tiles: print k, tiles[k]
   print 'Res:'
   for k  in res: print k, res[k]

def scan_coast_frequencies(files):
   return scan_terrains(files, lambda x,y,t: is_land(t), is_coastal)

def scan_river_frequences(files):
   return scan_terrains(files, lambda x,y,t: is_land(t) and not is_river(t),
         is_river)

default_options = {
   'version':'0.2',
   'verbose':True, 
   'basic':False,
   'debug':False,
   'mode':'GEN',
   'mapwidth':50,
   'mapheight':36,
   'filename':'map.coem',
   'border':2,
   'big_islands':True,
   'inland_seas':True,
   'landprob':55,
   'landsteps':5,
   'landr':5,
   'coast':True,
   'hillsteps':2,
   'hillprob':33,
   'hillr':4,
   'highmountr':8,
   'treesteps':1,
   'treeprob':38,
   'treer':4,
   'resprob':8,
   'randomprob':5,
   'randomradius':50,
   'rareprob':1,
   'rareradius':20,
   }
options = Values(default_options)

def mapgen(args=[]):
   if options.mode == "SCAN":
      key = args[0].lower()
      files = args[1:]
      if key.startswith('coast'):
         print_scan(*scan_coast_frequencies(files))
      elif key.startswith('river'):
         print_scan(* scan_river_frequences(files))
      else: 
         print 'Usage: -m SCAN (coast|river) <map files>'
      return
   elif options.mode == "SHOW":
      m = MapGen.from_coem(options.filename)
   elif options.mode == "GEN":
      m = MapGen(options.mapwidth,options.mapheight)
      m.shape_land(prob=options.landprob,border=options.border,
                   repeat=options.landsteps,r=options.landr)
      if options.coast:
         m.create_coastline()
      else:
         m.clear_coast()
      m.clear_land()
      if options.basic:
         m.basic_terrain()
      else:
         m.raise_mountains(repeat=options.hillsteps,prob=options.hillprob)
         m.plant_forests(repeat=options.treesteps,prob=options.treeprob)
         m.place_resources(prob=options.resprob)
         m.seed(options.randomprob,T_RANDOM,
               mask=m.mask_radius(options.randomradius))
         m.seed(options.rareprob,T_RANDOM_RARE,
               mask=m.mask_radius(options.rareradius))
      m.to_coem(options.filename)
   if options.verbose:
      print 'Map:', options.filename
      print m

def mapgen_main():
   from optparse import OptionParser, OptionGroup
   description='''Conquest of Elysium 3 random map generator.
Default values for options given in parentheses.'''

   global options
   parser = OptionParser(description=description, version=options.version)
   parser.set_defaults(**default_options)
   parser.add_option("-q","--quiet",action="store_false",dest="verbose")
   parser.add_option("--debug",action="store_true",dest="debug",
         help="Really verbose output")
   parser.add_option("-x","--mapw", type="int", dest="mapwidth",  
                        metavar="WIDTH", help="Map width in squares (50)")
   parser.add_option("-y","--maph", type="int", dest="mapheight",  
                        metavar="HEIGHT", help="Map height in squares (36)")
   parser.add_option("-f","--file", dest="filename", metavar="FILE", 
                        help="Filename of map (map.coem)")
   parser.add_option("-m","--mode",dest="mode",help="SHOW,GEN (GEN)")

   group = OptionGroup(parser, "Generation (GEN) mode parameters")
   group.add_option("--border", type="int", dest="border",  metavar="INT",
                        help="Sea border width (2)."
                             "  Set to 0 for all land map")
   group.add_option("--land-prob", type="int",dest="landprob", metavar="PROB",
                        help="Probability for seeding land vs sea. (55)")
   group.add_option("--land-steps", type="int", dest="landsteps", default=5,
                        metavar="STEPS",
                        help="Number of generations to shape land (5)")
   group.add_option("--land-r", type="int", dest="landr", default=5,
                        metavar="INT",
                        help="R value for shaping land (5)")
   group.add_option("--coast", action="store_true",dest="coast",
                        default=True)
   group.add_option("--no-coast", action="store_false",dest="coast")
   group.add_option("--hill-steps", type="int", dest="hillsteps", 
                        metavar="STEPS",
                        help="Number of generations to shape hills (3)")
   group.add_option("--hill-prob", type="int",dest="hillprob", metavar="PROB",
                        help="Probability for seeding hills/mtn on land (38)")
   group.add_option("--high-mount-r",type="int",dest="highmountr",
                        help="R value for high mountain (9)")
   group.add_option("--tree-steps", type="int", dest="treesteps", 
                        metavar="STEPS",
                        help="Number of generations to shape forests (2)")
   group.add_option("--tree-prob", type="int",dest="treeprob", metavar="PROB",
                        help="Probability for seeding forests on land (50)")
   group.add_option("--resource-prob", type="int", dest="resprob", 
                        metavar="PROB",
                        help="Probability for creating cities/mines/etc. (8)")
   group.add_option("--random-prob", type="int", dest="randomprob", 
                        metavar="PROB",
                        help="Probability of placing random tile on land. (5)")
   group.add_option("--random-radius", type="int", dest="randomradius", 
                  metavar="INT",
                  help="Radius from center of map to seed random tiles. (50)")
   group.add_option("--rare-prob", type="int", dest="rareprob", metavar="PROB",
                  help="Probability of placing random rare tile on land. (1)")
   group.add_option("--rare-radius", type="int" ,dest="rareradius", 
               metavar="INT",
               help="Radius from center of map to seed random rare tiles. (20)")
   group.add_option("--basic",action="store_true",dest="basic",
               help="Add mountains and forests, and set addfancyterrain in map")
   group.add_option("--no-inland-seas",action="store_false",dest="inland_seas")
   group.add_option("--big-islands",action="store_true",dest="big_islands")


   parser.add_option_group(group)
   (options, args) = parser.parse_args()
   mapgen(args)
   
if __name__ == "__main__":
#   m = MapGen.from_coem('maps/tmap2.coem')
#   print m

#   import sys
#   hist, tiles, res = scan_coasts(sys.argv[3:])
   mapgen_main()
