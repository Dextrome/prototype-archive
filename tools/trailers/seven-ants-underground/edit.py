"""Build the archive trailer from native Godot captures. No generated gameplay."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, json, math, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from scipy.signal import butter, sosfilt

ROOT=Path(os.environ.get('SEVEN_ANTS_PRODUCTION_ROOT',str(Path(__file__).resolve().parent)))
OUT=ROOT/'edit'
OUT.mkdir(exist_ok=True)
W,H,FPS=1600,900,60
CREAM='#f5eedb'; GOLD='#ffbb59'; CYAN='#78f1ef'; INK='#0a1017'
FONT='C:/Windows/Fonts/bahnschrift.ttf'
DISPLAY='C:/Windows/Fonts/impact.ttf'
def run(args):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def f(n,display=False):return ImageFont.truetype(DISPLAY if display else FONT,n)
def tracked(d,xy,text,font,fill,spacing=3):
    x,y=xy
    for c in text:
        d.text((x,y),c,font=font,fill=fill)
        x+=d.textlength(c,font=font)+spacing
def frame(shot,t,name):
    dest=OUT/f'{name}.jpg'
    run(['-ss',t,'-i',ROOT/f'{shot}.avi','-frames:v',1,dest])
    return Image.open(dest).convert('RGB')
def overlay(name,chapter,headline,detail='',accent=GOLD):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,61),fill=(10,16,23,247))
    d.rectangle((0,H-111,W,H),fill=(10,16,23,250))
    d.rectangle((48,H-91,54,H-28),fill=accent)
    tracked(d,(49,20),chapter,f(18),accent,3)
    d.text((W-51,16),'7A / UNDERGROUND',anchor='ra',font=f(21),fill=CREAM)
    size=46 if len(headline)<36 else 39
    d.text((75,H-91),headline,font=f(size,True),fill=CREAM)
    if detail:tracked(d,(77,H-36),detail,f(15),accent,1.6)
    im.save(OUT/f'{name}.png')
    return name
def title(name,tagline,subtitle,source,t):
    im=frame(source,t,name+'-bg').resize((W,H))
    im=ImageEnhance.Brightness(im).enhance(.17).convert('RGBA')
    wash=Image.new('RGBA',(W,H),(5,14,21,65));im=Image.alpha_composite(im,wash)
    contours=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(contours)
    for j in range(7):
        y=80+j*118
        pts=[(x,y+int(24*math.sin(x/170+j))) for x in range(-30,W+30,8)]
        d.line(pts,fill=(88,134,133,35),width=2)
    im=Image.alpha_composite(im,contours);d=ImageDraw.Draw(im)
    tracked(d,(93,106),'DESTRUCTIBLE TERRAIN / UNREASONABLE ANTS',f(18),CYAN,3)
    d.text((83,205),'7',font=f(256,True),fill=GOLD)
    d.text((265,222),'ANTS',font=f(213,True),fill=CREAM)
    d.text((94,440),'UNDERGROUND',font=f(155,True),fill=CREAM)
    d.line((96,647,1504,647),fill=GOLD,width=3)
    tracked(d,(98,680),tagline,f(27),GOLD,4)
    tracked(d,(98,804),subtitle,f(16),CYAN,2)
    im.convert('RGB').save(OUT/f'{name}.png')
    return name

overlay('hook','MANDIBLE CLAMP / WALL SPLAT','PERSONAL SPACE IS OPTIONAL.','ACTUAL GAME RULES / STAGED ENCOUNTER')
overlay('dig','TUNNEL BORE','MAKE YOUR OWN SHORTCUTS.')
overlay('breach','DESTRUCTIBLE TERRAIN','NO COVER. NO PROBLEM.','BREACH / BREAK THROUGH / FINISH THE FIGHT')
overlay('rope','NINJA ROPE','SWING INTO TROUBLE.','GRAPPLE / RETRACT / RELEASE / REATTACH',CYAN)
overlay('rope-kill','NINJA ROPE + BURROW ROCKET','SHOOT ON THE SWING.','A REAL AIRBORNE HIT. THEN STRAIGHT BACK TO THE ROPE.',CYAN)
overlay('spring','SPRING MINE','BOING.','A LAUNCHPAD WITH QUESTIONABLE INTENTIONS.')
overlay('bounce','BELLY BOUNCE','BUMP. FLY. PANIC.')
overlay('echo-shot','ECHO TOYBOX / ORIGINAL SHOT','FIRE ONCE.','YOUR PAST SHOT WILL REPLAY FROM THE SAME POSITION.',CYAN)
overlay('echo-replay','ECHO TOYBOX / +2.5s REPLAY','FIGHT YOUR OWN ECHO.','CYAN-TINTED PROJECTILES REPEAT YOUR EARLIER ATTACK.',CYAN)
overlay('panic','PANIC TOYBOX / RISING LAVA','THE FLOOR IS COMING FOR YOU.')
overlay('chaos','TOYBOX / FOUR-ANT SANDBOX','TINY ANTS. BIG PROBLEMS.','BOMBS / ROCKETS / SPRINGS / DIRT SPIKES / FALLING CLODS')
title('title','DIG. SWING. OUTSMART.','PLAYABLE PROTOTYPE / GAMEPLAY SHOWCASE','rope2',1.3)
title('end','DIG. SWING. OUTSMART.','PLAYABLE PROTOTYPE / STAGED IN-ENGINE GAMEPLAY','chaos',2.5)

# Ordered excerpts are forward cuts within each encounter. All play at 1x.
clips=[
 ('clamp',.5,1.4,'hook'),
 (None,0,1.4,'title'),
 ('rocket',.30,1.20,'dig'),
 ('breach',.35,1.20,'breach'),
 ('breach',2.60,1.0,'breach'),
 ('breach',4.80,1.20,'breach'),
 ('rope0',.10,5.75,'rope'),
 ('rope2',.25,3.70,'rope-kill'),
 ('spring',.05,1.85,'spring'),
 ('bounce',.55,1.2,'bounce'),
 ('echo',.45,1.60,'echo-shot'),
 ('echo',2.85,2.05,'echo-replay'),
 ('panic',.15,3.55,'panic'),
 ('chaos',.30,5.60,'chaos'),
 (None,0,3.50,'end'),
]
timeline=[];now=0
for shot,start,duration,art in clips:
    timeline.append(dict(shot=shot,source_start=start,duration=duration,overlay=art,timeline_start=round(now,3)))
    now+=duration
(ROOT/'edit-decision-list.json').write_text(json.dumps({'fps':FPS,'duration':now,'segments':timeline},indent=2))

def segment(i,c):
    shot,start,duration,art=c;dest=OUT/f'segment-{i:02}.mkv'
    if shot:
        args=['-ss',start,'-t',duration,'-i',ROOT/f'{shot}.avi','-loop',1,'-i',OUT/f'{art}.png',
          '-filter_complex','[0:v]eq=brightness=0.012:saturation=1.12:gamma=1.03[v];[v][1:v]overlay=0:0:shortest=1[out]',
          '-map','[out]','-map','0:a:0','-af','aresample=48000,volume=1.5']
    else:
        args=['-loop',1,'-framerate',60,'-i',OUT/f'{art}.png','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-map','0:v:0','-map','1:a:0']
        if art=='end':args+=['-vf','fade=t=in:st=0:d=0.12,fade=t=out:st=3:d=0.5']
    run([*args,'-t',duration,'-r',60,'-c:v','libx264','-preset','fast','-crf',17,'-pix_fmt','yuv420p','-c:a','pcm_s16le','-ar',48000,'-ac',2,dest])
    print('Edited',i,art,flush=True)
    return dest
with ThreadPoolExecutor(max_workers=3) as ex:
    files=list(ex.map(lambda v:segment(*v),enumerate(clips)))
(OUT/'concat.txt').write_text('\n'.join("file '"+str(v).replace('\\','/')+"'" for v in files))
run(['-f','concat','-safe',0,'-i',OUT/'concat.txt','-c','copy',OUT/'picture.mkv'])

# Original percussive electronic score, synthesized from oscillators and noise.
sr=48000;duration=now;N=int((duration+.5)*sr);mix=np.zeros((N,2),np.float32)
rng=np.random.default_rng(7717)
def add(at,sound,gain=1,pan=0):
    a=max(0,int(at*sr));end=min(N,a+len(sound));sound=np.asarray(sound[:end-a])*gain
    if end<=a:return
    mix[a:end,0]+=sound*math.sqrt((1-pan)/2)
    mix[a:end,1]+=sound*math.sqrt((1+pan)/2)
def tone(midi,length,kind='bass'):
    t=np.arange(int(length*sr))/sr;hz=440*2**((midi-69)/12)
    if kind=='bass':
        sig=sum(np.sin(2*np.pi*hz*k*t)/k**1.6 for k in range(1,9))
        env=(1-np.exp(-t*260))*np.exp(-t*8)
    else:
        sig=sum(np.sin(2*np.pi*hz*(1+det)*t) for det in [-.004,0,.004])/3
        sig+=.22*np.sin(2*np.pi*hz*2*t)
        env=(1-np.exp(-t*100))*np.exp(-t*5)
    return sig*env
def kick():
    t=np.arange(int(sr*.42))/sr
    phase=2*np.pi*(46*t+70*.025*(1-np.exp(-t/.025)))
    return np.sin(phase)*np.exp(-t*12)+.13*rng.normal(0,1,len(t))*np.exp(-t*140)
def snare():
    t=np.arange(int(sr*.25))/sr;noise=rng.normal(0,1,len(t))
    noise=sosfilt(butter(2,[900,11000],fs=sr,btype='bandpass',output='sos'),noise)
    return .65*noise*np.exp(-t*22)+.3*np.sin(2*np.pi*183*t)*np.exp(-t*28)
def hat(open=False):
    t=np.arange(int(sr*(.18 if open else .065)))/sr
    noise=sosfilt(butter(2,6500,fs=sr,btype='highpass',output='sos'),rng.normal(0,1,len(t)))
    return noise*np.exp(-t*(20 if open else 65))
beat=60/144;drop=2.8
for bar in range(22):
    base=drop+bar*4*beat
    if base>duration-3.5:break
    for q in [0,1.5,2,2.75,3.5]:add(base+q*beat,kick(),.7)
    for q in [1,3]:add(base+q*beat,snare(),.48)
    for n in range(8):add(base+n*beat/2,hat(n%4==3),.12 if n%2 else .17,(-1)**n*.4)
    root=[38,38,34,36][(bar//2)%4]
    notes=[root,root,root+7,root,root+3,root,root+10,root+7]
    for n,note in enumerate(notes):add(base+n*beat/2,tone(note,.34),.32)
    if base>8:
        lead=[62,69,65,72,69,65,64,69]
        for n,note in enumerate(lead):
            snd=tone(note+(12 if bar%4==3 else 0),.33,'lead')
            at=base+n*beat/2
            add(at,snd,.095,(-1)**n*.5);add(at+.18,snd,.035,(-1)**(n+1)*.6)
    # Short metallic chord stab on each bar.
    chord=sum(tone(root+v,.7,'lead') for v in [24,27,31])
    add(base,chord,.09)
for c in timeline:
    at=c['timeline_start']
    if c['overlay'] in ['hook','title','breach','rope','rope-kill','echo-replay','panic','chaos','end']:
        t=np.arange(int(sr*.65))/sr
        impact=np.sin(2*np.pi*(37*t+25*.06*(1-np.exp(-t/.06))))*np.exp(-t*7)
        add(at,impact,.40)
        if at>.3:
            n=int(sr*.22);noise=rng.normal(0,1,n);ramp=np.linspace(0,1,n)**2
            sw=sosfilt(butter(2,[1000,8000],fs=sr,btype='bandpass',output='sos'),noise)*ramp
            add(at-.22,sw,.12)
add(.75,kick(),.5);add(1.05,snare(),.3)
# Final low chord and decay, followed by a clean fade.
end_start=duration-3.5
for note in [38,50,57,62,65]:add(end_start,tone(note,3.4,'lead'),.14)
t=np.arange(N)/sr
fade=np.minimum(1,np.maximum(0,(duration-t)/.8))
mix=np.tanh(mix*1.25)*fade[:,None]*.60
with wave.open(str(OUT/'original-score.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
    w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
dest=ROOT/'7-Ants-Underground-gameplay-trailer.mp4'
run(['-i',OUT/'picture.mkv','-i',OUT/'original-score.wav','-filter_complex',
     '[0:a]volume=1.5[a];[a][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=7[aout]',
     '-map','0:v:0','-map','[aout]','-c:v','copy','-c:a','aac','-b:a','192k','-ar',48000,
     '-t',duration,'-movflags','+faststart',dest])
print('FINISHED',dest,'duration',duration,flush=True)
