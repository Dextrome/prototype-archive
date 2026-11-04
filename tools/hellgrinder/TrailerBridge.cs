using Godot;
using System;
using System.Linq;
using Hellgrinder.Prototype.StarterMachine;
using Hellgrinder.Prototype.Visuals;
using Hellgrinder.Prototype.Directives;
namespace Hellgrinder.Prototype;
public partial class HellgrinderPrototypeController
{
    public HellgrinderPrototypeState TrailerState=>_state;
    public void TrailerSeed(int seed){_runController=new PrototypeRunController(_state,seed);BeginRun();SyncUi();}
    static Button FindButton(Node n,string text)=>n.FindChildren("*","Button",true,false).OfType<Button>().First(b=>b.Text.Contains(text,StringComparison.OrdinalIgnoreCase));
    static Button Choice(Node n,int index)=>n.FindChildren("*","Button",true,false).OfType<Button>().Where(b=>b.IsVisibleInTree()).ElementAt(index);
    public Button TrailerTarget(string kind,int id=0)
    {
        return kind switch
        {
            "module"=>_machineSetupPanel.FindChildren("*","Button",true,false).OfType<HellgrinderStarterModuleCard>().First(b=>(int)b.ModuleId==id),
            "procure"=>FindButton(_machineSetupPanel,"CONFIRM"),
            "contract"=>_contractCards[id],
            "prep"=>_preparationCards[id],
            "directive"=>_directivePanel.FindChildren("*","Button",true,false).OfType<HellgrinderDirectiveCard>().First(b=>(int)b.Directive==id),
            "authorize"=>_directivePanel.GetNode<Button>("ConfirmButton"),
            "vent"=>_ventButton,"purge"=>_purgeButton,"release"=>_releaseButton,"overclock"=>_overclockButton,
            "debt"=>_payDebtButton,"continue"=>_continueButton,"wrap"=>_endButton,
            "event"=>Choice(_eventModal,id),
            "mid-modal"=>Choice(_midShiftModal,id),
            "mid-ticker"=>Choice(_midShiftTicker,id),
            _=>throw new Exception(kind)
        };
    }
}
