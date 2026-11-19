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
HOOK=mk([50,51,53,52,54,56,55,57,59,58,60,62],49,11)
R1=mk([60,58,59,56,57,54,52,53,55,58,57,61,64,63,67],61,13); R1[6][2]=50.2
R2=mk([50,52,51,53,52,54,53,55,54,56,57,60,63,66],49,17); R2[10]=[56,57.6,55.5,57]
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
def s1(img,t):
    hd(img,t,0,'Stop loss',2,'lagate ho kahan?')
    ch=chart(img,t,HOOK,kp(t,[(0,0),(1.4,12)]),44,66,'M15')
    lv=51+4*math.sin(t*2.3)+2.5*math.sin(t*5.1)
    if t>0.6:
        hline(img,ch.Y(lv),ch.box[0],ch.box[2],RED,4)
        place(img,icon('rr',150,60,30,RED),ch.box[2]-60,ch.Y(lv),1); place(img,TL('SL?',34,WH),ch.box[2]-60,ch.Y(lv),1)
    tx(img,t,4,'?',180,840,520,RED,'a',wob(t,2,8))
    tx(img,t,4,'?',130,260,560,RED,'a',wob(t,2.3,-8))
def s2(img,t):
    hd(img,t,6,'Wahan jahan',8,'dukh kam ho?')
    ic(img,t,8,mk_heart(380,RED) if False else icon('heart',380,(232,90,90)),540,640,1+0.05*math.sin(t*9))
    tx(img,t,10,'?',150,760,500,INK,'a',wob(t,2,6))
    tx(img,t,11,'HAAN,',120,330,960)
    tx(img,t,12,'tum.',160,740,950,OR,'s',wob(t,3,2))
def mk_heart_icon(s,col): return mk_heart(s,col)
def s3(img,t):
    hd(img,t,13,'Market',18,'structure dekhti hai')
    if card(img,t,14,420,460,290,690)>0:
        place(img,icon('heart',220,(232,90,90)),290,640,P(t,14)); place(img,TL('DARD',64,INK),290,830,P(t,15))
        if t>A(16): xmark(img,290,650,250,P(t,16,0.35))
    if card(img,t,18,420,460,790,690,WH,GRN)>0:
        place(img,zig(300,210),790,630,P(t,18)); place(img,TL('STRUCTURE',54,GRN),790,830,P(t,18))
        if t>A(19): place(img,icon('check',90,True),930,500,P(t,19,0.35))
def s4(img,t):
    hd(img,t,21,'Rule 1:',25,'swing ke peeche')
    ch=chart(img,t,R1,kp(t,[(A(21),0),(A(25),15)]),46,70,'M15')
    X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box
    sl=R1[6][2]; slv=sl-1.6
    if t>A(26):
        place(img,SS(90,90,lambda d,k:d.ellipse([4*k,4*k,86*k,86*k],outline=INK,width=6*k)),X(6),Y(sl),P(t,26,0.35))
        tag(img,t,27,'SWING LOW',X(6),Y(sl)-70,INK,WH,26)
    if t>A(33):
        u=ease((t-A(33))/0.4); hline(img,Y(slv),X(4),X(4)+(bx1-X(4))*u,RED,5)
        tag(img,t,34,'SL (THODA NEECHE)',X(12),Y(slv)+38,RED,WH,24)
    if t>A(41):
        zone(img,bx0,bx1,Y(slv),by1,(216,64,47,int(55*ease((t-A(41))/0.4))))
        tag(img,t,42,'YAHAN IDEA GALAT',X(3)+40,by1-34,RED,WH,24)
    if t>A(29): pill(img,t,29,'SELL? SL SWING HIGH KE UPAR',540,1070,INK,CREAM,30)
def s5(img,t):
    hd(img,t,47,'Rule 2:',49,'wick ko space do')
    n=kp(t,[(A(47),0),(A(49),11),(A(59),11),(A(60)+0.6,14)])
    ch=chart(img,t,R2[:10]+[R2[10]]+R2[11:],n,46,70,'M15')
    X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box
    slv=55.1
    if t>A(51):
        u=ease((t-A(51))/0.4); hline(img,Y(slv),X(6),X(6)+(bx1-X(6))*u,RED,5)
        tag(img,t,52,'SL BILKUL NEECHE',X(4),Y(slv)+40,RED,WH,24)
    if t>A(55):
        u=ease((t-A(55))/0.9); low=55.5-(55.5-52.4)*u
        if t>A(59)+0.6: low=52.4
        ImageDraw.Draw(img).line([(X(10),Y(55.5)),(X(10),Y(low))],fill=GRN,width=5)
        if low<slv:
            p=back((t-A(57))/0.4); place(img,icon('rr',290,96,26,RED),X(7),Y(48.6),p,min(1,p*2),-6); place(img,TL('SL HIT',54,WH),X(7),Y(48.6),p,min(1,p*2),-6)
    if t>A(59)+0.4:
        p=back((t-A(59)-0.4)/0.4); place(img,icon('rr',380,90,45,GRN),X(10),by0+40,p,min(1,p*2)); place(img,TL('PHIR UPAR!',44,WH),X(10),by0+40,p,min(1,p*2))
