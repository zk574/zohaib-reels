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
YD=mk([54,57,55,59,56,52,53,51,54,55],53,61); YD[3]=[55,60.0,54.6,59]; YD[7]=[53,53.4,50.0,51]
PDH,PDL=60.0,50.0
UPS=YD+mk([55,56.5,58,57.4,59.2,59.0,57,55,54,53.2],55,63); UPS[14]=[57.4,61.6,57.0,59.0]
DNS=YD+mk([55,53.5,52,52.6,50.8,51.0,53,55,56,57],55,65); DNS[14]=[52.6,53.0,48.4,51.0]
def pchart(img,t,ser,n):
    ch=chart(img,t,ser,n,46,64,'M15'); X,Y=ch.X,ch.Y; d=ImageDraw.Draw(img)
    xs=(X(9)+X(10))/2
    d.line([(xs,ch.box[1]),(xs,ch.box[3])],fill=SOFT,width=3)
    d.text((X(4),ch.box[1]-6),'KAL',font=F('m',24),fill=GRY); d.text((X(14),ch.box[1]-6),'AAJ',font=F('m',24),fill=GRY)
    return ch
def lines2(img,t,ch,ih=None,il=None):
    X,Y=ch.X,ch.Y; bx1=ch.box[2]
    for lv,i,lab,col in ((PDH,ih,'PDH',RED),(PDL,il,'PDL',GRN)):
        if i is None or t<A(i): continue
        u=ease((t-A(i))/0.45); hline(img,Y(lv),X(0),X(0)+(bx1-X(0))*u,col,4)
        if u>0.6: place(img,icon('rr',100,44,22,col),bx1-40,Y(lv)); place(img,TL(lab,26,WH),bx1-40,Y(lv))
def s1(img,t):
    hd(img,t,0,'Roz chart pe',3,'sau lines?')
    ch=chart(img,t,YD+UPS[10:],kp(t,[(0,0),(1.2,20)]),46,64,'M15'); X,Y=ch.X,ch.Y
    import random; r=random.Random(3); n=int(min(1,max(0,t-0.4)/1.8)*26)
    cols=[RED,GRN,BLUE,OR,INK,(150,90,200)]
    d=ImageDraw.Draw(img)
    for k in range(n):
        y=r.uniform(ch.box[1],ch.box[3]); x0=r.uniform(ch.box[0],ch.box[2]-200); c=cols[k%6]
        if k%3==0: d.line([(x0,y),(x0+r.uniform(120,500),y+r.uniform(-120,120))],fill=c,width=3)
        else: d.line([(ch.box[0],y),(ch.box[2],y)],fill=c,width=2)
    if t>A(5): place(img,TL('?!',150,RED,'a'),860,560,P(t,6,0.4),1,wob(t,2,6))
def s2(img,t):
    hd(img,t,8,'Bas',9,'do lines kaafi')
    ch=pchart(img,t,YD,10)
    lines2(img,t,ch,17,21)
    if t>A(13) and t<A(15)+0.3: pill(img,t,13,'HAAN, TUM.',540,1075,INK,CREAM,46)
    if t>A(22): pill(img,t,22,'PREVIOUS DAY HIGH / LOW',540,1075,OR,WH,40)
def dots(img,t,ch,lv,i,up,col,n=8):
    X,Y=ch.X,ch.Y
    for k in range(n):
        p=back((t-(A(i)+k*0.06))/0.3)
        if p>0: place(img,icon('circ',22,col),X(1)+k*48,Y(lv+(1.2+0.5*(k%2))*(1 if up else -1)),p)
def s3(img,t):
    hd(img,t,25,'Kyun?',61,'liquidity dono taraf')
    ch=pchart(img,t,YD,10); X,Y=ch.X,ch.Y
    lines2(img,t,ch,0,0)
    if t>A(35): dots(img,t,ch,PDL,36,False,RED); tag(img,t,37,'BUYERS KA SL',X(13),Y(PDL-2.6),RED,WH,22)
    if t>A(51): dots(img,t,ch,PDH,52,True,RED); tag(img,t,52,'SELLERS KA SL',X(13),Y(PDH+2.6),RED,WH,22)
    if t>A(61): pill(img,t,61,'LIQUIDITY KA DHER',540,1075,OR,WH,46)
