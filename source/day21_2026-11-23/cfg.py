import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/tmp/claude-0/-home-claude/5bc59be7-fe36-55cc-93e8-458be3daf313/scratchpad/d21/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Breaker block aur FVG, dono alag alag yaad hain? Ab dono ko mila do. ~ Isko kehte hain Unicorn model. Haan, tum, naam sun ke hans rahe ho na? Lekin ye setup bahut kaam ka hai. Step ek: price pehle liquidity sweep kare, aur structure break kare. Wahan breaker block ban jata hai. Step do: usi move mein ek FVG bhi chhoot jaye. Ab dekho, jahan breaker aur FVG ek doosre ke upar aa jayein, wahi overlap hai Unicorn zone. Do confirmation, ek jagah. Step teen: price wapas us zone mein aaye, to entry. Stop loss breaker ke peeche, aur target agla liquidity pool. ~ Yaad rakho, unicorn roz nahi milta. Isliye jab mile, to chhodna mat. Comment mein likho UNICORN. Follow karo, kal milte hain.""".split()
assert len(ROM)==126,len(ROM)
LAUGH=[14,104]
SCENE_STARTS=[0,15,20,36,53,63,84,105,117,121]
END=EN[-1]+0.7
