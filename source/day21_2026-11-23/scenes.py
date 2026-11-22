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
U=mk([60,58,59,56,58,57,54,52,53,50,56,60,64,63,66,63,60,58,61,65,68,71],61,41)
U[4]=[56,58.8,55.6,58]; U[10]=[50,56.6,49.6,56]; U[12]=[60,64.6,59.4,64]; U[17]=[60,60.4,57.2,58]; U[7][2]=51.0; U[9][2]=48.6
BRK_T,BRK_B=58.8,55.6; FVG_B,FVG_T=U[10][1],U[12][2]
def horn(s):
    def f(d,k):
        d.polygon([(s*.5*k,0),(s*.72*k,s*k-1),(s*.28*k,s*k-1)],fill=(232,190,60))
        for i in range(4):
            y=s*(.25+i*.18)*k; d.line([(s*(.5-.06-i*.045)*k,y+8*k),(s*(.5+.06+i*.045)*k,y-6*k)],fill=WH,width=5*k)
    return SS(s,s,f)
def star(img,cx,cy,r,p):
    if p<=0: return
    place(img,SS(2*r,2*r,lambda d,k:d.polygon([(r*k+(r*k if i%2==0 else r*.4*k)*math.cos(math.radians(i*45-90)),r*k+(r*k if i%2==0 else r*.4*k)*math.sin(math.radians(i*45-90))) for i in range(8)],fill=OR)),cx,cy,p,min(1,p*2),t_rot(cx))
def t_rot(x): return 0
def s1(img,t):
    hd(img,t,0,'Breaker block',3,'aur FVG')
    if card(img,t,0,400,260,280,620,WH,OR)>0: place(img,TL('BREAKER',66,OR),280,620,P(t,0))
    if card(img,t,3,400,260,800,620,WH,BLUE)>0: place(img,TL('FVG',90,BLUE),800,620,P(t,3))
    tx(img,t,9,'+',150,540,620,INK,'a')
    if t>A(12):
        p=P(t,12,0.45); place(img,icon('rr',600,140,70,INK),540,920,p,min(1,p*2)); place(img,TL('MILA DO!',70,CREAM),540,920,p,min(1,p*2))
def s2(img,t):
    tx(img,t,15,'Isko kehte hain',80,540,300)
    ic(img,t,18,horn(260),540,560,1,wob(t,1.5,6))
    tx(img,t,18,'UNICORN',170,540,800,INK)
    tx(img,t,19,'model',130,540,960,OR,'s')
    for k,(x,y) in enumerate([(220,500),(860,470),(300,700),(800,720)]):
        star(img,x,y+6*math.sin(t*4+k),28,P(t,18,0.4))
def s3(img,t):
    tx(img,t,20,'HAAN,',130,300,330); tx(img,t,21,'tum.',170,770,320,OR,'s',wob(t,3,2))
    tx(img,t,22,'naam sun ke',80,540,560,INK)
    tx(img,t,25,'hans rahe ho?',110,540,700,OR,'s',wob(t,2,3))
    if t>A(29): pill(img,t,31,'LEKIN SETUP KAAM KA HAI',540,920,GRN,WH,48)
def uchart(img,t,n):
    return chart(img,t,U,n,46,74,'M15')
def s4(img,t):
    hd(img,t,36,'Step 1:',40,'sweep + break')
    ch=uchart(img,t,kp(t,[(A(36)-0.1,0),(A(41),9),(A(46),13)])); X,Y=ch.X,ch.Y; bx1=ch.box[2]
    pl=U[3][2]
    if t>A(40):
        hline(img,Y(pl),X(3),X(10),INK,3); tag(img,t,41,'SWEEP',X(9),Y(U[9][2])+36,RED,WH,24)
    if t>A(44):
        u=ease((t-A(44))/0.4); hline(img,Y(BRK_T),X(4),X(4)+(X(12)-X(4))*u,INK,4); tag(img,t,45,'BOS',X(12),Y(BRK_T)-30,INK,WH,24)
    if t>A(48):
        u=ease((t-A(48))/0.4); zone(img,X(4)-ch.cw*.5,X(4)-ch.cw*.5+(bx1-X(4)+ch.cw*.5)*u,Y(BRK_T),Y(BRK_B),(233,120,66,90))
        tag(img,t,48,'BREAKER BLOCK',X(6),Y(BRK_B)+30,OR,WH,24)
