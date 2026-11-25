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
B=[[60,61,59.2,60.4],[60.4,61.2,59.5,59.8],[59.8,60.6,58.6,59],[59,59.6,57.4,57.8],[57.8,58.2,56,56.4],[56.4,56.6,50,50.4],[50.4,52.5,49.2,49.8],[49.8,50.3,47,47.6],[47.6,49,46.8,48.6],[48.6,51,48.2,50.8],[50.8,58.4,50.6,58],[58,59.2,54,58.6],[58.6,58.8,55.4,55.8],[55.8,56.2,53.6,54.2],[54.2,57,53.4,56.6],[56.6,59.6,56.2,59.2],[59.2,61.6,58.8,61.2],[61.2,63.4,60.8,63]]
BE_T,BE_B=56.0,52.5
BU_T,BU_B=54.0,51.0
OV_T,OV_B=54.0,52.5
def bchart(img,t,n): return chart(img,t,B,n,44,66,'M15')
def zbox(img,ch,i0,top,bot,rgba,u=1):
    X,Y=ch.X,ch.Y; x0=X(i0)-ch.cw*.5; x1=ch.box[2]
    zone(img,x0,x0+(x1-x0)*u,Y(top),Y(bot),rgba)
def s1(img,t):
    tx(img,t,0,'Ek FVG upar,',90,540,260,INK)
    tx(img,t,6,'ek FVG neeche',100,540,370,OR,'s')
    if card(img,t,1,400,300,290,690,WH,GRN)>0:
        place(img,TL('BULLISH',52,GRN),290,640,P(t,1)); place(img,TL('FVG',80,GRN),290,730,P(t,1))
    if card(img,t,7,400,300,790,690,WH,RED)>0:
        place(img,TL('BEARISH',52,RED),790,640,P(t,7)); place(img,TL('FVG',80,RED),790,730,P(t,7))
    tx(img,t,16,'KAUNSA?',100,540,970,INK,'m',wob(t,2,4))
def s2(img,t):
    tx(img,t,20,'HAAN,',130,300,330); tx(img,t,21,'tum.',170,770,320,OR,'s',wob(t,3,2))
    tx(img,t,22,'Jawab:',80,540,540,INK)
    p=P(t,24,0.45)
    if p>0: place(img,icon('rr',460,160,50,INK),540,700,p,min(1,p*2)); place(img,TL('DONO!',100,CREAM),540,700,p,min(1,p*2))
    if t>A(28):
        p=P(t,28,0.45); place(img,icon('rr',640,150,75,OR),540,920,p,min(1,p*2)); place(img,TL('BPR',100,WH),540,920,p,min(1,p*2))
    tx(img,t,29,'Balanced Price Range',60,540,1060,OR,'s')
def s3(img,t):
    hd(img,t,32,'Pehle neeche,',44,'phir wapas upar')
    n=kp(t,[(A(32)-0.1,4),(A(36),7),(A(44),9),(A(48),11),(A(55),12)])
    ch=bchart(img,t,n); X,Y=ch.X,ch.Y
    if t>A(40):
        zbox(img,ch,5,BE_T,BE_B,(216,64,47,80),ease((t-A(40))/0.45)); tag(img,t,41,'BEARISH FVG',X(2),Y(BE_T)-8,RED,WH,22)
    if t>A(53):
        zbox(img,ch,10,BU_T,BU_B,(46,158,91,80),ease((t-A(53))/0.45)); tag(img,t,54,'BULLISH FVG',X(14),Y(BU_B)+30,GRN,WH,22)
def s4(img,t):
    hd(img,t,56,'Overlap =',71,'BPR')
    ch=bchart(img,t,12); X,Y=ch.X,ch.Y
    zbox(img,ch,5,BE_T,BE_B,(216,64,47,60)); zbox(img,ch,10,BU_T,BU_B,(46,158,91,60))
    if t>A(60):
        a=int(110+60*abs(math.sin(t*4))); u=ease((t-A(60))/0.5)
        zbox(img,ch,10,OV_T,OV_B,(233,120,66,a),u)
        if u>0.5: tag(img,t,68,'BPR ZONE',X(15),Y(OV_T)-30,OR,WH,26)
    pill(img,t,76,'DONO TARAF KA KAAM PURA',540,1060,INK,CREAM,40)
    if t>A(84): pill(img,t,85,'STRONG ZONE',540,1060,GRN,WH,50)
def s5(img,t):
    hd(img,t,89,'Wapas BPR mein',96,'= entry')
    n=kp(t,[(0,12),(A(90),12),(A(94),14),(A(103),14),(A(106)+0.5,18)])
    ch=bchart(img,t,n); X,Y=ch.X,ch.Y; bx1=ch.box[2]
    zbox(img,ch,10,OV_T,OV_B,(233,120,66,120))
    if t>A(95): tag(img,t,96,'ENTRY',X(13),Y(B[12][1])-40,GRN,WH,26)
    if t>A(97):
        sl=OV_B-1.0; u=ease((t-A(97))/0.4); hline(img,Y(sl),X(9),X(9)+(bx1-X(9))*u,RED,4); tag(img,t,98,'SL',X(16),Y(sl)+28,RED,WH,24)
    if t>A(104):
        tg=61.2; u=ease((t-A(104))/0.4); hline(img,Y(tg),X(0),X(0)+(bx1-X(0))*u,GRN,4); tag(img,t,105,'TARGET: AGLA HIGH',X(6),Y(tg)-28,GRN,WH,22)
def s6(img,t):
    tx(img,t,108,'Do gap mile,',90,540,300,INK)
    p1=P(t,109,0.4); p2=P(t,111,0.4)
    if p1>0:
        dx=int(160*(1-min(1,ease((t-A(111))/0.6)) if t>A(111) else 160))
        place(img,icon('rr',300,140,24,(216,64,47)),540-dx,560,p1,min(1,p1*2)*0.85)
        place(img,icon('rr',300,140,24,(46,158,91)),540+dx,600,p1,min(1,p1*2)*0.85)
    if t>A(112)+0.3:
        p=back((t-A(112)-0.3)/0.4); place(img,icon('rr',300,60,16,OR),540,580,p); place(img,TL('BPR',40,WH),540,580,p)
    tx(img,t,112,'ek zone bana',100,540,820,OR,'s')
    if t>A(115): pill(img,t,116,'CONFUSION KHATAM',540,1000,GRN,WH,50)
def s7(img,t):
    hd(img,t,118,'Comment mein likho',121,'BPR')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,118,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,118,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,118,0.45))
    s='BPR'; a=A(120); b=EN[121]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,80,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
def s8(img,t):
    ic(img,t,122,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,122,'Follow karo',110,540,640,INK)
    tx(img,t,124,'kal milte hain',130,540,800,OR,'s')
    if t>A(123):
        p=P(t,123,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(20,s2,'z'),(32,s3,'r'),(56,s4,'l'),(89,s5,'u'),(108,s6,'z'),(118,s7,'l'),(122,s8,'u')]
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
