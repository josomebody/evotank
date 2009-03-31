			#############################################################
			#		EVO         *      TANK                     #
			#############################################################

Programming, graphics, sound, and music by JoJacob
Synopsis: Evo*Tank is an 8-directional tank fighting game similar to Combat. The enemy tank operation code is evolved from a simple genetic algorithm, giving each 
individual enemy type an organic and quirky modus operandi. The tanks have a simple high-speed repeating cannon prone to heat jamming, a six-speed throttle 
(three forward speeds, neutral, and two reverse speeds), and can move in eight directions. The enemy tanks have built-in operations to control their speed, steer,
and track the player and pickups. These operations make up ten opcodes that are sequenced in each tank's genetics.

Control: Evo*Tank currently uses a keyboard-only control scheme, though a joystick scheme would be easy to implement. The controls are as follows:

[ARROW KEYS]:
	THROTTLE UP
	       ^
	       |
STEER LEFT<----+---->STEER RIGHT
	       |
	       v
	THROTTLE DOWN

[SPACEBAR]: FIRE

Things in the game:
Player: You play the tank with the orange turret. A human tank pilot charged with training robots to effectively drive the tanks, your superiors have placed you in a
simulation chamber to do battle with your trainees. In the Breeding Pit, those who do well will combine their code to create the next generation of bots, and in
the event that only one survives, it will be propagated with mutations in the next round.

Heads Up Display: The colored bars at the bottom of the screen represent your status,and each item of your status is labeled accordingly on the bars. The bar labeled
"THROTTLE" represents your current speed. If the bar is to the right, you are moving forward, left in reverse. No bar means you are in neutral. The length of the bar
represents your speed. There is also a display of the name of each tank bot hovering over its respective tank, along with its breeding status in the Breeding Pit, 
and a simple console in the top left corner for displaying in-game messages.

Enemy Tanks: These are the green tanks. The are piloted by the autonomous robots whose code is evolving with each generation. The nature of their code will be 
discussed in its own section.

Pickups: The bots are to be trained, in addition to successfully piloting a tank and killing targets, to scavenge for spare armor, fuel, and ammunition. These items
are represented on the game board as icons.  A plate of steel represents armor, and will charge a tank's armor status to 100%. A gasoline gan represents fuel. Fuel
can only be picked up when the fuel tank is below a certain threshold. An image of a bullet represents ammunition. These items are worth 100 rounds, however, a tank
can only hold 100 rounds of ammunition at a time, and the rest is discarded.

In the Breeding Pit, pickups will be generated and placed at random.

Obstacles: These are crates and barrels that serve no purpose other than to get in the way. These items cannot be driven over by a tank.  There are no obstacles in
the Breeding Pit.

Tank Programming:
A graphical programmer for the enemy tanks will be provided with this package. With this program, you can view and edit the code of existing tanks, or create new 
ones to breed or place in user-made levels.

A tank bot is wired to the sensors and controls of its tank and can react in a limited way to this input. The bot's processor has five states, determined by the 
status of certain sensors. The thresholds under which each state is triggered are adjustable and evolve along with the procedure code for each state. The states
are as follows:
0--Search Drone: This is the bot's default state when no other states are triggered.
1--Low Armor: The bot goes into this state when armor drops below a certain threshold.
2--Low Fuel: This state is triggered when fuel drops below a certin threshold.
3--Low Ammunition: This state is of a low priority and triggers when ammunition is below the threshold allowed by the bot's genetic code.
5--Close to target: This state is triggered when the tank is within a certain distance of the enemy target and no other states (with the exception of State 0) have
been triggered this cycle.
Special Breeding Pit States:
Mating: This is triggered when a bot has determined itself to be a successful killer (after it has successfully landed five shots on its target, and every five shots
afterward). The tank will seek out the tank with the highest score and combine code with it to produce a new tank and robot.
Gestating: This state is the gestation period for a tank bot. It lasts 250 game cycles.

Each state (excluding the special states) executes a code segment containing eight commands to be run in a loop until the state is changed. Each of the eight slots
could be one of ten commands:
0--nop, skip this step
1--turn right
2--turn left
3--throttle up
4--throttle down
(5 through 8 all turn to face certain objects)
5--enemy target
6--fuel
7--armor
8--ammunition
9--fire cannon

Tank Bot Creation:
The tank bot code files for tanks used in the game are stored in the folder savedbots/.  The bots used in the Breeding Pit are stored in the evotank/ directory as
bot#, with the # being a number, starting with 0, for each bot to be used. If the bot# files do not exist, they will be generated randomly when the Breeding Pit 
program is run. Otherwise, they will be the bot files for all tank bots surviving the last round. They are saved every time your tank is destroyed.

Mating: If two tank bots mate, their code is combined randomly. Each state threshold and state code segment is chosen randomly either from the mother or the father.
Tank bots are hermaphroditic, and may serve as either parent. The offspring bot may at random also be slightly mutated.
Mutation: The act of mutation, if it occurs, randomly adjusts the value of a random state threshold, and the command in a random slot of a random state code segment.

Strategies for Survival:
Do to the nature of evolving code, learning one trick may not work for long as the tank bots adjust to your playing style. Watch the heat level of your cannon, as it
will slow the repeating rate of your cannon if it gets too high. Your tank will issue a verbal warning when the cannon is too hot to fire.  Take evasive action to 
let it cool off. Pay attention to the entire heads up display. Your tank will issue verbal warnings if armor, ammunition, or fuel are too low as well. Some tank bots
may behave aggressively if approached or fired upon, and may act completely randomly. Treat them like rabid dogs with guns.  Ramming also causes damage to the tanks,
and a few of the bots have learned this. This fact can also be used to your advantage to avoid cannon overheating.

Strategies for Breeding:
Breeding your own tank bots to fight your friends is fun and challenging. To do so, start either with randomly generated bots or a few you like and load them into
the breeding pit. You can get randomly generated bot files by deleting bot* from the evotank/ folder, or load existing bots by copying them to bot# files, starting
with bot0.  If you start with randomly generated bots, the first several generations will probably not do much more than twitch, but after several rounds, one will
come along with an interesting behavior. To save this bot, kill all the others to bring up an exit dialog, and exit the game. Your bot will be in the file bot0. 
Copy this file to evotank/savedbots/ as the name of the bot for reuse. To let this bot breed for a few generations, allow it to land five shots on your tank, and it
will select a mating partner. Once the new bot is concieved, it will burst out of the mother tank in 250 frames. Follow the offspring bots and observe their behavior
to find improvements.

CREDITS:
Graphics created in GIMP
Code created with VI, BoaConstructor, and DrPython
Sound effects created with Audacity and Espeak
Music created with Audacity, Hydrogen, and a Korg Electribe EA-1
Originally buit on Debian Etch http://www.debian.org GET LINUX!
This game was generated using all free software and is free for distribution, appropriation, and modification for all non-commercial purposes, as long as credit is
given to the original creator.
