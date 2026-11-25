import sys; sys.path.insert(0,'.')
from render import *
img=BG.copy(); topbar(img,0)
place(img,TL('BALANCED PRICE RANGE',50,GRY),540,255)
place(img,TL('BPR',200,INK),540,385)
place(img,TL('2 FVG, 1 zone',100,OR,'s'),540,520)
rows=[('1','BEARISH FVG','neeche'),('2','BULLISH FVG','upar'),('3','OVERLAP','= entry')]
for n,(num,a,b) in enumerate(rows):
    y=750+n*185
    place(img,icon('rr',880,160,44,WH,SOFT,3),540,y)
    place(img,icon('circ',100,OR),200,y); place(img,TL(num,72,CREAM,'a'),200,y-3)
    ta=TL(a,52,INK); place(img,ta,280+ta.width/2,y)
    tb=TL(b,46,OR,'s'); place(img,tb,945-tb.width/2,y+4)
place(img,TL('COMMENT: BPR',52,INK),660,1430)
place(img,icon('rr',520,110,55,INK),660,1560); place(img,TL('@chartbendfx',48,CREAM),660,1560)
p,m,x=pose_at(0.1); ks=0.40
sp=kid_sprite(0.15,p); sp=sp.resize((int(sp.width*ks),int(sp.height*ks)),Image.LANCZOS)
img.alpha_composite(sp,(55,1862-int(530*2*ks)))
img.convert('RGB').save('cover24.jpg',quality=92)
