def tx(img,t,i,s,size,cx,cy,fill=INK,kind='m',rot=0,sc=1):
    p=P(t,i)
    if p<=0: return
    place(img,TL(s,size,fill,kind),cx,cy,p*sc,min(1,p*2),rot)
def ic(img,t,i,lay,cx,cy,sc=1,rot=0,dy=0):
    p=P(t,i)
    if p<=0: return
    place(img,lay,cx,cy+dy,p*sc,min(1,p*2),rot)
def wob(t,f=1.5,a=8): return math.sin(2*math.pi*f*t)*a
def s1a(img,t):
    tx(img,t,0,'TRADING',175,540,330)
    tx(img,t,1,'seekhni hai?',150,540,520,OR,'s')
    ic(img,t,4,icon('yt',440),540,810,1,wob(t,1,2))
    if t>A(8):
        ic(img,t,9,icon('check',120,False),760,860)
        tx(img,t,8,'THAK GAYE?',100,540,1010)
def s1b(img,t):
    tx(img,t,12,'HAAN,',210,540,330)
    tx(img,t,13,'tum.',300,540,590,OR,'s',wob(t,3,2))
    ic(img,t,17,icon('phone',300),540,880,1,wob(t,1.2,4))
    tx(img,t,16,'YEH REEL',70,540,1050) if False else None
def s1c(img,t):
    ic(img,t,21,icon('octa',420),540,450,1,wob(t,2,3))
    tx(img,t,21,'RUKO',110,540,450,WH)
    ic(img,t,22,icon('nosign',300),540,850,1,0)
    tx(img,t,22,'SCROLL MAT KARNA',72,540,1030)
def s2a(img,t):
    ic(img,t,30,icon('logo',380),540,430,1,wob(t,1,3))
    tx(img,t,31,'CHART BENDER',125,540,740)
    tx(img,t,32,'FX',140,350,900,OR,'s')
    tx(img,t,33,'INSTITUTE',100,690,905)
def s2b(img,t):
    ic(img,t,34,icon('monitor',700),540,500)
    if t>A(37):
        pulse=0.5+0.5*math.sin(t*9)
        place(img,icon('rr',200,70,35,RED),300,235,P(t,37))
        place(img,TL('LIVE',44,WH),322,236,P(t,37))
        place(img,icon('circ',22,(255,255,255,int(150+100*pulse))),240,236,P(t,37))
    tx(img,t,37,'live',160,250,930,OR,'s')
    tx(img,t,38,'CLASSES',130,700,930)
def s2c(img,t):
    rows=[('RECORDED VIDEO',False,39,41),('ASLI MENTOR',True,42,42),('ASLI CHART',True,44,44),('LIVE SAWAL-JAWAB',True,47,47)]
    for n,(s,g,i,ic_i) in enumerate(rows):
        y=290+n*190
        p=P(t,i)
        if p<=0: continue
        card=icon('rr',900,150,36,WH if g else SOFT,SOFT if g else GRY,3)
        place(img,card,540,y,p,min(1,p*2))
        if t>A(ic_i)+0.15 or g: place(img,icon('check',90,g),150,y,P(t,ic_i) if g else P(t,41),1)
        else: place(img,icon('circ',90,SOFT),150,y)
        tl=TL(s,60 if len(s)<14 else 52,GRY if not g else INK)
        place(img,tl,560+0,y,p,min(1,p*2))
        if not g and t>A(41): 
            u=ease((t-A(41))/0.3); w=tl.width*u
            ImageDraw.Draw(img).line([(560-tl.width/2,y),(560-tl.width/2+w,y)],fill=RED,width=7)
def s2d(img,t):
    tx(img,t,50,'INSTITUTE',90,540,290)
    ic(img,t,51,icon('pin',360),540,590,1,0,-abs(math.sin(t*5))*18)
    tx(img,t,51,'Karachi',230,540,900,OR,'s')
    tx(img,t,52,'MEIN HAI',80,540,1030)
def s3a(img,t):
    tx(img,t,55,'AB SABSE',150,540,330)
    tx(img,t,57,'zaroori',230,540,580,OR,'s')
    tx(img,t,58,'BAAT!',210,540,830)
def s3b(img,t):
    tx(img,t,59,'PEHLE 5 STUDENTS',88,540,260)
    for n in range(5):
        ic(img,t,60,icon('avatar',130,True),540+(n-2)*160,430,1,0)  if t>A(60)+n*0.1 else None
    if t>A(64):
        p=P(t,64,0.5)
        place(img,icon('star',560),540,860,p*(1+0.02*math.sin(t*8)),min(1,p*2),wob(t,1,2))
        place(img,TL('50%',210,CREAM,'a'),540,840,p,min(1,p*2))
        place(img,TL('DISCOUNT',54,CREAM),540,985,p,min(1,p*2))
    if t>A(66):
        p=P(t,66,0.35)
        place(img,icon('rr',300,100,16,CREAM,RED,8),840,1000,p,min(1,p*2),-9)
        place(img,TL('SIRF 5',64,RED),840,1000,p,min(1,p*2),-9)
