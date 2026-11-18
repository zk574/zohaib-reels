import json
TEMPO=1.2
FPS=30
W,H=1080,1920
_d=json.load(open('./scribe.json'))
WORDS=[x for x in _d['segments'][0]['words'] if x['text'].strip()]
ST=[x['start_time']/TEMPO for x in WORDS]
EN=[x['end_time']/TEMPO for x in WORDS]
ROM="""Trading seekhni hai, lekin YouTube se seekh-seekh ke thak gaye ho? ~ Haan, tum jo abhi yeh reel dekh rahe ho. Ruko, scroll mat karna kyunki yeh tumhare liye hai. Chart Bender FX Institute, yahan milti hain live classes, recorded video nahi, asli mentor, asli chart aur live sawal-jawab aur institute Karachi mein hai. ~ Ab sabse zaroori baat, pehle paanch students ko milega 50% discount. Sirf paanch. Seats limited hain aur jaldi bhar rahi hain. Karachi se ho? Live classes ka address chahiye? DM karo, address mil jayega. India se ho? tumhare liye online classes available hain. Bas DM karo. To abhi DM mein likho Forex Trading. Main dekhna chahta hoon kaun-kaun pehle paanch mein aata hai. Yaad rakho, pehle paanch, 50% off. Follow karo Chart Bender FX aur apni seat pakki karo.""".split()
assert len(ROM)==134,len(ROM)
LAUGH=[11,54]
SCENE_STARTS=[0,12,21,30,34,39,50,55,59,68,76,84,89,98,101,108,118,124]
END=EN[-1]+0.7
