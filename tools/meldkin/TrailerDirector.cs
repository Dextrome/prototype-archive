using Godot;
using Meldkin.Core;
using Meldkin.UI;
using System;
using System.Reflection;
public partial class TrailerDirector:Node
{
    GameController? game; GrowthPanel? growth;
    int frame=-1; int combo; bool shop;
    public override void _Ready()
    {
        combo=int.Parse(System.Environment.GetEnvironmentVariable("TRAILER_COMBO")??"0");
        shop=combo==3;
        if(shop) {growth=GD.Load<PackedScene>("res://Scenes/Growth.tscn").Instantiate<GrowthPanel>();AddChild(growth);frame=0;return;}
        MapSelectPanel.SetPendingMapSelection(combo==1?"geode_v2":"interchange_v4");
        var root=GD.Load<PackedScene>("res://Scenes/Main.tscn").Instantiate(); AddChild(root);
        game=root.GetNode<GameController>("GameController");
    }
    void Invoke(string method,params object[] args)=>typeof(GrowthPanel).GetMethod(method,BindingFlags.Instance|BindingFlags.NonPublic)!.Invoke(growth,args);
    public override void _Process(double delta)
    {
        if(frame<0)
        {
            if(game?.TrailerReady!=true)return;
            game.TrailerStage(combo);frame=0;GD.Print($"[TRAILER] START movie_frame={Engine.GetProcessFrames()}");
        }
        frame++;
        if(shop)
        {
            if(frame==90){Invoke("ShowBranch","trunk",false);Invoke("Select","trunk_seed_1",false);}
            if(frame==210)Invoke("OnBuyPressed");
            if(frame==300){Invoke("ShowBranch","mortarcap",false);Invoke("Select","mc_grow",false);}
            if(frame==420)Invoke("OnBuyPressed");
            if(frame==510){Invoke("Select","mc_quick",false);}
            if(frame==630)Invoke("OnBuyPressed");
            if(frame==750)GetTree().Quit();
            return;
        }
        if(combo==0)
        {
            if(frame==240)game!.TrailerPanel(3,false);
            if(frame==450)game!.TrailerPanel(3,true);
            if(frame==570)game!.TrailerBuy(3,2,2);
            if(frame==660)game!.TrailerBuy(3,2,3);
            if(frame==780)game!.TrailerClose();
        }
        if(frame%150==0)game!.TrailerReport();
        if(frame==1200)GetTree().Quit();
    }
}
