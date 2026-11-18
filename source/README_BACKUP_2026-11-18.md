# Chart Bender FX – work backup (2026-11-18)

## Posted on Instagram (@chartbendfx, account id 17841472229932080)
| Date | Video | Instagram media id |
|---|---|---|
| 2026-11-18 | Institute promo (live classes Karachi, first 5 = 50% off, India online) | 18011165936781757 |
| 2026-11-18 | SMC Day 16 – Displacement | 17883066954543664 |
| 2026-11-17 | SMC Day 15 – Judas Swing | 17931482712180051 |
| 2026-11-16 | SMC Day 13 – Equal Highs/Lows | 18421567372092456 |
Earlier days (1-12) are in the GitHub repo zk574/zohaib-reels, folder reels/.

## Where everything lives
- GitHub repo: https://github.com/zk574/zohaib-reels  (reels/ = all videos + covers; source/ = this backup's code)
- Posting: Windsor.ai connector -> instagram -> create_video_post (video_url + cover_url from raw.githubusercontent.com/zk574/zohaib-reels/main/reels/<file>)
- YouTube: via Zapier (youtube_upload_video); connection is being moved to a new channel.
- Voice: ElevenLabs "Rahul – Punchy Energetic Storyteller" (voice_id tbNmrxvBSFe1YOyXX3mh). Word timings: ElevenLabs Speech-to-Text (Scribe) JSON export.

## Style rules (standing)
Cream #F7F1E8 + burnt orange #E97842, ink #1B1A17; Montserrat ExtraBold + Gelasio italic accents; 1080x1920, 30fps; Roman-Urdu voice, Roman-English captions; little black-hoodie kid with glasses and pointer under the chart; captions lead voice by ~0.25-0.3 s; voice tempo 1.2x; hashtags always #ChartBendFX #forexindia #forexpakistan + topic tags. Day 15 full-screen chart style was rejected.

## Rebuild the promo
cd promo_source; python3 prep.py (voice.mp3 -> vo.wav, env.npy, mix.wav); split frames across 2 procs: python3 render.py 0 666 p1.mp4 & python3 render.py 666 1332 p2.mp4; concat p1+p2 and mux mix.wav with ffmpeg. python3 cover.py for the cover. Needs Python, Pillow, numpy, ffmpeg, Montserrat/Gelasio/Anton fonts (Google Fonts).

## Not recoverable
The Day 1-16 renderers (render_dp.py etc.) were lost when the sandbox reset; the finished videos are safe in the repo, but changing an old video would mean rebuilding it.
## Pending
Day 17 only when Zohaib says. YouTube posts for Day 14/15/16/promo only if he asks.
