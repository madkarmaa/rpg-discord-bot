/* Schema for  `items` database */

/*
https://www.sqlitetutorial.net/

The USING keyword is used in an INNER JOIN or OUTER JOIN (LEFT JOIN, RIGHT JOIN, or FULL JOIN) to specify
the columns that are used to connect the tables. When you use the USING keyword, you only need to specify
the column names that are common to both tables, rather than having to specify the full column names for each table.

For example, suppose you have two tables named table1 and table2, and both tables have a column named id.
If you want to connect these tables using the id column, you could use the following INNER JOIN query:

SELECT * FROM table1
INNER JOIN table2
USING (id);

This query is equivalent to the following INNER JOIN query that uses the ON keyword to specify the columns
that are used to connect the tables:

SELECT * FROM table1
INNER JOIN table2
ON table1.id = table2.id;

Both of these queries will return a table that contains all rows from both table1 and table2 where the id values
are the same. The resulting table will include all columns from both table1 and table2.

In addition to simplifying the syntax of the JOIN clause, using the USING keyword can also make your query more
readable and easier to understand. It also ensures that the columns used to connect the tables are the same in both tables,
which can help prevent errors in your query.

In SQLite, it is not possible to define a column with a "list" data type. SQLite supports a limited set of data types, including INTEGER, REAL, TEXT, and BLOB, but it does not have a built-in data type for storing lists of values.

If you need to store a list of values in a SQLite table, one option is to use a TEXT field and encode the list as a string
using a delimiter character to separate the values. For example, you could encode a list of integers
as a string like this: "1,2,3,4,5". Then you can use the split() function and a regular expression to split the string
back into a list of values when you want to access the data.

Yes, it is possible to join tables from different databases in SQLite.
To do this, you would first need to create a new database that contains both tables, and then you can use a JOIN clause
in a SELECT statement to combine the data from the two tables. For example:

ATTACH DATABASE "database1.db" AS db1;
ATTACH DATABASE "database2.db" AS db2;

SELECT *
FROM db1.table1
JOIN db2.table2
ON db1.table1.column1 = db2.table2.column1;

This query would attach the databases database1.db and database2.db as db1 and db2, respectively,
and then use a JOIN clause to combine data from the table1 and table2 tables based on a common column1 in each table.

https://minecraft.fandom.com/wiki/Minecraft_Dungeons:Item

Max item level: 260
*/

BEGIN TRANSACTION;


CREATE TABLE IF NOT EXISTS melee (
    id                  INTEGER         PRIMARY KEY AUTOINCREMENT,
    name                TEXT            NOT NULL,
    rarity              TEXT            NOT NULL DEFAULT "common, rare",
    description         TEXT            NOT NULL,
    image_path          TEXT            NOT NULL,
    emoji_string        TEXT            NOT NULL,
    emoji_id            INTEGER         NOT NULL
);

CREATE TABLE IF NOT EXISTS melee_specials (
    id_melee            INTEGER         REFERENCES melee(id) NOT NULL,
    name                TEXT            NOT NULL,
    rarity              TEXT            NOT NULL DEFAULT "unique",
    description         TEXT            NOT NULL,
    image_path          TEXT            NOT NULL,
    emoji_string        TEXT            NOT NULL,
    emoji_id            INTEGER         NOT NULL
);


