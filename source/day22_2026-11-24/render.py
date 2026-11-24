import math,sys,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont
from cfg import *
CREAM=(247,241,232);OR=(233,120,66);INK=(27,26,23);SOFT=(234,223,207);RED=(216,64,47);GRN=(46,158,91);GRY=(150,140,128);WH=(255,255,255)
FD='/usr/share/fonts/truetype/google-fonts/ofl/'
_fc={}
def F(kind,size):
    k=(kind,size)
    if k not in _fc:
        if kind=='m': f=ImageFont.truetype(FD+'montserrat/Montserrat[wght].ttf',size); f.set_variation_by_axes([800])
        elif kind=='s': f=ImageFont.truetype(FD+'gelasio/Gelasio-Italic[wght].ttf',size); f.set_variation_by_axes([700])
        else: f=ImageFont.truetype(FD+'anton/Anton-Regular.ttf',size)
        _fc[k]=f
    return _fc[k]
_tc={}
def TL(s,size,fill=INK,kind='m'):
    k=(s,size,fill,kind)
    if k not in _tc:
        f=F(kind,size); b=f.getbbox(s); w=b[2]+20; h=int(size*1.5)
        im=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(im).text((10,int(size*0.2)),s,font=f,fill=fill+(255,))
        bb=im.getbbox(); _tc[k]=im.crop(bb) if bb else im
    return _tc[k]
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def back(x):
    x=min(max(x,0),1); c=1.70158; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def place(img,lay,cx,cy,s=1,a=1,rot=0):
    if s<=0.01 or a<=0: return
    if s!=1: lay=lay.resize((max(1,int(lay.width*s)),max(1,int(lay.height*s))),Image.BILINEAR)
    if rot: lay=lay.rotate(rot,expand=True,resample=Image.BILINEAR)
    if a<1:
        lay=lay.copy(); al=lay.getchannel('A').point(lambda v:int(v*a)); lay.putalpha(al)
    img.alpha_composite(lay,(int(cx-lay.width/2),int(cy-lay.height/2)))
def SS(w,h,fn,k=2):
    im=Image.new('RGBA',(w*k,h*k),(0,0,0,0)); d=ImageDraw.Draw(im); fn(d,k)
    return im.resize((w,h),Image.LANCZOS)
_ic={}
def icon(name,*a):
    k=(name,)+a
    if k not in _ic: _ic[k]=globals()['mk_'+name](*a)
    return _ic[k]
