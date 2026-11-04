// Capture-only partial class, compiled in an isolated copy of the game.
// The starting board/rosters are staged. Every subsequent change is a validated
// native Command. Mining, banking, movement, damage and deaths are never injected.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using AntDelve.Sim;
using Godot;

namespace AntDelve;

public partial class GameController
{
    private bool _trailerActive;
    private int _trailerFrame;
    private readonly List<object> _trailerAudit = new();
    private int _trailerPlacements, _trailerTurns;
    private readonly Axial _trailerGap = new(4, 2);
    private readonly Axial _trailerMine = new(4, 3);
    private readonly Axial _trailerHome = new(4, 0);
    private readonly Axial _trailerGuard = new(5, 4);

    private void StartTrailer()
    {
        if (Array.IndexOf(OS.GetCmdlineUserArgs(), "--trailer-four") >= 0) { StartFourPlayerTrailer(); return; }
        StartHotseat(2);
        _net.SetProcess(false);
        _demoMode = false;
        _shotFocus = Vector2.Zero; // suppress the automatic turn/fight camera
        _pendingTurnStartFocus = null;
        _playback.Skip();
        var cfg = new MatchConfig { Seed = 75, PlayerCount = 2, MapId = "slice2",
            Columns = 20, Rows = 12, LoamStartRow = 4, BedrockStartRow = 9,
            RoundLimit = 22, PredatorDensityPercent = 0 };
        var s = new Match(cfg).Snapshot();
        Array.Clear(s.CellStates); Array.Clear(s.CellMasks); Array.Clear(s.CellVeins);
        Array.Clear(s.CellVeinKinds); Array.Fill(s.CellNests, (sbyte)-1);
        Array.Clear(s.CellPheromone); Array.Fill(s.CellPheromoneOwner, (sbyte)-1);
        Array.Clear(s.CellFeatures); Array.Clear(s.CellChestIds);
        int I(Axial c) => c.R * cfg.Columns + c.Q - CellGrid.QMin(c.R);
        void Carve(Axial c, byte mask, int owner = -1)
        {
            int i = I(c); s.CellStates[i] = (byte)CellState.Excavated; s.CellMasks[i] = mask;
            if (owner >= 0) { s.CellPheromone[i] = 23; s.CellPheromoneOwner[i] = (sbyte)owner; }
        }
        Carve(_trailerHome, Maps.NestMask, 0); s.CellNests[I(_trailerHome)] = 0;
        Carve(new(4, 1), 0b100100, 0);
        Carve(_trailerMine, 0b100101); // NW to the gap; east to the soldier
        s.CellVeins[I(_trailerMine)] = 5;
        Carve(new(5, 3), 0b101000, 0); // west to sugar, SE to guard
        Carve(_trailerGuard, Maps.PocketMask);
        s.CellVeins[I(_trailerGuard)] = 5; s.CellVeinKinds[I(_trailerGuard)] = (byte)ResourceKind.Fungus;
        Carve(new(10, 0), Maps.NestMask, 1); s.CellNests[I(new(10, 0))] = 1;
        Carve(new(10, 1), 0b100100, 1); Carve(new(10, 2), 0b100100, 1);
        s.CellVeins[I(new(10, 3))] = 4; s.CellVeinKinds[I(new(10, 3))] = (byte)ResourceKind.Seed;
        s.CellVeins[I(new(10, 5))] = 3; s.CellVeinKinds[I(new(10, 5))] = (byte)ResourceKind.Fungus;
        s.CellVeins[I(new(5, 7))] = 3; s.CellVeinKinds[I(new(5, 7))] = (byte)ResourceKind.Seed;
        var ants = s.Ants.Select(a => a with {
            Q = a.Owner == 0 ? 4 : 10, R = 0, CarriedSugar = 0, CarriedSeed = 0,
            CarriedFungus = 0, CurioId = 0, Hp = Balance.CasteStats((Caste)a.Caste).MaxHp,
            MovePointsLeft = Balance.CasteStats((Caste)a.Caste).Move,
        }).ToArray();
        ants[0] = ants[0] with { Q = 4, R = 1 };
        ants[2] = ants[2] with { Q = 5, R = 3 };
        ants[5] = ants[5] with { Q = 10, R = 2 };
        _speculative = Match.FromSnapshot(s with {
            Ants = ants, Predators = [new PredatorSnap(0, (byte)PredatorKind.Antlion, 5, 4,
                Balance.PredatorStats(PredatorKind.Antlion).MaxHp)], NextPredatorId = 1,
            Scores = [0, 0], Phase = TurnPhase.Place, CurrentPlayer = 0, Round = 1,
        });
        File.WriteAllText(ProjectSettings.GlobalizePath("res://../start-state.json"),
            JsonSerializer.Serialize(Sim.Snapshot(), new JsonSerializerOptions { WriteIndented = true }));
        State = LobbyState.InMatch;
        _playback.RegisterRoster(Sim);
        _hud.ShowMatch(2); _hud.CombatLog.Hide();
        ClearSelection(); Refresh(); UpdateLobbyBackdropVisibility();
        _trailerActive = true;
        _trailerFrame = 0;
        TrailerCamera(0);
        GD.Print("[TRAILER] staged start; native simulation; 8 consecutive complete turns; 100 seconds at 30 fps");
    }

