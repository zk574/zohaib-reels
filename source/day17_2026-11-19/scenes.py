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
D1=mk([38,41,45,43,48,52,50,47,49,55,60,58,63,66,61,57,53,51],37,3)
H4=mk([30,28,26,27,24,23,25,31,37,36,38,34,30,27,25,26,29,34,40],31,5); H4[9]=[37,37.8,35.0,36]; H4[5][2]=22.2
M15=mk([60,58,59,56,57,54,55,52,53,50,53,55,58,56,54,59,63,67],61,7); M15[10]=[50,53.6,45.5,53]
SLS=mk([50,51,52,53,52,54,55,56,55,54,52,50,48,47],49,9)
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
def s1(img,t):
    hd(img,t,0,'Entry sahi,',8,'stop loss hit?')
    ch=chart(img,t,SLS,kp(t,[(0,0),(1.0,7),(2.2,11),(3.1,14)]),44,60,'M15')
    slp=51.2
    if t>A(8):
        u=ease((t-A(8))/0.4); hline(img,ch.Y(slp),ch.box[0],ch.box[0]+(ch.box[2]-ch.box[0])*u,RED)
        tag(img,t,8,'STOP LOSS',ch.box[2]-120,ch.Y(slp)+40,RED,WH,28)
    if t>A(1)+0.5:
        tag(img,t,1,'ENTRY',ch.X(6),ch.Y(57.8),GRN,WH,28)
    if t>A(10):
        p=P(t,10,0.4); place(img,icon('rr',300,100,26,RED),780,CY-170,p,min(1,p*2),-6); place(img,TL('SL HIT',58,WH),780,CY-170,p,min(1,p*2),-6)
def compass(s,ang):
    def f(d,k):
        c=s*k/2; d.ellipse([6*k,6*k,(s-6)*k,(s-6)*k],fill=WH,outline=INK,width=8*k)
        for a in range(0,360,45):
            r=math.radians(a); d.line([(c+(c-26*k)*math.sin(r),c-(c-26*k)*math.cos(r)),(c+(c-14*k)*math.sin(r),c-(c-14*k)*math.cos(r))],fill=GRY,width=4*k)
        r=math.radians(ang); L=c*.62
        d.polygon([(c+L*math.sin(r),c-L*math.cos(r)),(c+30*k*math.cos(r),c+30*k*math.sin(r)),(c-30*k*math.cos(r),c-30*k*math.sin(r))],fill=OR)
        r2=r+math.pi; d.polygon([(c+L*math.sin(r2),c-L*math.cos(r2)),(c+30*k*math.cos(r),c+30*k*math.sin(r)),(c-30*k*math.cos(r),c-30*k*math.sin(r))],fill=INK)
        d.ellipse([c-12*k,c-12*k,c+12*k,c+12*k],fill=CREAM)
    return SS(s,s,f)
def s2(img,t):
    hd(img,t,18,'Bina',21,'bias = andhera')
    ang=math.sin(t*3.1)*120+math.sin(t*5.3)*60
    ic(img,t,21,compass(460,ang),540,720)
    tx(img,t,23,'?',200,860,560,RED,'a')
    tx(img,t,24,'?',150,215,860,RED,'a')
def s3(img,t):
    tx(img,t,27,'HAAN,',200,540,360)
    tx(img,t,28,'tum.',320,540,640,OR,'s',wob(t,3,2))
def s4(img,t):
    hd(img,t,29,'Bias =','30','market ka rukh') if False else (tx(img,t,29,'Bias =',100,540,230),tx(img,t,31,'market ka rukh',100,540,335,OR,'s'))
    ic(img,t,31,compass(420,40),540,700)
    if t>A(36):
        for n,s in enumerate(['1','2','3']):
            p=back((t-(A(36)+n*0.18))/0.4)
            if p>0:
                place(img,icon('circ',130,OR),540+(n-1)*220,980,p,min(1,p*2)); place(img,TL(s,90,CREAM,'a'),540+(n-1)*220,975,p,min(1,p*2))
    tx(img,t,35,'3 STEPS',70,540,1090 if False else 1075) if False else None
