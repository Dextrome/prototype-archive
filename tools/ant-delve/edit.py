"""Add chapter captions and audit-derived cargo/score to the native recording."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import json
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--work', type=Path, default=Path('.openai/ant-delve'))
p.add_argument('--output', type=Path, default=Path('docs/assets/ant-delve/film-gameplay.mp4'))
a = p.parse_args()
audit = json.loads((a.work / 'audit.json').read_text())
chapters = [
    (0, 4, '7ANTS  /  A STRATEGY PROTOTYPE', 'ANT DELVE',
     'Connect tunnels. Mine resources. Carry your score home.'),
    (4, 12, '01  /  BUILD THE ROUTE', 'Connect the missing tunnel',
     'Choose a tile that joins the openings above and below.'),
    (12, 17, '02  /  PUT YOUR WORKERS TO WORK', 'Send a worker to the sugar',
     'Follow the route you just built. Mining happens at the end of your turn.'),
    (17, 25, '02  /  ONE MORE TURN, ONE MORE SUGAR', 'Build a haul at the vein',
     'Each turn mines one sugar. Rival turns are omitted.'),
    (25, 31, '03  /  BRING IT HOME', 'Walk the haul back to the nest',
     'Carrying resources is only half the job. Return home to score.'),
    (31, 34.5, '03  /  THE PAYOFF', 'Three sugar. Three points.',
     'End the turn at your nest to bank the load.'),
    (34.5, 39.5, '04  /  PUSH INTO DANGER', 'Send a soldier to clear the chamber',
     'An antlion guards the deeper fungus. Enter its cell to fight.'),
    (39.5, 43.2, '04  /  END THE TURN TO FIGHT', 'Trade blows. Watch your health.',
     'Native damage, health and combat outcome. Combat playback slowed for clarity.'),
    (43.2, 46, '04  /  THE WAY IS OPEN', 'Antlion defeated. Soldier survives.',
     'The guard is gone, and the soldier has started mining fungus.'),
    (46, 52, '7ANTS  /  HEX STRATEGY', 'ANT DELVE',
     'Dig deeper. Bring it home before they do.'),
]
regular = 'C:/Windows/Fonts/segoeui.ttf'
bold = 'C:/Windows/Fonts/segoeuib.ttf'
fonts = {size: ImageFont.truetype(bold if size in (15, 30, 39, 27) else regular, size)
         for size in (15, 18, 21, 27, 30, 39)}
gold, white, muted = '#E9B54E', '#F5F1E8', '#B9B8AD'
cache = {}

def banner(t, chapter, state):
    carry, score = state
    if t < 34.5:
        metric = f'CARRY  {carry} / 6'
        detail = f'{score} POINTS BANKED'
    elif t < 43.2:
        metric, detail = 'SOLDIER vs ANTLION', 'FUNGUS  /  3 POINTS PER UNIT'
    else:
        metric, detail = '3 POINTS BANKED', 'EXPLORE  /  MINE  /  RETURN'
    key = (chapter, metric, detail)
    if key in cache:
        return cache[key]
    _, _, eyebrow, title, subtitle = chapter
    im = Image.new('RGB', (1600, 120), '#151A17')
    d = ImageDraw.Draw(im)
    d.line((0, 0, 1599, 0), fill='#54604F', width=2)
    d.rectangle((0, 0, 7, 120), fill=gold)
    d.text((34, 9), eyebrow, font=fonts[15], fill=gold)
    d.text((32, 29), title, font=fonts[39 if title == 'ANT DELVE' else 30], fill=white)
    d.text((34, 82), subtitle, font=fonts[21], fill=muted)
    d.line((1150, 20, 1150, 100), fill='#3F483E', width=1)
    d.text((1180, 10), 'STAGED GAMEPLAY  /  REAL GAME RULES', font=fonts[15], fill=gold)
    d.text((1180, 38), metric, font=fonts[27], fill=white)
    d.text((1180, 82), detail, font=fonts[18], fill=muted)
    # Verify every string fits its column before encoding.
    for text, size, x, limit in ((subtitle, 21, 34, 1135), (title, 39 if title == 'ANT DELVE' else 30, 32, 1135),
                                (metric, 27, 1180, 1580), (detail, 18, 1180, 1580)):
        assert x + d.textlength(text, font=fonts[size]) < limit, text
    cache[key] = im.tobytes()
    return cache[key]

cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
       '-pixel_format', 'rgb24', '-video_size', '1600x120', '-framerate', '30',
       '-i', 'pipe:0', '-an', '-c:v', 'ffv1', str(a.work / 'captions.mkv')]
encoder = subprocess.Popen(cmd, stdin=subprocess.PIPE)
try:
    state = (0, 0)
    event_index = 0
    for f in range(1560):
        t = f / 30
        while event_index < len(audit) and audit[event_index]['frame'] <= f:
            state = (audit[event_index]['sugar'], audit[event_index]['score'])
            event_index += 1
        chapter = next(c for c in chapters if c[0] <= t < c[1])
        encoder.stdin.write(banner(t, chapter, state))
finally:
    encoder.stdin.close()
assert encoder.wait() == 0

a.output.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y',
    '-i', str(a.work / 'raw.avi'), '-i', str(a.work / 'captions.mkv'),
    '-filter_complex', '[0:v]pad=1600:900:0:0:color=0x151A17[game];'
                       '[game][1:v]overlay=0:780:shortest=1,'
                       'fade=t=in:st=0:d=0.25,fade=t=out:st=51.4:d=0.6,'
                       'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p[v]',
    '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19',
    '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-colorspace', 'bt709',
    '-color_primaries', 'bt709', '-color_trc', 'bt709',
    '-r', '30', '-t', '52', '-movflags', '+faststart',
    str(a.output)], check=True)
print(a.output.resolve())
