"use strict";

window.COMMERCIAL_VIABILITY = {
  reviewed: "5 November 2026",
  factors: [
    ["Paying demand", 20],
    ["Differentiation", 20],
    ["Discovery", 10],
    ["Access", 10],
    ["Play value", 10],
    ["Price fit", 10],
    ["Production scope", 15],
    ["Operations", 5]
  ],
  projects: {
    "hellgrinder": {
      grades: [3,5,4,3,4,3,4,5],
      deduction: 0,
      summary: "The contract is the hook. Choosing a risky clause should change how you run the same machine.",
      reasons: [
        "Retail Hell shows an audience for supernatural shift work. COALCOM and Nucleares show interest in operating machinery, with different audiences and expectations.",
        "Choosing a clause, adapting the station, and balancing debt against failure gives the player a distinct decision.",
        "An optional bonus followed by an escalating machine failure can explain the premise in a short clip.",
        "The first shift must teach which gauges matter and how a player can respond before a failure cascades.",
        "Two contracts can make the same workstation replayable if each rewards a different strategy.",
        "€9.99 fits a compact five-shift game. €12.99 depends on the contracts feeling meaningfully different.",
        "One workstation and reusable incidents keep the modeled lean release to about €31,500.",
        "A solo run can be played without matchmaking or an active player population."
      ],
      sources: [["Retail Hell","4174310"], ["COALCOM: Power Station","4411610"], ["Nucleares","1428420"]]
    },
    "murderbox": {
      grades: [4,3,5,3,4,3.5,4,5],
      deduction: 0,
      summary: "A single tile can change the behavior of an entire machine. That engineering decision has to earn the price.",
      reasons: [
        "Rogue Voltage and inventory build games show an audience for tinkering with systems and discovering synergies.",
        "Order Automatica already sells small-grid positioning and automatic fights. Murderbox combines a shared power budget, heat and adjacency inside one machine.",
        "Move one part and show why the same machine survives a fight it previously lost.",
        "Power, heat and adjacency need readable feedback so a loss teaches the player what to change.",
        "Several successful build families give players a reason to retry if encounters favor different layouts.",
        "The €14.99 offer sits near the deeper Rogue Voltage and well above Order Automatica. Its engineering needs to be evident before purchase.",
        "One chassis and reusable modules keep scope focused, but balancing their interactions still matters. The lean model is about €43,000.",
        "The single-player format avoids multiplayer scheduling and server support."
      ],
      sources: [["Rogue Voltage","1494560"], ["Order Automatica","2105840"]]
    },
    "tiny-convoy": {
      grades: [3,5,4,4,3,3,2,5],
      deduction: 0,
      summary: "The best reason to tow a trailer is also what makes abandoning it hurt.",
      reasons: [
        "Truckful and Jalopy support interest in physics and cargo. Keep Driving serves the road-trip audience. The overlap between those buyers is uncertain.",
        "A growing chain changes handling, and abandoning a useful trailer can change which route is available next.",
        "A near-crash clip is readable, but it should show why the trailer was worth towing before the player cuts it loose.",
        "The tradeoff is easy to explain. Camera, recovery, and steering must keep losses understandable.",
        "Losing fuel or recovery gear can give the same route a different consequence on the next run.",
        "€12.99 depends on a short trip feeling complete and cargo choices mattering beyond one dramatic moment.",
        "Stable towing, detachment, recovery, and route testing put the lean model near €45,000.",
        "A solo trip avoids dependence on a live service."
      ],
      sources: [["Truckful","3090810"], ["Jalopy","446020"], ["Keep Driving","2756920"]]
    },
    "tower-with-legs": {
      grades: [4,3,5,3,3,4,2,5],
      deduction: 0,
      summary: "Facing matters when turning one weapon toward a wave exposes another side.",
      reasons: [
        "Wanderburg demonstrates demand for mobile fortresses. Towerful Defense reported passing 10,000 Steam units.",
        "Broadside weapons, manual turret control and heat exist elsewhere. The distinction is orienting a walking fortress to protect an objective.",
        "The walking silhouette and a visible turn or stomp make the action clear in seconds.",
        "Players need responsive movement, clear firing arcs, and useful warnings about threats outside their current view.",
        "Replay depends on two loadouts changing how you defend the same position, rather than waves only adding more enemies.",
        "The proposed €14.99 matches Wanderburg's observed list price. The active defense package must stand on its own.",
        "Handling, impact feedback and enemy approaches make this the most expensive lean package in the shortlist, at about €55,000.",
        "The solo format keeps ongoing support focused on the game itself."
      ],
      sources: [["Wanderburg","3624140"], ["Towerful Defense","2453610"]]
    },
    "rot-garden-romance": {
      grades: [4,4,4,3,3,2.5,2,5],
      deduction: 0,
      summary: "A crop earns its place when the card it produces changes a date you care about.",
      reasons: [
        "Potionomics and The Piper of Dawn show a paying audience for management systems and relationships.",
        "The Piper of Dawn already combines occult farming and romance. Rot's edge is using what you grow to change a specific date through cards.",
        "A character invitation and the consequence of bringing one unusual card convey the hook more clearly than a farm montage.",
        "The garden, deck, and relationship systems need to teach each other without delaying the first meaningful date.",
        "Three short routes can support a satisfying finish if dates diverge early enough to reward another playthrough.",
        "€17.99 is about a third above The Piper of Dawn's observed €13.49. The compact romance routes need to earn that premium.",
        "Writing, route integration, character art and localization put the lean model around €51,500.",
        "The game is solo, with support centered on saves, route issues and text."
      ],
      sources: [["The Piper of Dawn","3804370"], ["Potionomics","1874490"]]
    },
    "meldkin": {
      grades: [3,3,3,3,3,3,3,5],
      deduction: 0,
      summary: "The sequence inside an enemy should change where and how you grow your defenses.",
      reasons: [
        "Bloons TD 6 and Gnomes show interest in tower defense with layered threats and build choices.",
        "Layered enemies already exist. An ordered body queue is distinct when swapping two bodies calls for a different counter.",
        "The organic look is easy to show. The tactical hook needs a clip that makes the next body and its consequence visible.",
        "Previewing what emerges next helps players connect a defense choice to the result.",
        "A focused set of enemy orders can reward different layouts if one tower build cannot handle them all.",
        "A compact campaign and challenges make €9.99 plausible if the sequence mechanic adds enough variety.",
        "Reusable organisms and a few encounter families contain scope, with balance and feedback the main costs.",
        "A solo defense game can run without matchmaking or live events."
      ],
      sources: [["Bloons TD 6","960090"], ["Gnomes","3133060"]]
    },
    "ant-delve": {
      grades: [2,3,3,2,4,3,2,3],
      deduction: 0,
      summary: "The key turn is when a rival changes the route a loaded ant needs to get home.",
      reasons: [
        "Digital board games have a paying audience, but Root’s established audience does not establish demand for a new ant strategy game.",
        "March of the Ants already combines rival nests, resources, hex exploration and tunnel control. Ant Delve centers the trip home through an underground network.",
        "One contested haul explains the stakes better than a full board of competing colonies.",
        "Players must learn routes, resource return and interference. A focused first scenario would help.",
        "Shared routes and rival moves can create different plans even when the same map is used.",
        "€9.99 is plausible for a complete digital board game with enough depth to replay.",
        "Teaching the rules and delivering AI or reliable group play add meaningful cost.",
        "The support burden depends on whether the release is built around solo AI, local groups or remote play."
      ],
      sources: [["Root","965580"], ["Armello","290340"]]
    },
    "shpinky-dinky": {
      grades: [2,3,3,3,2,2,3,1],
      deduction: 0,
      summary: "A placed trap is worth building around if the other player can read it and respond.",
      reasons: [
        "ROUNDS shows an audience for short duels. Ricochet Rodeo is a smaller reference for bouncing shots.",
        "Placed pads, vents and goo can give opponents something to react to before a redirected shot lands.",
        "A setup and its counter make a better clip than an unexplained ricochet.",
        "Two players must quickly understand what each placed tool does and where the safe routes are.",
        "The same pair must want repeated matches after learning each tool. A single surprising combo cannot carry the release.",
        "At €5.99 the package competes for a pair’s time against established duel games.",
        "A small set of arenas and tools limits content work, but physics and private matches still need polish.",
        "The game only delivers its core experience when two players can get a match started."
      ],
      sources: [["ROUNDS","1557740"], ["Ricochet Rodeo","2167380"]]
    },
    "dungeon-janitor": {
      grades: [2,2,4,4,3,2,4,5],
      deduction: -12,
      summary: "The top-down view has value when cleaning the dungeon becomes a routing puzzle.",
      reasons: [
        "Goblin Cleanup shows interest in dungeon cleaning. Wilmot’s Warehouse offers a separate audience for short logistics puzzles.",
        "Goblin Cleanup already offers solo dungeon jobs, and Serial Cleaner already combines top-down cleaning and routing under threat.",
        "A whole room, a wheelbarrow and a waking hero can show the problem and its consequence immediately.",
        "An overhead view and short retries can make the order of operations easy to learn.",
        "Rooms can reward different solutions if a trap or waking hero changes which route makes sense.",
        "A €7.99 room pack needs to feel like a complete puzzle game rather than a smaller cleaning sim.",
        "Focused 2D rooms are cheaper to produce than a full 3D cleaning career.",
        "The solo structure avoids reliance on matchmaking."
      ],
      sources: [["Goblin Cleanup","2748340"], ["Serial Cleaner","522210"], ["Wilmot’s Warehouse","839870"]],
      competition: "Substantial overlap: the dungeon-cleaning job is already available. The deduction reflects how much the top-down room puzzle would need to change the purchase."
    },
    "goblin-ballistics": {
      grades: [3,2,4,4,3,2,3,5],
      deduction: -20,
      summary: "The goblin needs a shot decision that existing combat pinball does not already offer.",
      reasons: [
        "Rollers of the Realm, Xenotilt and Runix show a paid audience for variations on action pinball.",
        "Rollers already makes fantasy characters the balls, with combat and replayable arena boards.",
        "Launching the goblin into a target explains the physical hook quickly.",
        "Flippers and nudges are familiar; hazards and control need to stay readable at speed.",
        "Replay could come from deliberately mastering cursed shots and alternative score routes.",
        "€7.99 is below Rollers’ observed price, but that game already offers many levels and arena boards.",
        "A compact table set can limit scope. Precision physics, feedback and table tuning still take work.",
        "A solo score-chase is playable without an active online player base."
      ],
      sources: [["Rollers of the Realm","262470"], ["Xenotilt","2008980"], ["Runix","3617290"]],
      competition: "Direct substitute: Rollers already sells fantasy character-ball combat and arena replay."
    },
    "mazacre-td": {
      grades: [2,3,2,1,4,1.5,3,5],
      deduction: -12,
      summary: "Revival makes killing the same creep twice part of the economy. That depth serves a narrow audience.",
      reasons: [
        "Gem Miner reviews show some veterans pay for faithful maze TD. The most relevant releases point to a small specialist audience.",
        "Revived creeps and repeated-kill income distinguish the route plan from ordinary checkpoint mazing.",
        "An intricate maze is easy to show. Why a second kill makes it better needs explanation.",
        "Ordered checkpoints, revival, and the economy must be learned together, giving it the steepest learning curve in the portfolio.",
        "Specialists could find many viable routes if revival and income reward different placements.",
        "At €8.99 it faces free AMazing TD and the low-priced Maze TD Battleground, which already offers ordered checkpoints and repeated crossings.",
        "Authored seeds and clear tutorials limit content work, but route logic and balance require care.",
        "A solo campaign and local seeds avoid the need for online opponents."
      ],
      sources: [["AMazing TD","1140030"], ["Maze TD Battleground","2873270"], ["Gem Miner TD","2835780"]],
      competition: "Substantial overlap: free and low-priced checkpoint maze games already satisfy much of the specialist purchase."
    },
    "gurk": {
      grades: [4,1,4,4,3,2,2,5],
      deduction: -20,
      summary: "A solo career needs job choices and tools that change how you clean the next dungeon.",
      reasons: [
        "Goblin Cleanup and Crime Scene Cleaner show demand for tactile aftermath cleanup.",
        "Goblin Cleanup already sells cleaning dungeons alone or with friends, with tools and progression that affect jobs.",
        "A dungeon before and after cleanup communicates the fantasy at a glance.",
        "Clear tools and obvious mess make the opening approachable; hidden remnants can turn it into a chore.",
        "An authored career can sustain play if job choice and upgrades change the work instead of adding more of it.",
        "€15.99 is hard to justify beside an existing game that already serves the solo dungeon-cleaning fantasy.",
        "Tactile 3D tools, hazards and varied jobs are expensive to author and polish.",
        "The proposed solo release avoids multiplayer support."
      ],
      sources: [["Goblin Cleanup","2748340"], ["Crime Scene Cleaner","1040200"]],
      competition: "Direct substitute: Goblin Cleanup already offers dungeon cleanup, traps, and solo play."
    },
    "brick-by-brick": {
      grades: [3,1,4,5,2,2,3,5],
      deduction: -20,
      summary: "Finding the missing piece is satisfying, but it is already the central promise of several games.",
      reasons: [
        "Tidy Up the Small Town shows interest in paid brick sorting and reconstruction.",
        "Existing brick games already offer finding pieces, sorting a pile and finishing builds.",
        "The missing piece snapping into place is a clear visual payoff.",
        "Picking, sorting and placing bricks are immediately understandable when selection and visibility work well.",
        "Finishing a model is satisfying. The current pitch gives little reason for the next build to play differently.",
        "A low price still competes with games that already sell the same tactile activity.",
        "Snapping, part visibility and a catalog of recognizable builds need more work than the simple pitch suggests.",
        "A solo building game requires no ongoing multiplayer operation."
      ],
      sources: [["Brick by Brick: Tidy Up the Small Town","5228920"], ["A Little to the Left","1629520"]],
      competition: "Direct substitute: Tidy Up the Small Town and other brick games already sell the search-and-build payoff."
    },
    "squabblobs": {
      grades: [4,1,4,3,3,2,2,1],
      deduction: -20,
      summary: "A missing section of terrain needs to change the next tactical problem for the group.",
      reasons: [
        "Bopl Battle shows strong interest in friend-group physics fighters, with a wide gap to smaller alternatives.",
        "Bopl already offers drafted powers, improvisation and abilities that alter platforms or consume the stage.",
        "A surprising ability combo makes a clear clip, especially when the terrain visibly changes.",
        "Players can start with a small move set, but three-power combinations and physics need to stay readable.",
        "Terrain can change how a rematch plays if the group adapts to a specific missing route.",
        "A paid group game needs a mode players would choose over the established options they already own.",
        "Readable physics, networking and arena design put pressure on a small production budget.",
        "Repeat play depends on friend groups returning and being able to play together reliably."
      ],
      sources: [["Bopl Battle","1686940"], ["Oblin Party","2643290"]],
      competition: "Direct substitute: Bopl Battle already sells power combinations and improvisation in a physics arena."
    },
    "seven-ants-underground": {
      grades: [2,2,3,2,3,1,2,1],
      deduction: -12,
      summary: "One private match needs a terrain objective distinct enough for a group to organize around.",
      reasons: [
        "Liero-style communities show interest in the format, but free alternatives weaken evidence of paid demand.",
        "Classes and specific terrain objectives can differ; digging and real-time destructive combat are already available.",
        "Collapsing terrain makes a readable clip when the viewer also sees how it changed the objective.",
        "New players must understand movement, class kits and what digging lets them achieve.",
        "A focused match mode could reward groups for learning how to reshape the arena together.",
        "€6.99 is hard to earn when established groups already have free Liero-style choices.",
        "Synchronizing destruction and building a polished flagship mode require substantial engineering.",
        "The value of the release depends on reliable sessions and groups having opponents."
      ],
      sources: [["Worms Rumble","1186040"], ["Soldat 2","474220"]],
      competition: "Substantial overlap: free Liero-style games already serve much of the real-time digging and combat experience."
    }
  }
};
