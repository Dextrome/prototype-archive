# 7 Ants Underground — rope & toybox trailer

36.2 seconds, 1600 × 900, 60 fps, H.264/AAC. The delivered film is `docs/assets/seven-ants-underground/film.mp4`.

The capture uses a separate copy of the current OreilChaos project, including its existing local changes. The original game and saves are preserved. `production.json` records staging and native mechanics; `edit-decision-list.json` records every selected excerpt. Raw AVIs remain outside the gallery repository.

The native host simulation receives ordinary scripted inputs. Actors, starting positions, loadouts and breach-room cover are staged. Hits, damage, rope motion and deaths are resolved by existing game code. The Panic shot begins at native lava tick 630. Gameplay plays at normal speed, with forward cuts. The only modification to an existing game source file in the capture copy replaces the wall clock used to restore native hit-stop with the fixed movie-frame clock.

`CaptureDirector.cs`, `SessionManager.Capture.cs` and `Capture.tscn` provide the capture fixture. `capture.ps1` copies the game into a production directory, builds it and renders the selected scenes. It needs Godot 4.6.1 Mono and the .NET 8 SDK. Capture opens an offscreen render window; it does not record the desktop.

```powershell
./capture.ps1 -SourceProject E:/Oreil/OreilChaos -ProductionRoot E:/trailer-production/seven-ants
$env:SEVEN_ANTS_PRODUCTION_ROOT = 'E:/trailer-production/seven-ants'
python ./edit.py
```

The edit requires FFmpeg on PATH and Python with NumPy, SciPy and Pillow. Typography uses Windows Bahnschrift and Impact. `edit.py` creates the title art, captions and an original synthesized electronic score, edits native procedural audio with the footage, and writes `7-Ants-Underground-gameplay-trailer.mp4` into the production directory. No external music or generated gameplay is used.