def s5(img,t):
    hd(img,t,38,'Step 1:',40,'Daily chart')
    s0=A(38)
    ch=chart(img,t,D1,kp(t,[(s0,0),(A(43),18)]),32,72,'D1')
    d=ch.d; X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box
    last=D1[-1][3]; lowr=min(c[2] for c in D1[7:9]); highr=D1[13][1]; eq=(lowr+highr)/2
    if t>A(43):
        place(img,icon('circ',26,OR),X(17),Y(last),P(t,44,0.3)); tag(img,t,44,'PRICE',X(17)-20,Y(last)-48,INK,WH,24)
    if t>A(45):
        u=ease((t-A(45))/0.4); zone(img,bx0,bx1,Y(highr),Y(highr)+(Y(eq)-Y(highr))*u,(233,120,66,70))
        hline(img,Y(highr),bx0,bx1,OR,3); tag(img,t,45,'PREMIUM',bx0+110,Y(highr)+34,OR,WH,26)
    if t>A(49):
        u=ease((t-A(49))/0.4); zone(img,bx0,bx1,Y(eq),Y(eq)+(Y(lowr)-Y(eq))*u,(46,158,91,60))
        hline(img,Y(lowr),bx0,bx1,GRN,3); tag(img,t,49,'DISCOUNT',bx0+120,Y(lowr)-34,GRN,WH,26)
        hline(img,Y(eq),bx0,bx1,GRY,2)
    lvl=D1[5][1]
    if t>A(52):
        u=ease((t-A(52))/0.5); hline(img,Y(lvl),X(5),X(5)+(X(10)-X(5))*u+40,INK,4)
        tag(img,t,53,'STRUCTURE HIGH',X(3)+30,Y(lvl)-36,INK,WH,24)
    if t>A(54):
        p=P(t,54,0.4); place(img,icon('circ',110,None,5) if False else SS(110,110,lambda dd,k:dd.ellipse([4*k,4*k,106*k,106*k],outline=RED,width=7*k)),X(10),Y(D1[10][3]),p)
        tag(img,t,54,'BREAK!',X(10),Y(D1[10][1])-60,RED,WH,26)
    if t>A(62):
        p=P(t,62,0.45); place(img,icon('rr',470,96,48,GRN),310,1070,p,min(1,p*2)); place(img,TL('BULLISH BIAS',44,WH),310,1070,p,min(1,p*2))
        d2=ImageDraw.Draw(img)
    if t>A(66):
        p=P(t,66,0.45); place(img,icon('rr',330,96,48,RED),760,1070,p,min(1,p*2)); place(img,TL('BEARISH',44,WH),760,1070,p,min(1,p*2))
