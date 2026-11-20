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
BRK=mk([50,53,56,54,52,55,58,57,54,50,47,45,47,46,43],48,21); BRK[6][1]=59.6
MIT=mk([50,53,56,54,52,54,55,53,50,47,45,47,49,52,54,51,48,45,42],48,23); MIT[6][1]=55.9; MIT[14][1]=55.4; MIT[2][1]=57.4
def ring(img,cx,cy,r,col,p=1):
    if p<=0: return
    place(img,SS(2*r+8,2*r+8,lambda d,k:d.ellipse([4*k,4*k,(2*r+4)*k,(2*r+4)*k],outline=col,width=6*k)),cx,cy,p)
def s1(img,t):
    hd(img,t,0,'Breaker block',2,'yaad hai?')
    if card(img,t,0,520,240,540,560,WH,OR)>0:
        place(img,TL('BREAKER',90,OR),540,560,P(t,0))
    if t>A(4):
        p=P(t,6,0.45)
        place(img,icon('rr',380,160,40,INK),540,860,p,min(1,p*2)); place(img,TL('MITIGATION',54,CREAM),540,860,p,min(1,p*2))
        tx(img,t,6,'chhota bhai',70,540,1010,OR,'s')
def s2(img,t):
    tx(img,t,11,'HAAN,',130,300,330); tx(img,t,12,'tum.',170,770,320,OR,'s',wob(t,3,2))
    for n,(i,s) in enumerate([(14,'BREAKER'),(16,'MITIGATION')]):
        x=300+n*480
        if card(img,t,i,420,300,x,700)>0:
            place(img,TL(s,52 if n else 64,INK),x,660,P(t,i)); place(img,TL('?',110,RED,'a'),x,760,P(t,i),1,wob(t,2+n,10))
    tx(img,t,18,'CONFUSE?',90,540,960,RED,'m',wob(t,1.5,3))
def s3(img,t):
    hd(img,t,26,'Breaker:',35,'sweep, phir break')
    ch=chart(img,t,BRK,kp(t,[(A(26)-0.1,0),(A(29),5),(A(31),7),(A(38),8),(A(40)+0.6,15)]),40,62,'M15')
    X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box
    ph=BRK[2][1]
    if t>A(28):
        u=ease((t-A(28))/0.4); hline(img,Y(ph),X(2),X(2)+(bx1-X(2))*u,INK,3); tag(img,t,28,'PURANA HIGH',X(2),Y(ph)-36,INK,WH,24)
    if t>A(31):
        ring(img,X(6),Y(BRK[6][1]),40,OR,P(t,31,0.35)); tag(img,t,31,'NAYA HIGH',X(9),Y(BRK[6][1])+10,OR,WH,24)
    if t>A(35): tag(img,t,35,'SWEEP!',X(6),Y(BRK[6][1])-60,RED,WH,26)
    lo=BRK[4][2]
    if t>A(38):
        u=ease((t-A(38))/0.4); hline(img,Y(lo),X(4),X(4)+(bx1-X(4))*u,RED,3)
    if t>A(40): tag(img,t,40,'BREAK',X(11),Y(lo)-36,RED,WH,26)
def mit_chart(img,t,n):
    ch=chart(img,t,MIT,n,38,60,'M15'); X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box
    ph=MIT[2][1]; hline(img,Y(ph),X(2),bx1,INK,3)
    return ch
def s4(img,t):
    hd(img,t,43,'Mitigation:',46,'naya high nahi')
    ch=mit_chart(img,t,kp(t,[(A(43)-0.1,0),(A(46),5),(A(52),7),(A(59),8),(A(60)+0.5,11)]))
    X,Y=ch.X,ch.Y; bx1=ch.box[2]
    place(img,TL('PURANA HIGH',24,INK),X(2)+30,Y(MIT[2][1])-28)
    if t>A(48): xmark(img,X(6)+10,Y(MIT[2][1])-10,70,P(t,50,0.35))
    if t>A(52):
        ring(img,X(6),Y(MIT[6][1]),38,OR,P(t,52,0.35)); tag(img,t,53,'LOWER HIGH',X(9),Y(MIT[6][1])+10,OR,WH,24)
    lo=MIT[4][2]
    if t>A(59):
        u=ease((t-A(59))/0.4); hline(img,Y(lo),X(4),X(4)+(bx1-X(4))*u,RED,3); tag(img,t,60,'BREAK',X(10),Y(lo)-34,RED,WH,26)
    pill(img,t,62,'BUYERS FAIL',540,1075,RED,WH,44)
def s5(img,t):
    hd(img,t,66,'Phanse buyers',73,'loss nikalna hai')
    ch=mit_chart(img,t,kp(t,[(0,11),(A(78),11),(A(87),15),(A(98),15),(A(102)+0.4,19)]))
    X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box; cw=ch.cw
    zt,zb=MIT[6][1],MIT[5][0]
    if t>A(82):
        u=ease((t-A(82))/0.5); zone(img,X(5)-cw*.5,X(5)-cw*.5+(bx1-X(5)+cw*.5)*u,Y(zt),Y(zb),(233,120,66,95))
        tag(img,t,85,'MITIGATION BLOCK',X(10),Y(zt)-30,OR,WH,24)
    if t>A(68): tag(img,t,69,'PHANSE BUYERS',X(6),Y(MIT[6][1])-70,INK,WH,24)
    if t>A(89): pill(img,t,95,'BADE PLAYERS MITIGATE',540,1075,INK,CREAM,40)
    if t>A(100): arrow(img,X(17),Y(MIT[16][3]),False,RED,40,10)
def s6(img,t):
    hd(img,t,104,'Rule',105,'simple hai')
    rows=[(108,'SWEEP',False),(110,'LOWER HIGH',True),(112,'STRUCTURE BREAK',True),(115,'ZONE PAR ENTRY',True)]
    for n,(i,s,g) in enumerate(rows):
        y=470+n*140
        if card(img,t,i,800,115,540,y,WH,SOFT)>0:
            place(img,icon('check',80,g),210,y,P(t,i)); place(img,TL(s if g else 'SWEEP NAHI',52,INK if g else RED),580,y,P(t,i))
    pill(img,t,119,'SL: US HIGH KE UPAR',540,1060,RED,WH,48)
def s7(img,t):
    hd(img,t,125,'Kabhi pakda hai?',134,'Comment karo')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,126,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,126,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,126,0.45))
    s='MB'; a=A(136); b=EN[137]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,80,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
    if t>A(137): pill(img,t,137,'MB = MITIGATION BLOCK',540,860,OR,WH,50)
def s8(img,t):
    ic(img,t,138,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,138,'Follow karo',110,540,640,INK)
    tx(img,t,140,'kal milte hain',130,540,800,OR,'s')
    if t>A(139):
        p=P(t,139,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(11,s2,'r'),(22,s3,'z'),(43,s4,'l'),(66,s5,'u'),(104,s6,'r'),(125,s7,'l'),(138,s8,'u')]
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