    private void TrailerCommand(Command command, bool animate = false)
    {
        int actor = Sim.CurrentPlayer;
        var validation = Sim.Validate(command, actor);
        if (!validation.Ok) throw new InvalidOperationException($"Trailer {command}: {validation.Reason}");
        var events = Sim.Apply(command, actor).ToArray();
        if (command is PlaceTile) _trailerPlacements++;
        if (command is EndTurn) _trailerTurns++;
        _playback.Enqueue(Sim, events, _hud.CombatLog, animateAntMoves: animate);
        _trailerAudit.Add(new { frame = _trailerFrame, actor,
            command = JsonSerializer.Serialize<Command>(command),
            events = events.Select(e => JsonSerializer.Serialize<SimEvent>(e)).ToArray(),
            checksum = Sim.Checksum().ToString("x16"), round = Sim.Round,
            currentPlayer = Sim.CurrentPlayer, phase = Sim.Phase.ToString(),
            sugar = Sim.Ant(0).CarriedSugar, score = Sim.Scores[0],
            blueSeed = Sim.Ant(5).CarriedSeed, blueScore = Sim.Scores[1],
            orangeFungus = Sim.Ant(2).CarriedFungus, blueFungus = Sim.Ant(7).CarriedFungus,
            placements = _trailerPlacements, turns = _trailerTurns,
            soldierHp = Sim.Ant(2).Hp, predators = Sim.PredatorCount });
        GD.Print($"[TRAILER] frame {_trailerFrame} P{actor + 1} {command}; sugar {Sim.Ant(0).CarriedSugar}; score {Sim.Scores[0]}");
        Refresh();
    }

    private void TrailerPreview(Axial cell)
    {
        SelectPlacementCell(cell); SelectPaletteShape("straight");
        // Preview the exact rotation that will be committed.
        int option = _placementOptions.FindIndex(o => o.ShapeId == "straight" && o.Rotation == 2);
        if (option < 0) throw new InvalidOperationException($"No straight preview at {cell}");
        PlacementOptionIndex = option; Refresh();
    }

    private void TrailerPlace(Axial cell)
    {
        TrailerCommand(new PlaceTile("straight", 2, cell)); ClearSelection();
    }

    private void TrailerMove(int ant, params Axial[] path)
    {
        TrailerCommand(new MoveAnt(ant, path), true); ClearSelection();
    }

    private void TrailerEnd()
    {
        ClearSelection(); TrailerCommand(new EndTurn());
    }

