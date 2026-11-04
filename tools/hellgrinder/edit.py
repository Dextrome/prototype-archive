from pathlib import Path
import subprocess,json,hashlib,sys,bisect
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
base=Path.cwd();stage=base/'work/hellgrinder-loop';cap=stage/'capture';edit=stage/'edit';edit.mkdir(exist_ok=True);out=base/'outputs';out.mkdir(exist_ok=True)
rows=json.loads((cap/'trace.json').read_text(encoding='utf-8'));probe=json.loads((stage/'probe/trace.json').read_text(encoding='utf-8'))
assert rows==probe,'Rendered replay diverged from the UI rehearsal.'
def phase(name,shift):return next(r for r in rows if r['eventType']=='phase' and r['state']['phase']==name and r['state']['shift']==shift)
def action(detail,shift):return next(r for r in rows if r['eventType']=='action' and r['detail']==detail and r['state'].get('shift')==shift)
def mid(name,shift):return next(r for r in rows if r['eventType']=='mid-event' and r['detail']==name and r['state']['shift']==shift)
segments=[]
def add(key,a,b,title,body,chapter):
 assert b>a
 segments.append({'key':key,'a':a,'b':b,'title':title,'body':body,'chapter':chapter})
add('menu',40,96,'CLOCK IN','Start a standard five-shift run. Hell has quotas. You have a debt.','NEW RUN')
add('equipment',120,367,'BUILD WITHIN THE BUDGET','Pick one part per department. This setup costs 120 BC and leaves 40 BC.','PROCUREMENT')
add('contract',373,484,'ACCEPT THE FIRST CONTRACT','Standard Soul Batch: ship 100 units before the 60-second shift ends.','SHIFT 1 / CONTRACT')
add('directive',487,605,'AUTHORIZE A DIRECTIVE','Baseline reduces heat and wear. Other directives trade safety for output or income.','SHIFT 1 / DIRECTIVE')
add('work',613,730,'PUT THE MACHINE TO WORK','Overclock boosts output by 40%, at the cost of heat and wear.','SHIFT 1 / OPERATE')
v=action('vent',1)['frame'];add('vent',v-24,v+126,'VENT THE HEAT','Venting drains heat and pressure, but adds sludge. Every control has a tradeoff.','SHIFT 1 / REACT')
p=action('purge',1)['frame'];add('purge',p-20,p+91,'KEEP THE PIPELINE CLEAR','Purging removes sludge, spends 5 BC and cuts purity by 10.','SHIFT 1 / REACT')
r=phase('Report',1)['frame'];add('success',r+6,r+147,'FIRST CONTRACT: PASSED','Shipment 122 / 100. The Receipt Printer adds 15 Bloodcoin to the payout.','SHIFT 1 / INVOICE')
c=phase('ContractSelect',2)['frame'];add('debt',c+3,c+99,'TURN EARNINGS INTO BREATHING ROOM','Pay 50 earned Bloodcoin to reduce contract debt by 50.','BETWEEN SHIFTS')
p=phase('Preparation',2)['frame'];add('valve',p+12,p+124,'ADD A PRESSURE VALVE','Between shifts, choose a module, maintenance or an operating policy.','SHIFT 2 / PREPARE')
m=mid('sales_rush_quota',2)['frame'];a=action('Resolve sales_rush_quota choice 1',2)['frame'];add('rush-event',m+10,a+24,'CORPORATE WANTS MORE','An extra quota offers +50 BC or +30 debt on a miss. Decline this one.','MID-SHIFT DECISION')
r=phase('Report',2)['frame'];add('rejection',r+8,r+145,'VOLUME IS NOT ENOUGH','Shipment 113 / 90 passes. Purity 65 / 70 fails. The order is rejected.','SHIFT 2 / FAILED ORDER')
p=phase('Preparation',3)['frame'];add('flywheel',p+10,p+124,'GROW THE BUILD','Greed Flywheel rewards time spent without venting. Profit creates another tradeoff.','SHIFT 3 / PREPARE')
m=mid('jam_with_flavor',3)['frame'];a=action('Resolve jam_with_flavor choice 0',3)['frame'];add('jam',m+10,a+70,'THE GRINDER JAMS','The incident ticker offers a choice. Purge the jam and restore the flow.','SHIFT 3 / INCIDENT')
a=action('Purge before disposal inspection',3)['frame'];r=phase('Report',3)['frame'];add('disposal',a-30,r+115,'PASS THE DISPOSAL INSPECTION','Purge before the timer expires. Final sludge: 4 against a maximum of 40.','SHIFT 3 / PASSED ORDER')
p=phase('Preparation',4)['frame'];add('repay-prep',p+15,p+124,'MAKE A DIFFERENT INVESTMENT','Choose debt repayment instead of adding another machine part.','SHIFT 4 / PREPARE')
a=action('Resolve marvis_visit choice 1',4)['frame'];add('later-machine',a+14,a+89,'THE SAME MACHINE HAS TO LAST','Upgrades carry forward. So does wear. Keep the line moving into later shifts.','SHIFT 4 / OPERATE')
p=phase('Preparation',5)['frame'];add('scrubber',p+10,p+123,'PREPARE FOR THE FINAL SHIFT','Choose an Audit Scrubber to help control the growing audit risk.','SHIFT 5 / PREPARE')
p=phase('DirectiveSelect',5)['frame'];add('final-directive',p+5,p+127,'TAKE A FASTER DIRECTIVE','Accelerated Throughput raises shipment output and heat, with a success bonus.','SHIFT 5 / AUTHORIZE')
a=[r for r in rows if r['eventType']=='action' and r['detail']=='vent' and r['state'].get('shift')==5][-1]['frame'];add('final-push',a-28,a+116,'ONE LAST ORDER','Keep the hot machine stable until the final shipment clears its quota.','SHIFT 5 / LAST PUSH')
r=phase('Report',5)['frame'];add('final-invoice',r+8,r+144,'FINAL CONTRACT: PASSED','Shipment 140 / 130. Collect the directive and Receipt Printer bonuses.','SHIFT 5 / INVOICE')
r=phase('RunComplete',5)['frame'];add('ending',r+8,r+207,'CONTRACT DEBT BELOW TARGET','Five shifts survived. Debt ends at 350, below the prototype’s 500 target.','RUN RESULT / SUCCESS')
assert all(a['b']<=b['a'] for a,b in zip(segments,segments[1:])),[(a['key'],b['key']) for a,b in zip(segments,segments[1:]) if a['b']>b['a']]
total=sum(s['b']-s['a'] for s in segments);assert total<3600
at=0
for s in segments:s['start']=at/30;at+=s['b']-s['a'];s['end']=at/30
(edit/'timeline.json').write_text(json.dumps(segments,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'seconds':total/30,'chapters':len(segments)}),flush=True)
if '--plan' in sys.argv:sys.exit()
fonts=lambda n,bold=False:ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
F36=fonts(36,True);F26=fonts(26);F17=fonts(17,True);F15=fonts(15)
def footer(s,index):
 im=Image.new('RGB',(1920,120),(22,16,14));d=ImageDraw.Draw(im)
 d.line((0,0,1920,0),fill=(105,75,43),width=2);d.rectangle((34,21,39,92),fill=(237,171,68))
 d.text((61,11),s['title'],font=F36,fill=(243,226,195))
 assert d.textlength(s['body'],font=F26)<1800,s['key']
 d.text((63,58),s['body'],font=F26,fill=(207,190,163))
 d.text((64,96),'Native UI inputs • Normal starting budget • Forward cuts skip unshown play',font=F15,fill=(156,137,111))
 tag=s['chapter'];d.text((1856-d.textlength(tag,font=F17),96),tag,font=F17,fill=(220,165,82))
 return im
