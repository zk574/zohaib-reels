import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/tmp/claude-0/-home-claude/5bc59be7-fe36-55cc-93e8-458be3daf313/scratchpad/d17/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Tum entry bilkul sahi lete ho, phir bhi stop loss hit ho jata hai. Pata hai kyun? ~ Kyunki tum bina bias ke trade le rahe ho. Haan, tum. Bias matlab market ka rukh. Aaj sirf teen step. Step ek: Daily chart kholo. Dekho price premium mein hai ya discount mein aur last structure break kis taraf hua. Upar break hua to bullish bias, neeche hua to bearish. Step do: 4 hour par apna point of interest dhoondo. Order block ya FVG, wahi jahan bade players ka order pada hai. Step teen: ab 15 minute par jao. Wahan sweep, choch aur entry ka wait karo. ~ Rule yaad rakho, daily bias bullish hai to sirf buy dhoondo. Sell ka khayal bhi mat lana, kyunki bade time frame ke khilaf trade matlab current ke khilaf tairna. Ab batao, tumhara aaj ka bias kya hai? Comment mein likho bias aur buy ya sell. Main dekhunga kaun-kaun sahi hai. ~ Follow karo, kal milte hain.""".split()
assert len(ROM)==162,len(ROM)
LAUGH=[17,105,156]
SCENE_STARTS=[0,18,27,29,38,68,90,106,123,135,156]
END=EN[-1]+0.7
