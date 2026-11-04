from pathlib import Path
import subprocess,json,hashlib
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
base=Path.cwd();stage=base/'work/meldkin-trailer';edit=stage/'edit';edit.mkdir(exist_ok=True)
out=base/'outputs';out.mkdir(exist_ok=True)
segments=[
 (2,5,9,'MELDKIN','Grow a defense. Peel the horde apart.','GAMEPLAY SHOWCASE'),
 (0,4,8,'BLOOM × NEEDLEBACK','Pollen lends nearby towers speed, detection and plate piercing.','INTERCHANGE'),
 (0,8.5,14.5,'KNOW YOUR ORGANISM','Inspect its reach, strip power and three growth paths.','TOWER PANEL'),
 (0,15,26,'CHOOSE A SPECIALTY','One path to rung 4. A second to rung 2. The third closes.','UPGRADE PATHS'),
 (1,4,12,'BLOOM × MORTARCAP','Combine rapid cap fire, heavy shells and Needleback support.','GEODE'),
 (2,3,12,'BORER × NEEDLEBACK','Borer culls inner layers. Needleback strips from the front.','INTERCHANGE'),
 (3,3,10,'GROW BETWEEN RUNS','Buy Seed gold I: +100 starting gold in every future run.','PERMANENT UPGRADES'),
 (3,10,18,'UNLOCK A NEW ORGANISM','Buy Mortarcap with XP to add it to the shop in every run.','PERMANENT UPGRADES'),
 (3,18,24,'INVEST IN ITS FUTURE','Buy Quicken to reduce Mortarcap’s recharge time in future runs.','PERMANENT UPGRADES'),
 (0,26,30,'BUILD A DIFFERENT ANSWER','Four organisms. Three paths each. Two maps to defend.','MELDKIN'),
]
total=sum(round((b-a)*30) for _,a,b,*_ in segments);assert total==2010
font=lambda size,bold=False:ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',size)
F42=font(42,True);F30=font(30);F21=font(21,True);F18=font(18)
def footer(index,local):
 c,a,b,title,body,chapter=segments[index]
 if index==3 and local>=210:title='RAVINE PURCHASED';body='Periodic huge strikes open a larger hazard on the lane.'
 elif index==3 and local>=120:title='CRATER PURCHASED';body='Heavy strikes leave a hazard for the next enemies to cross.'
 im=Image.new('RGB',(1920,170),(13,23,20));d=ImageDraw.Draw(im)
 d.rectangle((0,0,1920,1),fill=(65,88,67));d.rectangle((35,33,40,130),fill=(174,218,109))
 d.text((62,20),title,font=F42,fill=(238,241,225))
 d.text((64,81),body,font=F30,fill=(190,204,184))
 d.text((64,132),'Native gameplay • staged builds, funds and XP',font=F18,fill=(133,151,132))
 text=f'{index+1:02d} / {len(segments):02d}   {chapter}'
 d.text((1855-d.textlength(text,font=F21),135),text,font=F21,fill=(172,205,126))
 return im
video=edit/'video.mp4'
writer=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
caps={i:cv2.VideoCapture(str(stage/f'combo{i}/raw.avi')) for i in range(4)}
global_frame=0;timeline=[];stills={}
for idx,(combo,a,b,title,body,chapter) in enumerate(segments):
 cap=caps[combo];cap.set(cv2.CAP_PROP_POS_FRAMES,round(a*30));count=round((b-a)*30)
 timeline.append({'combo':combo,'source_start':a,'source_end':b,'start':global_frame/30,'end':(global_frame+count)/30,'title':title,'chapter':chapter})
 for n in range(count):
  ok,raw=cap.read();assert ok,(idx,n)
  small=cv2.resize(cv2.cvtColor(raw,cv2.COLOR_BGR2RGB),(1920,910),interpolation=cv2.INTER_AREA)
  im=Image.new('RGB',(1920,1080));im.paste(Image.fromarray(small),(0,0));im.paste(footer(idx,n),(0,910))
  d=ImageDraw.Draw(im);d.rectangle((0,1076,round(1920*(global_frame+1)/total),1079),fill=(172,205,126))
  if n==min(100,count//2):
   im.save(edit/f'section-{idx+1:02d}.jpg',quality=92)
   stills[idx]=im.copy()
  writer.stdin.write(im.tobytes());global_frame+=1
 print('edited',idx+1,title,flush=True)
writer.stdin.close();assert writer.wait()==0
for cap in caps.values():cap.release()
filters=[];audio=[]
for idx,(combo,a,b,*_) in enumerate(segments):
 dur=b-a;filters.append(f'[{combo+1}:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.035,afade=t=out:st={dur-.06}:d=0.06[a{idx}]');audio.append(f'[a{idx}]')
filters.append(''.join(audio)+f'concat=n={len(segments)}:v=0:a=1,loudnorm=I=-18:TP=-1.5:LRA=11[audio]')
film=out/'meldkin-builds-and-progression-trailer.mp4'
cmd=['ffmpeg','-y','-v','error','-i',str(video)]
for i in range(4):cmd+=['-i',str(stage/f'combo{i}/raw.avi')]
cmd+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[audio]','-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(film)]
subprocess.run(cmd,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(film),'-f','null','-'],check=True)
(edit/'timeline.json').write_text(json.dumps(timeline,indent=2))
sheet=Image.new('RGB',(1600,1350),(13,23,20));d=ImageDraw.Draw(sheet)
for k,idx in enumerate([0,2,3,4,5,7]):sheet.paste(stills[idx].resize((800,450)),((k%2)*800,(k//2)*450))
sheet.save(out/'meldkin-trailer-preview.jpg',quality=91)
hashes=json.loads((stage/'source-hashes.json').read_text());unchanged=all(hashlib.sha256((Path('E:/Meldkin')/p).read_bytes()).hexdigest()==h for p,h in hashes.items());assert unchanged
authored=all(hashlib.sha256((stage/'project'/p).read_bytes()).hexdigest()==h for p,h in hashes.items() if p!='project.godot' and not (p.startswith(('Assets/Generated/','Assets/GeneratedMobile/')) and (p.endswith(('_ground.res','_lane.res')) or p.endswith('/map_bakes.json'))));assert authored
print(json.dumps({'duration':global_frame/30,'bytes':film.stat().st_size,'original_files_unchanged':len(hashes),'copied_authored_files_unchanged':authored}),flush=True)
