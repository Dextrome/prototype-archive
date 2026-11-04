using Godot;
using System;
using Meldkin.Entities;
namespace Meldkin.Core;
public partial class GameController
{
    public bool TrailerReady => _buyBar != null && CurrentPhase == GamePhase.Draft;
    public void TrailerStage(int combo)
    {
        _runState.Currency = 60000; _runState.Lives = _runState.StartingLives = 500;
        _runState.WaveIndex = combo == 0 ? 21 : combo == 1 ? 30 : 38;
        string[] ids = combo == 0 ? new[]{"bloom","needleback","needleback","needleback"}
            : combo == 1 ? new[]{"bloom","mortarcap","mortarcap","needleback"}
            : new[]{"bloom","borer","borer","needleback","mortarcap"};
        int[][] paths = combo == 0 ? new[]{new[]{0,0,4},new[]{4,2,0},new[]{0,2,4},new[]{0,2,2}}
            : combo == 1 ? new[]{new[]{0,0,4},new[]{4,2,0},new[]{0,4,2},new[]{0,2,4}}
            : new[]{new[]{0,0,4},new[]{4,2,0},new[]{0,2,4},new[]{4,2,0},new[]{2,4,0}};
        Vector2 anchor=Vector2.Zero;
        for(int i=0;i<ids.Length;i++)
        {
            Vector2? p=null;
            if(i==0)
            {
                float nearest=float.MaxValue;
                for(int x=260;x<=900;x+=20) for(int y=200;y<=560;y+=20)
                {
                    var q=new Vector2(x,y);
                    float score=q.DistanceSquaredTo(new Vector2(600,400));
                    if(score<nearest && ResolvePlacement(q,ids[i]).Outcome==PlacementOutcome.Place && MapBounds.DistanceToPath(q,GetCurrentPathPoints())<95)
                    {p=q;nearest=score;}
                }
            }
            else p=ChooseClusteredHarnessPoint(anchor,100+i,ids[i]);
            if(p==null) throw new Exception("No legal place for "+ids[i]);
            var refusal=TryBuyOrganismAt(ids[i],p.Value);
            if(refusal!=null) throw new Exception(refusal);
            if(i==0) anchor=p.Value;
            int slot=-1;
            for(int s=0;s<_runState.Slots.Length;s++) if(_runState.Slots[s].Tower is TowerInstance t && t.TowerId==ids[i] && _runState.Slots[s].PlacedPosition==p.Value) slot=s;
            for(int line=0;line<3;line++) for(int rung=0;rung<paths[i][line];rung++) OnInspectRung(slot,line,rung);
            GD.Print($"[TRAILER] placed slot={slot} id={ids[i]} at={p} paths={string.Join(',',paths[i])}");
        }
        CloseInspect(); RefreshBuyBar(); FixtureJumpToWavePhase();
        GD.Print($"[TRAILER] staged combo={combo} map={_runState.SelectedMapId} wave={_runState.WaveIndex+1} vfx={!SkipsPlayerVfx}");
    }
    public void TrailerPanel(int slot,bool full)
    {
        if(_runState.Slots[slot].Tower is TowerInstance t) OpenInspect(t,slot);
        if(full) OpenUpgradePopup(slot);
        GD.Print($"[TRAILER] panel slot={slot} full={full}");
    }
    public void TrailerBuy(int slot,int line,int rung) => OnInspectRung(slot,line,rung);
    public void TrailerClose()=>CloseInspect();
    public void TrailerReport()=>GD.Print($"[TRAILER] result wave={_runState.WaveIndex+1} kills={_runState.TotalKills} stripped={_runState.TotalDamageDealt} alive={_runState.EnemiesAlive.Count} gold={_runState.Currency}");
}
