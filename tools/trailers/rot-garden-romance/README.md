# Rot Garden Romance — garden-to-date gameplay story

60 seconds, 30 fps, 1600×1000, silent. The original 19-second film is retained;
the archive now selects `film-gameplay.mp4` and classifies it as gameplay.

One continuous sequence connects planting a Blood Turnip, skipping eight minutes
of crop growth, selecting its native Reckless Compliment harvest option,
inspecting the resulting 15-card deck, and taking Mira to the Cemetery Picnic.
The card encounter uses the unchanged native rules. Six actions produce
10 → 13 → 16 → 24 → 24 → 27 affection, including an end turn. The native victory
advances Mira from Stranger to Bond and awards a new seed. The story returns to
the farm. Dialogue and choices are original game content; captions are editorial.

## Reproduce on the production machine

1. Copy `E:/RotGardenRomance` to `E:/trailer-production/rot-garden/game`, excluding
   `.git`, `.godot`, `.claude`, `.codex`, `artifacts`, `build`, `concept_art`, `Tests`.
2. Run `python tools/trailers/rot-garden-romance/prepare.py` from the archive.
3. Run `dotnet build E:/trailer-production/rot-garden/game/RotGardenRomance.csproj`.
4. Run `python tools/trailers/rot-garden-romance/capture.py import`.
5. Run `python tools/trailers/rot-garden-romance/capture.py`.
6. Run `python tools/trailers/rot-garden-romance/edit.py`.

The capture sets its own APPDATA/LOCALAPPDATA and project name. The original game
and player saves are untouched. A previously met Mira and completed tutorial are
starting conditions. The director searches native deterministic deck seeds for a
short winning line that actually plays the harvested card; the selected seed is
2. Actions invoke native UI handlers and button signals. Growth uses the game's
existing debug time-advance function; the film explicitly says eight minutes
later. Text reveal and next-line inputs are grouped, followed by reading holds.
Native focus styling identifies the card before each play. A debug button is
hidden for the capture; no combat, reward or relationship results are injected.

The editor adds a caption band outside the game viewport and closer farm/deck
crops. The date retains the full hand and meters. `validation.json` records the
actual deck, affection, energy, turns, outcome and resulting relationship;
`edit-decision-list.json` records the story chapters. The editor refuses to encode
unless it finds the native win, harvested card, expected meter changes and Bond.

Godot prints native texture/font resource-leak diagnostics during shutdown;
the verified capture exits successfully after 1800 recorded frames.
