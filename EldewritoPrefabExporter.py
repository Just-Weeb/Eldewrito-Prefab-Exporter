bl_info = {
	"name": "Eldewrito Prefab Exporter",
	"author": "Weebmaster",
	"version": (1, 0, 1),
	"blender": (2, 80, 0),
	"location": "File > Export > Eldewrito Prefab (.prefab)",
	"description": "Prefab exporter compatible with Eldewrito's forge prefab system ",
	"warning": "Requires OBJ files obtained from Eldewrito to properly display once exported from blender",
	"wiki_url": "",
	"category": "Import-Export",
}
import bpy
import mathutils
from math import radians
import struct
from pathlib import Path


def write_some_data(context, filepath, use_some_setting):
    #TODO: Move dictionary outside of the function and possibly pass it in, so it isnt created everytime the function is called.
    tagDict = {
        "BLOCK [01 x 05 x 05]": "0000015c",
        "BLOCK [01 x 1 x 05]": "00000158",
        "BLOCK [01 x 1 x 1]": "00000148",
        "BLOCK [01 x 2 x 05]": "00000156",
        "BLOCK [01 x 2 x 1]": "0000014c",
        "BLOCK [01 x 2 x 2]": "00000155",
        "BLOCK [01 x 3 x 05]": "0000015a",
        "BLOCK [01 x 3 x 1]": "0000014a",
        "BLOCK [01 x 3 x 2]": "00000154",
        "BLOCK [01 x 3 x 3]": "00000153",
        "BLOCK [01 x 4 x 05]": "00000159",
        "BLOCK [01 x 4 x 1]": "00000149",
        "BLOCK [01 x 4 x 2]": "00000141",
        "BLOCK [01 x 4 x 3]": "00000152",
        "BLOCK [01 x 4 x 4]": "00000151",
        "BLOCK [01 x 5 x 05]": "0000015b",
        "BLOCK [01 x 5 x 1]": "0000014b",
        "BLOCK [01 x 5 x 2]": "0000014f",
        "BLOCK [01 x 5 x 3]": "0000014e",
        "BLOCK [01 x 5 x 4]": "0000014d",
        "BLOCK [01 x 5 x 5]": "00000150",
        "BLOCK [01 x 10 x 05]": "00000157",
        "BLOCK [01 x 10 x 1]": "00000145",
        "BLOCK [01 x 10 x 2]": "00000144",
        "BLOCK [01 x 10 x 3]": "00000143",
        "BLOCK [01 x 10 x 4]": "00000142",
        "BLOCK [01 x 10 x 5]": "00000146",
        "BLOCK [01 x 10 x 10]": "00000147",
        "BLOCK [01 x 20 x 20]": "0000015d",
        "BLOCK [05 x 05 x 05]": "0000012a",
        "BLOCK [05 x 1 x 05]": "0000012b",
        "BLOCK [05 x 1 x 1]": "00000132",
        "BLOCK [05 x 2 x 1]": "00000136",
        "BLOCK [05 x 2 x 2]": "0000013f",
        "BLOCK [05 x 3 x 1]": "00000134",
        "BLOCK [05 x 3 x 2]": "0000013e",
        "BLOCK [05 x 3 x 3]": "0000013d",
        "BLOCK [05 x 4 x 1]": "00000133",
        "BLOCK [05 x 4 x 2]": "00000129",
        "BLOCK [05 x 4 x 3]": "0000013c",
        "BLOCK [05 x 4 x 4]": "0000013b",
        "BLOCK [05 x 5 x 1]": "00000135",
        "BLOCK [05 x 5 x 2]": "00000139",
        "BLOCK [05 x 5 x 3]": "00000138",
        "BLOCK [05 x 5 x 4]": "00000137",
        "BLOCK [05 x 5 x 5]": "0000013a",
        "BLOCK [05 x 10 x 1]": "0000012f",
        "BLOCK [05 x 10 x 2]": "0000012e",
        "BLOCK [05 x 10 x 3]": "0000012d",
        "BLOCK [05 x 10 x 4]": "0000012c",
        "BLOCK [05 x 10 x 5]": "00000130",
        "BLOCK [05 x 10 x 10]": "00000131",
        "BLOCK [05 x 20 x 20]": "00000128",
        "BLOCK [1 x 1 x 1]": "0000011f",
        "BLOCK [1 x 2 x 1]": "0000011b",
        "BLOCK [1 x 2 x 2]": "00000140",
        "BLOCK [1 x 3 x 1]": "0000011d",
        "BLOCK [1 x 3 x 2]": "00000113",
        "BLOCK [1 x 3 x 3]": "00000114",
        "BLOCK [1 x 4 x 1]": "0000011e",
        "BLOCK [1 x 4 x 2]": "00000126",
        "BLOCK [1 x 4 x 3]": "00000115",
        "BLOCK [1 x 4 x 4]": "00000116",
        "BLOCK [1 x 5 x 1]": "0000011c",
        "BLOCK [1 x 5 x 2]": "00000118",
        "BLOCK [1 x 5 x 3]": "00000119",
        "BLOCK [1 x 5 x 4]": "0000011a",
        "BLOCK [1 x 5 x 5]": "00000117",
        "BLOCK [1 x 10 x 1]": "00000122",
        "BLOCK [1 x 10 x 2]": "00000123",
        "BLOCK [1 x 10 x 3]": "00000124",
        "BLOCK [1 x 10 x 4]": "00000125",
        "BLOCK [1 x 10 x 5]": "00000121",
        "BLOCK [1 x 10 x 10]": "00000120",
        "BLOCK [1 x 20 x 20]": "00000127",
        "TRIANGLE [01 x 05 x 05]": "00000163",
        "TRIANGLE [01 x 1 x 1]": "00000164",
        "TRIANGLE [01 x 2 x 2]": "00000162",
        "TRIANGLE [01 x 3 x 3]": "00000161",
        "TRIANGLE [01 x 4 x 4]": "00000160",
        "TRIANGLE [01 x 5 x 5]": "0000015f",
        "TRIANGLE [01 x 10 x 10]": "0000015e",
        "TRIANGLE [05 x 05 x 05]": "00000112",
        "TRIANGLE [05 x 1 x 1]": "0000010b",
        "TRIANGLE [05 x 2 x 2]": "0000010f",
        "TRIANGLE [05 x 3 x 3]": "0000010e",
        "TRIANGLE [05 x 4 x 4]": "0000010d",
        "TRIANGLE [05 x 5 x 5]": "0000010c",
        "TRIANGLE [05 x 10 x 10]": "00000110",
        "TRIANGLE [1 x 05 x 05]": "00000105",
        "TRIANGLE [1 x 1 x 1]": "0000010a",
        "TRIANGLE [1 x 2 x 2]": "00000106",
        "TRIANGLE [1 x 3 x 3]": "00000107",
        "TRIANGLE [1 x 4 x 4]": "00000108",
        "TRIANGLE [1 x 5 x 5]": "00000109",
        "TRIANGLE [1 x 10 x 10]": "00000111",
        "TRIANGLE (EQUAL) [01 x 05 x 043]": "000000f7",
        "TRIANGLE (EQUAL) [01 x 1 x 087]": "000000f5",
        "TRIANGLE (EQUAL) [01 x 2 x 073]": "000000f4",
        "TRIANGLE (EQUAL) [01 x 3 x 06]": "000000f3",
        "TRIANGLE (EQUAL) [01 x 4 x 046]": "000000f2",
        "TRIANGLE (EQUAL) [01 x 5 x 033]": "000000f6",
        "CYLINDER [05 x 05 x 01]": "000000d6",
        "CYLINDER [05 x 05 x 05]": "000000ed",
        "CYLINDER [05 x 05 x 1]": "000000dd",
        "CYLINDER [05 x 05 x 2]": "000000e0",
        "CYLINDER [05 x 05 x 4]": "000000e3",
        "CYLINDER [1 x 1 x 01]": "000000d7",
        "CYLINDER [1 x 1 x 05]": "000000d8",
        "CYLINDER [1 x 1 x 1]": "000000dc",
        "CYLINDER [1 x 1 x 2]": "000000df",
        "CYLINDER [1 x 1 x 4]": "000000e2",
        "CYLINDER [2 x 2 x 01]": "000000d5",
        "CYLINDER [2 x 2 x 05]": "000000d9",
        "CYLINDER [2 x 2 x 1]": "000000db",
        "CYLINDER [2 x 2 x 2]": "000000de",
        "CYLINDER [2 x 2 x 4]": "000000e1",
        "CYLINDER [5 x 5 x 01]": "000000da",
        "CYLINDER [5 x 5 x 05]": "000000ec",
        "CYLINDER [5 x 5 x 1]": "000000eb",
        "CYLINDER [5 x 5 x 2]": "000000ea",
        "CYLINDER [5 x 5 x 4]": "000000e9",
        "CYLINDER [10 x 10 x 01]": "000000e8",
        "CYLINDER [10 x 10 x 05]": "000000e7",
        "CYLINDER [10 x 10 x 1]": "000000e6",
        "CYLINDER [10 x 10 x 2]": "000000e5",
        "CYLINDER [10 x 10 x 4]": "000000e4",
        "CYLINDER (HALF) [05 x 01 x 1]": "000000ef",
        "CYLINDER (HALF) [05 x 01 x 2]": "000000ee",
        "CYLINDER (HALF) [05 x 01 x 3]": "000000f0",
        "CYLINDER (HALF) [05 x 1 x 1]": "00000104",
        "CYLINDER (HALF) [05 x 1 x 2]": "00000101",
        "CYLINDER (HALF) [05 x 1 x 3]": "000000fe",
        "CYLINDER (HALF) [05 x 3 x 1]": "000000f9",
        "CYLINDER (HALF) [05 x 3 x 2]": "00000102",
        "CYLINDER (HALF) [05 x 3 x 3]": "000000ff",
        "CYLINDER (HALF) [05 x 4 x 1]": "000000fa",
        "CYLINDER (HALF) [05 x 4 x 2]": "00000103",
        "CYLINDER (HALF) [05 x 4 x 3]": "00000100",
        "CYLINDER (HALF) [05 x 10 x 1]": "000000fb",
        "CYLINDER (HALF) [05 x 10 x 2]": "000000fc",
        "CYLINDER (HALF) [05 x 10 x 3]": "000000fd",
        "HEMISPHERE [2 x 2 x 01]": "000000b9",
        "HEMISPHERE [2 x 2 x 05]": "000000b8",
        "HEMISPHERE [2 x 2 x 1]": "000000cf",
        "HEMISPHERE [5 x 5 x 025]": "000000bf",
        "HEMISPHERE [5 x 5 x 1]": "000000be",
        "HEMISPHERE [5 x 5 x 2]": "000000bd",
        "HEMISPHERE [10 x 10 x 05]": "000000c5",
        "HEMISPHERE [10 x 10 x 2]": "000000c4",
        "HEMISPHERE [10 x 10 x 5]": "000000c3",
        "HEMISPHERE [20 x 20 x 1]": "000000cb",
        "HEMISPHERE [20 x 20 x 5]": "000000ca",
        "HEMISPHERE [20 x 20 x 10]": "000000c9",
        "HEMISPHERE [1 x 2 x 01]": "000000ba",
        "HEMISPHERE [1 x 2 x 05]": "000000bb",
        "HEMISPHERE [1 x 2 x 1]": "000000bc",
        "HEMISPHERE [2 x 5 x 025]": "000000c0",
        "HEMISPHERE [2 x 5 x 1]": "000000c1",
        "HEMISPHERE [2 x 5 x 2]": "000000c2",
        "HEMISPHERE [5 x 10 x 1]": "000000c6",
        "HEMISPHERE [5 x 10 x 2]": "000000c7",
        "HEMISPHERE [5 x 10 x 5]": "000000c8",
        "HEMISPHERE [10 x 20 x 1]": "000000cc",
        "HEMISPHERE [10 x 20 x 5]": "000000cd",
        "HEMISPHERE [10 x 20 x 10]": "000000ce",
        "BARREL": "00002eb5",
        "BARREL, SMALL": "00002eb6",
        "DRUM, 12 GAL": "000034c1",
        "DRUM, 55 GAL": "00004df8",
        "BUSH, A": "00004F04",
        "BUSH, B": "00004F09",
        "BUSH, SMALL": "00004EF5",
        "ICICLE, 10 INCH": "00003A14",
        "ICICLE, 18 INCH": "00003A15",
        "ICICLE, 24 INCH": "00004B4E",
        "ICICLE, 6 INCH": "000041E9",
        "PALM BUSH, LARGE": "0000522A",
        "PALM BUSH, MEDIUM": "0000521A",
        "PALM TREE, SMALL": "00005225",
        "PINE TREE": "000034C3",
        "PINE TREE, LARGE": "000034c5" ,
        "AWNING": "000051EA",
        "BARRICADE": "000034aa",
        "BARRICADE, SMALL": "00003fd4",
        "BARRIER": "000047f2",
        "BARRIER, SHORT": "0000481a",
        "BATTLE SHIELD": "00005210",
        "DUMPSTER": "00004225",
        "ROADBLOCK": "00002eb8",
        "ROADBLOCK, LIGHT": "00005A83",
        "SANDBAGS": "000050f3",
        "SANDBAGS, 45° CORNER": "00004d4f",
        "SANDBAGS, 90° CORNER": "000050e9",
        "SANDBAGS, ENDCAP": "000050ee",
        "SANDBAGS, TURRET": "00004d16",
        "SANDBAG, SINGLE": "000050fd",
        "SANDBAG, TWO": "000050f8",
        "AMMO CASE": "000047b1",
        "AMMO CRATE": "00003fd6",
        "AMMO CRATE, SMALL": "00003fd5",
        "CABINET": "00004224",
        "CONTAINER": "0000517a",
        "CONTAINER, OPEN": "00005189",
        "CRATE, INDUSTRIAL": "000027ef",
        "CRATE, MULTI": "0000444c",
        "CRATE, MULTI, DESTRUCTIBLE": "00004221",
        "CRATE, SINGLE": "00002eb3",
        "CRATE, SINGLE, LARGE": "00002eb4",
        "DOUBLE BOX, OPEN": "00004e10",
        "EQUIPMENT CASE": "00002ebc",
        "EQUIPMENT CASE, LID": "00004EF0",
        "EQUIPMENT CASE, OPEN": "00004EE3",
        "EQUIPMENT CASE, SMALL": "000034a6",
        "FENCE BOX": "00004def",
        "MEDICAL CRATE": "000034ab",
        "METAL CRATE": "00003fd3",
        "METAL CRATE, SMALL": "00004220",
        "SUPPLY CASE": "000034c0",
        "TRIP MINE (ARMED)": "00005A68",
        "PLASMA BATTERY": "00002eba",
        "FUSION COIL": "000034a4",
        "POWER CORE": "00002ebb",
        "PROPANE BURNER": "00004baa",
        "PROPANE TANK": "0000486d",
        "COMPUTER": "00005427",
        "COMPUTER, SMALL": "00005441",
        "FLOODLIGHTS": "000047bb",
        "FORKLIFT": "00004965",
        "GENERATOR": "000047cd",
        "GENERATOR, INDUSTRIAL": "0000493D",
        "GENERATOR, SMALL": "00002ebd",
        "INDUSTRIAL CART": "0000444a",
        "MONITOR, MEDIUM": "00004686",
        "MONITOR, SMALL": "0000469f",
        "RADIO SET": "00002eaf",
        "RADIO SET, SMALL": "000034a7",
        "SOCCER BALL": "00004e58",
        "WEAPON HOLDER": "00002ebe",
        "GRAV LIFT": "00002ebf",
        "LIFT, GOLD": "00005AD5",
        "MAN CANNON": "00004e46",
        "SHIELD DOOR": "00004e41",
        "SHIELD DOOR 2": "00003a94",
        "SHIELD DOOR, LARGE": "00004e2b",
        "SHIELD DOOR, GOLD": "00002ee5",
        "CHAIR": "00004934",
        "COMPUTER MONITOR": "00004918",
        "FILING CABINET": "00004923",
        "FILING CABINET, SMALL": "0000492F",
        "KEYBOARD": "0000490E",
        "KITCHEN SINK": "000046a4",
        "STAND": "000054D1",
        "TABLE": "00004608",
        "TELEPHONE": "0000546b",
        "TELEPHONE, WALL": "000048EF",
        "BACKPACK": "00002EB0",
        "BEACON": "000055E6",
        "BLITZ CAN": "000034c2",
        "BRIDGE": "00004e20",
        "CAMPING STOOL": "00002eb2",
        "CHAIN LINK GATE": "000054A2",
        "CROWBAR": "00005709",
        "DROP BRIDGE": "000051c7",
        "DROP POD, CLOSED": "000034a8",
        "DROP POD, DEPLOYED": "0000348E",
        "DROP POD, PANEL": "000034a9",
        "FLOOR HATCH": "00005495",
        "GARBAGE CAN": "0000518e",
        "LOCKER": "000047e5",
        "LOUDSPEAKER": "000046be",
        "MEDICAL CABINET": "0000541C",
        "MEDICAL CART": "0000544a",
        "MEDICAL TRAY": "00005460",
        "MISSILE, BODY": "00004849",
        "MISSILE, STACK": "00004662",
        "MISSILE, WARHEAD": "0000484e",
        "MONGOOSE PLATFORM": "00003493",
        "PALLET": "00004222",
        "PALLET, LARGE": "00002eb7",
        "PHANTOM DESTROYED, BACK, LARGE": "000055FB",
        "PHANTOM DESTROYED, BACK, MEDIUM": "00005600",
        "PHANTOM DESTROYED, BACK, SMALL": "00005605",
        "PHANTOM DESTROYED, BOTTOM": "0000560A",
        "PHANTOM DESTROYED, FLAT, RIGHT": "00005614",
        "PHANTOM DESTROYED, SIDE, LEFT": "0000561E",
        "PHANTOM DESTROYED, SIDE, RIGHT": "00005623",
        "RADIO ANTENNAE": "000034a5",
        "STREET CONE": "00002eb9",
        "SWINGING DOOR": "00004223",
        "SWINGING LAMP": "000051FD",
        "TOOLBOX": "00004865",
        "TOOLBOX, SMALL": "00004853",
        "TRASH CAN": "00004226",
        "WARTHOG PLATFORM": "00003492",
        "WARTHOG TIRE": "00002A76",
        "WEAPON SHELF": "000046ad",
        "WIRE SPOOL": "00004e08",
        "RESPAWN POINT": "00002e90" ,
        "BOMB PLANT POINT": "00002ec6",
        "BOMB SPAWN POINT": "00002ec5",
        "STARTING POINT": "00002e98",
        "RESPAWN AREA": "00002e99",
        "RESPAWN, FLAG HOME": "00002e95",
        "RESPAWN, FLAG AWAY": "00002e96",
        "FLAG RETURN POINT": "00002ec4",
        "FLAG SPAWN POINT": "00002ec3",
        "STARTING POINT": "00002e91",
        "RESPAWN AREA": "00002e93",
        "STARTING POINT": "00002ea7",
        "RESPAWN AREA": "00002ea8",
        "SAFE HAVEN": "00002EDC",
        "GO TO POINT": "00002ec7",
        "HILL MARKER": "00002ec8",
        "STARTING POINT": "00002e9a",
        "RESPAWN AREA": "00002e9b",
        "BALL SPAWN POINT": "00002ec9",
        "STARTING POINT": "00002e9d",
        "RESPAWN AREA": "00002ecc",
        "STARTING POINT": "00002e9c",
        "RESPAWN AREA": "00002e97",
        "TERRITORY MARKER": "00002eca",
        "STARTING POINT": "00002e92",
        "RESPAWN AREA": "00002e94",
        "GO TO POINT": "00002ecb",
        "STARTING POINT": "00002e9e",
        "RESPAWN AREA": "00002e9f",
        "BUBBLE SHIELD": "00001564",
        "DEPLOYABLE COVER": "00001569",
        "FLARE": "00001565",
        "GRAV LIFT": "00002ea9",
        "INVINCIBILITY": "00001a6c",
        "POWER DRAIN": "00001561",
        "RADAR JAMMER": "00001560",
        "REGENERATOR": "00001566",
        "TRIP MINE": "00001567",
        "CONCUSSIVE BLAST": "0000156b",
        "HOLOGRAM": "0000156e",
        "LIGHTNING STRIKE": "00001573",
        "REFLECTIVE SHIELD": "0000156f",
        "VEHICLE CAMO": "00001563",
        "VISION": "00001577",
        "FRAG GRENADE": "000001ac",
        "PLASMA GRENADE": "000001af",
        "FIREBOMB GRENADE": "000001b5",
        "SPIKE GRENADE": "000001b2",
        "ACTIVE CAMO": "00002eaa",
        "OVERSHIELDS": "00002eab",
        "CUSTOM POWERUP": "00002eac",
        "AMMO CRATE": "00001b8e",
        "AMMO CRATE, SMALL": "00001b8f",
        "ASSAULT RIFLE": "0000151e",
        "ASSAULT RIFLE, ACCURACY": "00001583",
        "ASSAULT RIFLE, DAMAGE": "00001581",
        "ASSAULT RIFLE, POWER": "00001584",
        "ASSAULT RIFLE, RATE OF FIRE": "00001582",
        "BATTLE RIFLE": "0000157c",
        "BATTLE RIFLE, ACCURACY": "000015bc",
        "BATTLE RIFLE, AMMO": "00001585",
        "BATTLE RIFLE, DAMAGE": "00001586",
        "BATTLE RIFLE, POWER": "00001587",
        "BATTLE RIFLE, RANGE": "000015bd",
        "BATTLE RIFLE, RATE OF FIRE": "000015bb",
        "SMG": "0000157d",
        "SMG, ACCURACY": "0000158d",
        "SMG, DAMAGE": "0000158e",
        "SMG, POWER": "0000158f",
        "SMG, RATE OF FIRE": "0000158c",
        "DMR": "00001580",
        "DMR, ACCURACY": "00001588",
        "DMR, AMMO": "000015be",
        "DMR, DAMAGE": "0000158a",
        "DMR, POWER": "0000158b",
        "DMR, RATE OF FIRE": "00001589",
        "COVENANT CARBINE": "000014fe",
        "COVENANT CARBINE, ACCURACY": "000015c4",
        "COVENANT CARBINE, AMMO": "000015c1",
        "COVENANT CARBINE, DAMAGE": "000015c3",
        "COVENANT CARBINE, POWER": "00001591",
        "COVENANT CARBINE, RANGE": "000015c2",
        "COVENANT CARBINE, RATE OF FIRE": "000015c0",
        "MAULER": "00001504",
        "MAULER, POWER": "00001592",
        "MAGNUM": "0000157e",
        "MAGNUM, DAMAGE": "00001593",
        "MAGNUM, POWER": "00001594",
        "PLASMA PISTOL": "000014f7",
        "PLASMA PISTOL, POWER": "00001595",
        "MACHINE GUN TURRET": "0000284c",
        "MACHINE GUN TURRET, DETACHED": "000015b5",
        "PLASMA CANNON": "000014fb",
        "PLASMA CANNON, DETACHED": "0000150e",
        "MISSILE POD": "00003a18",
        "MISSILE POD, DETACHED": "00001a54",
        "BEAM RIFLE": "00001509",
        "BRUTE SHOT": "000014ff",
        "ENERGY SWORD": "0000159e",
        "FLAMETHROWER": "00001a55",
        "FUEL ROD GUN": "000014f9",
        "GRAVITY HAMMER": "0000150c",
        "NEEDLER": "000014f8",
        "PLASMA RIFLE": "00001525",
        "PLASMA RIFLE, POWER": "00001590",
        "ROCKET LAUNCHER": "000015b3",
        "SENTINEL BEAM": "00001a56",
        "SHOTGUN": "00001a45",
        "SNIPER RIFLE": "000015b1",
        "SPARTAN LASER": "000015b2",
        "SPIKER": "00001500",
        "BANSHEE": "0000151a",
        "CHOPPER": "00001518",
        "ELEPHANT": "00005A69",
        "GHOST": "00001517",
        "HORNET": "00001598",
        "HORNET, LITE": "0000159b",
        "MONGOOSE": "00001596",
        "PROWLER": "00005380",
        "SCORPION": "00001520",
        "SHADE TURRET": "00001516",
        "WARTHOG": "0000151f",
        "WARTHOG, GAUSS": "00004441",
        "WARTHOG, TROOP": "00004442",
        "WARTHOG, CIVILIAN": "00004443",
        "WARTHOG, DISABLED": "00004447",
        "WARTHOG, SNOW": "00001599",
        "WARTHOG, SNOW, GAUSS": "00004444",
        "WARTHOG, SNOW, TROOP": "00004445",
        "WARTHOG, SNOW, CIVILIAN": "00004446",
        "WARTHOG, SNOW, DISABLED": "00004448",
        "WRAITH": "00001519",
        "WRAITH, ANTI-AIR": "00004449",
        "TWO-WAY": "00002ec2",
        "RECEIVER": "00002ec1",
        "SENDER": "00002ec0",
        "SENDER, VEHICLE ONLY": "00004451",
        "RECEIVER, VEHICLE ONLY": "00004452",
        "TWO-WAY, VEHICLE ONLY": "00004453",
        "SENDER, VEHICLE": "0000444e",
        "RECEIVER, VEHICLE": "0000444f",
        "TWO-WAY, VEHICLE": "00004450",
    }
    print("running write_some_data...")
    #Get List of all objects in scene
    objectsList = list(bpy.data.objects)

    f = open(filepath, 'wb')
    objectsList1 = [x for x in objectsList if x.name in tagDict]
    objectsList2 = [x for x in objectsList if x.name[:x.name.rfind('.')] in tagDict]
    objectsList = objectsList1 + objectsList2
    #start obtain variables for header to write to file. 
    #magic, flags, version, date
    magic = bytearray([0x62, 0x66, 0x72, 0x70, 0x00, 0x00, 0x00, 0x00, 0xBE, 0x05, 0x57, 0x5F, 0x00, 0x00, 0x00, 0x00])
    f.write(magic)

    #Take prefab name and convert to binary and write to file.
    prefabname = bytes(Path(filepath).stem, 'utf-8') 
    buff = struct.pack("16s", prefabname)
    f.write(buff)

    #Take username and convert to binary and write to file.
    username = bytes(use_some_setting, 'utf-8')
    buff = struct.pack("16s", username)
    f.write(buff)

    #get number of objects in the scene and write to prefab
    buff = struct.pack('I',len(objectsList))
    f.write(buff)

    #padding between the headder and the objects
    padding = bytearray([0x00, 0x00, 0x00, 0x00])
    f.write(padding)
    
    #properties of object. Left default, so user can change in game.
    properties = bytearray([0xFF, 0x03, 0x0C, 0x08, 0x00, 0x1E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    for object in objectsList:
        if str(object.name) != 'Camera':

            #obtain filler and tag info
            flags = bytearray([0x00, 0x00, 0x00, 0x00])
            tagIndex= bytearray()
            if object.name.rfind('.') != -1:
                tagIndex = bytearray.fromhex(tagDict[object.name[:object.name.rfind('.')]])
            else:
                tagIndex = bytearray.fromhex(tagDict[object.name])
            
            tagIndex.reverse()
            


            rightVector = mathutils.Vector([1,0,0])
            upVector = mathutils.Vector([0,0,1])
            rightVector.rotate(object.rotation_euler)
            rightVector.normalize()
            upVector.rotate(object.rotation_euler)
            upVector.normalize()


            f.write(flags)
            f.write(tagIndex)
            data = [object.location.x,object.location.y, object.location.z]
            buf = struct.pack('%sf' % len(data), *data)
            f.write(buf)
            data = [rightVector.x,rightVector.y,rightVector.z,upVector.x,upVector.y,upVector.z]
            buf = struct.pack('%sf' % len(data), *data)
            f.write(buf)
            f.write(properties)
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """Export an Eldewrito prefab file"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".prefab"

    filter_glob = StringProperty(
            default="*.prefab",
            options={'HIDDEN'},
            maxlen=15,  # Max length of a prefab name to not crash dewrito
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = StringProperty(
            name="Author Name",
            description="Creator of the prefab",
            default="",
            maxlen=15,
            )

    

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Eldewrito Prefab (.prefab)")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)



def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')