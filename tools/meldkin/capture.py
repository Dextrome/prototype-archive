from pathlib import Path
import subprocess,os,sys,json
base=Path.cwd();stage=base/'work/meldkin-trailer';project=stage/'project'
godot='E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe'
if sys.argv[1]=='import':
    p=subprocess.run([godot,'--headless','--editor','--path',str(project),'--import'],stdout=(stage/'import.log').open('w'),stderr=subprocess.STDOUT)
    print('import',p.returncode);sys.exit(p.returncode)
combo=int(sys.argv[1]);out=stage/f'combo{combo}';out.mkdir(exist_ok=True)
profile=stage/f'profile{combo}';profile.mkdir(exist_ok=True)
env={**os.environ,'APPDATA':str(profile),'LOCALAPPDATA':str(profile),'TRAILER_COMBO':str(combo)}
cmd=[godot,'--path',str(project),'--scene','res://Trailer.tscn','--position','-10000,-10000','--resolution','2280x1080','--rendering-method','gl_compatibility','--write-movie',str(out/'raw.avi'),'--fixed-fps','30','--quit-after','4500','--','--window_size','2280x1080','--ui_scale','1.15','--no_sim_thread','--no_progression','--growth_save',str(out/'growth.cfg'),'--growth_grant_xp','30000']
if combo==3 and (out/'growth.cfg').exists():
    (out/'growth-first-attempt.cfg').write_bytes((out/'growth.cfg').read_bytes());(out/'growth.cfg').unlink()
log=(out/'capture.log').open('w',encoding='utf-8')
p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
(out/'pid.txt').write_text(str(p.pid));print(json.dumps({'pid':p.pid,'combo':combo}));p.wait();print('exit',p.returncode)
