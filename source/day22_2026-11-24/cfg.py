import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/home/claude/work/d22/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Price ne purana high toda, tumne breakout samajh ke buy kar diya, aur agle hi minute price neeche? ~ Mubarak ho, tum turtle soup ban gaye. Haan, tum. Turtle soup matlab fake breakout. Pehle ek purana high ya low hota hai, jahan sabke stop loss aur breakout orders pade hote hain. Price thoda sa upar jaata hai, sirf wick nikalti hai, sab ke orders bhar jaate hain. Phir candle wapas range ke andar close karti hai. Yahi signal hai. Breakout fail, liquidity le li gayi. Entry kab? Jab candle wapas level ke andar close kare, tab sell. Stop loss us wick ke upar, aur target range ka doosra side. ~ Rule yaad rakho. Body bahar close kare to breakout, sirf wick bahar ho to soup. Comment mein likho SOUP. Follow karo, kal milte hain.""".split()
assert len(ROM)==134,len(ROM)
LAUGH=[18,109]
SCENE_STARTS=[0,19,28,33,51,85,110,125,129]
END=EN[-1]+0.7
