import sys; sys.path.insert(0,'.')
import render,cfg
from PIL import Image
ts=[float(x) for x in sys.argv[2:]]
fr=[render.frame(t).resize((360,640)) for t in ts]
sh=Image.new('RGB',(360*len(fr),640))
for i,f in enumerate(fr): sh.paste(f,(360*i,0))
sh.save(sys.argv[1])
