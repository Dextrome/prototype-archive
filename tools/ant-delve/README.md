# Ant Delve: colony turns and four-player finale

86 seconds (1:26), 1600 × 900, 30 fps, silent H.264 MP4. A native 1600 × 780
viewport sits above a separate 120-pixel caption strip. Native HUD and ant cards
remain visible.

The first 62 seconds retain eight consecutive complete turns across four rounds
of the same two-colony match, played at **1.5×**. Concise captions explain each
turn, with phase labels and audit-derived cargo, score, tile and turn counters.
The old seven-second recap/end card is removed. Both colonies remain visible
except for a brief closer shot of the antlion fight.

The final **24 seconds** show a separate, zoomed-out **four-player AI match at
6× speed**. A fixed full-map camera fits every row between the HUD and cards.
The standard Slice5 map, seed 75, native camp draft, default rosters, predator
rules and unchanged GreedyAi planner supply all gameplay. The excerpt reaches
round nine: 34 tiles added, 34 completed turns, scores 2/2/2/5. The title returns
over the continuing gameplay rather than cutting to a separate end card.

| Film time | Sequence |
| --- | --- |
| 0–3.33 | Explain place → move → end turn |
| 3.33–18 | Round 1: orange connects sugar; blue opens seeds; both workers mine |
| 18–31.33 | Round 2: extend routes, advance teammates, mine again |
| 31.33–44.67 | Round 3: three-unit worker hauls, deeper fungus reached |
| 44.67–62 | Round 4: return both hauls, bank 3/6 points, replace a miner, defeat antlion |
| 62–86 | New match: four native AI colonies, full-board overview, 6× speed |

## Capture method

`prepare.py` copies the local game into `.openai/ant-delve/game`, excluding build
outputs, then adds the capture-only director partial classes and startup hook.
The original `E:/AntDelve` project is never modified.

For the two-colony opening, tunnels, veins, positions, rosters and the stationary
antlion are staged through a native MatchState snapshot; ambient predator spawns
are disabled. Subsequent actions use unchanged `Match.Validate` and `Match.Apply`.
All eight turns remain in the film, with continuous retiming and no skipped
rivals. The source director records 100 seconds; the edit uses its first 93.

`FourPlayerDirector.cs` starts a fresh standard four-colony match, lets native AI
choose camps before the excerpt, then replays native planned commands one at a
time, waiting for movement/combat playback to settle. Each completed turn must
match the planner's projected simulation checksum. It records 144 seconds; the
edit plays those frames at 6× in 24 seconds. No cargo, score, placement, damage,
kill, healing or AI decision is forced. Four-player native predator spawning is
retained. This is automated gameplay, not a claim of human play.

The native renderer, legal placement ghosts, selection and playback are retained.
Capture view adjustments hide the combat log, separate mixed-cell sprites and
draw ants above pits. Combat beat spacing is 0.80 rather than 0.34 seconds;
damage-number holds are 1.20 rather than 0.85 seconds. Movement playback timing
is unchanged in the sources. The labeled edit speeds apply after capture.
Captions are editorial, while counters follow the corresponding match audit.
The four-player transition and both speeds are disclosed on screen. No generated
gameplay imagery is used. The build has no native audio; the film is silent.

## Reproduce on Windows

Requires local Ant Delve source, Godot 4.6.1 .NET, .NET SDK, Python/Pillow, FFmpeg
and Segoe UI fonts. Run from the archive root:

```powershell
python tools/ant-delve/prepare.py --source E:/AntDelve
dotnet build .openai/ant-delve/game/AntDelve.csproj -v quiet
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --headless --editor --path .openai/ant-delve/game --import --quit
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --headless --path .openai/ant-delve/game --fixed-fps 30 -- --trailer
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --path .openai/ant-delve/game --resolution 1600x780 --position -2400,-1200 --fixed-fps 30 --disable-vsync --write-movie E:/prototype-archive/.openai/ant-delve/raw.avi -- --trailer
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --headless --path .openai/ant-delve/game --fixed-fps 30 -- --trailer --trailer-four
& E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe --path .openai/ant-delve/game --resolution 1600x780 --position -2400,-1200 --fixed-fps 30 --disable-vsync --write-movie E:/prototype-archive/.openai/ant-delve/four-raw.avi -- --trailer --trailer-four
python tools/ant-delve/edit.py
```

The directors write separate `start-state.json`/`audit.json` and
`four-start-state.json`/`four-audit.json` files beside the capture project.
The opening verifies all eight placements/turns and its native mining, banking
and combat outcome. The finale checks all four colonies participate, at least
16 tiles are added, and each completed AI turn replays exactly. The edit checks
chapter continuity, text fit and audited outcomes. Final output:
`docs/assets/ant-delve/film-gameplay.mp4`.

Review the exported actions, wide shots, transition and retiming; update the
catalog duration, production notes and media/catalog cache versions with edits.
