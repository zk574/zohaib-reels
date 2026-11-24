import random
BLUE=(70,130,190)
def tx(img,t,i,s,size,cx,cy,fill=INK,kind='m',rot=0,sc=1):
    p=P(t,i)
    if p<=0: return
    place(img,TL(s,size,fill,kind),cx,cy,p*sc,min(1,p*2),rot)
def ic(img,t,i,lay,cx,cy,sc=1,rot=0,dy=0):
    p=P(t,i)
    if p<=0: return
    place(img,lay,cx,cy+dy,p*sc,min(1,p*2),rot)
def wob(t,f=1.5,a=8): return math.sin(2*math.pi*f*t)*a
def hd(img,t,i1,s1,i2,s2):
    tx(img,t,i1,s1,84,540,225)
    tx(img,t,i2,s2,100,540,335,OR,'s')
def mk(closes,o0,seed,wick=(0.5,1.6)):
    r=random.Random(seed);out=[];o=o0
    for c in closes:
        out.append([o,max(o,c)+r.uniform(*wick),min(o,c)-r.uniform(*wick),c]);o=c
    return out
CX,CY,CW,CH=540,700,940,640
def kp(t,pts):
    if t<=pts[0][0]: return pts[0][1]
    for (a,x),(b,y) in zip(pts,pts[1:]):
        if t<=b: return x+(y-x)*(t-a)/(b-a)
    return pts[-1][1]
class Ch: pass
def chart(img,t,series,nvis,lo,hi,tf):
    x0,y0=CX-CW//2,CY-CH//2
    card=icon('rr',CW,CH,40,WH,SOFT,3); img.alpha_composite(card,(x0,y0))
    d=ImageDraw.Draw(img)
    d.ellipse([x0+34,y0+30,x0+48,y0+44],fill=OR)
    d.text((x0+64,y0+22),'XAUUSD  ·  '+tf,font=F('m',28),fill=GRY)
    d.line([(x0,y0+78),(x0+CW,y0+78)],fill=SOFT,width=2)
    px0,px1=x0+40,x0+CW-90; py0,py1=y0+110,y0+CH-40
    N=len(series); cw=(px1-px0)/N
    for g in range(5):
        yy=py0+(py1-py0)*g/4; d.line([(px0,yy),(px1,yy)],fill=(240,233,222),width=2)
    ch=Ch(); ch.X=lambda i:px0+(i+0.5)*cw; ch.Y=lambda p:py1-(p-lo)/(hi-lo)*(py1-py0); ch.cw=cw; ch.box=(px0,py0,px1,py1)
    ch.d=d
    for i,(o,h,l,c) in enumerate(series):
        v=min(1,max(0,nvis-i))
        if v<=0: continue
        cc=o+(c-o)*v; hh=o+(h-o)*v if h>o else h; ll=l
        hh=max(max(o,cc),o+(h-o)*v); ll=min(min(o,cc),o-(o-l)*v)
        col=GRN if cc>=o else RED
        x=ch.X(i); d.line([(x,ch.Y(hh)),(x,ch.Y(ll))],fill=col,width=4)
        d.rounded_rectangle([x-cw*.28,ch.Y(max(o,cc)),x+cw*.28,max(ch.Y(min(o,cc)),ch.Y(max(o,cc))+4)],4,fill=col)
    return ch
def zone(img,x1,x2,y1,y2,rgba):
    if x2<=x1 or y2<=y1: return
    tmp=Image.new('RGBA',img.size,(0,0,0,0)); ImageDraw.Draw(tmp).rectangle([x1,y1,x2,y2],fill=rgba); img.alpha_composite(tmp)
def hline(img,y,x1,x2,col,w=4,dash=14):
    d=ImageDraw.Draw(img); x=x1
    while x<x2:
        d.line([(x,y),(min(x+dash,x2),y)],fill=col,width=w); x+=dash*1.8
