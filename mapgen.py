#!/usr/bin/env python
import types
import random

T_PLAIN = 0
T_SEA = 69
T_COAST = 65 
T_MOUNTAIN = 12 
T_HIGH_MOUNTAIN = 71

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
   return t in [73,74]

def terrain_to_str(t):
   if t == T_SEA:
      return '#'
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
   else:
      return '+'

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

   def seed_land(self,prob,terr):
      for x,y,t in self.itermap():
         if is_land(t) and random.randrange(100) < prob:
            if isinstance(terr,types.FunctionType):
               self.map[x][y] = terr()
            elif isinstance(terr,int):
               self.map[x][y] = terr
    
   def raise_mountains(self,repeat=3,prob=40):
      self.clear_land()
      self.seed_land(prob,lambda: random.choice([73,74,12]))
      for r in range(repeat):
         nmap = eval(repr(self.map))
         for x,y,t in self.itermap():
            if not is_land(t):
               continue
            val = self.R(x,y,[73,74]) + self.R(x,y,12) + 2*self.R(x,y,71)
            if val >= 7:
               nmap[x][y] = random.choice([12,12,12,71])
            elif val >= 4:
               nmap[x][y] = random.choice([73,74])
            else:
               nmap[x][y] = T_PLAIN
         self.map = nmap
      for x,y,t in self.itermap():
         if t == T_PLAIN and random.randrange(100) < 5:
            self.map[x][y] = random.choice([73,74])
         
   def place_resources(self,prob=10):
      for x,y,t in self.itermap():
         if random.randrange(100) >= prob:
            continue
         if t == T_PLAIN:
            nt = random.choice([5,5,6,6,7,7,8,9,17,18])
         elif t in [73,74]:
            nt = random.choice([14,105])
         elif t in [12,71]:
            nt = random.choice([14,14,15,33,34,101,102])
         elif t == 56:
            nt = random.choice([75,75,79])
         elif t == 57:
            nt = random.choice([76,76,80])
         elif t == 58:
            nt = random.choice([77,77,81])
         elif t == 59:
            nt = random.choice([78,78,82])
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

   def generate(self, filename ):
      self.seed(prob=kwargs["seedprob"],sea=kwargs["border"])
      self.carve(repeat=5)
      self.mark_coast()
      self.create_coastline()
      self.raise_mountains()
      self.place_resources()
      self.to_coem(kwargs["filename"])

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
   parser.add_option("--file", dest="filename", metavar="FILE", 
                        default="map.coem", 
                        help="Filename of map (map.coem)")
   parser.add_option("-m","--mode",dest="mode",help="SHOW,GEN (GEN)")

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
   group.add_option("--resource-prob", type="int", dest="resprob", default=10,
                        metavar="PROB",
                        help="Probability for creating cities/mines/etc. (10)")
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
      m.raise_mountains(repeat=options.hillsteps,prob=options.hillprob)
      m.place_resources(prob=options.resprob)
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
