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
    private readonly Axial _trailerGap = new(4, 2);
    private readonly Axial _trailerMine = new(4, 3);
    private readonly Axial _trailerHome = new(4, 0);
    private readonly Axial _trailerGuard = new(5, 4);

    private void StartTrailer()
    {
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
        GD.Print("[TRAILER] staged start; native simulation; 52 seconds at 30 fps");
    }

    private void TrailerCommand(Command command, bool animate = false)
    {
        int actor = Sim.CurrentPlayer;
        var validation = Sim.Validate(command, actor);
        if (!validation.Ok) throw new InvalidOperationException($"Trailer {command}: {validation.Reason}");
        var events = Sim.Apply(command, actor).ToArray();
        _playback.Enqueue(Sim, events, _hud.CombatLog, animateAntMoves: animate);
        _trailerAudit.Add(new { frame = _trailerFrame, actor,
            command = JsonSerializer.Serialize<Command>(command),
            events = events.Select(e => JsonSerializer.Serialize<SimEvent>(e)).ToArray(),
            checksum = Sim.Checksum().ToString("x16"), round = Sim.Round,
            sugar = Sim.Ant(0).CarriedSugar, score = Sim.Scores[0],
            soldierHp = Sim.Ant(2).Hp, predators = Sim.PredatorCount });
        GD.Print($"[TRAILER] frame {_trailerFrame} P{actor + 1} {command}; sugar {Sim.Ant(0).CarriedSugar}; score {Sim.Scores[0]}");
        Refresh();
    }

    private void TrailerEndAndPassRival()
    {
        ClearSelection(); TrailerCommand(new EndTurn());
        // A forward edit: the other colony passes. Both are native commands,
        // validated and audited. The film explicitly discloses omitted rival turns.
        TrailerCommand(new SkipPlace()); TrailerCommand(new EndTurn());
        Refresh();
    }

    private void TrailerTick()
    {
        int f = _trailerFrame++;
        switch (f)
        {
            case 165: SelectPlacementCell(_trailerGap); SelectPaletteShape("straight"); break;
            case 255:
                TrailerCommand(new PlaceTile("straight", 2, _trailerGap)); ClearSelection(); break;
            case 390: SelectAnt(0); break;
            case 450:
                TrailerCommand(new MoveAnt(0, [new(4, 2), _trailerMine]), true); ClearSelection(); break;
            case 510: TrailerEndAndPassRival(); break;
            case 585: TrailerCommand(new SkipPlace()); TrailerEndAndPassRival(); break;
            case 660: TrailerCommand(new SkipPlace()); TrailerEndAndPassRival(); break;
            case 795: SelectAnt(0); break;
            case 825:
                TrailerCommand(new SkipPlace());
                TrailerCommand(new MoveAnt(0, [new(4, 2), new(4, 1), _trailerHome]), true);
                ClearSelection(); break;
            case 915: TrailerEndAndPassRival(); break;
            case 1080: SelectAnt(2); break;
            case 1125:
                TrailerCommand(new SkipPlace());
                TrailerCommand(new MoveAnt(2, [_trailerGuard]), true); ClearSelection(); break;
            case 1185: TrailerEndAndPassRival(); break;
            case 1558:
                if (Sim.Scores[0] != 3 || Sim.Ant(0).CarriedTotal != 0 || Sim.PredatorCount != 0
                    || Sim.Ant(2).Hp <= 0) throw new InvalidOperationException("Trailer outcome validation failed");
                File.WriteAllText(ProjectSettings.GlobalizePath("res://../audit.json"),
                    JsonSerializer.Serialize(_trailerAudit, new JsonSerializerOptions { WriteIndented = true }));
                GD.Print("[TRAILER] VERIFIED: 3 mined, 3 banked, antlion defeated, soldier survived");
                break;
            case 1559: GetTree().Quit(); break;
        }
        TrailerCamera(f / 30f);
    }

    private void TrailerCamera(float seconds)
    {
        // Explicit scene framing prevents colony jumps. Ease only between shots;
        // hold the camera during inputs, mining and combat.
        (float T, Vector2 P, float Z)[] keys = [
            (0, new(740, 205), 1.25f), (3.8f, new(740, 205), 1.25f),
            (5.0f, new(554, 192), 2.05f), (14.7f, new(554, 192), 2.05f),
            (16.5f, new(610, 288), 3.35f), (24.8f, new(610, 288), 3.35f),
            (26.3f, new(535, 152), 1.55f), (29.3f, new(535, 152), 1.55f),
            (30.4f, new(443, 0), 3.0f), (33.6f, new(443, 0), 3.0f),
            (35.2f, new(776, 360), 3.25f), (44.7f, new(776, 360), 3.25f),
            (46.5f, new(690, 205), 1.35f), (52, new(690, 205), 1.35f),
        ];
        var left = keys[0]; var right = keys[^1];
        for (int i = 1; i < keys.Length; i++) if (seconds <= keys[i].T) { left = keys[i-1]; right = keys[i]; break; }
        float t = Mathf.Clamp((seconds - left.T) / (right.T - left.T), 0, 1);
        t = t * t * (3 - 2 * t);
        ApplyView(left.P.Lerp(right.P, t), Mathf.Lerp(left.Z, right.Z, t));
    }
}
