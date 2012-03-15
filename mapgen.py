#!/usr/bin/env python
import types
import random

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

TA_FORESTS = [2,4]
TA_MOUNTAINS = [12,71]
TA_HILLS = [73,74]
COASTS = [
 (56, ['c.', 'c', '#c', '.', 'c', '#c', 'c.', 'c', 'c#']),
 (57, ['c#', 'c', 'c.', '#c', 'c', '.', 'c#', 'c', 'c.']),
 (58, ['c.', '.', 'c.', 'c', 'c', 'c', 'c#', '#c', 'c#']),
 (59, ['c#', 'c#', 'c#', 'c', 'c', 'c', 'c.', '.', 'c.']),
 (60, ['c.', '.', 'c.', '.', 'c', 'c', 'c.', 'c', '#c']),
 (61, ['c.', '.', 'c.', 'c', 'c', '.', 'c#', 'c', 'c.']),
 (62, ['c.', 'c', 'c#', '.', 'c', 'c', 'c.', '.', 'c.']),
 (63, ['c#', 'c', 'c.', 'c', 'c', '.', 'c.', '.', 'c.']),
 (64, ['.', 'c', '#c', 'c', 'c', 'c#', 'c#', 'c#', 'c#']),
# (65, ['c.', '.', 'c.', 'c.', 'c', 'c.', 'c#', 'c#', 'c#']),
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
 (144, ['c#', '#', '#c', 'c', 'c', 'c', '.', 'c', '.']),
 (145, ['.', 'c', 'c#', 'c', 'c', 'c#', '.', 'c', 'c#']),
 (146, ['c#', 'c', '.', 'c#', 'c', 'c', '#c', 'c', '.']),
 (147, ['.', 'c', 'c#', 'c', 'c', 'c', 'c#', 'c', '.']),
 (148, ['c#', 'c', '.', 'c', 'c', 'c', '.', 'c', 'c#']),
 (149, ['c.', 'c', '.', '.', 'c', 'c', 'c.', 'c', '#c']),
 (150, ['c.', 'c', '#c', '.', 'c', 'c', '.', 'c', '.']),
 (151, ['.', 'c', '.', 'c', 'c', '.', '#c', 'c', 'c.']),
 (152, ['#c', 'c', 'c.', 'c', 'c', '.', '.', 'c', 'c.'])
] 


def is_coastal(t):
   return (56<=t<=68 or 75<=t<=82 or 139<=t<=152 
          or 198<=t<=201 or t in [108, 109])

def is_land(t):
   return not (t==T_SEA or is_coastal(t))

def is_hill(t):
   return t in TA_HILLS

def terrain_to_str(t):
   if t == T_SEA:
      return '#'
   elif 75<=t<=82: #show coastal villages and ports as '+'
      return '+'
   elif is_coastal(t):
      return 'c'
   elif is_hill(t):
      return 'n'
   elif t == T_MOUNTAIN:
      return '^'
   elif t == T_HIGH_MOUNTAIN:
      return 'M'
   elif t == T_PLAIN:
      return '.'
   elif t == T_FOREST:
      return 'f'
   elif t == T_ANCIENT_FOREST:
      return 'F'
   elif t == T_RANDOM:
      return '?'
   elif t == T_RANDOM_RARE:
      return '!'
   else:
      return '+'

def choose(arg):
   if isinstance(arg,list):
      return random.choice(arg)
   elif isinstance(arg,dict):
      r = random.randrange(sum(arg.values()))
      for k,v in arg.iteritems():
         if r < v:
            return k
         r -= v
   else:
      raise ValueError("only list and dict are supported.")

