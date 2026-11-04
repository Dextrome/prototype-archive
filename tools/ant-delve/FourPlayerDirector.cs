// Separate native four-player AI match for the wide time-lapse finale.
// The standard Slice5 map, camp choices, AI and simulation rules are unchanged.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using AntDelve.Sim;
using AntDelve.Net;
using Godot;

namespace AntDelve;

public partial class GameController
{
    private bool _trailerFourActive;
    private readonly Queue<Command> _fourPlan = new();
    private readonly List<object> _fourAudit = new();
    private readonly int[] _fourTurns = new int[4];
    private int _fourNextCommandFrame = 45;
    private int _fourPlacements;
    private string? _fourPlannedChecksum;
    private const int FourCaptureFrames = 4320; // 144 seconds, edited at 6x into 24 seconds.

    private void StartFourPlayerTrailer()
    {
        StartHotseat(4);
        _net.SetProcess(false); _demoMode = false;
        _shotFocus = Vector2.Zero; _pendingTurnStartFocus = null; _playback.Skip();
        _speculative = new Match(Maps.Slice5Config(75, 4));
        // Complete the native camp draft before the footage starts.
        while (Sim.Phase == TurnPhase.CampSelect)
        {
            var choice = GreedyAi.PlanTurn(Match.FromSnapshot(Sim.Snapshot())).Single();
            var valid = Sim.Validate(choice, Sim.CurrentPlayer);
            if (!valid.Ok) throw new InvalidOperationException(valid.Reason);
            Sim.Apply(choice, Sim.CurrentPlayer);
        }
        File.WriteAllText(ProjectSettings.GlobalizePath("res://../four-start-state.json"),
            JsonSerializer.Serialize(Sim.Snapshot(), new JsonSerializerOptions { WriteIndented = true }));
        State = LobbyState.InMatch;
        _playback.RegisterRoster(Sim); _hud.ShowMatch(4); _hud.CombatLog.Hide();
        ClearSelection(); Refresh(); UpdateLobbyBackdropVisibility();
        _trailerFrame = 0; _trailerActive = true; _trailerFourActive = true;
        FourPlayerCamera();
        GD.Print("[FOUR] standard Slice5; 4 native AI colonies; 144 seconds, full-board camera");
    }

    private void FourPlayerCamera()
    {
        // Capture framing fits the entire map BETWEEN the native HUD and cards.
        // Set the view directly because the manual camera's zoom floor uses the
        // full viewport, which would put the deepest row behind the card strip.
        var visible = VisibleBoardRect(12);
        var (x0, y0, x1, y1) = HexLayout.GridPixelBounds(Sim.Grid.Columns, Sim.Grid.Rows, HexSize);
        _zoom = Mathf.Min(visible.Size.X / (x1 - x0), visible.Size.Y / (y1 - y0));
        _board.Scale = Vector2.One * _zoom;
        _board.Position = visible.GetCenter() - new Vector2((x0 + x1) / 2, (y0 + y1) / 2) * _zoom;
        _board.QueueRedraw();
    }

    private void FourPlayerTrailerTick()
    {
        int f = _trailerFrame++;
        if (f < FourCaptureFrames - 60 && f >= _fourNextCommandFrame && _playback.Idle && !Sim.IsFinished)
        {
            if (_fourPlan.Count == 0)
            {
                var projection = Match.FromSnapshot(Sim.Snapshot());
                foreach (var planned in GreedyAi.PlanTurn(projection)) _fourPlan.Enqueue(planned);
                _fourPlannedChecksum = projection.Checksum().ToString("x16");
            }
            if (_fourPlan.TryDequeue(out var command))
            {
                int actor = Sim.CurrentPlayer;
                var validation = Sim.Validate(command, actor);
                if (!validation.Ok) throw new InvalidOperationException($"Four-player {command}: {validation.Reason}");
                var events = Sim.Apply(command, actor).ToArray();
                _playback.Enqueue(Sim, events, _hud.CombatLog, animateAntMoves: true);
                if (command is PlaceTile) _fourPlacements++;
                if (command is EndTurn)
                {
                    _fourTurns[actor]++;
                    if (Sim.Checksum().ToString("x16") != _fourPlannedChecksum)
                        throw new InvalidOperationException("Four-player replay differs from native AI projection");
                }
                _fourAudit.Add(new {
                    frame = f, actor, round = Sim.Round, currentPlayer = Sim.CurrentPlayer,
                    command = JsonSerializer.Serialize<Command>(command),
                    events = events.Select(e => JsonSerializer.Serialize<SimEvent>(e)).ToArray(),
                    checksum = Sim.Checksum().ToString("x16"), scores = Sim.Scores.ToArray(),
                    turns = (int[])_fourTurns.Clone(), placements = _fourPlacements,
                });
                ClearSelection(); Refresh();
                _fourNextCommandFrame = f + (command is EndTurn ? 18 : 9);
            }
        }
        FourPlayerCamera();
        if (f == FourCaptureFrames - 2)
        {
            if (_fourTurns.Any(t => t < 4) || _fourPlacements < 16 || Sim.AntCount != 20)
                throw new InvalidOperationException("Four-player footage contains insufficient progression");
            File.WriteAllText(ProjectSettings.GlobalizePath("res://../four-audit.json"),
                JsonSerializer.Serialize(_fourAudit, new JsonSerializerOptions { WriteIndented = true }));
            GD.Print($"[FOUR] VERIFIED: round {Sim.Round}; {_fourPlacements} tiles; turns {string.Join('/', _fourTurns)}; scores {string.Join('/', Sim.Scores)}");
        }
        if (f == FourCaptureFrames - 1) GetTree().Quit();
    }
}
