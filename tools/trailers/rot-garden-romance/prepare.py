"""Prepare an isolated capture copy. Never modifies game source or player saves."""
from pathlib import Path
import shutil

production = Path('E:/trailer-production/rot-garden')
game = production / 'game'
here = Path(__file__).resolve().parent
for name in ('CaptureDirector.cs', 'Capture.tscn'):
    shutil.copy2(here / name, game / name)
p = game / 'project.godot'
text = Path('E:/RotGardenRomance/project.godot').read_text(encoding='utf-8')
text = text.replace('config/name="RotGardenRomance"', 'config/name="RotGardenTrailerCapture"')
text = text.replace('[autoload]', '[autoload]\n\nTrailerDirector="*res://Capture.tscn"')
# Director must run after the context autoload has initialized.
text = text.replace('TrailerDirector="*res://Capture.tscn"\n', '')
text = text.replace('[display]', 'TrailerDirector="*res://Capture.tscn"\n\n[display]')
text = text.replace('run/main_scene="res://Scenes/Boot.tscn"', 'run/main_scene="res://Scenes/Farming/FarmingMode.tscn"')
text = text.replace('viewport_width=1280', 'viewport_width=1600').replace('viewport_height=720', 'viewport_height=900')
p.write_text(text, encoding='utf-8')
p = game / 'Scripts/UI/Game/DateScreen.cs'
text = Path('E:/RotGardenRomance/Scripts/UI/Game/DateScreen.cs').read_text(encoding='utf-8').replace('int seed = unchecked((int)System.DateTime.UtcNow.Ticks);', 'int seed = int.Parse(System.Environment.GetEnvironmentVariable("ROT_TRAILER_SEED")!);')
p.write_text(text, encoding='utf-8')
print(game)
