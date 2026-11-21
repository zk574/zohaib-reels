import json
TEMPO=1.15
FPS=30
W,H=1080,1920
_d=json.load(open('/tmp/claude-0/-home-claude/5bc59be7-fe36-55cc-93e8-458be3daf313/scratchpad/d20/scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Gold naya low bana raha hai, aur tum sell daba rahe ho? ~ Ruko. Pehle silver ko dekho. Haan, tum. Aaj ka concept hai SMT divergence. Gold aur silver aksar saath chalte hain, dono bhai hain. Lekin jab gold naya low banaye, aur silver naya low na banaye, to samjho kuch gadbad hai. Ek bhai neeche gaya, doosre ne mana kar diya. Yehi hai SMT divergence. Matlab neeche ki liquidity sweep ho gayi, aur smart money chupke se buy kar rahi hai. Ab entry kab? Jab gold wapas upar aakar structure break kare. Tab buy, aur stop loss us naye low ke neeche. ~ Ulta bhi same hai. Gold naya high banaye, silver na banaye, to sell ka signal. Yaad rakho, ek chart jhooth bol sakta hai, do chart mushkil se. Comment mein likho SMT. Follow karo, kal milte hain.""".split()
assert len(ROM)==140,len(ROM)
LAUGH=[12,103]
SCENE_STARTS=[0,13,20,36,66,104,119,131,135]
END=EN[-1]+0.7
