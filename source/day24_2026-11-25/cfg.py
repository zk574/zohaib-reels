import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/home/claude/work/d24/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Ek FVG upar jaate waqt bana, ek FVG neeche aate waqt. Tum confuse ho gaye ki kaunsa use karein? ~ Haan, tum. Jawab hai, dono. Isko kehte hain BPR, Balanced Price Range. Pehle price tezi se neeche gaya, aur ek bearish FVG chhod gaya. Phir price tezi se wapas upar aaya, aur ek bullish FVG bana. Ab dekho, dono gaps jahan ek doosre ke upar aa jaate hain, wahi hissa hai BPR. Matlab market ne wahan dono taraf ka kaam pura kar liya. Ye zone bahut strong hota hai. Jab price wapas BPR mein aaye, to entry. Stop loss zone ke doosri taraf, aur target agla high. ~ Do gap mile, ek zone bana, aur tumhara confusion khatam. Comment mein likho BPR. Follow karo, kal milte hain.""".split()
assert len(ROM)==127,len(ROM)
LAUGH=[19,107]
SCENE_STARTS=[0,20,32,56,89,108,118,122]
END=EN[-1]+0.7