def s4(img,t):
    hd(img,t,64,'PDH ke upar wick',85,'to sell dhoondo')
    n=kp(t,[(A(64)-0.1,10),(A(72),14),(A(78),14),(A(80)+0.2,15),(A(84),15),(A(86)+0.5,20)])
    ch=pchart(img,t,UPS,n); X,Y=ch.X,ch.Y
    lines2(img,t,ch,0,0)
    if t<A(80): dots(img,t,ch,PDH,0,True,RED)
    if t>A(79): tag(img,t,79,'WICK',X(14),Y(UPS[14][1])-30,RED,WH,24)
    if t>A(85): tag(img,t,85,'SELL',X(18),Y(UPS[17][3])+50,RED,WH,26)
def s5(img,t):
    hd(img,t,87,'PDL ke neeche wick',97,'to buy dhoondo')
    n=kp(t,[(A(87)-0.1,10),(A(89),14),(A(91),14),(A(92)+0.2,15),(A(96),15),(A(98)+0.4,20)])
    ch=pchart(img,t,DNS,n); X,Y=ch.X,ch.Y
    lines2(img,t,ch,0,0)
    if t<A(92): dots(img,t,ch,PDL,0,False,RED)
    if t>A(91): tag(img,t,91,'WICK',X(14),Y(DNS[14][2])+30,RED,WH,24)
    if t>A(97): tag(img,t,97,'BUY',X(18),Y(DNS[17][3])-50,GRN,WH,26)
def s6(img,t):
    hd(img,t,100,'Body close bahar?',109,'= breakout')
    p=P(t,102,0.4)
    if p>0:
        def f(d,k):
            w,h=300,420; ly=250
            d.line([(0,ly*k),(w*k,ly*k)],fill=RED,width=6*k)
            d.line([(w/2*k,30*k),(w/2*k,380*k)],fill=GRN,width=8*k)
            d.rounded_rectangle([90*k,70*k,210*k,230*k],12*k,fill=GRN)
        place(img,SS(300,420,f),540,620,p,min(1,p*2)); place(img,TL('PDH',30,RED),720,600+p*20,p)
    if t>A(109): pill(img,t,109,'BREAKOUT',540,900,GRN,WH,60)
    if t>A(111):
        p=P(t,111,0.4); place(img,icon('rr',380,100,30,SOFT,RED,4),540,1050,p,min(1,p*2)); tl=TL('ULTA SELL',50,RED); place(img,tl,540,1050,p,min(1,p*2))
        if t>A(112)+0.1: ImageDraw.Draw(img).line([(540-tl.width/2-10,1050),(540+tl.width/2+10,1050)],fill=RED,width=8)
def moon(s):
    def f(d,k):
        d.ellipse([0,0,s*k-1,s*k-1],fill=(240,200,90)); d.ellipse([s*.32*k,-s*.08*k,s*1.2*k,s*.8*k],fill=CREAM)
    return SS(s,s,f)
def s7(img,t):
    hd(img,t,114,'Raat ko 2 lines',122,'subah plan ready')
    ic(img,t,114,moon(170),220,470,1,wob(t,1,4))
    if card(img,t,117,640,330,600,620)>0:
        d=ImageDraw.Draw(img)
        d.line([(310,540),(890,540)],fill=RED,width=6); d.line([(310,700),(890,700)],fill=GRN,width=6)
        place(img,TL('PDH',30,RED),840,515,P(t,118)); place(img,TL('PDL',30,GRN),840,725,P(t,118))
    if t>A(124): place(img,icon('check',120,True),860,880,P(t,125,0.35)); pill(img,t,124,'PLAN READY',480,880,GRN,WH,50)
def s8(img,t):
    hd(img,t,126,'Comment mein likho',129,'PDH')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,126,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,126,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,126,0.45))
    s='PDH'; a=A(128); b=EN[129]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,80,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
def s9(img,t):
    ic(img,t,130,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,130,'Follow karo',110,540,640,INK)
    tx(img,t,132,'kal milte hain',130,540,800,OR,'s')
    if t>A(131):
        p=P(t,131,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(8,s2,'z'),(25,s3,'r'),(64,s4,'l'),(87,s5,'r'),(100,s6,'u'),(114,s7,'z'),(126,s8,'l'),(130,s9,'u')]
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