reader=cv2.VideoCapture(str(cap/'raw.avi'));video=edit/'video.mp4'
writer=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1200','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
frame=0;stills={}
for idx,s in enumerate(segments):
 reader.set(cv2.CAP_PROP_POS_FRAMES,s['a']);bar=footer(s,idx)
 for n in range(s['b']-s['a']):
  ok,raw=reader.read();assert ok,(s['key'],n)
  im=Image.new('RGB',(1920,1200));im.paste(Image.fromarray(cv2.cvtColor(raw,cv2.COLOR_BGR2RGB)),(0,0));im.paste(bar,(0,1080))
  ImageDraw.Draw(im).rectangle((0,1196,round(1920*(frame+1)/total),1199),fill=(230,166,65))
  if n==min(70,(s['b']-s['a'])//2):
   im.save(edit/(s['key']+'.jpg'),quality=93);stills[s['key']]=im.copy()
  writer.stdin.write(im.tobytes());frame+=1
 print('edited',s['key'],flush=True)
writer.stdin.close();assert writer.wait()==0;reader.release()
filters=[];labels=[]
for idx,s in enumerate(segments):
 duration=(s['b']-s['a'])/30
 filters.append(f"[1:a]atrim=start={s['a']/30}:end={s['b']/30},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={duration-.06}:d=0.06[a{idx}]");labels.append(f'[a{idx}]')
filters.append(''.join(labels)+f'concat=n={len(segments)}:v=0:a=1,loudnorm=I=-18:TP=-1.5:LRA=11[audio]')
film=out/'hellgrinder-full-loop-trailer.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(video),'-i',str(cap/'raw.avi'),'-filter_complex',';'.join(filters),'-map','0:v','-map','[audio]','-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(film)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(film),'-f','null','-'],check=True)
last=rows[-1]['state'];assert last['result']=='PrototypeWin' and last['debt']==350 and last['shift']==5
reports=[r for r in rows if r['eventType']=='phase' and r['state']['phase']=='Report'];assert len(reports)==5
assert any('shipment rejected' in reason for r in reports for reason in r['state']['reasons'])
hashes=json.loads((stage/'source-hashes.json').read_text());assert all(hashlib.sha256((Path('E:/Hellgrinder')/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
assert all(hashlib.sha256((stage/'project'/p).read_bytes()).hexdigest()==h for p,h in hashes.items() if p!='project.godot')
assert not any(x in (cap/'engine.log').read_text(encoding='utf-8') for x in ['ERROR:','Exception'])
report={'seconds':frame/30,'resolution':[1920,1200],'seed':7,'starting_budget':160,'machine_cost':120,'coin_retained':40,'shifts':5,'ending':last['result'],'final_debt':last['debt'],'final_coin':last['coin'],'final_output':last['output'],'unchanged_original_files':len(hashes),'native_replay_matches_probe':True,'bytes':film.stat().st_size,'sha256':hashlib.sha256(film.read_bytes()).hexdigest()}
(edit/'validation.json').write_text(json.dumps(report,indent=2));sheet=Image.new('RGB',(1600,1500),(22,16,14))
for i,key in enumerate(['equipment','directive','vent','rejection','jam','ending']):sheet.paste(stills[key].resize((800,500)),((i%2)*800,(i//2)*500))
sheet.save(out/'hellgrinder-full-loop-preview.jpg',quality=93)
print(json.dumps(report,indent=2),flush=True)
