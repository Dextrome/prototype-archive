"""Caption the verified 60-second native gameplay story; keep all decisions in order."""
from pathlib import Path
import json
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

work = Path('E:/trailer-production/rot-garden')
here = Path(__file__).resolve().parent
output = Path('docs/assets/rot-garden-romance/film-gameplay.mp4')
audit = json.loads((work / 'audit.json').read_text())
assert audit[-1]['action'] == 'verified native bond and date win'
assert audit[-1]['bond'] == 'Bond'
assert 'cemetery_picnic' in audit[-1]['won']
moves = [e for e in audit if 'affection' in e]
assert [e['affection'] for e in moves] == [10, 13, 16, 24, 24, 27]
assert moves[-1]['outcome'] == 'Win'
harvest = next(e for e in audit if e['action'] == 'harvest adds reckless compliment')
assert harvest['deck'].count('reckless_compliment') == 1
chapters = [
    (0, 3, '7ANTS / A FARMING & DATING PROTOTYPE', 'ROT GARDEN ROMANCE', 'Some gardens grow more than vegetables.'),
    (3, 8, '01 / A QUESTIONABLE BEGINNING', 'Plant a little courage.', 'Start with a Blood Turnip. Try not to ask why it has a pulse.'),
    (8, 11, '01 / EIGHT MINUTES LATER', 'Something is ready.', 'Growth time skipped. The garden has something for your next date.'),
    (11, 18, '02 / KEEP THE HEART', 'Harvest a Reckless Compliment.', 'Choose a card instead of seeds or resources. Romance starts in the soil.'),
    (18, 24, '02 / FROM THE GARDEN TO YOUR DECK', 'Something to bring to the picnic.', 'The card you grew joins your date deck. Mira is waiting.'),
    (24, 32, '03 / MIRA\u2019S CEMETERY PICNIC', 'A mostly clean blanket.', 'Get comfortable. Even the mold has made an effort.'),
    (32, 38.5, '04 / LET THE VEGETABLES DO THE FLIRTING', 'A compliment with consequences.', 'Reckless Compliment: +9 Affection, +4 Awkwardness. A little courage has a cost.'),
    (38.5, 43.5, '04 / A LITTLE CLOSER', 'Small talk. A homemade gift.', 'The affection grows. One more word might be enough.'),
    (43.5, 47, '04 / GIVE IT A MOMENT', 'Take a breath. Start another turn.', 'A fresh hand, one less turn of patience. Small Talk closes the gap.'),
    (47, 53, '05 / THE GOOD KIND OF DAMP', 'The picnic went well.', 'Let Mira have the last word.'),
    (53, 57, '05 / A BOND TAKES ROOT', 'A date won. A new seed to plant.', '27 / 25 Affection. Mira: Bond. The garden gets another beginning.'),
    (57, 60, '7ANTS / GAMEPLAY', 'ROT GARDEN ROMANCE', 'Plant something. See what grows.'),
]
(here / 'edit-decision-list.json').write_text(json.dumps(chapters, indent=2, ensure_ascii=False), encoding='utf-8')
font = lambda size, bold=False: ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf', size)
eyebrow_font, title_font, body_font = font(14, True), font(30, True), font(20)
cache = {}
for chapter in chapters:
    _, _, eyebrow, title, subtitle = chapter
    im = Image.new('RGB', (1600, 100), '#130e1a')
    d = ImageDraw.Draw(im)
    d.line((0, 0, 1600, 0), fill='#69512f', width=2)
    d.rectangle((0, 1, 5, 100), fill='#e4a2ca')
    d.text((28, 7), eyebrow, font=eyebrow_font, fill='#d8ba73')
    d.text((26, 24), title, font=title_font, fill='#f6eaf2')
    d.text((28, 66), subtitle, font=body_font, fill='#cbbfcd')
    d.line((1400, 19, 1400, 80), fill='#4e3d51', width=1)
    d.text((1430, 27), 'GAMEPLAY', font=font(18, True), fill='#e4a2ca')
    d.text((1430, 55), '7ants', font=font(16), fill='#b4a4b8')
    for text, f in ((eyebrow, eyebrow_font), (title, title_font), (subtitle, body_font)):
        assert d.textlength(text, font=f) < 1340, text
    cache[chapter] = im.tobytes()
encoder = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
    '-pixel_format', 'rgb24', '-video_size', '1600x100', '-framerate', '30', '-i', 'pipe:0',
    '-an', '-c:v', 'ffv1', str(work / 'captions.mkv')], stdin=subprocess.PIPE)
try:
    for frame in range(1800):
        chapter = next(c for c in chapters if c[0] <= frame / 30 < c[1])
        encoder.stdin.write(cache[chapter])
finally:
    encoder.stdin.close()
assert encoder.wait() == 0
# Tightened farm and deck shots enlarge the crop and the newly harvested card.
# The date stays wide so both the hand and native meters remain visible.
filters = (
    '[0:v]trim=duration=60,setpts=PTS-STARTPTS,split=3[wide][farm][deck];'
    '[farm]crop=960:540:640:100,scale=1600:900[farmclose];'
    '[deck]crop=1160:652:220:20,scale=1600:900[deckclose];'
    '[wide][farmclose]overlay=0:0:enable=\'gte(t,5)*lt(t,11)\'[withfarm];'
    '[withfarm][deckclose]overlay=0:0:enable=\'gte(t,18)*lt(t,21)\'[game];'
    '[game]pad=1600:1000:0:0:color=0x130e1a[padded];'
    '[padded][1:v]overlay=0:900:shortest=1,'
    'fade=t=in:st=0:d=0.3,fade=t=out:st=59.4:d=0.6,'
    'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p[v]'
)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(work / 'raw.avi'),
    '-i', str(work / 'captions.mkv'), '-filter_complex', filters, '-map', '[v]', '-an',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30',
    '-t', '60', '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709',
    '-color_trc', 'bt709', '-movflags', '+faststart', str(output)], check=True)
shutil.copy2(work / 'audit.json', here / 'validation.json')
print(output.resolve())