def s3c(img,t):
    tx(img,t,68,'SEATS',160,540,300)
    tx(img,t,69,'limited',190,540,500,OR,'s')
    fill=[A(72),A(73),A(74),A(75),A(75)+0.3]
    for n in range(5):
        ic(img,t,68,icon('avatar',150,t>fill[n]),540+(n-2)*170,760,1,0)
    tx(img,t,72,'JALDI BHAR RAHI HAIN',62,540,960,RED if int(t*4)%2==0 else INK)
def s4a(img,t):
    tx(img,t,76,'Karachi',200,540,320,OR,'s')
    tx(img,t,77,'SE HO?',150,540,510)
    ic(img,t,79,icon('pin',300),540,790,1,0,-abs(math.sin(t*5))*14)
    tx(img,t,81,'LIVE CLASSES KA ADDRESS?',56,540,1030)
def s4b(img,t):
    ic(img,t,84,icon('bubble',760,300,OR),540,420)
    tx(img,t,84,'DM KARO',165,540,400,CREAM)
    if t>A(86):
        p=P(t,86)
        place(img,icon('rr',820,230,40,WH,SOFT,3),540,800,p,min(1,p*2))
        place(img,icon('pin',140),230,800,p,min(1,p*2))
        place(img,TL('ADDRESS',90,INK),620,770,p,min(1,p*2))
        place(img,TL('MIL JAYEGA',70,OR,'s'),620,850,p,min(1,p*2))
def s5a(img,t):
    tx(img,t,89,'India',210,540,320,OR,'s')
    tx(img,t,90,'SE HO?',140,540,500)
    ic(img,t,94,icon('laptop',560),540,790,1,0,wob(t,1,5))
    if t>A(94): place(img,TL('ONLINE',92,OR),540,770,P(t,94),1)
    tx(img,t,95,'CLASSES AVAILABLE',72,540,1010)
def s5b(img,t):
    ic(img,t,98,icon('bubble',800,330,OR),540,560,1+0.03*math.sin(t*10))
    tx(img,t,99,'BAS DM KARO',120,540,540,CREAM)
def s6a(img,t):
    tx(img,t,101,'TO ABHI',120,540,290)
    tx(img,t,103,'DM mein likho:',100,540,470,OR,'s')
    place(img,icon('rr',900,150,75,WH,INK,5),520,700)
    place(img,icon('circ',110,OR),920,700)
    place(img,TL('>',70,CREAM),925,698)
    s='FOREX TRADING'; a=A(105); b=EN[107]-0.12
    n=int(len(s)*min(1,max(0,(t-a)/(b-a)))) if t>a else 0
    txt=s[:n]
    if txt: 
        tl=TL(txt,66,INK); img.alpha_composite(tl,(110,int(700-tl.height/2)))
    if int(t*2.5)%2==0 and t<EN[107]+0.2:
        cx=110+(TL(txt,66,INK).width if txt else 0)+8; ImageDraw.Draw(img).rectangle([cx,665,cx+5,735],fill=OR)
    if t>EN[107]-0.05:
        p=P(t,107,0.4) if False else back((t-(EN[107]-0.05))/0.4)
        place(img,icon('bubble',760,200,OR),540,950,p,min(1,p*2))
        place(img,TL('FOREX TRADING',78,CREAM),540,930,p,min(1,p*2))
def s6b(img,t):
    tx(img,t,108,'FIRST 5 MEIN',120,540,290)
    tx(img,t,112,'kaun-kaun?',170,540,480,OR,'s')
    for n in range(5):
        i=113+n if 113+n<=117 else 117
        p=back((t-(A(113)+n*0.28))/0.4)
        if p>0:
            place(img,icon('circ',150,OR),540+(n-2)*180,760,p,min(1,p*2))
            place(img,TL(str(n+1),110,CREAM,'a'),540+(n-2)*180,755,p,min(1,p*2))
    tx(img,t,116,'AATA HAI?',70,540,980)
def s7a(img,t):
    tx(img,t,118,'YAAD RAKHO',100,540,290,OR,'s')
    tx(img,t,120,'PEHLE 5',250,540,520)
    if t>A(122):
        p=P(t,122,0.5)
        place(img,icon('star',560),540,860,p,min(1,p*2),wob(t,1,3))
        place(img,TL('50% OFF',150,CREAM,'a'),540,860,p,min(1,p*2))
def s7b(img,t):
    ic(img,t,126,icon('logo',260),540,430,1,wob(t,1.2,3))
    tx(img,t,127,'CHART BENDER FX',92,540,690)
    tx(img,t,124,'@chartbendfx',90,540,810,OR,'s')
    if t>A(124):
        p=P(t,125)
        place(img,icon('rr',520,120,60,OR),540,960,p,min(1,p*2))
        place(img,TL('FOLLOW',74,CREAM),540,960,p,min(1,p*2))
    tx(img,t,130,'APNI SEAT PAKKI KARO',58,540,1060)
SC=[(0,s1a,'u'),(12,s1b,'r'),(21,s1c,'z'),(30,s2a,'l'),(34,s2b,'u'),(39,s2c,'r'),(50,s2d,'z'),(55,s3a,'l'),(59,s3b,'u'),(68,s3c,'r'),(76,s4a,'z'),(84,s4b,'l'),(89,s5a,'u'),(98,s5b,'z'),(101,s6a,'r'),(108,s6b,'u'),(118,s7a,'z'),(124,s7b,'l')]
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