    private void TrailerTick()
    {
        if (_trailerFourActive) { FourPlayerTrailerTick(); return; }
        int f = _trailerFrame++;
        switch (f)
        {
            // Round 1: both colonies connect a resource and send a worker.
            case 174: TrailerPreview(_trailerGap); break;
            case 240: TrailerPlace(_trailerGap); break;
            case 285: SelectAnt(0); break;
            case 330: TrailerMove(0, new(4, 2), _trailerMine); break;
            case 420: TrailerEnd(); break;
            case 534: TrailerPreview(new(10, 3)); break;
            case 600: TrailerPlace(new(10, 3)); break;
            case 630: SelectAnt(5); break;
            case 660: TrailerMove(5, new Axial(10, 3)); break;
            case 720: TrailerEnd(); break;
            // Round 2: teammates advance while the original workers mine.
            case 834: TrailerPreview(new(5, 5)); break;
            case 900: TrailerPlace(new(5, 5)); break;
            case 930: SelectAnt(1); break;
            case 960: TrailerMove(1, new Axial(4, 1)); break;
            case 1020: TrailerEnd(); break;
            case 1134: TrailerPreview(new(10, 4)); break;
            case 1200: TrailerPlace(new(10, 4)); break;
            case 1230: SelectAnt(7); break;
            case 1260: TrailerMove(7, new(10, 1), new(10, 2), new(10, 3), new(10, 4)); break;
            case 1320: TrailerEnd(); break;
            // Round 3: third loads at the first veins; deeper fungus reached.
            case 1434: TrailerPreview(new(5, 6)); break;
            case 1500: TrailerPlace(new(5, 6)); break;
            case 1530: SelectAnt(1); break;
            case 1560: TrailerMove(1, new Axial(4, 2)); break;
            case 1620: TrailerEnd(); break;
            case 1734: TrailerPreview(new(10, 5)); break;
            case 1800: TrailerPlace(new(10, 5)); break;
            case 1830: SelectAnt(7); break;
            case 1860: TrailerMove(7, new Axial(10, 5)); break;
            case 1920: TrailerEnd(); break;
            // Round 4: banking, a replacement miner, and native combat.
            case 2034: TrailerPreview(new(5, 7)); break;
            case 2100: TrailerPlace(new(5, 7)); break;
            case 2115: SelectAnt(0); break;
            case 2145: TrailerMove(0, new(4, 2), new(4, 1), _trailerHome); break;
            case 2190: SelectAnt(1); break;
            case 2220: TrailerMove(1, _trailerMine); break;
            case 2250: SelectAnt(2); break;
            case 2280: TrailerMove(2, _trailerGuard); break;
            case 2310: TrailerEnd(); break;
            case 2454: TrailerPreview(new(10, 6)); break;
            case 2520: TrailerPlace(new(10, 6)); break;
            case 2550: SelectAnt(5); break;
            case 2580: TrailerMove(5, new(10, 2), new(10, 1), new(10, 0)); break;
            case 2670: TrailerEnd(); break;
            case 2998:
                if (Sim.Scores[0] != 3 || Sim.Scores[1] != 6 || Sim.Ant(0).CarriedTotal != 0
                    || Sim.Ant(5).CarriedTotal != 0 || Sim.PredatorCount != 0 || Sim.Ant(2).Hp <= 0
                    || Sim.Round != 5 || Sim.CurrentPlayer != 0 || _trailerPlacements != 8 || _trailerTurns != 8)
                    throw new InvalidOperationException("Trailer outcome validation failed");
                File.WriteAllText(ProjectSettings.GlobalizePath("res://../audit.json"),
                    JsonSerializer.Serialize(_trailerAudit, new JsonSerializerOptions { WriteIndented = true }));
                GD.Print("[TRAILER] VERIFIED: 8 placements, 8 full turns, 4 rounds; scores 3 / 6; antlion defeated");
                break;
            case 2999: GetTree().Quit(); break;
        }
        TrailerCamera(f / 30f);
    }

    private void TrailerCamera(float seconds)
    {
        // Whole turns and handoffs share the same view of BOTH colonies.
        // Pull back as tunnels grow; approach only the round-four fight.
        (float T, Vector2 P, float Z)[] keys = [
            (0, new(910, 255), 1.0f), (26.8f, new(910, 255), 1.0f),
            (28.5f, new(935, 310), 0.82f), (74.5f, new(935, 310), 0.82f),
            (75.7f, new(776, 360), 2.65f), (80.2f, new(776, 360), 2.65f),
            (81, new(935, 310), 0.82f), (100, new(935, 310), 0.82f),
        ];
        var left = keys[0]; var right = keys[^1];
        for (int i = 1; i < keys.Length; i++) if (seconds <= keys[i].T) { left = keys[i-1]; right = keys[i]; break; }
        float t = Mathf.Clamp((seconds - left.T) / (right.T - left.T), 0, 1);
        t = t * t * (3 - 2 * t);
        ApplyView(left.P.Lerp(right.P, t), Mathf.Lerp(left.Z, right.Z, t));
    }
}
