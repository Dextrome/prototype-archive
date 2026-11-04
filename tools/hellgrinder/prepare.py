from pathlib import Path
import shutil,hashlib,json,subprocess
src=Path('E:/Hellgrinder');stage=Path('work/hellgrinder-loop');dst=stage/'project';stage.mkdir(parents=True,exist_ok=True)
roots=['Assets','Scripts','Scenes','Core','Tests']
files=[src/n for n in ['project.godot','Hellgrinder.csproj','Hellgrinder.sln','default_bus_layout.tres']]
for name in roots:files += [p for p in (src/name).rglob('*') if p.is_file() and not any(x in {'bin','obj','.godot'} for x in p.relative_to(src/name).parts)]
hashes={p.relative_to(src).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(stage/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
(stage/'source-git-status.txt').write_text(subprocess.run(['git','status','--porcelain=v1','--untracked-files=all'],cwd=src,capture_output=True,text=True,check=True).stdout)
for p in files:
 dest=dst/p.relative_to(src);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
cfg=(dst/'project.godot').read_text(encoding='utf-8-sig')
cfg='\n'.join(l for l in cfg.splitlines() if not l.startswith(('GodotAIBridgeRuntime=','enabled=PackedStringArray(')))
cfg=cfg.replace('config/name="Hellgrinder"','config/name="Hellgrinder Trailer Isolated"')
(dst/'project.godot').write_text(cfg,encoding='utf-8')
print(json.dumps({'files':len(files),'bytes':sum(p.stat().st_size for p in files),'copy':str(dst.resolve())}))

for name in ['TrailerBridge.cs','TrailerDirector.cs']:
    shutil.copy2(Path(__file__).parent/name,dst/name)
for source,target in [('ISimulationStrategy.cs','TrailerStrategyInterface.cs'),('Strategies.cs','TrailerStrategies.cs')]:
    shutil.copy2(src/'Tests/Simulation'/source,dst/target)
cfg=(dst/'project.godot').read_text(encoding='utf-8').replace('[autoload]','[autoload]\n\nTrailerDirector="*res://TrailerDirector.cs"')
(dst/'project.godot').write_text(cfg,encoding='utf-8')
