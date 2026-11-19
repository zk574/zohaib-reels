import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/tmp/claude-0/-home-claude/5bc59be7-fe36-55cc-93e8-458be3daf313/scratchpad/d18/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Stop loss lagate ho kahan? ~ Wahan jahan dukh kam ho? Haan, tum. Market tumhara dard nahi dekhti, structure dekhti hai. Rule ek: stop loss hamesha swing low ya swing high ke peeche, thoda neeche, kyunki wahi wo jagah hai jahan tumhara idea galat sabit hota hai. Rule do: candle ke bilkul neeche mat lagao. Wick wahan aakar tumhe uda degi. Rule teen: pehle stop loss, phir lot size. Risk sirf 1%. Lot size stop loss se nikalta hai, dil se nahi. ~ Aur risk reward? 1:3 to teen se kam mat lo. Teen trade mein do galat bhi hui, to bhi tum green ho. Socho, 10 trade, chhe loss, chaar jeet, phir bhi account upar. Ye hai maths ka jadoo. Comment mein likho RR aur batao tumhara risk reward kya hai? ~ Follow karo, kal milte hain.""".split()
assert len(ROM)==138,len(ROM)
LAUGH=[5,82,132]
SCENE_STARTS=[0,6,13,21,47,61,83,105,121,133]
END=EN[-1]+0.7