class MapGen(object):
   def __init__(self,width,height):
      self.width = width
      self.height = height
      self.map = [[T_SEA for i in range(height)] for j in range(width)]

   def seed(self, prob=45, sea=2):
      for x,y,_ in self.itermap():
          self.map[x][y] = T_SEA if (random.randrange(100) < prob
                or x < sea or x >= self.width-sea or y < sea or 
                y >= self.height-sea) else T_PLAIN


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
               if isinstance(terrain,list) and self.map[i][j] in terrain:
                  cnt += 1
               if isinstance(terrain,int) and self.map[i][j] == terrain:
                  cnt += 1
      return cnt
      
   def carve(self,repeat=1,r=5):
      for i in range(repeat):
         self.map = [[ T_SEA if self.R(x,y,T_SEA) >= r else T_PLAIN
                    for y in range(self.height)] for x in range(self.width)]

   def clear_land(self):
      for x,y,t in self.itermap():
         if is_land(t):
            self.map[x][y] = T_PLAIN

   def seed_land(self,prob,terr,radius=None):
      if radius is None:
         radius = max(self.width,self.height)
      if prob < 1 or radius < 1:
         return
      print prob,terr
      cx = self.width/2.0
      cy = self.height/2.0
      for x,y,t in self.itermap():
         if radius**2 < (x-cx)**2+(y-cy)**2:
            continue
         if is_land(t) and random.randrange(100) < prob:
            if isinstance(terr,types.FunctionType):
               self.map[x][y] = terr()
            elif isinstance(terr,int):
               self.map[x][y] = terr
            else:
               raise ValueError("")
    
   def raise_mountains(self,repeat=3,prob=40):
      if repeat > 0:
         self.seed_land(prob,lambda: choose(TA_HILLS + [T_MOUNTAIN]))
         print self
      for r in range(repeat):
         nmap = eval(repr(self.map))
         for x,y,t in self.itermap():
            if not is_land(t):
               continue
            val = (self.R(x,y,TA_HILLS) + self.R(x,y,T_MOUNTAIN) + 
                  2*self.R(x,y,T_HIGH_MOUNTAIN))
            if val >= 7:
               nmap[x][y] = choose({T_MOUNTAIN:3,T_HIGH_MOUNTAIN:1})
            elif val >= 4:
               nmap[x][y] = choose(TA_HILLS)
            else:
               nmap[x][y] = T_PLAIN
         self.map = nmap
      for x,y,t in self.itermap():
         if t == T_PLAIN and random.randrange(100) < 5:
            self.map[x][y] = choose(TA_HILLS)

   def plant_forests(self,repeat=2,prob=43):
      if repeat > 0:
         self.seed_land(prob, T_FOREST)
      for r in range(repeat):
         nmap = eval(repr(self.map))
         for x,y,t in self.itermap():
            if not is_land(t):
               continue
            val = self.R(x,y,TA_FORESTS)
            if val == 9:
               nmap[x][y] = choose(TA_FORESTS)
            elif val >= 7:
               nmap[x][y] = choose({T_FOREST:4,T_ANCIENT_FOREST:1})
            elif val >= 5:
               nmap[x][y] = T_FOREST
            elif t == T_FOREST:
               nmap[x][y] = T_PLAIN
         self.map = nmap
      for x,y,t in self.itermap():
         if t == T_PLAIN and random.randrange(100) < 5:
            self.map[x][y] = T_FOREST

   def place_resources(self,prob=10):
      for x,y,t in self.itermap():
         if random.randrange(100) >= prob:
            continue
         if t == T_PLAIN:
            nt = choose({5:2,6:2,7:2,8:1,9:1,17:1,18:1})
         elif t in TA_HILLS:
            nt = choose([14,105])
         elif t in TA_MOUNTAINS:
            nt = choose({14:2,15:2,33:1,34:1,101:1,102:1})
         elif t == 56:
            nt = choose({75:2,79:1})
         elif t == 57:
            nt = choose({76:2,80:1})
         elif t == 58:
            nt = choose({77:2,81:1})
         elif t == 59:
            nt = choose({78:2,82:1})
         else:
            nt = t
         self.map[x][y] = nt

   def create_coastline(self):
      #Ensure every sea terrain bordering land is converted to coastline
      for x,y,t in self.itermap():
         if t == T_SEA and self.R(x,y,T_PLAIN,bounded=True) >= 1:
            self.map[x][y] = T_COAST

      for map_x,map_y,map_t in self.itermap():
         if not is_coastal(map_t):
            continue
         rng = [(map_x+j,map_y+i) for i in range(-1,2) for j in range(-1,2)]
         for t, neighbors in COASTS:
            if all(map( lambda x,y,n: not self.in_range(x,y) or
                           terrain_to_str(self.map[x][y]) in n, 
               [i[0] for i in rng], [i[1] for i in rng], neighbors)):
               self.map[map_x][map_y] = t
               break

   def clear_coast(self):
      #Convert all coastline to sea
      for x,y,t in self.itermap():
         if is_coastal(t):
            self.map[x][y] = T_SEA

   def to_coem(self,filename="map.coem"):
      f = open(filename,'w')
      f.write("mapsize {0} {1}\n".format(self.width,self.height))
      for y in range(self.height):
         f.write("terrainrow {0} ".format(y))
         for x in range(self.width):
            f.write("{0},".format(self.map[x][y]))
         f.write("\n")
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

