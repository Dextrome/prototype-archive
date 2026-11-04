from pathlib import Path
import os,subprocess,sys,json
base=Path.cwd();stage=base/'work/hellgrinder-loop';project=stage/'project';mode=sys.argv[1]
out=stage/mode;out.mkdir(exist_ok=True);profile=out/'profile';profile.mkdir(exist_ok=True)
env={**os.environ,'APPDATA':str(profile),'LOCALAPPDATA':str(profile),'HELL_TRAILER_OUT':str(out)}
cmd=['E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe','--path',str(project)]
if mode=='import':cmd+=['--headless','--editor','--import']
else:
 cmd+=['--resolution','1920x1080','--fixed-fps','30','--quit-after','18000','--rendering-method','gl_compatibility']
 cmd+=['--headless','--disable-render-loop'] if mode=='probe' else ['--position','-10000,-10000','--write-movie',str(out/'raw.avi')]
log=out/'engine.log';p=subprocess.Popen(cmd,stdout=log.open('w',encoding='utf-8'),stderr=subprocess.STDOUT,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
print(json.dumps({'mode':mode,'pid':p.pid,'log':str(log)}),flush=True);p.wait();print('exit',p.returncode,flush=True)
