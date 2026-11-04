"""A tighter eight-turn walkthrough followed by a wide native four-player time-lapse."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import json
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--work', type=Path, default=Path('.openai/ant-delve'))
p.add_argument('--output', type=Path, default=Path('docs/assets/ant-delve/film-gameplay.mp4'))
a = p.parse_args()
audit = json.loads((a.work / 'audit.json').read_text(encoding='utf-8'))
four_audit = json.loads((a.work / 'four-audit.json').read_text(encoding='utf-8'))
FPS, WALK_SPEED, FOUR_SPEED = 30, 1.5, 6
WALK_SOURCE, FOUR_SOURCE = 93, 144
WALK_DURATION, FOUR_DURATION = WALK_SOURCE / WALK_SPEED, FOUR_SOURCE / FOUR_SPEED
DURATION = int(WALK_DURATION + FOUR_DURATION)
assert DURATION == 86
# Walkthrough chapter times use SOURCE seconds; every turn and handoff survives.
# Fewer, shorter captions give each explanation more reading time at 1.5x.
chapters = [
    (0, 5, None, 'ANT DELVE  /  STAGED START, NATIVE GAMEPLAY', 'Place. Move. Mine. Return.',
     'Each turn: place a tunnel, move ants, then end to mine or bank.'),
    (5, 17, 0, 'ROUND 1  /  ORANGE', 'Connect sugar. Send a worker.',
     'End the turn to mine one sugar. Cargo is not score yet.'),
    (17, 27, 1, 'ROUND 1  /  BLUE', 'Blue opens a route to seeds',
     'Place the tile, move onto the seeds, then end the turn to mine.'),
    (27, 37, 0, 'ROUND 2  /  ORANGE', 'Extend deeper. Bring a teammate.',
     'The first worker stays on sugar and mines a second unit.'),
    (37, 47, 1, 'ROUND 2  /  BLUE', 'Dig down. Send in the soldier.',
     'The soldier advances while the worker gathers a second seed.'),
    (47, 57, 0, 'ROUND 3  /  ORANGE', 'Keep digging while the haul grows',
     'A replacement worker follows. The miner now carries three sugar.'),
    (57, 67, 1, 'ROUND 3  /  BLUE', 'Reach fungus with the soldier',
     'Blue gathers its third seed and first fungus. Both still need banking.'),
    (67, 75, 0, 'ROUND 4  /  ORANGE', 'Bring the haul home. Replace the miner.',
     'The loaded worker returns; a teammate takes over at the vein.'),
    (75, 81, 0, 'ROUND 4  /  ORANGE', 'Clear the guard. Bank three points.',
     'The soldier fights at end turn; the worker banks its three sugar.'),
    (81, 93, 1, 'ROUND 4  /  BLUE', 'Bring three seeds home for six points',
     'Extend the route, return the worker, then end the turn to bank.'),
]
assert chapters[0][0] == 0 and chapters[-1][1] == WALK_SOURCE
assert all(x[1] == y[0] for x, y in zip(chapters, chapters[1:]))
assert (audit[-1]['turns'], audit[-1]['placements'], audit[-1]['score'], audit[-1]['blueScore']) == (8, 8, 3, 6)
assert len(four_audit[-1]['scores']) == 4 and min(four_audit[-1]['turns']) >= 4
fonts = {size: ImageFont.truetype('C:/Windows/Fonts/' + name, size)
         for size, name in [(15, 'segoeuib.ttf'), (18, 'segoeui.ttf'), (21, 'segoeui.ttf'),
                            (23, 'segoeuib.ttf'), (30, 'segoeuib.ttf'), (39, 'segoeuib.ttf')]}
gold, white, muted = '#E9B54E', '#F5F1E8', '#B9B8AD'
team_colors = [gold, '#77C7E3', '#EFB6D4', '#65BD98']
cache = {}

def banner(title, subtitle, eyebrow, state, four=False):
    key = (title, subtitle, eyebrow, state, four)
    if key in cache:
        return cache[key]
    im = Image.new('RGB', (1600, 120), '#151A17')
    d = ImageDraw.Draw(im)
    d.line((0, 0, 1599, 0), fill='#54604F', width=2)
    d.rectangle((0, 0, 7, 119), fill=gold)
    title_size = 39 if title == 'ANT DELVE' else 30
    labels = [(eyebrow, 15, 34, 9, gold, 1135),
              (title, title_size, 32, 29, white, 1135),
              (subtitle, 21, 34, 82, muted, 1135)]
    d.line((1150, 16, 1150, 107), fill='#3F483E', width=1)
    if four:
        s0, s1, s2, s3, round_num, tiles = state
        labels.append(('FOUR AI COLONIES  /  6x SPEED', 15, 1180, 9, muted, 1580))
        for i, score in enumerate((s0, s1, s2, s3)):
            x, y = 1180 + (i % 2) * 185, 31 + (i // 2) * 28
            labels.append((f'P{i + 1}  {score} pts', 23, x, y, team_colors[i], x + 178))
        labels.append((f'ROUND {round_num}   |   {tiles} TILES ADDED', 15, 1180, 92, muted, 1580))
    else:
        sugar, seed, score, blue_score, turns, tiles = state
        labels.extend([
            ('WORKER CARGO  /  BANKED SCORE', 15, 1180, 9, muted, 1580),
            (f'ORANGE   {sugar} sugar  /  {score} pts', 23, 1180, 31, gold, 1580),
            (f'BLUE        {seed} seeds  /  {blue_score} pts', 23, 1180, 59, team_colors[1], 1580),
            (f'{turns} / 8 TURNS ENDED   |   {tiles} TILES ADDED', 15, 1180, 92, muted, 1580),
        ])
        for r in range(4):
            x = 34 + r * 274
            d.rectangle((x, 116, x + 264, 119), fill=gold if turns >= (r + 1) * 2 else '#364236')
    for text, size, x, y, color, limit in labels:
        assert x + d.textlength(text, font=fonts[size]) < limit, text
        d.text((x, y), text, font=fonts[size], fill=color)
    cache[key] = im.tobytes()
    return cache[key]

# Check every chapter before starting the encoder.
for _, _, _, eyebrow, title, subtitle in chapters:
    banner(title, subtitle, eyebrow + '  /  END TURN  /  1.5x', (3, 3, 3, 6, 8, 8))
banner('Four colonies. One shared board.', 'New match: watch all four colonies build, mine and bank.',
       'NEW MATCH  /  FOUR-PLAYER GAMEPLAY  /  6x SPEED', (20, 20, 20, 20, 22, 88), True)

encoder = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
       '-pixel_format', 'rgb24', '-video_size', '1600x120', '-framerate', str(FPS),
       '-i', 'pipe:0', '-an', '-c:v', 'ffv1', str(a.work / 'captions.mkv')], stdin=subprocess.PIPE)
try:
    walk_index = four_index = 0
    latest = None
    for f in range(FPS * DURATION):
        t = f / FPS
        if t < WALK_DURATION:
            source_frame = int(f * WALK_SPEED)
            while walk_index < len(audit) and audit[walk_index]['frame'] <= source_frame:
                latest = audit[walk_index]
                walk_index += 1
            source_time = source_frame / FPS
            chapter = next(c for c in chapters if c[0] <= source_time < c[1])
            _, _, owner, eyebrow, title, subtitle = chapter
            phase = 'PLACE'
            if latest and latest['actor'] == owner:
                phase = 'END TURN' if json.loads(latest['command'])['t'] == 'EndTurn' else latest['phase'].upper()
            if owner is not None:
                eyebrow += f'  /  {phase}  /  1.5x'
            else:
                eyebrow += '  /  1.5x'
            state = tuple(latest[k] for k in ('sugar', 'blueSeed', 'score', 'blueScore', 'turns', 'placements')) if latest else (0,) * 6
            pixels = banner(title, subtitle, eyebrow, state)
        else:
            source_frame = int((t - WALK_DURATION) * FPS * FOUR_SPEED)
            while four_index < len(four_audit) and four_audit[four_index]['frame'] <= source_frame:
                four_index += 1
            entry = four_audit[four_index - 1] if four_index else None
            state = (*entry['scores'], entry['round'], entry['placements']) if entry else (0, 0, 0, 0, 1, 0)
            eyebrow = 'NEW MATCH  /  FOUR-PLAYER GAMEPLAY  /  6x SPEED'
            title = 'Four colonies. One shared board.'
            subtitle = 'New match: watch all four colonies build, mine and bank.'
            if t >= 66:
                eyebrow = 'FOUR-PLAYER GAMEPLAY  /  NATIVE AI  /  6x SPEED'
                title = 'The tunnel networks spread'
                subtitle = 'All four colonies take turns as their routes grow across the same map.'
            if t >= 82:
                title = 'ANT DELVE'
                subtitle = 'Dig deeper. Bring it home before they do.'
            pixels = banner(title, subtitle, eyebrow, state, four=True)
        encoder.stdin.write(pixels)
finally:
    encoder.stdin.close()
assert encoder.wait() == 0

# Retiming is applied to gameplay before adding normally timed captions.
# The walkthrough loses only its old seven-second recap/end card.
filters = (f'[0:v]trim=end={WALK_SOURCE},setpts=(PTS-STARTPTS)/{WALK_SPEED},fps=30,setsar=1[walk];'
           f'[1:v]trim=end={FOUR_SOURCE},setpts=(PTS-STARTPTS)/{FOUR_SPEED},fps=30,setsar=1[four];'
           '[walk][four]concat=n=2:v=1:a=0,pad=1600:900:0:0:color=0x151A17[game];'
           '[game][2:v]overlay=0:780:shortest=1,'
           f'fade=t=in:st=0:d=0.2,fade=t=out:st={DURATION - 0.4}:d=0.4,'
           'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p[v]')
a.output.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y',
    '-i', str(a.work / 'raw.avi'), '-i', str(a.work / 'four-raw.avi'), '-i', str(a.work / 'captions.mkv'),
    '-filter_complex', filters, '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19',
    '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-colorspace', 'bt709',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', str(FPS), '-t', str(DURATION),
    '-movflags', '+faststart', str(a.output)], check=True)
print(a.output.resolve())
