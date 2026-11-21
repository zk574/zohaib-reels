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
    d.text((x0+64,y0+22),(tf if '(' in tf else 'XAUUSD  ·  '+tf),font=F('m',28),fill=GRY)
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
GLD=mk([60,58,59,55,56,52,54,53,57,55,51,48,50,53,52,56,58,57,61,64],61,31); GLD[11][2]=46.8; GLD[5][2]=50.6; GLD[8][1]=57.6
SLV=mk([30,29,29.5,27.5,28,26,27,26.5,28.5,27.5,26.8,27.2,28,29,28.6,30,31,30.6,32,33.5],30.5,33,(0.25,0.7)); SLV[5][2]=25.4; SLV[10][2]=26.3
SILV=(150,150,160)
def chart_at(img,t,series,n,lo,hi,tf,cy,h):
    global CY,CH
    o=(CY,CH); CY,CH=cy,h
    ch=chart(img,t,series,n,lo,hi,tf)
    CY,CH=o
    return ch
def coin(s,col,txt):
    def f(d,k):
        d.ellipse([0,0,s*k-1,s*k-1],fill=col); d.ellipse([s*.1*k,s*.1*k,s*.9*k,s*.9*k],outline=WH,width=int(s*.05*k))
    im=SS(s,s,f); tl=TL(txt,int(s*.22),WH); im.alpha_composite(tl,(int(s/2-tl.width/2),int(s/2-tl.height/2)))
    return im
