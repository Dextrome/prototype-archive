from pathlib import Path
import shutil, hashlib, json, re
src=Path('E:/Meldkin'); stage=Path('work/meldkin-trailer'); dst=stage/'project'
stage.mkdir(parents=True,exist_ok=True)
roots=['Assets','Data','Scenes','Scripts','lib','Meldkin.Tests']
files=[src/n for n in ['project.godot','Meldkin.csproj','Meldkin.sln','icon.svg','icon.svg.import'] if (src/n).exists()]
files += list(src.glob('icon*.png'))
for name in roots:
    files += [p for p in (src/name).rglob('*') if p.is_file() and not any(x in {'bin','obj','.godot'} for x in p.relative_to(src/name).parts)]
hashes={p.relative_to(src).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(stage/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
for p in files:
    dest=dst/p.relative_to(src);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
cfg=(dst/'project.godot').read_text(encoding='utf-8-sig')
cfg='\n'.join(l for l in cfg.splitlines() if not l.startswith('GodotAIBridgeRuntime=') and not l.startswith('enabled=PackedStringArray('))
cfg=cfg.replace('config/name="Meldkin"','config/name="Meldkin Trailer Isolated"')
(dst/'project.godot').write_text(cfg,encoding='utf-8')
print(json.dumps({'files':len(files),'bytes':sum(p.stat().st_size for p in files),'copy':str(dst.resolve())}))

for name in ["TrailerStage.cs","TrailerDirector.cs","Trailer.tscn"]:
    shutil.copy2(Path(__file__).parent/name,dst/name)
