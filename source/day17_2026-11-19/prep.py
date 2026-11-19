import subprocess,numpy as np,wave,cfg
from cfg import *
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','voice.mp3','-af',f'atempo={TEMPO}','-ar','44100','-ac','1','vo.wav'],check=True)
raw=subprocess.run(['ffmpeg','-loglevel','error','-i','vo.wav','-f','s16le','-ac','1','-ar','44100','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
dur=len(x)/44100
n=int(END*FPS)+2
hop=44100//FPS
env=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) if i*hop<len(x) else 0 for i in range(n)])
env=env/np.percentile(env,95); env=np.clip(env,0,1)
sm=env.copy()
for i in range(1,n): sm[i]=0.55*env[i]+0.45*sm[i-1]
np.save('env.npy',sm)
# music + whooshes
sr=44100; L=int(END*sr)+sr
t=np.arange(L)/sr
bpm=104; beat=60/bpm
m=np.zeros(L)
rng=np.random.default_rng(1)
chords=[[220,261.6,329.6],[174.6,220,261.6],[261.6,329.6,392],[196,246.9,293.7]]
bar=beat*4
for i,tt in enumerate(t[::1]) if False else []: pass
ci=(t//(bar)).astype(int)%4
for k,ch in enumerate(chords):
    mask=(ci==k)
    pad=sum(np.sin(2*np.pi*f*t)*0.5+np.sin(2*np.pi*f*2*t)*0.15 for f in ch)/3
    m+=pad*mask*0.35
# bass
bf=np.array([110,87.3,130.8,98])[ci]
ph=np.cumsum(bf)/sr
m+=np.sin(2*np.pi*ph)*0.25*(0.6+0.4*np.sin(2*np.pi*t/beat*2)**2)
# kick + hat
for b in np.arange(0,END+1,beat):
    i=int(b*sr); l=int(0.18*sr)
    if i+l>L: break
    tt=np.arange(l)/sr
    m[i:i+l]+=np.sin(2*np.pi*(120*np.exp(-tt*25)+45)*tt)*np.exp(-tt*18)*0.7
    j=int((b+beat/2)*sr); h=int(0.04*sr)
    if j+h<L: m[j:j+h]+=rng.standard_normal(h)*np.exp(-np.arange(h)/sr*90)*0.08
m/=np.abs(m).max()
m*=0.16
m*=np.minimum(1,(END-t)/1.2).clip(0,1)
for i in SCENE_STARTS[1:]:
    s=int(max(ST[i]-0.3,0)*sr); l=int(0.3*sr)
    nz=rng.standard_normal(l); 
    k=np.convolve(nz,np.ones(40)/40,mode='same')
    e=np.sin(np.linspace(0,np.pi,l))**2
    m[s:s+l]+=k*e*0.12
vo=np.zeros(L); vo[:len(x)]=x
mix=vo*0.95+m
mix/=max(1,np.abs(mix).max()/0.97)
w=wave.open('mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((mix[:int(END*sr)]*32767).astype(np.int16).tobytes()); w.close()
print(dur,END)