GOLDC=(214,163,40)
def s1(img,t):
    hd(img,t,0,'Gold naya low',8,'sell daba rahe ho?')
    ch=chart(img,t,GLD[:12],kp(t,[(0,0),(1.6,12)]),44,62,'M15')
    X,Y=ch.X,ch.Y
    if t>A(2): tag(img,t,2,'NAYA LOW',X(9),Y(GLD[11][2])+30,RED,WH,26)
    if t>A(8):
        p=P(t,9,0.35); place(img,icon('rr',300,110,30,RED),780,CY-CH//2+170,p*(1-0.06*abs(math.sin(t*12))),min(1,p*2)); place(img,TL('SELL',64,WH),780,CY-CH//2+170,p,min(1,p*2))
def s2(img,t):
    p=P(t,13,0.4)
    if p>0: place(img,icon('octa',300),540,380,p,min(1,p*2)); place(img,TL('RUKO',80,WH),540,380,p,min(1,p*2))
    tx(img,t,14,'Pehle',90,540,620)
    ic(img,t,15,coin(220,SILV,'SILVER'),540,800,1,wob(t,1.5,6))
    tx(img,t,18,'HAAN,',100,330,1030); tx(img,t,19,'tum.',130,740,1020,OR,'s',wob(t,3,2))
def s3(img,t):
    hd(img,t,20,'Aaj ka concept:',24,'SMT divergence')
    ic(img,t,26,coin(260,GOLDC,'GOLD'),330,640,1,wob(t,1.2,4))
    ic(img,t,28,coin(260,SILV,'SILVER'),750,640,1,wob(t,1.2,4))
    if t>A(30):
        d=ImageDraw.Draw(img); u=ease((t-A(30))/0.6)
        for x0,col in ((150,GOLDC),(570,SILV)):
            pts=[(x0+i*36,900-i*14+12*math.sin(i*1.3)) for i in range(int(2+8*u))]
            if len(pts)>1: d.line(pts,fill=col,width=10,joint='curve')
        tx(img,t,30,'SAATH CHALTE HAIN',50,540,1000,INK)
    if t>A(33): pill(img,t,34,'DONO BHAI',540,1080,OR,WH,44)
def dual(img,t,ng,ns):
    g=chart_at(img,t,GLD,ng,44,66,'XAUUSD (GOLD)',595,360)
    s=chart_at(img,t,SLV,ns,24.5,35,'XAGUSD (SILVER)',980,360)
    return g,s
def s4(img,t):
    hd(img,t,36,'Gold naya low',43,'silver nahi')
    g,s=dual(img,t,kp(t,[(A(36)-0.1,0),(A(41),12)]),kp(t,[(A(42)-0.1,0),(A(47),12)]))
    d=ImageDraw.Draw(img)
    if t>A(41):
        u=ease((t-A(41))/0.4); x0,y0=g.X(5),g.Y(GLD[5][2]); x1,y1=g.X(11),g.Y(GLD[11][2])
        d.line([(x0,y0),(x0+(x1-x0)*u,y0+(y1-y0)*u)],fill=RED,width=6); tag(img,t,41,'LOWER LOW',g.X(15),g.Y(48),RED,WH,24)
    if t>A(47):
        u=ease((t-A(47))/0.4); x0,y0=s.X(5),s.Y(SLV[5][2]); x1,y1=s.X(10),s.Y(SLV[10][2])
        d.line([(x0,y0),(x0+(x1-x0)*u,y0+(y1-y0)*u)],fill=GRN,width=6); tag(img,t,47,'HIGHER LOW',s.X(15),s.Y(27),GRN,WH,24)
    if t>A(51):
        p=P(t,51,0.4); place(img,icon('rr',330,90,30,RED),780,790,p,min(1,p*2),-5); place(img,TL('GADBAD!',48,WH),780,790,p,min(1,p*2),-5)
    if t>A(63):
        p=P(t,64,0.45); place(img,icon('rr',600,100,50,OR),540,790,p,min(1,p*2)); place(img,TL('SMT DIVERGENCE',50,WH),540,790,p,min(1,p*2))
def s5(img,t):
    hd(img,t,66,'Liquidity sweep,',74,'smart money buy')
    g,s=dual(img,t,kp(t,[(0,12),(A(85),12),(A(92),19),(A(94),20)]),kp(t,[(0,12),(A(85),12),(A(92),19),(A(94),20)]))
    X,Y=g.X,g.Y
    if t>A(69): tag(img,t,69,'SWEEP',X(11),Y(GLD[11][2])+30,RED,WH,24)
    if t>A(74): tag(img,t,74,'SMART MONEY BUY',X(3)+20,Y(GLD[11][2])+30,GRN,WH,22) if t<A(90) else None
    lv=GLD[8][1]
    if t>A(90):
        u=ease((t-A(90))/0.4); hline(img,Y(lv),X(8),X(8)+(X(18)-X(8))*u,INK,4); tag(img,t,91,'BOS',X(13),Y(lv)-28,INK,WH,24)
    if t>A(94): tag(img,t,94,'BUY',X(19)-20,Y(GLD[19][3])-40,GRN,WH,28)
    if t>A(96):
        slv=GLD[11][2]-1.2; hline(img,Y(slv),X(9),g.box[2],RED,4); tag(img,t,97,'SL',X(16),Y(slv)+28,RED,WH,24)
def spark(w,h,pts,col):
    def f(d,k):
        d.line([(x*w*k,y*h*k) for x,y in pts],fill=col,width=9*k,joint='curve')
    return SS(w,h,f)
def s6(img,t):
    hd(img,t,104,'Ulta bhi',106,'same hai')
    G=[(0,.8),(.25,.35),(.5,.6),(.8,.1),(1,.45)]; S=[(0,.8),(.25,.3),(.5,.6),(.8,.45),(1,.75)]
    if card(img,t,108,430,420,290,640)>0:
        place(img,TL('GOLD',50,GOLDC),290,480,P(t,108)); place(img,spark(330,220,G,GOLDC),290,650,P(t,108))
        if t>A(110): tag(img,t,110,'NAYA HIGH',290,790,INK,WH,26)
    if card(img,t,112,430,420,790,640)>0:
        place(img,TL('SILVER',50,SILV),790,480,P(t,112)); place(img,spark(330,220,S,SILV),790,650,P(t,112))
        if t>A(113): tag(img,t,113,'HIGH NAHI',790,790,RED,WH,26)
    if t>A(115): pill(img,t,116,'SELL SIGNAL',540,960,RED,WH,58)
def s7(img,t):
    hd(img,t,119,'Ek chart jhooth',127,'do chart mushkil se')
    if card(img,t,121,380,380,280,640)>0:
        place(img,spark(260,180,[(0,.8),(.3,.4),(.6,.7),(1,.2)],INK),280,620,P(t,121)); place(img,TL('?',140,RED,'a'),280,640,P(t,123),1,wob(t,2,8))
        place(img,TL('1 CHART',40,GRY),280,790,P(t,121))
    if card(img,t,127,380,380,790,640,WH,GRN)>0:
        place(img,spark(260,120,[(0,.8),(.3,.3),(.6,.6),(1,.1)],GOLDC),790,590,P(t,127)); place(img,spark(260,120,[(0,.8),(.3,.4),(.6,.6),(1,.2)],SILV),790,680,P(t,128))
        place(img,TL('2 CHART',40,GRN),790,790,P(t,127)); place(img,icon('check',90,True),930,480,P(t,129,0.35))
def s8(img,t):
    hd(img,t,131,'Comment mein likho',134,'SMT')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,131,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,131,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,131,0.45))
    s='SMT'; a=A(133); b=EN[134]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,80,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
def s9(img,t):
    ic(img,t,135,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,135,'Follow karo',110,540,640,INK)
    tx(img,t,137,'kal milte hain',130,540,800,OR,'s')
    if t>A(136):
        p=P(t,136,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(13,s2,'z'),(20,s3,'r'),(36,s4,'l'),(66,s5,'u'),(104,s6,'r'),(119,s7,'l'),(131,s8,'u'),(135,s9,'z')]
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
