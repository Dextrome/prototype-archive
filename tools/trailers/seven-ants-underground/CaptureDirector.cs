using System;
using System.IO;
using System.Linq;
using Godot;
using OreilChaos.Autoloads;
using OreilChaos.Game;
using OreilChaos.Game.Modes;
using OreilChaos.Entities;
using OreilChaos.Terrain;
public partial class CaptureDirector:Node
{
    GameSession s=null!; SessionManager m=null!; PlayerWorm a=null!,b=null!,c=null!,d=null!;
    string outputDir="E:/trailer-production/seven-ants";
    string shot="rope"; int frame=0,step=0,variant=0; double acc=0; Camera2D cam=null!;
    StreamWriter log=null!;
    public override void _Ready()
    {
        System.Globalization.CultureInfo.CurrentCulture=System.Globalization.CultureInfo.InvariantCulture;
        SettingsManager.LoadOrCreate();
        OreilChaos.Sim.LieroConst.UseLieroPhysics=true;
        foreach(var arg in OS.GetCmdlineUserArgs()) if(arg.StartsWith("out="))outputDir=arg[4..];
        foreach(var arg in OS.GetCmdlineUserArgs()) if(arg.StartsWith("shot=")) shot=arg[5..];
        foreach(var arg in OS.GetCmdlineUserArgs()) if(arg.StartsWith("variant="))variant=int.Parse(arg[8..]);
        Engine.PhysicsTicksPerSecond=70;
        GD.Seed(7717);
        var mode=shot=="breach"?MatchModeKind.ExperimentalColony:shot=="echo"?MatchModeKind.EchoToybox:shot=="panic"?MatchModeKind.PanicToybox:shot=="bounce"||shot=="clamp"?MatchModeKind.SumoToybox:MatchModeKind.ToyboxColony;
        SettingsManager.SelectedMatchMode=mode;
        GetNode<NetworkManager>("/root/NetworkManager").Host();
        s=GD.Load<PackedScene>("res://scenes/GameSession.tscn").Instantiate<GameSession>(); AddChild(s);
        m=SessionManager.Instance!; m.CaptureInit(s,mode);
        if(shot=="breach")s.Terrain.ConfigureForPreset(ArenaPreset.ToyboxArena);
        s.Terrain.LevelSeed=7717; s.Terrain.BuildDefaultMap();
        s.GetNode<CanvasLayer>("Hud").Hide();
        GetNode("/root/DebugOverlay").SetProcess(false);
        if(GetNode("/root/DebugOverlay") is CanvasLayer debugLayer) debugLayer.Hide();
        cam=s.GetNode<Camera2D>("MainCamera"); cam.PositionSmoothingEnabled=false;
        cam.LimitLeft=-10000;cam.LimitRight=10000;cam.LimitTop=-10000;cam.LimitBottom=10000;
        var cyan=new Color("66f2f5");var red=new Color("ff6655");var gold=new Color("ffd35e");
        WeaponKind[] kit={WeaponKind.BurrowRocket,WeaponKind.CrumbBombToy,WeaponKind.NinjaRopeTool};
        Vector2 pa=new(483,380),pb=new(917,380),pc=new(700,245);
        if(shot=="clamp") {pa=new(920,343);pb=new(957,343);pc=new(308,214);kit=new[]{WeaponKind.MandibleClamp,WeaponKind.BellyBounce,WeaponKind.PheromoneYank};}
        if(shot=="bounce") {pa=new(910,343);pb=new(940,343);pc=new(308,214);kit=new[]{WeaponKind.BellyBounce,WeaponKind.MandibleClamp,WeaponKind.PheromoneYank};}
        if(shot=="spring") {pa=new(655,200);pb=new(917,380);pc=new(483,380);kit=new[]{WeaponKind.SpringMine,WeaponKind.BurrowRocket,WeaponKind.NinjaRopeTool};}
        if(shot=="rocket") {pa=new(185,388);pb=new(483,380);pc=new(917,380);kit=new[]{WeaponKind.TunnelBore,WeaponKind.BurrowRocket,WeaponKind.NinjaRopeTool};}
        if(shot=="breach") {pa=new(510,350);pb=new(760,350);pc=new(917,380);kit=new[]{WeaponKind.Rocket,WeaponKind.Grenade,WeaponKind.NinjaRopeTool};}
        if(shot=="burrow") {pa=new(570,350);pb=new(710,320);pc=new(917,380);}
        if(shot=="chaos") {pa=new(483,376);pb=new(917,380);pc=new(700,200);}
        if(shot=="rope") {pa=new(483,376);pb=new(917,380);pc=new(700,535);}
        if(shot=="echo") {pa=new(350,344);pb=new(1030,344);pc=new(500,510);kit=new[]{WeaponKind.BurrowRocket,WeaponKind.CrumbBombToy,WeaponKind.SpringMine};}
        if(shot=="panic") {pa=new(685,245);pb=new(728,245);pc=new(700,390);kit=new[]{WeaponKind.CrumbBombToy,WeaponKind.MandibleClamp,WeaponKind.SpringMine};}
        if(shot=="breach") {
            for(int px=460;px<=800;px+=12)m.CaptureStamp(new Vector2(px,375),12,TerrainEditMode.PaintHard);
            m.CaptureStamp(new Vector2(660,330),55,TerrainEditMode.Paint);
        }
        if(shot=="burrow") {
            for(int px=530;px<=790;px+=15)m.CaptureStamp(new Vector2(px,375),12,TerrainEditMode.PaintHard);
            m.CaptureStamp(new Vector2(660,330),32,TerrainEditMode.Paint);
            for(int px=703;px<=775;px+=12)m.CaptureStamp(new Vector2(px,352),12,TerrainEditMode.PaintHard);
        }
        a=m.CaptureActor(1,pa,1,cyan,kit); b=m.CaptureActor(2,pb,0,red,kit); c=m.CaptureActor(3,pc,3,gold,kit);
        if(shot=="chaos") {
            b=m.CaptureActor(2,pb,0,red,WeaponKind.CrumbBombToy,WeaponKind.NinjaRopeTool,WeaponKind.PheromoneYank);
            c=m.CaptureActor(3,pc,3,gold,WeaponKind.SpringMine,WeaponKind.CeilingClod,WeaponKind.NinjaRopeTool);
            d=m.CaptureActor(4,new Vector2(700,535),4,new Color("ea75ff"),WeaponKind.DirtSpike,WeaponKind.BellyBounce,WeaponKind.NinjaRopeTool);
        }
        m.CaptureStart();
        if(shot=="panic")m.CaptureClock(630);
        log=new StreamWriter($"{outputDir}/{shot}{(variant==0?"":variant.ToString())}-events.csv");
        log.WriteLine("time,id,x,y,vx,vy,alive,rope,attached,projectiles,edits");
        ProcessPriority=100;
    }
    InputCmd Cmd(int t,float move=0,float aim=0,bool fire=false,int slot=0,bool jump=false,bool rope=false,float retract=0,bool dig=false)
        =>new(){Version=NetProtocol.SimVersion,Sequence=t,MoveX=move,AimAngle=aim,Fire=fire,WeaponSlot=slot,WeaponSelectSlot=slot,Jump=jump,RopeJustPressed=rope,RopeLengthInput=retract,DigPressed=dig,DigDirX=move};
    void Inputs(int t)
    {
        var x=Cmd(t);var y=Cmd(t,aim:Mathf.Pi);var z=Cmd(t,aim:Mathf.Pi);
        if(shot=="breach") {x=Cmd(t,aim:0,fire:t==45||t==195||t==345);y=Cmd(t);z=Cmd(t);}
        if(shot=="burrow") { x=Cmd(t,aim:-0.25f,fire:t==60); y=Cmd(t);z=Cmd(t); }
        if(shot=="clamp") { x=Cmd(t,aim:0.0f,fire:t==63); y=Cmd(t);z=Cmd(t); }
        if(shot=="bounce") { x=Cmd(t,fire:t==63);y=Cmd(t);z=Cmd(t); }
        if(shot=="rocket") {x=Cmd(t,move:t>35&&t<85?1:0,aim:0,fire:t==35||t==85||t==135||t==185||t==250,slot:t<240?0:1,dig:t%14==0);y=Cmd(t);}
        if(shot=="spring") {x=Cmd(t,move:t>50&&t<185?1:0,aim:t<80?Mathf.Pi/2:(b.GlobalPosition-a.GlobalPosition).Angle(),fire:t==10||t==240,slot:t<80?0:1);y=Cmd(t);}
        if(shot=="rope")
        {
            int release=150;
            float aim=t<release?(-0.35f-variant*0.1f):(new Vector2(700,100)-a.GlobalPosition).Angle();
            bool attack=t==(variant==2?120:260);
            if((variant==2&&t>=95&&t<=140)||(variant!=2&&t>=240&&t<=280))aim=(b.GlobalPosition-a.GlobalPosition).Angle();
            x=Cmd(t,move:t<release?1:-1,aim:aim,rope:t==25||t==release||t==release+15,retract:a.RopeAttached?-1:0,fire:attack,jump:t==15);
            y=Cmd(t);z=Cmd(t);
        }
        if(shot=="echo") {x=Cmd(t,move:t>90&&t<150?-1:0,aim:-0.3f,fire:t==50||t==110);y=Cmd(t,aim:Mathf.Pi+0.3f,fire:t==85||t==145);}
        if(shot=="panic") {x=Cmd(t,move:t<100?-1:1,aim:-0.5f,fire:t>40&&t<110,jump:t==120||t==210,slot:0);y=Cmd(t,move:t<120?1:-1,aim:Mathf.Pi+0.5f,fire:t>90&&t<160,jump:t==120||t==210);z=Cmd(t,move:t<80?1:-1,jump:t==20||t==100,fire:t==80,slot:2,aim:Mathf.Pi/2);}
        if(shot=="chaos") {
            float aa=t<100?-0.55f:(b.GlobalPosition-a.GlobalPosition).Angle();
            x=Cmd(t,move:t<150?1:-1,aim:aa,rope:t==25||t==150||t==170,retract:a.RopeAttached?-1:0,fire:t==120,jump:t==15);
            y=Cmd(t,move:t>130?-1:0,aim:-2.5f,fire:t>30&&t<95,jump:t==130);
            z=Cmd(t,move:t>45?-1:0,aim:t<100?Mathf.Pi/2:-Mathf.Pi/2,fire:t==10||t==150,slot:t<100?0:1);
            m.CaptureInput(4,Cmd(t,aim:(a.GlobalPosition-d.GlobalPosition).Angle(),fire:t==90||t==160||t==230,jump:t==30));
        }
        m.CaptureInput(1,x);m.CaptureInput(2,y);m.CaptureInput(3,z);
    }
    public override void _Process(double delta)
    {
        if(frame++==0)return;
        acc+=delta;
        while(acc>=1.0/70){acc-=1.0/70;Inputs(++step);m.CaptureStep();}
        if(frame%6==0)foreach(var p in s.Players.Values)log.WriteLine($"{step/70f:F3},{p.PeerId},{p.GlobalPosition.X:F1},{p.GlobalPosition.Y:F1},{p.Velocity.X:F1},{p.Velocity.Y:F1},{p.Alive},{p.RopeOut},{p.RopeAttached},{s.Projectiles.Count},{m.TerrainEditCount}");
        Vector2 center=new(700,360);float zoom=1.55f;
        if(shot=="clamp"||shot=="bounce"){center=new(1040,420);zoom=1.7f;}
        if(shot=="breach"){center=new(650,380);zoom=2.6f;}
        if(shot=="burrow"){center=new(670,340);zoom=2.8f;}
        if(shot=="rocket"){center=new(440,380);zoom=2.25f;}
        if(shot=="spring"){center=new(800,330);zoom=1.8f;}
        if(shot=="rope"){center=new(700,330);zoom=1.55f;}
        if(shot=="chaos"){center=new(700,360);zoom=1.45f;}
        if(shot=="echo"){center=new(520,430);zoom=2.0f;}
        if(shot=="panic"){center=new(700,420);zoom=1.65f;}
        cam.Zoom=new Vector2(zoom,zoom);cam.Position=center;
        double duration=shot=="chaos"?7:shot=="rope"?12:shot=="echo"?8:shot=="panic"?9:6;
        if(frame>=duration*60){log.Dispose();GD.Print($"CAPTURE COMPLETE {shot}");GetTree().Quit();}
    }
}