def mk_rr(w,h,r,fill,outline=None,ow=0):
    return SS(w,h,lambda d,k:d.rounded_rectangle([ow*k//2,ow*k//2,w*k-ow*k//2-1,h*k-ow*k//2-1],r*k,fill=fill,outline=outline,width=ow*k))
def mk_circ(d_,fill,outline=None,ow=0):
    return SS(d_,d_,lambda d,k:d.ellipse([ow*k//2,ow*k//2,d_*k-ow*k//2-1,d_*k-ow*k//2-1],fill=fill,outline=outline,width=ow*k))
def mk_yt(w):
    h=int(w*0.7)
    def f(d,k):
        d.rounded_rectangle([0,0,w*k-1,h*k-1],int(h*0.3)*k,fill=(220,40,40))
        d.polygon([(w*.40*k,h*.28*k),(w*.40*k,h*.72*k),(w*.68*k,h*.5*k)],fill=WH)
    return SS(w,h,f)
def mk_octa(s):
    def f(d,k):
        c=s*k/2; r=s*k/2-4*k
        pts=[(c+r*math.cos(math.radians(22.5+45*i)),c+r*math.sin(math.radians(22.5+45*i))) for i in range(8)]
        d.polygon(pts,fill=RED); r2=r-14*k
        pts=[(c+r2*math.cos(math.radians(22.5+45*i)),c+r2*math.sin(math.radians(22.5+45*i))) for i in range(8)]
        d.polygon(pts,outline=WH,width=7*k)
    return SS(s,s,f)
def mk_nosign(s):
    def f(d,k):
        d.ellipse([8*k,8*k,(s-8)*k,(s-8)*k],fill=WH,outline=RED,width=22*k)
        c=s*k/2
        for dy in(-30,10):
            d.line([(c-45*k,c+(dy+20)*k),(c,c+dy*k),(c+45*k,c+(dy+20)*k)],fill=INK,width=16*k,joint='curve')
        d.line([(s*.22*k,s*.78*k),(s*.78*k,s*.22*k)],fill=RED,width=22*k)
    return SS(s,s,f)
def mk_phone(w):
    h=int(w*1.9)
    def f(d,k):
        d.rounded_rectangle([0,0,w*k-1,h*k-1],int(w*.16)*k,fill=INK)
        d.rounded_rectangle([int(w*.06)*k,int(w*.06)*k,(w-int(w*.06))*k,(h-int(w*.06))*k],int(w*.12)*k,fill=CREAM)
        cx=w*k/2;cy=h*k*.45
        d.ellipse([cx-w*.28*k,cy-w*.28*k,cx+w*.28*k,cy+w*.28*k],fill=OR)
        d.polygon([(cx-w*.08*k,cy-w*.14*k),(cx-w*.08*k,cy+w*.14*k),(cx+w*.16*k,cy)],fill=WH)
        d.rounded_rectangle([w*.2*k,h*.8*k,w*.8*k,h*.84*k],8*k,fill=SOFT)
        d.rounded_rectangle([w*.2*k,h*.88*k,w*.6*k,h*.92*k],8*k,fill=SOFT)
    return SS(w,h,f)
def mk_logo(s):
    def f(d,k):
        d.rounded_rectangle([0,0,s*k-1,s*k-1],int(s*.24)*k,fill=OR)
        for i,(x,hh,off) in enumerate([(.26,.34,.30),(.5,.5,.2),(.74,.28,.42)]):
            cx=s*x*k; top=(s*off)*k; bot=top+s*hh*k
            d.line([(cx,top-s*.07*k),(cx,bot+s*.07*k)],fill=CREAM,width=int(s*.035*k))
            d.rounded_rectangle([cx-s*.07*k,top,cx+s*.07*k,bot],int(s*.02*k),fill=CREAM if i!=1 else INK)
    return SS(s,s,f)
def mk_check(s,good):
    def f(d,k):
        d.ellipse([0,0,s*k-1,s*k-1],fill=GRN if good else RED)
        if good: d.line([(s*.27*k,s*.52*k),(s*.44*k,s*.68*k),(s*.74*k,s*.33*k)],fill=WH,width=int(s*.12*k),joint='curve')
        else:
            d.line([(s*.3*k,s*.3*k),(s*.7*k,s*.7*k)],fill=WH,width=int(s*.12*k)); d.line([(s*.7*k,s*.3*k),(s*.3*k,s*.7*k)],fill=WH,width=int(s*.12*k))
    return SS(s,s,f)
def mk_pin(s):
    w=int(s*.7)
    def f(d,k):
        cx=w*k/2;r=w*k/2
        d.ellipse([0,0,w*k-1,w*k-1],fill=OR)
        d.polygon([(cx-r*.82,r*1.35),(cx+r*.82,r*1.35),(cx,s*k-2)],fill=OR)
        d.ellipse([cx-r*.38,r-r*.38,cx+r*.38,r+r*.38],fill=CREAM)
    return SS(w,s,f)
def mk_star(s):
    def f(d,k):
        c=s*k/2; pts=[]
        for i in range(32):
            r=c-3*k if i%2==0 else c*0.86
            a=math.radians(i*11.25); pts.append((c+r*math.cos(a),c+r*math.sin(a)))
        d.polygon(pts,fill=OR)
        d.ellipse([c-c*.8,c-c*.8,c+c*.8,c+c*.8],outline=CREAM,width=5*k)
    return SS(s,s,f)
def mk_avatar(s,filled):
    def f(d,k):
        fill=OR if filled else SOFT; ln=OR if filled else GRY
        d.ellipse([2*k,2*k,s*k-2*k,s*k-2*k],fill=fill,outline=ln,width=5*k)
        c=s*k/2
        hc=INK if filled else GRY
        d.ellipse([c-s*.16*k,s*.2*k,c+s*.16*k,s*.2*k+s*.32*k],fill=CREAM if filled else (200,190,175))
        d.pieslice([c-s*.3*k,s*.55*k,c+s*.3*k,s*1.1*k],180,360,fill=CREAM if filled else (200,190,175))
    return SS(s,s,f)
def mk_laptop(w):
    h=int(w*.66)
    def f(d,k):
        d.rounded_rectangle([w*.1*k,0,w*.9*k,h*.78*k],int(w*.04*k),fill=INK)
        d.rounded_rectangle([w*.14*k,w*.04*k,w*.86*k,h*.74*k],int(w*.02*k),fill=CREAM)
        d.rounded_rectangle([0,h*.8*k,w*k-1,h*k-1],int(w*.03*k),fill=(60,58,54))
    return SS(w,h,f)
def mk_bubble(w,h,fill,tail=True):
    def f(d,k):
        d.rounded_rectangle([0,0,w*k-1,(h-26)*k],int(h*.3)*k,fill=fill)
        if tail: d.polygon([(w*.12*k,(h-30)*k),(w*.12*k+50*k,(h-30)*k),(w*.1*k,(h-2)*k)],fill=fill)
    return SS(w,h,f)
def mk_monitor(w):
    h=int(w*.72)
    def f(d,k):
        d.rounded_rectangle([0,0,w*k-1,h*.86*k],int(w*.04)*k,fill=INK)
        d.rounded_rectangle([w*.03*k,w*.03*k,w*.97*k,h*.83*k],int(w*.025)*k,fill=CREAM)
        d.rectangle([w*.4*k,h*.86*k,w*.6*k,h*.95*k],fill=INK); d.rounded_rectangle([w*.28*k,h*.94*k,w*.72*k,h*k-1],8*k,fill=INK)
        import random; r=random.Random(5); y=h*.5
        x0=w*.1; 
        for i in range(11):
            o=y+r.uniform(-.2,.1)*h; c=r.uniform(.05,.14)*h; up=r.random()<.55
            col=GRN if up else RED; x=(x0+i*w*.075)*k
            d.line([(x,(o-c-.05*h)*k),(x,(o+.05*h)*k)],fill=col,width=3*k)
            d.rectangle([x-9*k,(o-c/2)*k,x+9*k,(o+c/2)*k],fill=col)
            y=o-(.02*h if up else -.02*h)
    return SS(w,h,f)
# ---------- kid ----------
def kid_sprite(m,pose):
    k=2; Wd,Hd=440,560
    im=Image.new('RGBA',(Wd*k,Hd*k),(0,0,0,0)); d=ImageDraw.Draw(im)
    S=lambda *v:[x*k for x in v]
    SK=(233,183,150);BK=(23,23,26)
    d.ellipse(S(100,512,340,548),fill=(0,0,0,38))
    # legs
    for side,(dx,lift) in (('l',pose['lf']),('r',pose['rf'])):
        x=165+dx if side=='l' else 235+dx
        d.rounded_rectangle(S(x,395,x+40,505-lift),10*k,fill=(43,47,58))
        d.rounded_rectangle(S(x-14,495-lift,x+54,530-lift),16*k,fill=OR)
        d.rectangle(S(x-12,520-lift,x+52,527-lift),fill=WH)
    # left arm (viewer left)
    a=math.radians(pose['la']); sx,sy=148,288
    hx,hy=sx+105*math.sin(a)*-1,sy+105*math.cos(a)
    d.line(S(sx,sy,hx,hy),fill=BK,width=34*k); d.ellipse(S(sx-17,sy-17,sx+17,sy+17),fill=BK)
    d.ellipse(S(hx-17,hy-17,hx+17,hy+17),fill=SK)
    # torso
    d.rounded_rectangle(S(128,250,312,425),44*k,fill=BK)
    d.ellipse(S(160,228,280,300),fill=(40,40,46))
    d.line(S(205,288,200,335),fill=WH,width=4*k);d.line(S(235,288,240,335),fill=WH,width=4*k)
    d.ellipse(S(196,333,205,342),fill=WH);d.ellipse(S(236,333,245,342),fill=WH)
    d.rounded_rectangle(S(168,372,272,408),12*k,outline=(60,60,66),width=3*k)
    d.ellipse(S(206,314,234,342),fill=OR)
    # hood behind head
    d.ellipse(S(122,78,318,268),fill=BK)
    # right arm with stick
    a=math.radians(pose['ra']); sx,sy=296,288
    hx,hy=sx+105*math.sin(a),sy-105*math.cos(a)*-1 if False else sy+105*math.cos(a)
    d.line(S(sx,sy,hx,hy),fill=BK,width=34*k); d.ellipse(S(sx-17,sy-17,sx+17,sy+17),fill=BK)
    sa=math.radians(pose['sa'])
    ex,ey=hx+200*math.sin(sa),hy-200*math.cos(sa)
    d.line(S(hx,hy,ex,ey),fill=(201,139,74),width=9*k)
    d.ellipse(S(ex-11,ey-11,ex+11,ey+11),fill=OR)
    d.ellipse(S(hx-18,hy-18,hx+18,hy+18),fill=SK)
    # head
    d.ellipse(S(130,168,156,196),fill=SK);d.ellipse(S(284,168,310,196),fill=SK)
    d.ellipse(S(142,97,298,253),fill=SK)
    d.chord(S(142,97,298,253),198,342,fill=BK)
    # brows
    bo=pose['br']
    d.line(S(168,138-bo,208,134-bo),fill=BK,width=5*k);d.line(S(232,134-bo,272,138-bo),fill=BK,width=5*k)
    # glasses
    for cx in(190,250):
        d.ellipse(S(cx-29,143,cx+29,201),fill=(255,255,255,215),outline=INK,width=6*k)
        px=cx+pose['ex']
        d.ellipse(S(px-8,166,px+8,182),fill=BK);d.ellipse(S(px-3,168,px+1,172),fill=WH)
    d.line(S(219,170,221,170),fill=INK,width=6*k)
    d.line(S(132,168,161,172),fill=INK,width=5*k);d.line(S(279,172,308,168),fill=INK,width=5*k)
    d.ellipse(S(150,198,178,214),fill=(240,150,130,110));d.ellipse(S(262,198,290,214),fill=(240,150,130,110))
    # mouth
    mw=34+26*m+pose['mw']; mh=3+34*m
    cy=224
    if m<0.1 and not pose['sm']:
        d.arc(S(220-18,cy-14,220+18,cy+6),20,160,fill=(110,50,40),width=4*k)
    elif m<0.1:
        d.chord(S(220-24,cy-12,220+24,cy+14),0,180,fill=(110,40,40))
    else:
        d.ellipse(S(220-mw/2,cy-mh/3,220+mw/2,cy+mh*2/3),fill=(100,32,34))
        d.ellipse(S(220-mw/3.2,cy+mh*0.25,220+mw/3.2,cy+mh*2/3-1),fill=(226,110,120))
    return im
def kid_frame(t,m,pose,x,feet=1890,ks=0.46*1.0):
    sp=kid_sprite(m,pose)
    # tilt about feet
    if pose['tilt']: sp=sp.rotate(pose['tilt'],center=(220*2,530*2),resample=Image.BILINEAR)
    w=int(sp.width*ks*1.0); h=int(sp.height*ks*1.0)
    sc=pose['spin']
    ww=max(2,int(w*abs(sc)))
    sp=sp.resize((ww,h),Image.LANCZOS)
    if sc<0: sp=sp.transpose(Image.FLIP_LEFT_RIGHT)
    return sp,int(x-ww/2),int(feet-pose['dy']-530*ks*2/2*1.0-(h-560*ks*2/2*1.0*0)+0) 
# ---------- timeline ----------
def A(i): return ST[i]-0.12
def P(t,i,d=0.4): return back((t-A(i))/d)       # pop 0..~1.1
def Ea(t,i,d=0.3): return ease((t-A(i))/d)
def LA(): 
    return [(ST[i],EN[i]) for i in LAUGH]
env=np.load('/home/claude/work/d22/env.npy')
def pose_at(t):
    p=dict(lf=(0,0),rf=(0,0),la=-12,ra=40,sa=25,br=0,ex=5,mw=0,sm=False,tilt=0,dy=0,spin=1.0)
    x=540; m=float(env[min(int(t*FPS),len(env)-1)])
    sw=math.sin(2*math.pi*1.2*t)
    p['dy']=abs(sw)*4; p['ra']=38+6*sw; p['sa']=22+8*sw
    for i in LAUGH:
        s,e=ST[i],EN[i]
        if s-0.05<=t<=e+0.35:
            m=0.55+0.45*abs(math.sin(2*math.pi*6*t)); p['dy']=abs(math.sin(2*math.pi*3*t))*40; p['tilt']=math.sin(2*math.pi*3*t)*5
            p['sm']=True; p['br']=8; p['la']=-30; p['ra']=60
    if ST[26]<=t<=EN[27]+0.2:
        p['ra']=80; p['sa']=70; p['ex']=6; p['br']=6
    if ST[79]-0.1<=t<=EN[80]+0.2: p['ra']=150; p['sa']=0; p['br']=5; p['ex']=0
    if ST[51]-0.1<=t<=EN[59]+0.2:
        u=(t-ST[51]); span=EN[59]-ST[51]+0.2
        x=540-130*math.sin(min(1,max(0,u/span))*math.pi)
        ph=u*7
        p['lf']=(int(14*math.sin(ph)),int(max(0,math.sin(ph+1.6))*14)); p['rf']=(int(-14*math.sin(ph)),int(max(0,-math.sin(ph+1.6))*14))
        p['tilt']=-6; p['ra']=100; p['sa']=40; p['la']=-20
    for i in (31,96):
        if ST[i]-0.1<=t<=ST[i]+0.8:
            u=(t-(ST[i]-0.1))/0.9
            p['dy']=abs(math.sin(math.pi*u))*100; p['ra']=150;p['sa']=10; p['br']=10; p['sm']=True
    for a_,b_ in ((125,128),(129,132)):
        if ST[a_]<=t<=EN[b_]:
            u=t*3.6
            p['tilt']=math.sin(u)*8; p['dy']=abs(math.sin(u))*26; p['la']=-60+50*math.sin(u); p['ra']=70+40*math.sin(u+math.pi); p['sa']=30+30*math.sin(u)
            p['lf']=(int(10*math.sin(u)),int(max(0,math.sin(u))*12)); p['rf']=(int(-10*math.sin(u)),int(max(0,-math.sin(u))*12)); p['sm']=True
    if ST[133]-0.2<=t:
        u=min(1,(t-(ST[133]-0.2))/0.9); p['spin']=math.cos(2*math.pi*u); p['dy']=abs(math.sin(math.pi*u))*100
    if abs(p['spin'])<0.08: p['spin']=0.08 if p['spin']>=0 else -0.08
    return p,m,x
# ---------- captions ----------
GR=[];cur=[]
for i,w in enumerate(ROM):
    if w=='~': 
        if cur: GR.append(cur);cur=[]
        continue
    cur.append(i)
    if w[-1] in ',.?!' or len(cur)>=4:
        GR.append(cur);cur=[]
if cur: GR.append(cur)
def caption(img,t):
    g=None
    for j,gr in enumerate(GR):
        s=ST[gr[0]]-0.25
        e=(ST[GR[j+1][0]]-0.25) if j+1<len(GR) else END
        if s<=t<e or (j==0 and t<e): g=gr;break
    if g is None: return
    for i in LAUGH:
        if ST[i]-0.1<=t<=EN[i]+0.1: g=None
    if g is None:
        for i in LAUGH:
            if ST[i]-0.1<=t<=EN[i]+0.1:
                tl=TL('HA HA HA!',150,OR,'s'); place(img,tl,540,1260,1+0.05*math.sin(t*20),1,math.sin(t*14)*3)
        return
    toks=[(i,ROM[i].upper().rstrip(',.?')+('?' if ROM[i].endswith('?') else '')) for i in g]
    f=F('m',92); 
    # wrap to 2 lines
    def width(ts): return sum(f.getlength(s) for _,s in ts)+22*(len(ts)-1)
    lines=[toks]
    if width(toks)>960:
        for k in range(1,len(toks)):
            a,b=toks[:k],toks[k:]
            if width(a)<=960 and width(b)<=960: lines=[a,b];break
    d=ImageDraw.Draw(img)
    y0=1195 if len(lines)==2 else 1235
    for li,ln in enumerate(lines):
        x=540-width(ln)/2; y=y0+li*118
        for i,s in ln:
            if t<ST[i]-0.25: x+=f.getlength(s)+22; continue
            cur_=(t>=ST[i]-0.25) and (t<ST[i+1]-0.25 if i+1<len(ST) else True)
            col=OR if cur_ else INK
            d.text((x+3,y+4),s,font=f,fill=(0,0,0,40) if False else SOFT)
            d.text((x,y),s,font=f,fill=col)
            x+=f.getlength(s)+22
exec(open('/home/claude/work/d22/scenes.py').read())
# ---------- bg ----------
def make_bg():
    im=Image.new('RGBA',(W,H),CREAM+(255,)); d=ImageDraw.Draw(im)
    for x in range(0,W,60): d.line([(x,0),(x,H)],fill=(236,228,214,255),width=1)
    for y in range(0,H,60): d.line([(0,y),(W,y)],fill=(236,228,214,255),width=1)
    d.rectangle([0,1862,W,H],fill=SOFT)
    d.line([(0,1862),(W,1862)],fill=OR,width=6)
    return im
BG=make_bg()
def topbar(img,t):
    place(img,icon('logo',70),95,105)
    tb=TL('CHART BENDER FX',44,INK); place(img,tb,160+tb.width/2,102)
    pill=icon('rr',250,64,32,OR); place(img,pill,935,105)
    place(img,TL('SMC · DAY 22',30,CREAM),935,105)
def frame(t):
    img=BG.copy()
    topbar(img,t)
    draw_scenes(img,t)
    caption(img,t)
    p,m,x=pose_at(t)
    sp=kid_sprite(m,p)
    if p['tilt']: sp=sp.rotate(p['tilt'],center=(440,1060),resample=Image.BILINEAR)
    ks=0.5
    w=int(sp.width*ks);h=int(sp.height*ks)
    ww=max(2,int(w*abs(p['spin'])))
    sp=sp.resize((ww,h),Image.LANCZOS)
    if p['spin']<0: sp=sp.transpose(Image.FLIP_LEFT_RIGHT)
    # feet at sprite y=530*2*ks from top
    fy=int(530*2*ks)
    img.alpha_composite(sp,(int(x-ww/2),int(1880-fy-p['dy'])))
    return img.convert('RGB')
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2]); out=sys.argv[3]
    pr=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for f in range(a,b): pr.stdin.write(frame(f/FPS).tobytes())
    pr.stdin.close(); pr.wait()
