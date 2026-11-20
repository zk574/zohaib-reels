import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/tmp/claude-0/-home-claude/5bc59be7-fe36-55cc-93e8-458be3daf313/scratchpad/d19/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Breaker block yaad hai? Aaj uska chhota bhai, mitigation block. ~ Haan, tum, jo breaker aur mitigation mein confuse ho jaate ho. Farq sirf ek hai. Breaker mein price pehle naya high banata hai, liquidity sweep karta hai, phir neeche break karta hai. Mitigation mein price naya high bana hi nahi pata. Lower high banta hai, aur wahi se neeche break. Matlab buyers fail ho gaye. Ab jo log upar phanse hain, woh apna loss nikalna chahte hain. Jab price wapas us lower high wali candle par aata hai, bade players wahan apne purane orders mitigate karte hain, aur price phir se neeche. ~ To rule simple hai. Sweep nahi, lower high, structure break, phir wapas zone par entry. Stop loss us high ke upar. Ab batao, chart par kabhi mitigation block pakda hai? Comment mein likho MB. Follow karo, kal milte hain.""".split()
assert len(ROM)==143,len(ROM)
LAUGH=[10,103]
SCENE_STARTS=[0,11,22,43,66,104,125,138]
END=EN[-1]+0.7