def zones(img,t,ch,show_brk=True,show_fvg=True,hl=0):
    X,Y=ch.X,ch.Y; bx1=ch.box[2]; cw=ch.cw
    if show_brk: zone(img,X(4)-cw*.5,bx1,Y(BRK_T),Y(BRK_B),(233,120,66,70))
    if show_fvg: zone(img,X(10)-cw*.5,bx1,Y(FVG_T),Y(FVG_B),(70,130,190,80))
    if hl>0:
        a=int(90+60*abs(math.sin(t*4)))
        zone(img,X(10)-cw*.5,bx1,Y(min(BRK_T,FVG_T)),Y(max(BRK_B,FVG_B)),(233,190,60,int(a*hl)))
def s5(img,t):
    hd(img,t,53,'Step 2:',59,'usi move mein FVG')
    ch=uchart(img,t,13); X,Y=ch.X,ch.Y
    zones(img,t,ch,True,t>A(59))
    place(img,TL('BREAKER',22,OR),X(6),Y(BRK_B)+22)
    if t>A(59): tag(img,t,59,'FVG',X(14),Y(FVG_T)-26,BLUE,WH,24)
def s6(img,t):
    hd(img,t,63,'Overlap =',78,'Unicorn zone')
    ch=uchart(img,t,13); X,Y=ch.X,ch.Y
    zones(img,t,ch,True,True,ease((t-A(75))/0.5) if t>A(75) else 0)
    if t>A(78):
        tag(img,t,78,'UNICORN ZONE',X(15),Y(min(BRK_T,FVG_T))-30,(200,150,20),WH,26)
        place(img,horn(70),X(10)-60,Y(58),P(t,78,0.4))
    pill(img,t,81,'2 CONFIRMATION, 1 JAGAH',540,1075,INK,CREAM,40)
def s7(img,t):
    hd(img,t,84,'Step 3:',87,'zone mein entry')
    ch=uchart(img,t,kp(t,[(0,13),(A(86),13),(A(92),18),(A(99),18),(A(103)+0.4,22)])); X,Y=ch.X,ch.Y; bx1=ch.box[2]
    zones(img,t,ch,True,True,0.6)
    if t>A(92): tag(img,t,93,'ENTRY',X(17),Y(U[17][2])+40,GRN,WH,26)
    if t>A(94):
        slv=BRK_B-1.2; hline(img,Y(slv),X(10),bx1,RED,4); tag(img,t,94,'SL',X(19),Y(slv)+28,RED,WH,24)
    if t>A(100):
        tv=71.5; u=ease((t-A(100))/0.4); hline(img,Y(tv),X(8),X(8)+(bx1-X(8))*u,GRN,4); tag(img,t,101,'TARGET: LIQUIDITY',X(13),Y(tv)+30,GRN,WH,22)
def s8(img,t):
    hd(img,t,105,'Unicorn',108,'roz nahi milta')
    ic(img,t,107,horn(300),540,640,1,wob(t,1.2,5))
    if t>A(111): pill(img,t,113,'JAB MILE, CHHODNA MAT!',540,950,OR,WH,52)
def s9(img,t):
    hd(img,t,117,'Comment mein likho',120,'UNICORN')
    place(img,icon('rr',900,150,75,WH,INK,5),520,620,P(t,117,0.45))
    place(img,icon('circ',110,OR),920,620,P(t,117,0.45)); place(img,TL('>',70,CREAM),925,618,P(t,117,0.45))
    s='UNICORN'; a=A(119); b=EN[120]
    if t>a:
        n=int(len(s)*min(1,(t-a)/(b-a))); txt=s[:n]
        if txt: tl=TL(txt,80,INK); img.alpha_composite(tl,(110,int(620-tl.height/2)))
def s10(img,t):
    ic(img,t,121,icon('logo',260),540,380,1,wob(t,1.2,3))
    tx(img,t,121,'Follow karo',110,540,640,INK)
    tx(img,t,123,'kal milte hain',130,540,800,OR,'s')
    if t>A(122):
        p=P(t,122,0.45); place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2)); place(img,TL('@chartbendfx',58,CREAM),540,960,p,min(1,p*2))
SC=[(0,s1,'u'),(15,s2,'z'),(20,s3,'r'),(36,s4,'l'),(53,s5,'u'),(63,s6,'z'),(84,s7,'r'),(105,s8,'u'),(117,s9,'l'),(121,s10,'z')]
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
