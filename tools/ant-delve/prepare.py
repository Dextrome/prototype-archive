"""Make an isolated Ant Delve capture project; never edit the original game."""
from pathlib import Path
import argparse
import shutil

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, default=Path('E:/AntDelve'))
p.add_argument('--output', type=Path, default=Path('.openai/ant-delve/game'))
a = p.parse_args()
here = Path(__file__).resolve().parent
a.output.mkdir(parents=True, exist_ok=True)
for directory in ('Scripts', 'Scenes', 'Assets', 'AntDelve.Sim', 'AntDelve.Net'):
    shutil.copytree(a.source / directory, a.output / directory, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('bin', 'obj', '.godot'))
shutil.copy2(a.source / 'AntDelve.csproj', a.output / 'AntDelve.csproj')
config = (a.source / 'project.godot').read_text(encoding='utf-8-sig')
config = config.replace('[autoload]\n\nGodotAIBridgeRuntime="*res://addons/godot_ai_bridge/runtime_bridge.gd"', '')
config = config.replace('enabled=PackedStringArray("res://addons/godot_ai_bridge/plugin.cfg")', 'enabled=PackedStringArray()')
config = config.replace('viewport_width=1280', 'viewport_width=1600').replace('viewport_height=720', 'viewport_height=780')
config = config.replace('window/size/mode=2', 'window/size/mode=0')
config = config.replace('renderer/rendering_method="forward_plus"', 'renderer/rendering_method="gl_compatibility"')
(a.output / 'project.godot').write_text(config, encoding='utf-8')
controller = a.output / 'Scripts/Core/GameController.cs'
code = controller.read_text(encoding='utf-8-sig')
code = code.replace('        ParseDemoArgs();', '        ParseDemoArgs();\n        if (System.Array.IndexOf(OS.GetCmdlineUserArgs(), "--trailer") >= 0) CallDeferred(nameof(StartTrailer));')
code = code.replace('        UpdateLobbyBackdropVisibility();', '        if (_trailerActive) { TrailerTick(); return; }\n        UpdateLobbyBackdropVisibility();', 1)
controller.write_text(code, encoding='utf-8')
shutil.copy2(here / 'TrailerDirector.cs', a.output / 'Scripts/Core/TrailerDirector.cs')
shutil.copy2(here / 'FourPlayerDirector.cs', a.output / 'Scripts/Core/FourPlayerDirector.cs')
# Presentation-only capture adjustments: keep the ant visible beside the pit
# and hold combat beats long enough to read their native HP/damage numbers.
for relative, old, new in (
    ('Scripts/Board/AntLayer.cs', 'var pos = center + anchor.Offset;',
     'var pos = center + anchor.Offset + (placement.Mixed ? new Vector2(-_hexSize * 0.22f, 0f) : Vector2.Zero);'),
    ('Scripts/Board/PredatorLayer.cs', 'DrawByKind(kind, coord, anchor.Offset, PhaseFor(id), t, loaded);',
     'DrawByKind(kind, coord, anchor.Offset + (placement is { Mixed: true } ? new Vector2(_hexSize * 0.22f, 0f) : Vector2.Zero), PhaseFor(id), t, loaded);'),
    ('Scripts/Board/BoardView.cs', '_ants = new AntLayer();', '_ants = new AntLayer { ZIndex = 1 };'),
    ('Scripts/Board/BoardView.cs', '_fx = new FxLayer();', '_fx = new FxLayer { ZIndex = 2 };'),
    ('Scripts/Core/ViewTunables.cs', 'BlowSeconds = 0.34f', 'BlowSeconds = 0.80f'),
    ('Scripts/Core/ViewTunables.cs', 'DamageNumberSeconds = 0.85f', 'DamageNumberSeconds = 1.20f'),
):
    target = a.output / relative
    text = target.read_text(encoding='utf-8-sig')
    assert old in text, (relative, old)
    target.write_text(text.replace(old, new), encoding='utf-8')
print(a.output.resolve())
