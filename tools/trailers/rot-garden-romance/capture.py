from pathlib import Path
import os
import subprocess
import sys

work = Path('E:/trailer-production/rot-garden')
game = work / 'game'
godot = 'E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe'
profile = work / 'profile'
profile.mkdir(exist_ok=True)
env = {**os.environ, 'APPDATA': str(profile), 'LOCALAPPDATA': str(profile),
       'ROT_TRAILER_AUDIT': str(work / 'audit.json')}
if len(sys.argv) > 1 and sys.argv[1] == 'import':
    cmd = [godot, '--headless', '--editor', '--path', str(game), '--import']
else:
    cmd = [godot, '--path', str(game), '--rendering-method', 'gl_compatibility',
           '--position', '-10000,-10000', '--resolution', '1600x900',
           '--fixed-fps', '30', '--write-movie', str(work / 'raw.avi'), '--quit-after', '1810']
with (work / ('import.log' if 'import' in sys.argv else 'capture.log')).open('w', encoding='utf-8') as log:
    result = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT,
                            creationflags=subprocess.CREATE_NO_WINDOW)
print('exit', result.returncode)
sys.exit(result.returncode)