def tag(img,t,i,s,cx,cy,fill,txtc=WH,size=34,w=None):
    p=P(t,i,0.35)
    if p<=0: return
    tl=TL(s,size,txtc); bw=tl.width+44
    place(img,icon('rr',bw,size+30,(size+30)//2,fill),cx,cy,p,min(1,p*2))
    place(img,tl,cx,cy,p,min(1,p*2))
def arrow(img,x,y,up,col,L=90,w=14):
    d=ImageDraw.Draw(img); s=-1 if up else 1
    d.line([(x,y),(x,y+s*L)],fill=col,width=w); 
    d.polygon([(x-30,y+s*L),(x+30,y+s*L),(x,y+s*(L+44))],fill=col)
# --- scenes ---
def mk_heart(s,col):
    def f(d,k):
        r=s*k*0.27
        c=s*k*.5; y0=s*k*.14
        d.ellipse([c-1.85*r,y0,c+0.15*r,y0+2*r],fill=col)
        d.ellipse([c-0.15*r,y0,c+1.85*r,y0+2*r],fill=col)
        d.polygon([(c-1.8*r,y0+1.25*r),(c+1.8*r,y0+1.25*r),(c,s*k*.9)],fill=col)
        d.rectangle([c-0.5*r,y0+0.6*r,c+0.5*r,y0+1.4*r],fill=col)
    return SS(s,s,f)
def xmark(img,cx,cy,s,p=1,col=RED):
    if p<=0: return
    place(img,SS(s,s,lambda d,k:(d.line([(s*.15*k,s*.15*k),(s*.85*k,s*.85*k)],fill=col,width=int(s*.13*k)),d.line([(s*.85*k,s*.15*k),(s*.15*k,s*.85*k)],fill=col,width=int(s*.13*k)))),cx,cy,p,min(1,p*2))
def zig(w,h):
    def f(d,k):
        pts=[(0,.85),(.2,.5),(.35,.65),(.55,.3),(.7,.45),(1,.05)]
        d.line([(x*w*k,y*h*k) for x,y in pts],fill=GRN,width=10*k,joint='curve')
        for x,y in pts[1:-1]: d.ellipse([x*w*k-9*k,y*h*k-9*k,x*w*k+9*k,y*h*k+9*k],fill=INK)
    return SS(w,h,f)
def card(img,t,i,w,h,cx,cy,fill=WH,ol=SOFT):
    p=P(t,i,0.4)
    if p>0: place(img,icon('rr',w,h,40,fill,ol,3),cx,cy,p,min(1,p*2))
    return p
def pill(img,t,i,s,cx,cy,fill,txt=WH,size=50,w=None,rot=0):
    p=P(t,i,0.4)
    if p<=0: return
    tl=TL(s,size,txt); bw=w or tl.width+70; bh=int(size*1.9)
    place(img,icon('rr',bw,bh,bh//2,fill),cx,cy,p,min(1,p*2),rot); place(img,tl,cx,cy,p,min(1,p*2),rot)
# ---------- scenes ----------
TS=mk([54,56,55,58,57,59.5,57,55,56,58,57.5,59,58.4,56,54,52,51,50.5],53,51)
TS[5]=[57,60.0,56.6,59.5]; TS[12]=[59,62.6,58.2,58.4]; TS[11][1]=59.6
OLDH=60.0; WTOP=62.6
def bowl(s):
    def f(d,k):
        d.chord([0,-s*.5*k,s*k-1,s*k-1],0,180,fill=OR); d.rectangle([s*.05*k,s*.22*k,s*.95*k,s*.3*k],fill=(200,95,50))
        for i in range(3):
            x=s*(.3+i*.2)*k; d.arc([x-14*k,s*.0*k,x+14*k,s*.2*k],90,270,fill=GRY,width=4*k)
    return SS(s,int(s*.75),f)
def turtle(s):
    def f(d,k):
        d.ellipse([s*.15*k,s*.25*k,s*.85*k,s*.8*k],fill=GRN); d.ellipse([s*.28*k,s*.36*k,s*.72*k,s*.7*k],outline=(30,110,60),width=6*k)
        d.ellipse([s*.78*k,s*.38*k,s*.98*k,s*.58*k],fill=(120,190,110)); d.ellipse([s*.88*k,s*.44*k,s*.92*k,s*.48*k],fill=INK)
        for x in (.25,.62): d.ellipse([s*x*k,s*.72*k,s*(x+.13)*k,s*.86*k],fill=(120,190,110))
    return SS(s,s,f)
def tchart(img,t,n,cy=None):
    return chart(img,t,TS,n,48,64,'M15')
def wick_draw(img,ch,top):
    X,Y=ch.X,ch.Y; ImageDraw.Draw(img).line([(X(12),Y(59)),(X(12),Y(top))],fill=RED,width=5)
def s1(img,t):
    hd(img,t,0,'Purana high toda,',6,'tumne buy kiya?')
    n=kp(t,[(0,0),(A(3),12),(A(5)+0.3,12.6),(A(16),13),(A(17)+0.3,18)])
    ch=tchart(img,t,n); X,Y=ch.X,ch.Y
    hline(img,Y(OLDH),X(4),ch.box[2],INK,3)
    if t>A(3): place(img,TL('PURANA HIGH',22,INK),ch.box[2]-70,Y(OLDH)+20)
    if t>A(9): tag(img,t,9,'BUY',X(12)+50,Y(WTOP)-10,GRN,WH,26)
    if t>A(16): arrow(img,X(16),Y(53)-30,False,RED,40,10)
def s2(img,t):
    tx(img,t,19,'Mubarak ho!',110,540,300,INK)
    ic(img,t,22,bowl(420),540,690,1,wob(t,1.2,3))
    ic(img,t,22,turtle(220),540,600,1,wob(t,2,6))
    tx(img,t,22,'turtle soup',120,540,950,OR,'s')
    tx(img,t,26,'HAAN, TUM.',90,540,1080,INK)
def s3(img,t):
    tx(img,t,28,'Turtle soup =',90,540,330,INK)
    p=P(t,31,0.45)
    if p>0:
        place(img,icon('rr',760,200,50,RED),540,620,p,min(1,p*2),-3); place(img,TL('FAKE BREAKOUT',80,WH),540,620,p,min(1,p*2),-3)
    ic(img,t,31,turtle(200),540,880,1,wob(t,2,5))
def s4(img,t):
    hd(img,t,33,'Purana high:',43,'sabke stop loss')
    ch=tchart(img,t,12); X,Y=ch.X,ch.Y; bx1=ch.box[2]
    hline(img,Y(OLDH),X(4),bx1,INK,3); tag(img,t,36,'PURANA HIGH',X(3),Y(OLDH)-30,INK,WH,24)
    if t>A(43):
        for k in range(9):
            p=back((t-(A(43)+k*0.06))/0.3)
            if p>0: place(img,icon('circ',22,RED),X(5)+k*42,Y(OLDH+1.1+0.5*(k%2)),p)
        tag(img,t,44,'STOPS',X(8),Y(OLDH+3.2),RED,WH,24)
    if t>A(46): tag(img,t,46,'BREAKOUT ORDERS',X(8),Y(OLDH+4.8),GRN,WH,22)
def s5(img,t):
    hd(img,t,51,'Sirf wick bahar,',67,'close andar')
    n=kp(t,[(0,12),(A(51),12),(A(57),12.6),(A(68),12.6),(A(73)+0.3,13)])
    ch=tchart(img,t,n); X,Y=ch.X,ch.Y; bx1=ch.box[2]
    hline(img,Y(OLDH),X(4),bx1,INK,3)
    if A(57)<t:
        u=ease((t-A(57))/0.6); wick_draw(img,ch,59+(WTOP-59)*u)
        for k in range(9):
            if u<0.5+k*0.05: place(img,icon('circ',22,RED),X(5)+k*42,Y(OLDH+1.1+0.5*(k%2)))
        tag(img,t,58,'WICK',X(12)+60,Y(WTOP),RED,WH,24)
    else:
        for k in range(9): place(img,icon('circ',22,RED),X(5)+k*42,Y(OLDH+1.1+0.5*(k%2)))
    if t>A(64): tag(img,t,64,'ORDERS BHAR GAYE',X(6),Y(OLDH+4.5),INK,WH,22)
    if t>A(72): ring(img,X(12),Y(58.6),40,OR,P(t,73,0.35)); tag(img,t,73,'CLOSE ANDAR',X(9),Y(56.5),OR,WH,22)
    if t>A(79): pill(img,t,79,'BREAKOUT FAIL = SIGNAL',540,1075,RED,WH,42)
def ring(img,cx,cy,r,col,p=1):
    if p<=0: return
    place(img,SS(2*r+8,2*r+8,lambda d,k:d.ellipse([4*k,4*k,(2*r+4)*k,(2*r+4)*k],outline=col,width=6*k)),cx,cy,p)
def s6(img,t):
    hd(img,t,85,'Entry kab?',95,'close andar = sell')
    n=kp(t,[(0,13),(A(95),13),(A(104),15),(A(107)+0.5,18)])
    ch=tchart(img,t,n); X,Y=ch.X,ch.Y; bx1=ch.box[2]
    hline(img,Y(OLDH),X(4),bx1,INK,3); wick_draw(img,ch,WTOP)
    if t>A(95): tag(img,t,96,'SELL',X(13)+40,Y(TS[13][1])-30,RED,WH,26)
    if t>A(97):
        sl=WTOP+0.7; u=ease((t-A(97))/0.4); hline(img,Y(sl),X(10),X(10)+(bx1-X(10))*u,RED,4); tag(img,t,99,'SL WICK KE UPAR',X(8),Y(sl)-28,RED,WH,22)
    if t>A(104):
        tg=50.6; u=ease((t-A(104))/0.4); hline(img,Y(tg),X(3),X(3)+(bx1-X(3))*u,GRN,4); tag(img,t,105,'TARGET: RANGE LOW',X(7),Y(tg)+28,GRN,WH,22)
def candle_ic(img,cx,cy,body_out,p):
    if p<=0: return
    def f(d,k):
        w,h=200,300
        d.line([(w/2*k,10*k),(w/2*k,(h-10)*k)],fill=RED if not body_out else GRN,width=8*k)
        top=40 if body_out else 150
        d.rounded_rectangle([60*k,top*k,140*k,(top+110)*k],10*k,fill=GRN if body_out else RED)
        d.line([(0,110*k),(w*k,110*k)],fill=INK,width=5*k)
    place(img,SS(200,300,f),cx,cy,p,min(1,p*2))
def s7(img,t):
    hd(img,t,110,'Rule',111,'yaad rakho')
    if card(img,t,113,440,520,290,690,WH,GRN)>0:
        candle_ic(img,290,640,True,P(t,113)); place(img,TL('BODY BAHAR',40,INK),290,830,P(t,113)); place(img,TL('= BREAKOUT',44,GRN),290,890,P(t,118))
    if card(img,t,119,440,520,790,690,WH,RED)>0:
        candle_ic(img,790,640,False,P(t,119)); place(img,TL('SIRF WICK',40,INK),790,830,P(t,119)); place(img,TL('= SOUP',50,RED),790,890,P(t,124))
def s8(img,t):
    hd(img,t,125,'Comment mein likho',128,'SOUP')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,125,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,125,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,125,0.45))
    s='SOUP'; a=A(127); b=EN[128]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,80,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
    ic(img,t,128,bowl(260),540,900,1,0)
def s9(img,t):
    ic(img,t,129,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,129,'Follow karo',110,540,640,INK)
    tx(img,t,131,'kal milte hain',130,540,800,OR,'s')
    if t>A(130):
        p=P(t,130,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(19,s2,'z'),(28,s3,'r'),(33,s4,'l'),(51,s5,'u'),(85,s6,'r'),(110,s7,'z'),(125,s8,'l'),(129,s9,'u')]
def draw_scenes(img,t):
    n=len(SC)
    for k,(i0,fn,ent) in enumerate(SC):
        s=0 if k==0 else ST[i0]-0.2
        e=END+1 if k==n-1 else ST[SC[k+1][0]]-0.2
        if not(s<=t<e+0.2): continue
        lay=Image.new('RGBA',(W,H),(0,0,0,0))
        fn(lay,t)
        u=ease((t-s)/0.3) if k else 1
        a=1.0
        if t>e: a=max(0,1-(t-e)/0.2)
        dx=dy=0
        if ent=='u': dy=(1-u)*120
        elif ent=='l': dx=-(1-u)*160
        elif ent=='r': dx=(1-u)*160
        a*=min(1,u*1.5) if k else 1
        if dx or dy: lay=lay.transform((W,H),Image.AFFINE,(1,0,-dx,0,1,-dy))
        if a<1:
            al=lay.getchannel('A').point(lambda v:int(v*a)); lay.putalpha(al)
        img.alpha_composite(lay)