def s6(img,t):
    hd(img,t,61,'Rule 3:',63,'pehle stop loss')
    for n,(i,s) in enumerate([(64,'STOP LOSS'),(67,'LOT SIZE')]):
        y=480+n*160
        if card(img,t,i,760,130,540,y)>0:
            place(img,icon('circ',90,OR),220,y,P(t,i)); place(img,TL(str(n+1),62,CREAM,'a'),220,y-2,P(t,i))
            place(img,TL(s,62,INK),570,y,P(t,i))
    if t>A(70):
        p=P(t,71,0.5); place(img,icon('star',300),540,820,p*(1+0.03*math.sin(t*8)),min(1,p*2),wob(t,1,2))
        place(img,TL('RISK',40,CREAM),540,778,p,min(1,p*2)); place(img,TL('1%',110,CREAM,'a'),540,840,p,min(1,p*2))
    pill(img,t,72,'LOT = RISK ÷ SL',470,1040,INK,CREAM,46)
    if t>A(79):
        place(img,icon('heart',110,(232,90,90)),880,1040,P(t,79)); xmark(img,880,1040,130,P(t,81,0.35))
def s7(img,t):
    hd(img,t,83,'Risk : Reward',86,'kam se kam 1:3')
    y=540; 
    if t>A(84):
        p=P(t,84); place(img,icon('rr',170,150,24,RED),200,y,p,min(1,p*2)); place(img,TL('1R',56,WH),200,y,p,min(1,p*2))
    for k in range(3):
        p=back((t-(A(86)+k*0.15))/0.4)
        if p>0: place(img,icon('rr',170,150,24,GRN),420+k*190,y,p,min(1,p*2)); place(img,TL('+1R',48,WH),420+k*190,y,p,min(1,p*2))
    tx(img,t,86,'RISK',34,200,640,RED); tx(img,t,86,'REWARD x3',34,610,640,GRN)
    rows=[(96,'TRADE 1','-1R',False),(97,'TRADE 2','-1R',False),(102,'TRADE 3','+3R',True)]
    for n,(i,lab,v,g) in enumerate(rows):
        x=220+n*320
        if card(img,t,i,280,200,x,820,WH,GRN if g else RED)>0:
            place(img,TL(lab,30,GRY),x,760,P(t,i)); place(img,TL(v,70,GRN if g else RED,'a'),x,850,P(t,i))
    pill(img,t,103,'= +1R  GREEN!',540,1030,GRN,WH,54)
def s8(img,t):
    hd(img,t,105,'10 trade:',108,'6 loss, 4 jeet')
    for k in range(10):
        g=k>=6; st=(A(108)+k*0.12) if not g else (A(110)+(k-6)*0.15)
        p=back((t-st)/0.35)
        if p<=0: continue
        x=180+(k%5)*180; y=470+(k//5)*150
        place(img,icon('rr',150,120,24,GRN if g else RED),x,y,p,min(1,p*2)); place(img,TL('+3R' if g else '-1R',44,WH),x,y,p,min(1,p*2))
    pill(img,t,112,'-6R  +  12R',540,780,INK,CREAM,56)
    if t>A(114):
        p=P(t,115,0.5); place(img,icon('rr',560,150,75,GRN),540,930,p,min(1,p*2)); place(img,TL('= +6R  UPAR',72,WH),540,930,p,min(1,p*2))
    tx(img,t,118,'maths ka jadoo',90,540,1070,OR,'s')
def s9(img,t):
    hd(img,t,121,'Comment mein likho',124,'RR')
    place(img,icon('rr',900,150,75,WH,INK,5),520,560,P(t,121,0.45))
    place(img,icon('circ',110,OR),920,560,P(t,121,0.45)); place(img,TL('>',70,CREAM),925,558,P(t,121,0.45))
    s='RR 1:3'; a=A(124); b=EN[129]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,70,INK); img.alpha_composite(tl,(110,int(560-tl.height/2)))
    for k,(s2,c) in enumerate([('1:1',GRY),('1:2',INK),('1:3',GRN)]):
        p=back((t-(A(126)+k*0.15))/0.4)
        if p>0: place(img,icon('rr',250,130,40,c),240+k*300,800,p,min(1,p*2)); place(img,TL(s2,70,WH,'a'),240+k*300,800,p,min(1,p*2))
    tx(img,t,130,'Tumhara kya hai?',70,540,1000,INK)
def s10(img,t):
    ic(img,t,133,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,133,'Follow karo',110,540,640,INK)
    tx(img,t,135,'kal milte hain',130,540,800,OR,'s')
    if t>A(134):
        p=P(t,134,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
mk_heart_=mk_heart
globals()['mk_heart']=mk_heart
SC=[(0,s1,'u'),(6,s2,'r'),(13,s3,'z'),(21,s4,'l'),(47,s5,'u'),(61,s6,'r'),(83,s7,'l'),(105,s8,'u'),(121,s9,'r'),(133,s10,'l')]
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
