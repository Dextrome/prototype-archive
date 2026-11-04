# Ant Delve gameplay trailer

52 seconds, 1600 × 900, 30 fps, silent H.264 MP4. The gameplay area is a native
1600 × 780 viewport, with a separate 120-pixel caption strip. The strip never
obscures the native HUD, cards, movement highlights or combat numbers.

The sequence follows one orange worker through a connected loop, then switches
to a soldier encounter on the same board:

| Time | Scene | Native result |
| --- | --- | --- |
| 0–4 | Establish the two colonies and the nearby resources | Staged starting board |
| 4–12 | Preview and place a straight tile in the missing connection | Validated PlaceTile |
| 12–25 | Move a worker to sugar; mine over three turns | Three ResourceMined events, one unit each |
| 25–34.5 | Walk the worker home and end the turn | ResourceDeposited, three points, empty cargo |
| 34.5–46 | Move a soldier into the antlion's cell and end the turn | Four CombatBlow events, PredatorDied, soldier at 50/150 HP |
| 46–52 | Return to the wider colony view | The final board and banked score |

## Capture method

`prepare.py` copies the local game into `.openai/ant-delve/game`, excluding build
outputs. It adds `TrailerDirector.cs` as a capture-only partial class and inserts
the startup/process hook. The original `E:/AntDelve` project is never modified.

Starting tunnel geometry, resource veins, colony positions and the stationary
antlion are authored through a native MatchState snapshot. Ambient predator
spawns are disabled. All subsequent changes use unchanged `Match.Validate` and
`Match.Apply`; the director records each command, native event and checksum.
Rival colonies pass through validated commands; those idle turns are omitted
from the film. There is no injected cargo, score, damage, kill or healing.

The native renderer, HUD, selection, legal placement ghost, movement playback,
combat playback, HP and damage effects are retained. The combat log is hidden.
Capture-only view changes separate mixed-cell sprites horizontally and draw ants
above the antlion's pit so neither combatant disappears. Combat beat spacing is
0.80 seconds instead of 0.34; damage numbers remain for 1.20 seconds instead of
0.85. Movement timing and simulation rules are unchanged. Camera zooms and holds
are authored independently of the game's automatic colony camera.

The cargo/score caption values come from the capture audit. All other captions
are editorial. The game has no native sound effects in this build; the film is
silent. No generated gameplay imagery is used.

## Reproduce on Windows

Requires the local Ant Delve source, Godot 4.6.1 .NET, the .NET SDK, Python with
Pillow, FFmpeg and Segoe UI fonts. Run from the archive root:

```powershell
python tools/ant-delve/prepare.py --source E:/AntDelve
dotnet build .openai/ant-delve/game/AntDelve.csproj -v quiet
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --headless --editor --path .openai/ant-delve/game --import --quit
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --headless --path .openai/ant-delve/game --fixed-fps 30 -- --trailer
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --path .openai/ant-delve/game --resolution 1600x780 --position -2400,-1200 --fixed-fps 30 --disable-vsync --write-movie E:/prototype-archive/.openai/ant-delve/raw.avi -- --trailer
python tools/ant-delve/edit.py
```

The director verifies the outcome before exiting and writes `start-state.json`
and `audit.json` in `.openai/ant-delve`. The final file is
`docs/assets/ant-delve/film-gameplay.mp4`. Review the native actions and chapter
boundaries in the exported movie before replacing gallery media.
