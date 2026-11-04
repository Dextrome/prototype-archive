window.PROJECTS = [
  {
    "id": "gurk",
    "title": "Gurk",
    "category": "Simulation",
    "genre": "Dungeon cleaning",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "The heroes had their adventure. You have a mop.",
    "description": "Gurk (Goblin Janitor 3D) puts you in a goblin janitor’s boots after a dungeon raid. Scrub blood and slime, haul monsters to recycling and dispose of heroes before the next party arrives. Between shifts, return to your lair to spend your wages on better tools and useful gear.",
    "loop": [
      "Choose a dungeon job from the lair.",
      "Scrub, rinse, haul and recycle the mess.",
      "Lure waking heroes onto traps and finish before the next party.",
      "Clock out, collect wages and improve your equipment."
    ],
    "note": "First-person cleaning with career progression, job variants and a daily dungeon. Development footage; presentation may change.",
    "images": [
      {
        "src": "assets/gurk/01.jpg",
        "caption": "A torchlit dungeon waiting for its next cleaning shift."
      },
      {
        "src": "assets/gurk/02.jpg",
        "caption": "The real mop clears stains during a command-driven job."
      },
      {
        "src": "assets/gurk/03.jpg",
        "caption": "Explore the rooms and corridors from a janitor’s eye level."
      }
    ],
    "video": {
      "src": "assets/gurk/film-extended.mp4",
      "kind": "gameplay",
      "label": "Extended feature trailer",
      "duration": "1:56",
      "note": "Captured in the real Gurk renderer with staged starting states, scripted player inputs and edited timing. Shows existing game systems, not a continuous player run. Original score and edited game sound effects; no voiceover."
    }
  },
  {
    "id": "dungeon-janitor",
    "title": "Goblin Janitor",
    "category": "Simulation",
    "genre": "Top-down cleaning",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "A little goblin. A very unpleasant job.",
    "description": "Play Grub, the dungeon owner’s overworked cleaner. Mop the floor, move bodies, push a wheelbarrow of monsters to recycling and drag heroes to disposal. Some of those heroes are only pretending to be dead.",
    "loop": [
      "Take a seeded dungeon-cleaning job.",
      "Scrub the floor and rinse the overloaded mop.",
      "Sort bodies, reset traps and lure waking heroes onto the spikes.",
      "Clock out for wages and permanent tool upgrades."
    ],
    "note": "Standalone top-down game with five job ratings. The featured film is the factory’s authored V5 room study; screenshots show the standalone build.",
    "images": [
      {
        "src": "assets/dungeon-janitor/01.jpg",
        "caption": "A generated multi-room job with separate monster and hero disposal routes."
      },
      {
        "src": "assets/dungeon-janitor/02.jpg",
        "caption": "A waking survivor meets one of the dungeon’s traps."
      },
      {
        "src": "assets/dungeon-janitor/03.jpg",
        "caption": "Wheelbarrow transport through the dungeon’s connected spaces."
      }
    ],
    "video": {
      "src": "assets/dungeon-janitor/film-v5.mp4",
      "kind": "staged",
      "label": "V5 concept showcase",
      "duration": "59 SEC",
      "note": "Original DungeonJanitorV5 factory film, preserved intact. Shows trap reset, hero pursuit, trapping and disposal around 0:34–0:44, alongside cleaning, sorting and recycling. Scripted single-room showcase; silent."
    }
  },
  {
    "id": "meldkin",
    "title": "Meldkin",
    "category": "Strategy",
    "genre": "Organism tower defense",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Grow a defense. Peel the enemy apart.",
    "description": "Buy living defenses and grow them along authored upgrade paths. Enemies are ordered queues of bodies: remove the front layer and the next creature keeps moving. Placement and complementary capabilities matter as waves become denser.",
    "loop": [
      "Buy an organism and place it beside the lane.",
      "Choose branching upgrades for its role.",
      "Strip enemy layers and answer special defenses.",
      "Survive waves, earn permanent XP and buy upgrades for future runs."
    ],
    "note": "Two maps and four buyable organisms, each with three upgrade paths. Permanent XP upgrades carry into future runs. The showcase stages later-wave builds, funds and XP in an isolated copy; combat, tower purchases and upgrade rules are native.",
    "images": [
      {
        "src": "assets/meldkin/01-geode-build.jpg",
        "caption": "Bloom, Mortarcap and Needleback combine their capabilities on Geode."
      },
      {
        "src": "assets/meldkin/02-upgrade-paths.jpg",
        "caption": "The native Needleback upgrade sheet: SPIKE reaches Ravine while LANCE stops at rung two."
      },
      {
        "src": "assets/meldkin/03-permanent-upgrades.jpg",
        "caption": "The permanent Upgrades tree with Mortarcap unlocked and Quicken selected for purchase."
      }
    ],
    "video": {
      "src": "assets/meldkin/film-builds-and-progression.mp4",
      "kind": "gameplay",
      "label": "Builds & progression showcase",
      "duration": "1:07",
      "note": "Three tower combinations on Interchange and Geode, a live tower panel, Crater and Ravine path purchases, and the permanent shop buying Seed gold I, Mortarcap and Quicken. Native gameplay with staged later-wave setups, funds and XP; explanatory captions and native procedural sound."
    }
  },
  {
    "id": "murderbox",
    "title": "Murderbox",
    "category": "Strategy",
    "genre": "Machine building / auto-battler",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Sixteen squares. One terrible machine.",
    "description": "Draft parts onto a tiny 4×4 combat machine and let it fight for you. Weapons compete for energy, power makes heat, and adjacent modules alter the behavior of the build. A stronger machine can also be a more dangerous machine.",
    "loop": [
      "Draft a module, upgrade or mutation.",
      "Fit parts onto the 4×4 grid and exploit adjacency.",
      "Watch the machine fight while energy and heat interact.",
      "Survive the wave and reshape the build for the next threat."
    ],
    "note": "A draft loop, mutations, relics and multiple module types exist. The player builds rather than aiming or shooting directly. The showcase stages six builds and enemy waves in an isolated copy; the original project and its combat rules are unchanged.",
    "images": [
      {
        "src": "assets/murderbox/01-adjacency.jpg",
        "caption": "The native cannon tooltip shows 24.3 damage per salvo from two adjacent Splitters; editorial text explains the stacking bonus."
      },
      {
        "src": "assets/murderbox/02-defenses.jpg",
        "caption": "A Repair Drone heals adjacent armor while a Shield Emitter protects the lower row from Spitter shots."
      },
      {
        "src": "assets/murderbox/03-vent.jpg",
        "caption": "The heat-heavy build triggers a native emergency vent: a blast hits every enemy and temporarily disables a module."
      }
    ],
    "video": {
      "src": "assets/murderbox/film-modules.mp4",
      "kind": "gameplay",
      "label": "Modules & synergies showcase",
      "duration": "1:01",
      "note": "All three weapons and 14 module types: stacking adjacent Splitters, Focuser/Gearbox/Reactor bonuses, Echo Chamber repeat fire, armor repairs, shield blocks, Demon Reactor damage, vent blasts and cooling. Includes a native hover tooltip and editorial explanations. Staged builds and enemy waves; native combat rules, outcomes and sound effects."
    }
  },
  {
    "id": "mazacre-td",
    "title": "Mazacre TD",
    "category": "Strategy",
    "genre": "Mazing tower defense",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Build the route. Kill them again.",
    "description": "Towers and blockers shape a maze through ordered checkpoints. Creeps revive where they die and keep walking, turning route length and repeated kills into the heart of the economy. Research and tower specializations expand the options.",
    "loop": [
      "Shape a legal maze around checkpoints and terrain.",
      "Place and specialize towers along the route.",
      "Earn score and lives from repeated creep kills.",
      "Reinvest wave income in the maze, upgrades and research."
    ],
    "note": "Working title for the EntropyRemake project. The playable scope is solo, with six tutorials and local ranked seeds. The progression film uses the Pocket practice seed, native bot maze plans and curated purchases; the original project and game rules are unchanged.",
    "images": [
      {
        "src": "assets/mazacre-td/01-checkpoint-groups.jpg",
        "caption": "Editorial colors identify two checkpoint groups and the shared choke that the required route crosses four times."
      },
      {
        "src": "assets/mazacre-td/02-developed-maze.jpg",
        "caption": "Wave nine runs through the expanded maze with a specialized Piledriver, local upgrades, depots, blockers and all four research categories purchased."
      }
    ],
    "video": {
      "src": "assets/mazacre-td/film-progression.mp4",
      "kind": "gameplay",
      "label": "Run progression showcase",
      "duration": "1:17",
      "note": "A nine-wave solo run grows the maze from 37 to 190 route cells. Explains checkpoint groups and a shared choke, Piledriver specialization, local damage/speed upgrades, supply depots, blockers and all four research choices. Native UI purchases spend earned minerals. Bot-planned maze with curated upgrades; native 4× combat, short held planning shots and game sound effects."
    }
  },
  {
    "id": "tower-with-legs",
    "title": "Tower With Legs",
    "category": "Concept studies",
    "genre": "Walking defense / action",
    "players": "Solo concept",
    "stage": "Concept study",
    "pitch": "The tower is the build.",
    "description": "Instead of placing a field of defenses, pilot one walking tower. Position the machine, rotate useful weapons into the threat and bolt on new hardware between waves. More firepower means more decisions about heat and facing.",
    "loop": [
      "Walk and rotate the defensive machine.",
      "Bring the right weapon face toward the wave.",
      "Stomp close threats and manage heat.",
      "Install a visible upgrade and face the next attack."
    ],
    "note": "A staged concept demonstration with scripted combat and upgrade beats. The prototype tests the fantasy of being the tower.",
    "images": [
      {
        "src": "assets/tower-with-legs/01.jpg",
        "caption": "The walking tower after a visible weapon upgrade."
      },
      {
        "src": "assets/tower-with-legs/02.jpg",
        "caption": "A new pressure point in the walking-defense concept."
      },
      {
        "src": "assets/tower-with-legs/03.jpg",
        "caption": "A new pressure point in the walking-defense concept."
      }
    ],
    "video": {
      "src": "assets/tower-with-legs/film.mp4",
      "kind": "staged",
      "label": "Staged concept film",
      "duration": "29 SEC",
      "note": "Original GodotPrototypeFactory concept film. Interactions, outcomes and progression are staged to communicate the intended game."
    }
  },
  {
    "id": "squabblobs",
    "title": "Squabblobs",
    "category": "Action & physics",
    "genre": "Ability party fighter",
    "players": "Local / online multiplayer",
    "stage": "Playable prototype",
    "pitch": "Tiny ants. Extremely unreasonable abilities.",
    "description": "Draft a set of powers, then fight across destructible arenas as a flexible ant-blob. Movement, crawling, knockback and combinations of abilities turn short rounds into improvised physics problems. The last survivor takes the round.",
    "loop": [
      "Join a lobby and choose a match setup.",
      "Draft a three-ability loadout.",
      "Combine powers and terrain destruction to eliminate rivals.",
      "Score rounds, reach the match result and rematch."
    ],
    "note": "The project lives in the Bopl folder. Local play, online host/join, teams and sandbox are implemented. The film combines controlled weapon demonstrations with native four-player bot matches; it does not test network play.",
    "images": [
      {
        "src": "assets/squabblobs/01-four-player.jpg",
        "caption": "Four native CPU players exchange attacks in Snowy Arena; this free-for-all runs through ordinary bot inputs and game rules."
      },
      {
        "src": "assets/squabblobs/02-weapons.jpg",
        "caption": "The guided missile splits into three warheads in the faster nine-power montage."
      }
    ],
    "video": {
      "src": "assets/squabblobs/film-four-player.mp4",
      "kind": "gameplay",
      "label": "Arsenal & four-player gameplay",
      "duration": "44 SEC",
      "note": "A tighter 27-second montage keeps all nine weapon/power demonstrations, followed by 16 seconds of four-player free-for-all across Snowy Arena, Volcano and Classic Arena. The finale uses the game’s native bots: real movement, attacks, terrain damage, eliminations and round wins. Staged demo starts, closer camera framing and native sound effects; draft picks are accelerated."
    }
  },
  {
    "id": "tiny-convoy",
    "title": "Tiny Convoy",
    "category": "Concept studies",
    "genre": "Driving / survival",
    "players": "Solo concept",
    "stage": "Concept study",
    "pitch": "Take everything. Regret it later.",
    "description": "A little utility truck tows everything you own through a dangerous desert. Every trailer is useful, and every extra axle makes the convoy harder to control. The decisive moment is knowing when to abandon something valuable to save the rest.",
    "loop": [
      "Drive a small truck along a hostile route.",
      "Attach useful salvage and extend the trailer chain.",
      "Manage the weight, swing and danger you created.",
      "Cut cargo loose when survival matters more than greed."
    ],
    "note": "A scripted concept demonstration. The film explores the intended driving and cargo loop; it is not evidence of a finished survival game.",
    "images": [
      {
        "src": "assets/tiny-convoy/01.jpg",
        "caption": "Trailer weight turns a useful convoy into a dangerous chain."
      },
      {
        "src": "assets/tiny-convoy/02.jpg",
        "caption": "The canyon-edge consequence of taking too much."
      }
    ],
    "video": {
      "src": "assets/tiny-convoy/film.mp4",
      "kind": "staged",
      "label": "Staged concept film",
      "duration": "30 SEC",
      "note": "Original GodotPrototypeFactory concept film. Interactions, outcomes and progression are staged to communicate the intended game."
    }
  },
  {
    "id": "seven-ants-underground",
    "title": "7 Ants Underground",
    "category": "Action & physics",
    "genre": "Destructible-terrain arena",
    "players": "Online multiplayer",
    "stage": "Playable prototype",
    "pitch": "Dig a way through. Make everyone else regret it.",
    "description": "An ant-colony arena built on a Liero-like foundation. Destructible terrain, class kits and host-authoritative combat support a family of experiments, from an arcade colony mode to fixed-kit toybox and environmental ring-out variants.",
    "loop": [
      "Host or join a match.",
      "Choose the class or toy kit allowed by its mode.",
      "Dig, fire and use the terrain against other ants.",
      "Survive the round and race for match wins."
    ],
    "note": "Also known as OreilChaos. Multiple modes are experiments within one developing arena project, rather than separate finished games.",
    "images": [
      {
        "src": "assets/seven-ants-underground/01.jpg?v=6cb5e608ebc4",
        "caption": "A ninja-rope swing becomes a midair Burrow Rocket attack in the native game renderer."
      },
      {
        "src": "assets/seven-ants-underground/02.jpg?v=6cb5e608ebc4",
        "caption": "A staged breach encounter demonstrates native terrain destruction and combat."
      },
      {
        "src": "assets/seven-ants-underground/03.jpg?v=6cb5e608ebc4",
        "caption": "Four scripted ants use bombs, rockets, springs, dirt spikes and falling clods in the Toybox arena."
      }
    ],
    "video": {
      "src": "assets/seven-ants-underground/film.mp4?v=6cb5e608ebc4",
      "kind": "gameplay",
      "label": "Rope & toybox gameplay",
      "duration": "36 SEC",
      "note": "Ninja-rope swings and an airborne rocket kill, a terrain breach, spring launches, wall splats, echo shots, rising lava and four-ant mayhem. Staged encounters using native game rules. Original score and native sound effects."
    }
  },
  {
    "id": "ant-delve",
    "title": "Ant Delve",
    "category": "Strategy",
    "genre": "Hex strategy / competition",
    "players": "2–4 colonies",
    "stage": "Playable prototype",
    "pitch": "Dig deeper. Bring it home before they do.",
    "description": "Competing ant colonies carve shared tunnels through a hex-based cross-section of the earth. Place tunnel tiles, move a team of ants, mine valuable resources and return them to the nest while rivals and predators complicate the route.",
    "loop": [
      "Choose a colony and starting camp.",
      "Extend the tunnel network with a hex tile.",
      "Move ants to mine, fight, trade and carry resources home.",
      "Bank the best score before the round limit."
    ],
    "note": "Hotseat, AI and online relay play are implemented. Balance and onboarding remain active areas of development.",
    "images": [
      {
        "src": "assets/ant-delve/01.jpg",
        "caption": "Three competing colonies dig into a shared underground hex board."
      },
      {
        "src": "assets/ant-delve/02.jpg",
        "caption": "Close view of ants, tunnels and resource/creature encounters."
      },
      {
        "src": "assets/ant-delve/03.jpg",
        "caption": "The turn-based board after additional AI colony actions."
      }
    ],
    "video": {
      "src": "assets/ant-delve/film-gameplay.mp4",
      "kind": "gameplay",
      "label": "Dig, mine & return showcase",
      "duration": "52 SEC",
      "note": "Actual gameplay with staged starting positions: connect a tunnel, mine sugar over three turns, bank the haul and clear an antlion chamber. Scripted legal commands, focused cameras and explanatory captions. Rival turns omitted; combat playback slowed for clarity. Silent."
    }
  },
  {
    "id": "hellgrinder",
    "title": "Hellgrinder",
    "category": "Simulation",
    "genre": "Roguelite management",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Hell has quotas. You have a debt.",
    "description": "Operate an infernal soul-processing machine under an increasingly unpleasant contract. Choose starter equipment, accept clauses, juggle heat and pressure, and decide whether an extra payout is worth another chance of catastrophe.",
    "loop": [
      "Start a run and procure four machine parts within the budget.",
      "Pick a contract and authorize an operating directive.",
      "Run the shift, manage meters and respond to incidents.",
      "Collect the result, choose upgrades and repay debt before the next shift."
    ],
    "note": "Five-shift standard runs and a two-shift employee orientation are playable. Contracts, operating directives, mid-shift decisions, between-shift upgrades and debt repayment shape each run.",
    "images": [
      {
        "src": "assets/hellgrinder/01-operated-machine.jpg",
        "caption": "The fifth shift: the original machine now carries a vent, Pressure Valve, Greed Flywheel and Audit Scrubber."
      },
      {
        "src": "assets/hellgrinder/02-procurement.jpg",
        "caption": "Procurement selects four parts within 160 Bloodcoin; this build costs 120 and retains 40."
      },
      {
        "src": "assets/hellgrinder/03-run-result.jpg",
        "caption": "The native success screen after five shifts: 350 debt, below the prototype’s 500 target."
      }
    ],
    "video": {
      "src": "assets/hellgrinder/film-full-loop.mp4",
      "kind": "gameplay",
      "label": "Full run gameplay",
      "duration": "1:34",
      "note": "A complete standard-run arc: start, equipment, contracts, directives, operator actions, a purity rejection, upgrades, incidents, debt payments and the final success screen. Normal starting funds and native outcomes; forward cuts skip unshown play. Includes explanatory captions and native procedural audio."
    }
  },
  {
    "id": "rot-garden-romance",
    "title": "Rot Garden Romance",
    "category": "Strategy",
    "genre": "Farming / dating / deckbuilding",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Grow something you probably shouldn’t fall in love with.",
    "description": "An opinionated cursed garden feeds a card-based dating game. Plant strange crops, choose their harvest rewards and build decks for three very different romance routes. Residents change the farm, while real-time growth keeps the garden moving between visits.",
    "loop": [
      "Plant and tend crops while they grow.",
      "Choose cards, seeds or resources at harvest.",
      "Build a deck and face a tactical date encounter.",
      "Deepen relationships, welcome residents and reach an ending."
    ],
    "note": "Three romance routes and a shared finale exist. The garden grows in real time; audiovisual polish remains in development.",
    "images": [
      {
        "src": "assets/rot-garden-romance/03.jpg",
        "caption": "Mira’s real Cemetery Picnic encounter and starter hand."
      },
      {
        "src": "assets/rot-garden-romance/01.jpg",
        "caption": "Three actual crop types planted in the farm."
      },
      {
        "src": "assets/rot-garden-romance/02.jpg",
        "caption": "Harvest Shame Beet and choose a real reward."
      },
      {
        "src": "assets/rot-garden-romance/04.jpg",
        "caption": "A Small Talk card changes the real affection meter."
      }
    ],
    "video": {
      "src": "assets/rot-garden-romance/film-gameplay.mp4",
      "kind": "gameplay",
      "label": "Gameplay trailer",
      "duration": "1:00",
      "note": "A garden-to-date gameplay story: grow a Blood Turnip, harvest Reckless Compliment and play Mira’s Cemetery Picnic through to a real Bond. Scripted inputs use native planting, rewards, dialogue, card effects and progression. Growth time is skipped; dialogue is advanced for readable holds. Silent footage."
    }
  },
  {
    "id": "shpinky-dinky",
    "title": "ShpinkyDinky",
    "category": "Action & physics",
    "genre": "Arena sabotage",
    "players": "Two-player multiplayer",
    "stage": "Playable prototype",
    "pitch": "Your best weapon might be where you put the trap.",
    "description": "Fight inside a readable utility chamber using a blaster and placed sabotage tools. Sticky bombs, bounce pads, vents and goo alter bodies and projectiles, making setup and redirection part of the fight.",
    "loop": [
      "Enter a duel in the utility chamber.",
      "Move and fire while placing sabotage.",
      "Redirect attacks and force a rival into danger.",
      "Resolve the round, reset and try another setup."
    ],
    "note": "A two-player arena-sabotage prototype. This showcase stages four readable interactions using the existing movement, device and damage systems.",
    "images": [
      {
        "src": "assets/shpinky-dinky/01-bank-shot.jpg",
        "caption": "A deliberately angled bounce pad redirects a real blaster shot toward the red opponent."
      },
      {
        "src": "assets/shpinky-dinky/02-goo-exit.jpg",
        "caption": "The runner crosses a prepared goo lane while the dropped bomb counts down."
      },
      {
        "src": "assets/shpinky-dinky/03-vent-trap.jpg",
        "caption": "A shove vent forces the opponent toward the bomb waiting at the exit."
      }
    ],
    "video": {
      "src": "assets/shpinky-dinky/film-engineered.mp4",
      "kind": "gameplay",
      "label": "Engineered kills showcase",
      "duration": "27 SEC",
      "note": "Four scripted duels show each setup and payoff. Real game physics and damage, staged starting positions, simplified device labels and edited timing. Includes native game audio."
    }
  },
  {
    "id": "brick-by-brick",
    "title": "Brick by Brick",
    "category": "Concept studies",
    "genre": "Tactile sorting / building",
    "players": "Solo concept",
    "stage": "Concept study",
    "pitch": "The piece you need is in there somewhere.",
    "description": "Dig through a sprawling mixed pile of construction bricks, sort useful parts and turn a mess into a finished little build. Rare finds and the satisfaction of uncovering one missing piece are the center of the concept.",
    "loop": [
      "Rummage through a mixed pile.",
      "Inspect, move and sort useful pieces.",
      "Find the parts needed for a small order.",
      "Complete the build and return to the pile."
    ],
    "note": "A staged concept demonstration. The pile uses authored depth and motion rather than a full physical brick simulation.",
    "images": [
      {
        "src": "assets/brick-by-brick/01.jpg",
        "caption": "A mixed pile of parts and the build waiting to be completed."
      },
      {
        "src": "assets/brick-by-brick/02.jpg",
        "caption": "A different readable moment from the staged sorting sequence."
      },
      {
        "src": "assets/brick-by-brick/03.jpg",
        "caption": "A different readable moment from the staged sorting sequence."
      }
    ],
    "video": {
      "src": "assets/brick-by-brick/film.mp4",
      "kind": "staged",
      "label": "Staged concept film",
      "duration": "28 SEC",
      "note": "Original GodotPrototypeFactory concept film. Interactions, outcomes and progression are staged to communicate the intended game."
    }
  },
  {
    "id": "goblin-ballistics",
    "title": "Goblin Ballistics",
    "category": "Action & physics",
    "genre": "Combat pinball",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Be the ball. Be a problem.",
    "description": "A goblin becomes the ball in a cursed pinball pit. Launch, flip and nudge through targets, bumpers, bombs and spikes while trying to keep the run alive. Speed, saves and ricochets are the appeal.",
    "loop": [
      "Launch the goblin from the plunger lane.",
      "Use flippers and nudges to control the ricochets.",
      "Smash targets, build combos and avoid hazards.",
      "Clear the table or lose your balls and try again."
    ],
    "note": "Also called Pit Goblin Pinball. The current playable build is a one-table arcade loop; roguelite upgrade/table progression is a planned direction.",
    "images": [
      {
        "src": "assets/goblin-ballistics/03.jpg",
        "caption": "The ball moves among living targets and table hazards."
      },
      {
        "src": "assets/goblin-ballistics/01.jpg",
        "caption": "The complete goblin pinball table and controls."
      },
      {
        "src": "assets/goblin-ballistics/02.jpg",
        "caption": "A real launch sends the goblin ball into play."
      }
    ],
    "video": {
      "src": "assets/goblin-ballistics/film-timed.mp4",
      "kind": "gameplay",
      "label": "Gameplay trailer",
      "duration": "20 SEC",
      "note": "Real gameplay with reactive scripted inputs: each flipper taps independently as the ball approaches its reach, then rests. Two excerpts from the same run; native physics and scoring. Silent development footage."
    }
  },
  {
    "id": "sobriety-kills",
    "title": "Sobriety Kills",
    "category": "Strategy",
    "genre": "Drafting / risk auto-battler",
    "players": "Solo",
    "stage": "Playable prototype",
    "pitch": "Power is a combination. So is disaster.",
    "description": "Draft substances into a stash, combine them into cocktails and decide what to activate before combat. Strong effects help beat escalating enemies, while dangerous pairings push an overdose meter toward a very abrupt ending.",
    "loop": [
      "Draft an offer into the stash.",
      "Merge compatible items or keep them separate.",
      "Choose an active stack with an eye on the risk.",
      "Fight a wave, survive the consequences and draft again."
    ],
    "note": "The playable vertical slice includes draft, merge, activation and combat with a limited catalog. The larger roster and presentation remain in development.",
    "images": [
      {
        "src": "assets/sobriety-kills/02-combat.jpg",
        "caption": "Mushrooms and Diphenhydramine alternate wrong-angle attacks and uncontrolled flailing."
      },
      {
        "src": "assets/sobriety-kills/01-combinations.jpg",
        "caption": "The real merge UI combines Cocaine and Mushrooms into one medium-risk cocktail."
      },
      {
        "src": "assets/sobriety-kills/03-overdose.jpg",
        "caption": "A fatal Cocaine–Heroin pairing fills the native OD meter and ends in cardiac arrest."
      }
    ],
    "video": {
      "src": "assets/sobriety-kills/film-combinations.mp4",
      "kind": "gameplay",
      "label": "Combo & overdose showcase",
      "duration": "46 SEC",
      "note": "Six combinations across all seven slice substances, mixed attack styles, enemy slowdown, a merge and two native overdose endings. Staged wave-four stashes; existing combat and OD rules. The overdose sequences are slowed for readability. Silent."
    }
  }
];
