import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/home/claude/work/d23/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Roz chart pe sau lines kheenchte ho? ~ Bas do lines kaafi hain. Haan, tum. Kal ka high, aur kal ka low. PDH aur PDL. Kyun? Kyunki kal jo log buy kar ke baithe the, unka stop loss kal ke low ke neeche hai. Aur jo sell kar ke baithe the, unka stop kal ke high ke upar. Matlab dono taraf liquidity ka dher. Aaj market pehle in mein se ek ko touch karegi. Agar price PDH ke upar wick maar ke wapas aaye, to sell dhoondo. Agar PDL ke neeche wick maar ke wapas aaye, to buy dhoondo. ~ Aur agar body ke saath close ho jaye, to breakout hai, ulta mat jaana. Kal raat ko sirf do lines lagao, aur subah ka plan ready. Comment mein likho PDH. Follow karo, kal milte hain.""".split()
assert len(ROM)==135,len(ROM)
LAUGH=[7,99]
SCENE_STARTS=[0,8,25,64,87,100,114,126,130]
END=EN[-1]+0.7
