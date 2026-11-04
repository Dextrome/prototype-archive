using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text.Json;
using Godot;
using RotGardenRomance.Core.Game;
using RotGardenRomance.UI.Game;
using RotGardenRomance.Farming;

// Only installed in the isolated capture copy. All actions call native handlers.
public partial class CaptureDirector : Node
{
    private int frame;
    private GameContext ctx = null!;
    private readonly List<object> audit = new();
    private readonly List<string> plan = new();
    private int move;
    private static object Field(object obj, string name) => obj.GetType().GetField(name, BindingFlags.Instance | BindingFlags.NonPublic)!.GetValue(obj)!;
    private static object? Invoke(object obj, string name, params object[] args) => obj.GetType().GetMethod(name, BindingFlags.Instance | BindingFlags.NonPublic)!.Invoke(obj, args);
    private Node Scene => GetTree().CurrentScene;
    private FarmingMode Farm => (FarmingMode)Scene;
    private static IEnumerable<Node> Walk(Node n) { yield return n; foreach (Node child in n.GetChildren(includeInternal: true)) foreach (var item in Walk(child)) yield return item; }
    private DialogueOverlay Overlay => Walk(Scene).OfType<DialogueOverlay>().First(n => !n.IsQueuedForDeletion());
    private void Press(string text) => Walk(Scene).OfType<Button>().First(b => b.IsVisibleInTree() && !b.Disabled && b.Text.Contains(text, StringComparison.OrdinalIgnoreCase)).EmitSignal(BaseButton.SignalName.Pressed);
    private void Line() { Invoke(Overlay, "SkipReveal"); Invoke(Overlay, "OnContinue"); Invoke(Overlay, "SkipReveal"); }
    private void Log(string action) { audit.Add(new { frame, action, deck = ctx.Farm.DeckCardIds.ToArray(), bond = ctx.Farm.Mira.Level.ToString(), won = ctx.Farm.WonDateIds.ToArray() }); GD.Print($"[trailer] {frame / 30.0:F2} {action}"); System.IO.File.WriteAllText(System.Environment.GetEnvironmentVariable("ROT_TRAILER_AUDIT")!, JsonSerializer.Serialize(audit, new JsonSerializerOptions { WriteIndented = true })); }