INSERT INTO melee (name, description, image_path, emoji_string, emoji_id)
VALUES
        ("Anchor",
        "Those strong enough to wield the Anchor in battle follow the tradition of legendary seafaring warriors.",
        ".\src\img\melee\Anchor\Anchor.png",
        "<:Anchor:1039206310077546497>",
        1039206310077546497),

        ("Axe",
        "The axe is an effective weapon, favored by the relentless Vindicators of the Arch-Illager's army.",
        ".\src\img\melee\Axe\Axe.png",
        "<:Axe:1039214131850514523>",
        1039214131850514523),

        ("Backstabber",
        "The preferred blade of thieves and assassins, the Backstabber is a must in any rogue's pack.",
        ".\src\img\melee\Backstabber\Backstabber.png",
        "<:Backstabber:1039217021973430314>",
        1039217021973430314),

        ("Battlestaff",
        "The battlestaff is a perfectly balanced staff that is ready for any battle.",
        ".\src\img\melee\Battlestaff\Battlestaff.png",
        "<:Battlestaff:1039218457658544189>",
        1039218457658544189),

        ("Boneclub",
        "Those who wield a Bone Club prefer as less-subtle approach to problem-solving.",
        ".\src\img\melee\Boneclub\Boneclub.png",
        "<:Boneclub:1039219424739217419>",
        1039219424739217419),

        ("Broken Sawblade",
        "The Broken Sawblade has been ravaged by time, but it still does considerable damage.",
        ".\src\img\melee\Broken Sawblade\Broken Sawblade.png",
        "<:BrokenSawblade:1039221402617794650>",
        1039221402617794650),

        ("Claymore",
        "A massive sword that seems impossibly heavy yet rests easily in a just warrior's hands.",
        ".\src\img\melee\Claymore\Claymore.png",
        "<:Claymore:1039222963276353606>",
        1039222963276353606),

        ("Coral Blade",
        "The Coral Blade cuts through enemies with stinging accuracy.",
        ".\src\img\melee\Coral Blade\Coral Blade.png",
        "<:CoralBlade:1039225096990117918>",
        1039225096990117918),

        ("Cutlass",
        "This curved blade, wielded by the warriors of the Squid Coast, requires a steady hand in battle.",
        ".\src\img\melee\Cutlass\Cutlass.png",
        "<:Cutlass:1039225988158070854>",
        1039225988158070854),

        ("Daggers",
        "Daggers are the weapon of cravens - or so folk say.",
        ".\src\img\melee\Daggers\Daggers.png",
        "<:Daggers:1039227783097892965>",
        1039227783097892965),

        ("Double Axe",
        "A devastating weapon fit for barbaric fighters.",
        ".\src\img\melee\Double Axe\Double Axe.png",
        "<:DoubleAxe:1039261440374222878>",
        1039261440374222878),

        ("Gauntlets",
        "Gauntlets call back to an ancient style of hand to hand combat.",
        ".\src\img\melee\Gauntlets\Gauntlets.png",
        "<:Gauntlets:1039261948392517733>",
        1039261948392517733),

        ("Glaive",
        "The glaive, wielded by the servants of the Nameless One, is a weapon with style and power.",
        "src\img\melee\Glaive\Glaive.png",
        "<:Glaive:1039264222086975538>",
        1039264222086975538),

        ("Great Hammer",
        "Blacksmiths and soldiers alike use the Great Hammer for its strength in forging and in battle.",
        ".\src\img\melee\Great Hammer\Great Hammer.png",
        "<:GreatHammer:1039264270992543794>",
        1039264270992543794),

        ("Katana",
        "A blade fit for expert warriors and fighters, its blade is crafted to inflict precision damage.",
        ".\src\img\melee\Katana\Katana.png",
        "<:Katana:1039266364675862569>",
        1039266364675862569),

        ("Mace",
        "The Mace is a brutal tool of war and what it lacks in finesse; it makes up for in power.",
        ".\src\img\melee\Mace\Mace.png",
        "<:Mace:1039268443553267752>",
        1039268443553267752),

        ("Obsidian Claymore",
        "This massive blade cleaves even the thickest shulker shells with style and ease.",
        ".\src\img\melee\Obsidian Claymore\Obsidian Claymore.png",
        "<:ObsidianClaymore:1039273302713172009>",
        1039273302713172009),

        ("Pickaxe",
        "The pickaxe has been the iconic tool of adventurers and heroes for as long as anyone can remember.",
        ".\src\img\melee\Pickaxe\Pickaxe.png",
        "<:Pickaxe:1039274752679882772>",
        1039274752679882772),

        ("Rapier",
        "The rapier, a nimble and narrow blade, strikes with quick ferocity.",
        ".\src\img\melee\Rapier\Rapier.png",
        "<:Rapier:1039274788088184882>",
        1039274788088184882),

        ("Sickles",
        "A ceremonial weapon that hails from the same region as the Desert Temple.",
        ".\src\img\melee\Sickles\Sickles.png",
        "<:Sickles:1039276794051829781>",
        1039276794051829781),

        ("Soul Knife",
        "A ceremonial knife that uses magical energy to hold the wrath of souls inside its blade.",
        ".\src\img\melee\Soul Knife\Soul Knife.png",
        "<:SoulKnife:1039276839820066856>",
        1039276839820066856),

        ("Soul Scythe",
        "A cruel reaper of souls, the Soul Scythe is unsentimental in its work.",
        ".\src\img\melee\Soul Scythe\Soul Scythe.png",
        "<:SoulScythe:1039278506770710549>",
        1039278506770710549),

        ("Spear",
        "The spear, with its long reach and powerful range, is a solid choice of weapon.",
        ".\src\img\melee\Spear\Spear.png",
        "<:Spear:1039278551226134699>",
        1039278551226134699),

        ("Sword",
        "A sturdy and reliable blade. but with its magic, it could be of a good use.",
        ".\src\img\melee\Sword\Sword.png",
        "<:Sword:1039282214371860533>",
        1039282214371860533),

        ("Tempest Knife",
        "This knife slices through enemies like the winds that cuts between the mountaintops.",
        ".\src\img\melee\Tempest Knife\Tempest Knife.png",
        "<:TempestKnife:1039282257652887682>",
        1039282257652887682),

        ("Void Touched Blades",
        "These Blades are infused with a disturbing purpose after countless ages trapped in the End.",
        ".\src\img\melee\Void Touched Blades\Void Touched Blades.png",
        "<:VoidTouchedBlades:1039284700755263528>",
        1039284700755263528),

        ("Whip",
        "A whip made of sturdy rope, very dangerous in the right hands.",
        ".\src\img\melee\Whip\Whip.png",
        "<:Whip:1039284735668658246>",
        1039284735668658246);