def s6(img,t):
    hd(img,t,68,'Step 2:',70,'4H POI')
    s0=A(68)+0.25
    ch=chart(img,t,H4,kp(t,[(s0,0),(A(72),19)]),18,44,'H4')
    X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box; cw=ch.cw
    ob=H4[5]; 
    if t>A(78):
        u=ease((t-A(78))/0.4); zone(img,X(5)-cw*.5,X(5)-cw*.5+(bx1-X(5)+cw*.5)*u,Y(ob[0]),Y(ob[2]),(233,120,66,95))
        tag(img,t,78,'ORDER BLOCK',X(11),Y(23.6)+0,OR,WH,24)
    if t>A(81):
        u=ease((t-A(81))/0.4); zone(img,X(7)-cw*.5,X(7)-cw*.5+(bx1-X(7)+cw*.5)*u,Y(H4[9][2]),Y(H4[7][1]),(70,130,190,100))
        tag(img,t,81,'FVG',X(13),Y(33.8),BLUE,WH,24)
    if t>A(84):
        p=P(t,84,0.45); place(img,icon('rr',560,84,42,INK),540,CY-CH//2+142,p,min(1,p*2)); place(img,TL('BADE PLAYERS KA ORDER',30,CREAM),540,CY-CH//2+142,p,min(1,p*2))
    if t>A(86):
        pulse=0.5+0.5*math.sin(t*8); rr=int(70+16*pulse)
        place(img,SS(rr*2+4,rr*2+4,lambda dd,k:dd.ellipse([4*k,4*k,(rr*2)*k,(rr*2)*k],outline=OR,width=6*k)),X(14),Y(24),1,1)
def s7(img,t):
    hd(img,t,90,'Step 3:',93,'15 minute')
    pts=[(A(90)+0.25,0),(A(96),10),(A(98)+0.2,11),(A(100),13),(A(101)+0.3,15),(A(103),15.2),(A(104)+0.8,18)]
    ch=chart(img,t,M15,kp(t,pts),42,70,'M15')
    X,Y=ch.X,ch.Y; bx0,by0,bx1,by1=ch.box
    lowl=M15[9][2]
    if t>A(98):
        hline(img,Y(lowl),X(3),X(14),RED,3); tag(img,t,98,'SWEEP',X(13),Y(lowl)+40,RED,WH,26)
        p=P(t,98,0.4); arrow(img,X(10),Y(M15[10][2])+110,True,RED,50,10)
    lh=M15[8][1]
    if t>A(99):
        u=ease((t-A(99))/0.4); hline(img,Y(lh),X(8),X(8)+(X(12)-X(8)+40)*u,GRN,4); tag(img,t,99,'CHoCH',X(15),Y(lh)-10,GRN,WH,26)
    if t>A(101):
        tag(img,t,101,'ENTRY',X(14),Y(M15[14][2])+44,INK,WH,26)
        arrow(img,X(14),Y(M15[14][2])+95,True,INK,0,0) if False else None
def s8(img,t):
    hd(img,t,106,'Rule yaad rakho:',109,'daily bias')
    p=P(t,111,0.45)
    if p>0:
        place(img,icon('rr',800,170,50,WH,SOFT,3),540,560,p,min(1,p*2))
        place(img,TL('BULLISH',96,GRN),480,560,p,min(1,p*2))
        d=ImageDraw.Draw(img); arrow(img,860,610,True,GRN,80,18) if p>0.9 else None
    p=P(t,114,0.45)
    if p>0:
        place(img,icon('rr',800,160,50,GRN),540,790,p,min(1,p*2)); place(img,TL('SIRF BUY',100,WH),540,790,p,min(1,p*2))
    p=P(t,117,0.45)
    if p>0:
        place(img,icon('rr',800,160,50,SOFT,GRY,4),540,990,p,min(1,p*2)); tl=TL('SELL',100,GRY); place(img,tl,540,990,p,min(1,p*2))
        if t>A(119)+0.2:
            u=ease((t-A(119)-0.2)/0.3); ImageDraw.Draw(img).line([(540-tl.width/2-10,990),(540-tl.width/2-10+(tl.width+20)*u,990)],fill=RED,width=10)
            place(img,icon('check',110,False),880,990,P(t,121,0.35))
def s9(img,t):
    hd(img,t,123,'Bade time frame','127','ke khilaf?') if False else (tx(img,t,123,'Bade time frame',84,540,225),tx(img,t,128,'ke khilaf?',100,540,335,OR,'s'))
    d=ImageDraw.Draw(img)
    if t>A(131):
        for k in range(5):
            y=520+k*95
            pts=[(100+x,y+14*math.sin((x+t*180)/70)) for x in range(0,880,10)]
            d.line(pts,fill=(70,130,190,255),width=8)
        place(img,TL('CURRENT',72,BLUE),540,470,P(t,131,0.4))
    if t>A(124):
        p=P(t,124,0.45)
        place(img,icon('rr',640,130,40,OR),540,430 if t<=A(131) else 940,p,min(1,p*2)); place(img,TL('BADA TIMEFRAME',56,CREAM),540,430 if t<=A(131) else 940,p,min(1,p*2))
    if t>A(129):
        p=P(t,129,0.45); y=700
        place(img,icon('rr',400,120,36,INK),420,y,p,min(1,p*2)); place(img,TL('TUMHARA TRADE',36,CREAM),420,y,p,min(1,p*2))
        place(img,icon('check',100,False),700,y,P(t,133,0.4))
def s10(img,t):
    hd(img,t,135,'Aaj ka bias?',143,'Comment karo')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,143,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,143,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,143,0.45))
    s='BIAS  BUY'; a=A(145); b=EN[148]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a)))
        txt=s[:n]
        if txt:
            tl=TL(txt,66,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
    if t>A(147):
        place(img,icon('rr',330,130,40,GRN),340,860,P(t,148,0.4)); place(img,TL('BUY',70,WH),340,860,P(t,148,0.4))
        place(img,icon('rr',330,130,40,RED),740,860,P(t,150,0.4)); place(img,TL('SELL',70,WH),740,860,P(t,150,0.4))
    tx(img,t,152,'Main dekhunga kaun sahi!',58,540,1030,INK)
def s11(img,t):
    ic(img,t,156,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,157,'Follow karo',110,540,640,INK)
    tx(img,t,159,'kal milte hain',130,540,800,OR,'s')
    if t>A(157):
        p=P(t,158,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(18,s2,'r'),(27,s3,'z'),(29,s4,'l'),(38,s5,'u'),(68,s6,'r'),(90,s7,'l'),(106,s8,'u'),(123,s9,'z'),(135,s10,'r'),(156,s11,'l')]
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
