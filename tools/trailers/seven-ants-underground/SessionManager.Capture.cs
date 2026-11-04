using Godot;
using OreilChaos.Game;
using OreilChaos.Game.Modes;
using OreilChaos.Entities;
namespace OreilChaos.Autoloads;
public partial class SessionManager
{
    public void CaptureInit(GameSession s, MatchModeKind mode)
    {
        SetPhysicsProcess(false);
        _session=s;
        SetMatchMode(mode);
        _roundWaitingForLoadouts=false;
        _preMatchCountdownTicks=0;
        _bonusSpawnCooldownTicks=100000;
        _matchTicksRemaining=100000;
        _tick=0;
    }
    public PlayerWorm CaptureActor(long id, Vector2 pos, int cls, Color color, params WeaponKind[] kit)
    {
        _playerLoadouts[id]=kit;
        _playerClasses[id]=cls;
        var p=_session!.SpawnPlayer(id,pos,false);
        p.Respawn(pos); p.SetHealth(1); p.SetAntClass(cls); p.SetOutlineColor(color);
        p.SetPhysicsProcess(false); p.SetSpawnProtected(false);
        return p;
    }
    public void CaptureStart() { _gameMode.OnRoundStart(_session!.Players); }
    public void CaptureInput(long id, InputCmd cmd) { _latestInputs[id]=cmd; }
    public void CaptureStep() { StepHostSimulation(); }
    public void CaptureClock(int tick) { _tick=tick; }
    public void CaptureStamp(Vector2 p,float r,TerrainEditMode mode) {HostApplyTerrainEdit(p,r,mode,1);}
}