INSERT INTO melee_specials (id_melee, name, description, image_path, emoji_string, emoji_id)
VALUES
        (1,
        "Encrusted Anchor",
        "This Encrusted Anchor was lost at sea long ago and has become harsh and corrosive during its ages of neglect.",
        ".\src\img\melee\Anchor\specials\EncrustedAnchor.png",
        "<:EncrustedAnchor:1039206336795267193>",
        1039206336795267193),

        (2,
        "Firebrand",
        "Crafted in the blackest depths of the Fiery Forge and enchanted with fiery powers.",
        ".\src\img\melee\Axe\specials\Firebrand.png",
        "<:Firebrand:1039214157888749609>",
        1039214157888749609),

        (2,
        "Highland Axe",
        "Expertly crafted and a polished weapon of war, the Highland Axe also makes a daring backscratcher",
        ".\src\img\melee\Axe\specials\Highland Axe.png",
        "<:HighlandAxe:1039214162582179870>",
        1039214162582179870),

        (3,
        "Swift Striker",
        "A blade for those who know that the surest way to victory is to strike without being seen.",
        ".\src\img\melee\Backstabber\specials\Swift Striker.png",
        "<:SwiftStriker:1039217038343811112>",
        1039217038343811112),

        (4,
        "Battlestaff of Terror",
        "This staff overwhelms its target in battle to explosive effect.",
        ".\src\img\melee\Battlestaff\specials\Battlestaff of Terror.png",
        "<:BattlestaffofTerror:1039218480530067476>",
        1039218480530067476),

        (4,
        "Growing Staff",
        "A staff that grows and shifts as it attacks, the Growing Staff is unpredictable and powerful.",
        ".\src\img\melee\Battlestaff\specials\Growing Staff.png",
        "<:GrowingStaff:1039218483021492224>",
        1039218483021492224),

        (5,
        "Bone Cudgel",
        "The Bone Cudgel is old enough to be considered an ancient treasure, but still menacing even by modern standards.",
        ".\src\img\melee\Boneclub\specials\Bone Cudgel.png",
        "<:BoneCudgel:1039219439893225493>",
        1039219439893225493),

        (6,
        "Mechanized Sawblade",
        "The Mechanized Sawblade still glows from the fires of the Nether where it was forged.",
        ".\src\img\melee\Broken Sawblade\specials\Mechanized Sawblade.png",
        "<:MechanizedSawblade:1039221418581315716>",
        1039221418581315716),

        (7,
        "Broadsword",
        "Only those with the strength of a champion and the heart of a hero can carry this massive blade.",
        ".\src\img\melee\Claymore\specials\Broadsword.png",
        "<:Broadsword:1039222984663105567>",
        1039222984663105567),

        (7,
        "Great Axeblade",
        "A lucky blacksmith turned a workshop blunder into a battlefield wonder, fusing two weapons into something new.",
        ".\src\img\melee\Claymore\specials\Great Axeblade.png",
        "<:GreatAxeblade:1039222987586543637>",
        1039222987586543637),

        (7,
        "Heartstealer",
        "Gifted to one of the Arch-Illager's most distinguished generals upon their conquest of the Squid Coast - this runeblade is infused with dark witchcraft.",
        ".\src\img\melee\Claymore\specials\Heartstealer.png",
        "<:Heartstealer:1039222991529185280>",
        1039222991529185280),

        (8,
        "Sponge Striker",
        "This blade may look colorless and dead, but it soaks up energy in combat and expels it in a powerful burst.",
        ".\src\img\melee\Coral Blade\specials\Sponge Striker.png",
        "<:SpongeStriker:1039225111955386450>",
        1039225111955386450),

        (9,
        "Dancer's Sword",
        "Warriors who view battle as a dance with death prefer double-bladed swords.",
        ".\src\img\melee\Cutlass\specials\Dancers Sword.png",
        "<:DancersSword:1039226011851706378>",
        1039226011851706378),

        (9,
        "Nameless Blade",
        "This deadly blade's story was lost to the endless sands of time.",
        ".\src\img\melee\Cutlass\specials\Nameless Blade.png",
        "<:NamelessBlade:1039226014070493184>",
        1039226014070493184),

        (10,
        "Fangs of Frost",
        "These lauded twin daggers of the northern mountains are known to freeze their foes to solid ice.",
        ".\src\img\melee\Daggers\specials\Fangs of Frost.png",
        "<:FangsofFrost:1039227809534578809>",
        1039227809534578809),

        (10,
        "Moon Daggers",
        "These curved blades shine like the crescent moon on a dark night.",
        ".\src\img\melee\Daggers\specials\Moon Daggers.png",
        "<:MoonDaggers:1039227812478996520>",
        1039227812478996520),

        (10,
        "Sheer Daggers",
        "Even the simplest of farmers can wield these Shear Daggers with savage results.",
        ".\src\img\melee\Daggers\specials\Sheer Daggers.png",
        "<:SheerDaggers:1039227815423377498>",
        1039227815423377498),

        (11,
        "Cursed Axe",
        "This cursed, poisonous axe leaves their victims sick for years with just a single scratch.",
        ".\src\img\melee\Double Axe\specials\Cursed Axe.png",
        "<:CursedAxe:1039261462696312932>",
        1039261462696312932),

        (11,
        "Whirlwind",
        "Whirlwind, forged during an epic windstorm, is a double-bladed axe that levitates slightly.",
        ".\src\img\melee\Double Axe\specials\Whirlwind.png",
        "<:Whirlwind:1039261465015762984>",
        1039261465015762984),

        (12,
        "Fighter's Bindings",
        "Made in the wilds beyond the mountains, these gauntlets have been worn by warriors for centuries.",
        ".\src\img\melee\Gauntlets\specials\Fighters Bindings.png",
        "<:FightersBindings:1039261968546148402>",
        1039261968546148402),

        (12,
        "Maulers",
        "These claw-like weapons, wielded by ancient Illager soldiers, are savage in battle.",
        ".\src\img\melee\Gauntlets\specials\Maulers.png",
        "<:Maulers:1039261971918373004>",
        1039261971918373004),

        (12,
        "Soul Fists",
        "Soul Fists are gauntlets clad with great gemstones, each containing a powerful soul.",
        ".\src\img\melee\Gauntlets\specials\Soul Fists.png",
        "<:SoulFists:1039261974619492454>",
        1039261974619492454),

        (13,
        "Grave Bane",
        "A relic from ages of darkness; this glaive radiates potent magical energy to ward off the undead.",
        ".\src\img\melee\Glaive\specials\Grave Bane.png",
        "<:GraveBane:1039264241414324404>",
        1039264241414324404),

        (13,
        "Venom Glaive",
        "A toxic cloud seems to follow the Venom Glaive wherever it goes...",
        ".\src\img\melee\Glaive\specials\Venom Glaive.png",
        "<:VenomGlaive:1039264244606185482>",
        1039264244606185482),

        (14,
        "Hammer of Gravity",
        "A hammer, embedded with a crystal that harnesses the power of gravity, that is incredibly powerful.",
        ".\src\img\melee\Great Hammer\specials\Hammer of Gravity.png",
        "<:HammerofGravity:1039264288356966400>",
        1039264288356966400),

        (14,
        "Stormlander",
        "The Stormlander, enchanted with the power of the raging storm, is a treasure of the Illagers.",
        ".\src\img\melee\Great Hammer\specials\Stormlander.png",
        "<:Stormlander:1039264291376873492>",
        1039264291376873492),

        (15,
        "Dark Katana",
        "A blade that will not rest until the battle has been won.",
        ".\src\img\melee\Katana\specials\Dark Katana.png",
        "<:DarkKatana:1039266386326855771>",
        1039266386326855771),

        (15,
        "Master's Katana",
        "The Master's Katana has existed throughout the ages, appearing to heroes at the right moment.",
        ".\src\img\melee\Katana\specials\Masters Katana.png",
        "<:MastersKatana:1039266388713410560>",
        1039266388713410560),

        (16,
        "Flail",
        "This ancient weapon inflicts grave blunt damage to those who cannot evade the deadly metal ball.",
        ".\src\img\melee\Mace\specials\Flail.png",
        "<:Flail:1039268460523429889>",
        1039268460523429889),

        (16,
        "Sun's Grace",
        "This mace, engraved with secret healing runes, grants powerful restorative powers.",
        ".\src\img\melee\Mace\specials\Suns Grace.png",
        "<:SunsGrace:1039268463715295342>",
        1039268463715295342),

        (17,
        "The Starless Night",
        "The Starless Night is haunted by echoes of pain that linger within the pitch-black blade.",
        ".\src\img\melee\Obsidian Claymore\specials\The Starless Night.png",
        "<:TheStarlessNight:1039273317955280918>",
        1039273317955280918),

        (18,
        "Diamond Pickaxe",
        "Diamond is one of the most durable materials, making it an excellent choice for a pickaxe.",
        ".\src\img\melee\Pickaxe\specials\Diamond Pickaxe.png",
        "<:DiamondPickaxe:1039274767401877605>",
        1039274767401877605),

        (19,
        "Bee Stinger",
        "The Bee Stinger, a swift blade inspired by a bee's barb, can draw friendly bees into the fray to fight alongside you.",
        ".\src\img\melee\Rapier\specials\Bee Stinger.png",
        "<:BeeStinger:1039274806773813298>",
        1039274806773813298),

        (19,
        "Freezing Foil",
        "This needle-like blade is cold to the touch and makes quick work of any cut.",
        ".\src\img\melee\Rapier\specials\Freezing Foil.png",
        "<:FreezingFoil:1039274809982459974>",
        1039274809982459974),

        (20,
        "Nightmare's Bite",
        "The twin blades of Nightmare's Bite drip with deadly venom, still potent after all these years.",
        ".\src\img\melee\Sickles\specials\Nightmares Bite.png",
        "<:NightmaresBite:1039276813744099349>",
        1039276813744099349),

        (20,
        "The Last Laugh",
        "Strange, distorted laughter seems to whisper from these menacing looking sickles.",
        ".\src\img\melee\Sickles\specials\The Last Laugh.png",
        "<:TheLastLaugh:1039276817305055333>",
        1039276817305055333),

        (21,
        "Eternal Knife",
        "A disturbing aura surrounds this knife, as if it has existed for all time and will outlive us all.",
        ".\src\img\melee\Soul Knife\specials\Eternal Knife.png",
        "<:EternalKnife:1039276860040827001>",
        1039276860040827001),

        (21,
        "Truthseeker",
        "The warden of Highblock Keep kept this unpleasant blade by their side during interrogations.",
        ".\src\img\melee\Soul Knife\specials\Truthseeker.png",
        "<:Truthseeker:1039276862578364516>",
        1039276862578364516),

        (22,
        "Frost Scythe",
        "The Frost Scythe is an indestructible blade that is freezing to the touch and never seems to melt.",
        ".\src\img\melee\Soul Scythe\specials\Frost Scythe.png",
        "<:FrostScythe:1039278526559424512>",
        1039278526559424512),

        (22,
        "Jailor's Scythe",
        "This scythe belonged to the terror of Highblock Keep, the Jailor.",
        ".\src\img\melee\Soul Scythe\specials\Jailors Scythe.png",
        "<:JailorsScythe:1039278529575145484>",
        1039278529575145484),

        (23,
        "Fortune Spear",
        "A spear that is watched over by lucky souls, bringing luck to any who wield it.",
        ".\src\img\melee\Spear\specials\Fortune Spear.png",
        "<:FortuneSpear:1039278570649964614>",
        1039278570649964614),

        (23,
        "Whispering Spear",
        "Legend says that this cursed spear is plagued by a soul that controls the mind of any who wield it.",
        ".\src\img\melee\Spear\specials\Whispering Spear.png",
        "<:WhisperingSpear:1039278573544013844>",
        1039278573544013844),

        (24,
        "Diamond Sword",
        "The Diamond Sword is the true mark of a hero and an accomplished adventurer.",
        ".\src\img\melee\Sword\specials\Diamond Sword.png",
        "<:DiamondSword:1039282231404920853>",
        1039282231404920853),

        (24,
        "Hawkbrand",
        "The Hawkbrand is the legendary sword of proven warriors.",
        ".\src\img\melee\Sword\specials\Hawkbrand.png",
        "<:Hawkbrand:1039282235133665392>",
        1039282235133665392),

        (25,
        "Chill Gale Knife",
        "Created from the never-melting ice atop the mountain peaks, this knife is forever icy to the touch.",
        ".\src\img\melee\Tempest Knife\specials\Chill Gale Knife.png",
        "<:ChillGaleKnife:1039282278938980482>",
        1039282278938980482),

        (25,
        "Resolute Tempest Knife",
        "Passed down by nomads who roam the mountain peaks, this knife has been used in countless battles.",
        ".\src\img\melee\Tempest Knife\specials\Resolute Tempest Knife.png",
        "<:ResoluteTempestKnife:1039282281644314674>",
        1039282281644314674),

        (26,
        "The Beginning and The End",
        "Forged by the survivors of a doomed expedition to the End, these twin blades carry dark secrets.",
        ".\src\img\melee\Void Touched Blades\specials\The Beginning and The End.png",
        "<:TheBeginningandTheEnd:1039284713610817606>",
        1039284713610817606),

        (27,
        "Vine Whip",
        "A sturdy whip made from thick, thorn-laden vines capable of poisoning anything it touches. Be careful not to scratch yourself!",
        ".\src\img\melee\Whip\specials\Vine Whip.png",
        "<:VineWhip:1039284748255756288>",
        1039284748255756288);


COMMIT TRANSACTION;