    public override void _Ready()
    {
        ctx = GetNode<GameContext>("/root/GameContext");
        ctx.StartNewGame();
        ctx.Farm.TutorialActive = false;
        ctx.Farm.TutorialPromptResolved = true;
        ctx.Farm.TutorialCompleted = true;
        ctx.Farm.MetGirlIds.Add("mira"); // This is a return visit, not a first meeting.
        ctx.Farm.SecondsToNextNight = 1800;
        FindPlan();
    }
    private void FindPlan()
    {
        var deck = ctx.Farm.DeckCardIds.Concat(new[] { "reckless_compliment" }).ToArray();
        var def = ctx.Dates.All["cemetery_picnic"];
        for (int seed = 0; seed < 10000; seed++)
        {
            var rt = new DateRuntime(def, ctx.Cards.All, deck, seed);
            rt.ApplyStartingOffsets(1, new Dictionary<string, int> { ["Awkwardness"] = -1 });
            rt.Begin();
            if (!rt.Deck.Hand.Any(c => c.CardId == "reckless_compliment")) continue;
            var steps = new List<string>();
            bool usedHarvest = false;
            while (rt.Outcome == DateOutcome.Ongoing && steps.Count < 6)
            {
                var card = Pick(rt);
                if (card == null) { steps.Add("end_turn"); rt.EndTurn(); }
                else { steps.Add(card.CardId); usedHarvest |= card.CardId == "reckless_compliment"; rt.TryPlay(card); }
            }
            if (rt.Outcome != DateOutcome.Win || !usedHarvest) continue;
            System.Environment.SetEnvironmentVariable("ROT_TRAILER_SEED", seed.ToString());
            plan.AddRange(steps);
            audit.Add(new { action = "plan", seed, steps, finalAffection = rt.Affection });
            GD.Print($"[trailer] seed {seed}, plan {string.Join(",", steps)}");
            return;
        }
        throw new Exception("No native six-action winning line found.");
    }
    private CardInstance? Pick(DateRuntime rt)
    {
        return rt.Deck.Hand.Where(c => ctx.Cards.All[c.CardId].Playable && ctx.Cards.All[c.CardId].Cost <= rt.EnergyThisTurn)
            .OrderByDescending(c => c.CardId == "reckless_compliment" ? 100 : c.CardId == "small_talk" ? 90 : c.CardId == "homemade_gift" ? 80 : c.CardId == "compliment" ? 70 : c.CardId == "nervous_laugh" ? 20 : 0)
            .FirstOrDefault(c => c.CardId != "change_the_subject");
    }
    private void PlayMove()
    {
        if (move >= plan.Count) return;
        var date = (DateScreen)Scene;
        var rt = (DateRuntime)Field(date, "_rt");
        string id = plan[move++];
        if (id == "end_turn") Invoke(date, "OnEndTurn");
        else
        {
            int index = rt.Deck.Hand.ToList().FindIndex(c => c.CardId == id);
            if (index < 0) throw new Exception($"Planned card {id} missing.");
            ((Button)((HBoxContainer)Field(date, "_handRow")).GetChild(index)).EmitSignal(BaseButton.SignalName.Pressed);
        }
        audit.Add(new { frame, action = id, affection = rt.Affection, energy = rt.EnergyThisTurn, turn = rt.TurnNumber, awkwardness = rt.Dangers["Awkwardness"], outcome = rt.Outcome.ToString() });
        Log(id);
    }
    private void FocusMove()
    {
        if (move >= plan.Count) return;
        var date = (DateScreen)Scene;
        if (plan[move] == "end_turn") ((Button)Field(date, "_endTurnButton")).GrabFocus();
        else
        {
            var rt = (DateRuntime)Field(date, "_rt");
            int index = rt.Deck.Hand.ToList().FindIndex(c => c.CardId == plan[move]);
            ((Button)((HBoxContainer)Field(date, "_handRow")).GetChild(index)).GrabFocus();
        }
    }
    public override void _Process(double delta)
    {
        frame++;
        try
        {
            if (frame is 182 or 572 or 1010 or 1310 or 1385 or 1450 or 1620 or 1750)
                GetViewport().GetTexture().GetImage().SavePng(System.IO.Path.Combine(System.IO.Path.GetDirectoryName(System.Environment.GetEnvironmentVariable("ROT_TRAILER_AUDIT"))!, $"frame-{frame}.png"));
            switch (frame)
            {
                case 30:
                    foreach (var b in Walk(Scene).OfType<Button>().Where(b => b.Text.StartsWith("[debug]"))) b.Hide();
                    break;
                case 90: Invoke(Farm, "OpenPlantDialog", 0); Log("choose crop"); break;
                case 150: Press("Blood Turnip"); Log("plant blood turnip"); break;
                case 240: Invoke(Farm, "DebugAdvanceCrops", 480.0); Log("forward growth by 8 minutes"); break;
                case 330: Invoke(Farm, "OpenHarvestDialog", 0); Log("harvest"); break;
                case 360: Line(); break;
                case 480: Press("Save the heart"); Log("harvest adds reckless compliment"); break;
                case 540: Invoke(Farm, "OpenDeckScreen"); Log("inspect deck"); break;
                case 630: Invoke(Farm, "CloseActiveDialog"); break;
                case 660: Invoke(Farm, "OpenDatePicker"); break;
                case 720: Press("Cemetery Picnic"); Log("start cemetery picnic"); break;
                case 729: Line(); break;
                case 738: Line(); break;
                case 747: Line(); break;
                case 855: Press("beautiful in a concerning way"); Log("compliment picnic blanket"); break;
                case 864: Line(); break;
                case 873: Line(); break;
                case 960: Line(); Log("begin native card encounter"); break;
                case 975: case 1050: case 1125: case 1200: case 1275: case 1350: FocusMove(); break;
                case 1005: case 1080: case 1155: case 1230: case 1305: case 1380: PlayMove(); break;
                case 1410: case 1419: case 1428: Line(); break;
                case 1590: Line(); Log("resolve date dialogue"); break;
                case 1710: Press("Continue"); Log("return to garden"); break;
                case 1795:
                    if (!ctx.Farm.WonDateIds.Contains("cemetery_picnic")) throw new Exception("Native date did not win.");
                    Log("verified native bond and date win");
                    System.IO.File.WriteAllText(System.Environment.GetEnvironmentVariable("ROT_TRAILER_AUDIT")!, JsonSerializer.Serialize(audit, new JsonSerializerOptions { WriteIndented = true }));
                    break;
                case 1800: GetTree().Quit(); break;
            }
            // Reveal accumulated dialogue immediately in the capture, then hold it.
            // Text and choices remain the game's original content and handlers.
            if (Walk(Scene).OfType<DialogueOverlay>().FirstOrDefault(n => !n.IsQueuedForDeletion()) is { } overlay)
                Invoke(overlay, "SkipReveal");
        }
        catch (Exception ex) { GD.PrintErr($"[TRAILER FAILED] frame {frame}: {ex}"); GetTree().Quit(1); }
    }
}
