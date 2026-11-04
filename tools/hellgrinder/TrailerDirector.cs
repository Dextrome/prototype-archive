using Godot;
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text.Json;
using System.IO;
using Hellgrinder.Prototype;
using Hellgrinder.Prototype.MidShift;
using Hellgrinder.Prototype.Contracts;
using Hellgrinder.Tests.Simulation;
public partial class TrailerDirector:Node
{
    readonly ISimulationStrategy strategy=new Strategies.Balanced();
    readonly List<object> trace=new();
    HellgrinderPrototypeController? game;
    TrailerPointer pointer=null!;
    int frame,age,midAge; string phase="",mid="",incident=""; bool seeded;
    string output=>System.Environment.GetEnvironmentVariable("HELL_TRAILER_OUT")!;
    public override void _Ready()
    {
        var layer=new CanvasLayer{Layer=100};AddChild(layer);pointer=new TrailerPointer();layer.AddChild(pointer);
    }
    object State()
    {
        if(game==null)return new{phase="Menu"};var s=game.TrailerState;
        return new{phase=s.Phase.ToString(),shift=s.CurrentShift,time=s.ShiftTimeRemaining,output=s.OutputGenerated,coin=s.Bloodcoin,debt=s.ContractDebt,heat=s.Hellfire,pressure=s.SoulPressure,sludge=s.SinSludge,purity=s.Purity,wear=s.Wear,contract=s.ActiveContract?.Id,directive=s.ActiveDirective.ToString(),incident=s.ActiveIncident.ToString(),mid=s.ActiveMidShiftEvent?.Id,result=s.RunResult.ToString(),shiftResult=s.LastShiftResult.ToString(),reasons=s.LastShiftReasons.ToArray(),installed=s.InstalledChoices.ToArray()};
    }
    void Log(string evt,string detail="") {trace.Add(new{frame,eventType=evt,detail,state=State()});if(evt!="tick")GD.Print($"[TRAILER] frame={frame} {evt} {detail} {JsonSerializer.Serialize(State())}");}
    void Press(Button button,string detail)
    {
        if(!button.IsVisibleInTree()||button.Disabled)throw new Exception($"Unavailable button {detail}: {button.Name}");
        pointer.Tap(button.GetGlobalRect().GetCenter());button.EmitSignal(BaseButton.SignalName.Pressed);Log("action",detail);
    }
    void Action(string kind,int id=0,string? detail=null)=>Press(game!.TrailerTarget(kind,id),detail??kind);
    public override void _Process(double delta)
    {
        frame++;pointer.Advance((float)delta);
        if(GetTree().CurrentScene is not HellgrinderPrototypeController controller)
        {
            if(frame==1)Log("menu");
            if(frame==90)
            {
                var button=GetTree().CurrentScene.FindChildren("*","Button",true,false).OfType<Button>().First(b=>b.Text.Contains("STANDARD",StringComparison.OrdinalIgnoreCase));
                Press(button,"Start standard run");
            }
            return;
        }
        game=controller;
        if(!seeded){game.TrailerSeed(7);seeded=true;Log("seed","Native standard run, seed 7; no state grants.");}
        var s=game.TrailerState;
        var key=s.Phase+":"+s.CurrentShift;
        if(key!=phase){phase=key;age=0;Log("phase",key);}
        age++;
        if(frame%30==0)Log("tick");
        if(incident!=s.ActiveIncident.ToString()){incident=s.ActiveIncident.ToString();Log("incident",incident);}
        switch(s.Phase)
        {
            case PrototypePhase.MachineSetup:
                var machine=strategy.ChooseStarterMachine(s);
                if(age==30)Action("module",(int)machine.Input,"Choose "+machine.Input);
                if(age==90)Action("module",(int)machine.Grinder,"Choose "+machine.Grinder);
                if(age==150)Action("module",(int)machine.Output,"Choose "+machine.Output);
                if(age==210)Action("module",(int)machine.Support,"Choose "+machine.Support);
                if(age==270)Action("procure",detail:"Confirm 120 BC procurement; 40 BC retained");
                break;
            case PrototypePhase.ContractSelect:
            case PrototypePhase.Preparation:
            case PrototypePhase.DirectiveSelect:
                if(age>=30 && age%25==5 && strategy.ShouldRepayDebt(s))Action("debt",detail:"Pay 50 BC toward debt");
                if(s.Phase==PrototypePhase.DirectiveSelect && age==60)Action("directive",(int)strategy.ChooseDirective(s),"Choose "+strategy.ChooseDirective(s));
                if(age>=120 && !strategy.ShouldRepayDebt(s))
                {
                    if(s.Phase==PrototypePhase.ContractSelect){var id=strategy.ChooseContract(s.OfferedContracts,s);Action("contract",s.OfferedContracts.FindIndex(c=>c.Id==id),"Accept "+id);}
                    else if(s.Phase==PrototypePhase.Preparation){var id=strategy.ChoosePreparation(s.OfferedPreparationChoices,s);Action("prep",s.OfferedPreparationChoices.FindIndex(c=>c.Id==id),"Prepare "+id);}
                    else Action("authorize",detail:"Authorize shift");
                }
                break;
            case PrototypePhase.Shift:
                if(s.ActiveMidShiftEvent!=null)
                {
                    if(mid!=s.ActiveMidShiftEvent.Id){mid=s.ActiveMidShiftEvent.Id;midAge=0;Log("mid-event",mid);}
                    midAge++;
                    if(midAge==90)
                    {
                        var e=s.ActiveMidShiftEvent;int idx=strategy.ChooseMidShiftEventResponse(e,s);
                        Action(e.Resolution==MidShiftEventResolutionMode.PauseAndModal?"mid-modal":"mid-ticker",idx,"Resolve "+e.Id+" choice "+idx);
                    }
                    break;
                }
                mid="";
                // The existing Balanced policy, dispatched through the real UI buttons for native effects/audio.
                if(s.Hellfire>=70 && s.VentCooldownRemaining<=0)Action("vent");
                if(s.SoulPressure>=70 && s.ReleaseCooldownRemaining<=0)Action("release");
                if(s.SinSludge>=60 && s.PurgeCooldownRemaining<=0)Action("purge");
                // A curated player decision: meet the disposal contract's final-sludge cap.
                if(s.ActiveContract?.Type==PrototypeContractType.SludgeDisposalRequest && s.ShiftTimeRemaining<6 && s.SinSludge>=38 && s.PurgeCooldownRemaining<=0)
                    Action("purge",detail:"Purge before disposal inspection");
                if(s.Hellfire<45 && s.SoulPressure<55 && s.SinSludge<40 && s.OverclockCooldownRemaining<=0)Action("overclock");
                break;
            case PrototypePhase.Report:
                if(age==150)Action("continue",detail:"Continue past native shift report");
                break;
            case PrototypePhase.EventModal:
                if(age==120){var e=s.PendingEvents.Peek();Action("event",strategy.ChooseEventResponse(e,s),"Resolve "+e.Id);}
                break;
            case PrototypePhase.RunComplete:
                if(age==210){Log("finished");File.WriteAllText(Path.Combine(output,"trace.json"),JsonSerializer.Serialize(trace,new JsonSerializerOptions{WriteIndented=true}));GetTree().Quit();}
                break;
        }
        if(frame>18000)throw new Exception("Run exceeded recording frame limit.");
    }
}
public partial class TrailerPointer:Control
{
    Vector2 point=new(-100,-100);float pulse;
    public TrailerPointer(){MouseFilter=MouseFilterEnum.Ignore;SetAnchorsAndOffsetsPreset(LayoutPreset.FullRect);}
    public void Tap(Vector2 at){point=at;pulse=1;QueueRedraw();}
    public void Advance(float dt){pulse=Mathf.Max(0,pulse-dt*1.7f);QueueRedraw();}
    public override void _Draw()
    {
        if(pulse<=0)return;
        var c=new Color(1f,.79f,.33f,pulse);
        DrawArc(point,12+(1-pulse)*32,0,Mathf.Tau,48,c,3,true);
        DrawCircle(point,5,c);
    }
}