def scan_coast_frequencies(files):
   hist = {}
   for f in files: 
      print f
      m = MapGen.from_coem(f)
      print m
      for x,y,terr in m.itermap():
         if is_coastal(terr):
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

def run_main():
   from optparse import OptionParser, OptionGroup
   
   description='''Conquest of Elysium 3 random map generator.
Default values for options given in parentheses.'''

   parser = OptionParser(description=description, version="0.1")
   parser.add_option("-q","--quiet",action="store_false",dest="verbose",
                        default=True)
   parser.add_option("--mapw", type="int", dest="mapwidth", default=50, 
                        metavar="WIDTH",
                        help="Map width in squares (50)")
   parser.add_option("--maph", type="int", dest="mapheight", default=36, 
                        metavar="HEIGHT",
                        help="Map height in squares (36)")
   parser.add_option("-f","--file", dest="filename", metavar="FILE", 
                        default="map.coem", 
                        help="Filename of map (map.coem)")
   parser.add_option("-m","--mode",dest="mode",help="SHOW,GEN (GEN)",
                     default="GEN")

   group = OptionGroup(parser, "Generation (GEN) mode parameters")
   group.add_option("--border", type="int", dest="border", default=2, 
                        metavar="INT",
                        help="Sea border width (2)."
                             "  Set to 0 for all land map")
   group.add_option("--sea-prob", type="int",dest="seaprob", default=45,
                        metavar="PROB",
                        help="Probability for seeding land vs sea. (45)")
   group.add_option("--carve-steps", type="int", dest="carvesteps", default=5,
                        metavar="STEPS",
                        help="Number of generations to shape land (5)")
   group.add_option("--carve-r", type="int", dest="carver", default=5,
                        metavar="INT",
                        help="R value for carve (5)")
   group.add_option("--coast", action="store_true",dest="coast",
                        default=True)
   group.add_option("--no-coast", action="store_false",dest="coast")
   group.add_option("--hill-steps", type="int", dest="hillsteps", default=3,
                        metavar="STEPS",
                        help="Number of generations to shape hills (3)")
   group.add_option("--hill-prob", type="int",dest="hillprob",default=40,
                        metavar="PROB",
                        help="Probability for seeding hills/mtn on land (40)")
   group.add_option("--tree-steps", type="int", dest="treesteps", default=2,
                        metavar="STEPS",
                        help="Number of generations to shape forests (2)")
   group.add_option("--tree-prob", type="int",dest="treeprob",default=43,
                        metavar="PROB",
                        help="Probability for seeding forests on land (43)")
   group.add_option("--resource-prob", type="int", dest="resprob", default=10,
                        metavar="PROB",
                        help="Probability for creating cities/mines/etc. (10)")
   group.add_option("--random-prob", type="int", dest="randomprob", default=5,
                        metavar="PROB",
                        help="Probability of placing random tile on land. (5)")
   group.add_option("--random-radius", type="int", dest="randomradius", 
                  default=20, metavar="INT",
                  help="Radius from center of map to seed random tiles. (20)")
   group.add_option("--rare-prob", type="int", dest="rareprob", default=5,
                  metavar="PROB",
                  help="Probability of placing random rare tile on land. (5)")
   group.add_option("--rare-radius", type="int" ,dest="rareradius", 
               default=20, metavar="INT",
               help="Radius from center of map to seed random rare tiles. (20)")
   parser.add_option_group(group)
   (options, args) = parser.parse_args()

   if options.mode == "SHOW":
      m = MapGen.from_coem(options.filename)
   elif options.mode == "GEN":
      m = MapGen(options.mapwidth,options.mapheight)
      m.seed(prob=options.seaprob,sea=options.border)
      m.carve(repeat=options.carvesteps,r=options.carver)
      if options.coast:
         m.create_coastline()
      else:
         m.clear_coast()
      m.clear_land()
      m.raise_mountains(repeat=options.hillsteps,prob=options.hillprob)
      m.plant_forests(repeat=options.treesteps,prob=options.treeprob)
      m.place_resources(prob=options.resprob)
      m.seed_land(options.randomprob,T_RANDOM,options.randomradius)
      m.seed_land(options.rareprob,T_RANDOM_RARE,options.rareradius)
      m.to_coem(options.filename)
   if options.verbose:
      print 'Map:', options.filename
      print m
if __name__ == "__main__":
#   m = MapGen.from_coem('maps/tmap2.coem')
#   print m

#   import sys
#   hist, tiles, res = scan_coasts(sys.argv[3:])
   run_main()
