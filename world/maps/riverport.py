from evennia.contrib.grid.xyzgrid import xymap_legend

# Roads
class Intersection(xymap_legend.MapNode):
    display_symbol = "#"
    prototype = {
            "prototype_parent": "riverport_xyz_room",
            "key": "An intersection",
            "desc": "An intersection of Riverport roads."
        }

class RoadNode(xymap_legend.MapNode):
    display_symbol = "#"
    prototype = {
            "prototype_parent": "riverport_xyz_room",
            "key": "A road",
            "desc": "A road through Riverport."
        }

class FountainNode(xymap_legend.MapNode):
    display_symbol = "|b⇈|n"

class GateNode(xymap_legend.MapNode):
    # Note: these nodes will need to be manually connected to the overworld
    display_symbol = "#"
    prototype = {
            "prototype_parent": "riverport_xyz_room",
            "key": "A gate",
            "desc": "A gateway set into the walls of Riverport.",
            "tags": [('area_exit', 'area_def')],
        }

class HouseNode(xymap_legend.MapNode):
    display_symbol = "|C∆|n"
    prototype = {
            "prototype_parent": "riverport_xyz_room",
            "key": "Inside",
            "desc": "A building inside Riverport."
        }

class ChiefHouseNode(HouseNode):
    display_symbol = "|g♔|n"

class TavernNode(xymap_legend.MapNode):
    display_symbol = "|c♫|n"
    prototype = {
        "prototype_parent": "riverport_xyz_room"
    }

class BankNode(xymap_legend.MapNode):
    display_symbol = "|y$|n"
    prototype = {
        "prototype_parent": "riverport_xyz_room"
    }

class FarmStoreNode(xymap_legend.MapNode):
    display_symbol = "|g⚶|n"
    prototype = {
        "prototype_parent": "riverport_xyz_room"
    }

class FoodStoreNode(xymap_legend.MapNode):
    display_symbol = "|g♨|n"
    prototype = {
        "prototype_parent": "riverport_xyz_room"
    }

class ItemStoreNode(xymap_legend.MapNode):
    display_symbol = "|r⚔|n"
    prototype = {
        "prototype_parent": "riverport_xyz_room"
    }

class MagicStoreNode(xymap_legend.MapNode):
    display_symbol = "|r🜛|n"
    prototype = {
        "prototype_parent": "riverport_xyz_room"
    }

class BridgeNode(xymap_legend.MapNode):
    display_symbol = "Ξ"
    prototype = {
            "prototype_parent": "riverport_xyz_room",
            "key": "A bridge",
            "desc": "A bridge over the river."
        }

class BridgeLink(xymap_legend.MapLink):
    symbol = "Ξ"
    display_symbol = "Ξ"
    directions = { 'e': 'w', 'w': 'e' }
    prototype = {
            "prototype_parent": "xyz_exit",
        }


LEGEND = {
    'B': BridgeNode,
    'Ξ': BridgeLink,
    'X': Intersection,
    'R': RoadNode,
    "⇈": FountainNode,
    'G': GateNode,
    'H': HouseNode,
    "♔": ChiefHouseNode,
    "♫": TavernNode,
    "$": BankNode,
    "⚶": FarmStoreNode,
    "♨": FoodStoreNode,
    "⚔": ItemStoreNode,
    "🜛": MagicStoreNode,
}

PROTOTYPES = {
    # (5, 8): {},
    # (7, 4): {},
    (8, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "West Market Square",
        "desc": """
The western edge of Riverport's |CMarket Square|n feels a world away from the bustling, earthy chaos closer to the fountain. Here, the stalls are less ramshackle and more refined, draped with colorful silks and displaying goods aimed at those with a bit more coin in their purses. The air is perfumed with exotic scents – incense, fine perfumes, and the sweet aroma of imported fruits.

The cobblestones here are cleaner, swept regularly by vendors eager to impress discerning customers. Stalls boast polished wooden counters instead of simple blankets, and many feature small awnings offering shade from the sun or protection from light rain.

The clientele here is different too. You’ll see merchants in fine robes, wealthy landowners, visiting nobles, and adventurers who've struck it rich – all browsing the stalls with a discerning eye. The bargaining is less frantic, more polite, and often accompanied by a glass of wine or a sweetcake.

Musicians playing softer melodies – lutes and flutes rather than drums and fiddles – provide a more refined backdrop to the shopping experience. The western end of the |CMarket Square|n isn’t just about buying goods; it's about displaying status, indulging in luxuries, and enjoying the finer things in life. It’s Riverport’s little slice of elegance amidst the everyday bustle.
"""
    },
    (8, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CThe Starspire|n"
    },
    (8, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CMarket Square|n"
    },
    (8, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CSunstone and (west road name)|n"
    },
    (8, 7): {
        "prototype_parent": "riverport_xyz_room",
        "key": "The Starspire",
        "aliases": ["wizard tower", "magic"],
        "desc": """
Rising above the western edge of the |CMarket Square|n, and seemingly defying gravity with its slender form, stands |CThe Starspire|n. It isn’t a grand, imposing structure like a castle keep; rather, it feels organically grown, as if sprung from the earth itself. Constructed primarily of dark grey stone interwoven with living vines and glowing moss, the tower spirals upwards in a series of increasingly narrow tiers.

The base is broad and sturdy, blending seamlessly with the surrounding buildings, but as you ascend, the tower becomes more whimsical – windows are oddly shaped, balconies jut out at unexpected angles, and small gargoyles perch on every ledge, their stone eyes seeming to follow your movements. A spiral staircase winds its way around the outside of the tower, accessible via a sturdy wooden door adorned with arcane symbols.

The air around the tower hums with subtle magical energy – you can almost feel it tingling on your skin. Strange plants grow in abundance, some blooming with flowers that shift colors, others emitting a soft, ethereal glow. The scent is a blend of ozone, herbs, and something faintly metallic.

Inside, the tower is crammed with books, scrolls, alchemical apparatuses, and curious artifacts collected from across the land. Each tier serves a different purpose: a library filled with ancient tomes, a laboratory for brewing potions and crafting |Yrunestones|n, an observatory for charting the stars, and a cozy sitting room where |GElmsworth|n often receives visitors.

The walls are covered in intricate murals depicting scenes of magical battles, celestial events, and strange creatures from other realms. Light filters through stained-glass windows, casting colorful patterns across the stone floors.

|GElmsworth|n’s specialty is |YRunestones|n – large, polished stones etched with arcane symbols that allow even those without formal magical training to cast spells. He sells them in a variety of colors, each corresponding to a different element or effect: red for |rfire|n, blue for |bwater|n, green for |gearth|n, and so on.

|CThe Starspire|n isn't just a shop; it’s a repository of knowledge, a haven for magic, and a testament to |GElmsworth|n’s eccentric genius. It feels like stepping into another world – one where anything is possible with the right runestone in hand.
"""
    },
    (8, 7, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CWest Market Square|n"
    },
    (10, 5): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Riverport Bank",
        "desc": """
The |CRiverport Bank|n stands as a symbol of stability and wealth in a town often bustling with transient sailors and fortune-seekers. Unlike many buildings in Riverport constructed from salvaged wood, the bank is built entirely of grey stone, quarried from the hills north of town, giving it an air of permanence and solidity. It’s a two-story structure, imposing but not ostentatious, with thick walls and narrow windows reinforced with iron bars – security is paramount.

The front entrance features a pair of heavy oak doors, flanked by carved stone pillars depicting river serpents coiled around stacks of coins. Above the door, a simple gold sign proclaims: “|CRiverport Bank|n - Secure Your Fortune.”

Inside, the bank is surprisingly cool and quiet, a welcome respite from the bustling |CMarket Square|n just outside. The main hall is spacious, with polished stone floors and high ceilings supported by sturdy columns. Several teller windows line one wall, manned by clerks in neat uniforms who meticulously record transactions in large ledgers.

Private counting rooms offer more discreet service for larger deposits or withdrawals. These rooms are furnished with comfortable chairs, heavy wooden desks, and strongboxes to safeguard valuables. The air smells faintly of ink, parchment, and the reassuring scent of gold.

The bank offers a variety of services: safe deposit boxes for storing valuables, loans for merchants and adventurers, currency exchange for travelers from distant lands, and even letters of credit for those conducting business further afield.

Guards – typically burly mercenaries hired by the bank – patrol the hall, keeping a watchful eye on customers and ensuring no sticky fingers attempt to relieve them of their wealth. The |CRiverport Bank|n isn’t just a place to store gold; it's a cornerstone of the town’s economy, representing trust, security, and the promise of future prosperity. It’s where Riverport’s fortunes are carefully counted, guarded, and invested – ensuring the town continues to thrive on the banks of the Southrun River.
"""
    },
    (10, 5, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CMarket Square|n"
    },
    (10, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Market Square",
        "aliases": ["market", "square"],
        "desc": """
Riverport’s |CMarket Square|n isn't so much a |isquare|I as a bustling, organic sprawl that has grown around |CThe Heartstone Fountain|n like barnacles on a hull. It’s a patch of packed earth and cobblestones constantly shifting with activity – a vibrant chaos contained by the surrounding buildings. The air hums with the calls of vendors hawking their wares, the chatter of shoppers bargaining for prices, and the occasional bleating of livestock penned near the edges.

Stalls are constructed from whatever materials merchants can find: brightly colored awnings stretched over wooden frames, rough-hewn tables laden with goods, even simple blankets spread on the ground. The scent is a heady mix of everything imaginable – fresh fish, ripe fruit, fragrant spices, tanned leather, and the earthy aroma of vegetables pulled straight from the fields.

On any given day, you might find anything here: bolts of silk imported from the Eastern Kingdoms, sturdy tools forged by Riverport’s blacksmith, baskets overflowing with plump berries, cages filled with squawking chickens, gleaming silverware, exotic spices, and even the occasional travelling peddler selling curiosities from distant lands.

The square isn't particularly clean. Mud splatters are common, especially after a rain, and discarded vegetable leaves and fish scales litter the ground. But it’s rarely quiet. Musicians often set up near the center of the square, adding to the lively atmosphere with their fiddles and drums. Children weave through the crowds, chasing stray dogs or begging for sweetcakes.

To the north, the sturdy facade of |CTiber's General Goods|n store anchors that side of the square, while to the south, the more imposing stone building of the |CRiverport Bank|n exudes an air of solid wealth. But the heart of |CThe Market Square|n is its energy – a constant flow of people and goods, making it the true lifeblood of Riverport. It’s where deals are struck, gossip is exchanged, and fortunes are made (and lost) with every sunrise.
"""
    },
    (10, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CTiber's General Goods|n"
    },
    (10, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CHeartstone Fountain|n"
    },
    (10, 6, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CRiverport Bank|n"
    },
    (10, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CWest Market Square|n"
    },
    (10, 7): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Tiber's General Goods",
        "aliases": ["item shop"],
        "desc": """
|CTiber’s General Goods|n isn’s your grandmother’s pantry. While it |idoes|I stock the basics – rope, candles, cooking pots – its true focus lies squarely on equipping those brave (or foolish) enough to venture into the darkness beneath the land. The building itself is a solid two-story structure of dark wood and stone, smelling strongly of oiled leather, polished steel, and something faintly metallic.

The front window isn't filled with pretty displays; instead, it showcases a rotating selection of weaponry – a gleaming longsword, a sturdy battleaxe, or perhaps a wicked-looking curved scimitar – all hinting at the treasures within. A sign above the door proclaims in bold lettering: “|GTiber|n’s - For When ‘Just Surviving’ Isn't Enough.”

Inside, the store is surprisingly spacious, though crammed to bursting with goods. Shelves line every wall, reaching almost to the high ceiling, and are stacked with everything an adventurer could need. Rows of backpacks hang from hooks, alongside cloaks woven with protective runes, and sturdy boots reinforced with iron.

The air thrums with a subtle energy – perhaps from the enchanted items Tiber stocks, or simply from the anticipation of countless expeditions begun within its walls. You can find:

|uWeapons & Armor:|U Swords, axes, daggers, maces, bows, arrows, shields - in varying qualities and price ranges. Leather armor, chainmail, even a few pieces of plate for those with deeper pockets.
|uPotions & Scrolls:|U Healing potions, mana potions, stamina potions, scrolls of protection, scrolls of illumination – |GTiber|n has a potion for almost every ailment and a scroll for most magical needs.
|uRations & Supplies:|U Dried meats, hardtack biscuits, travel rations, waterskins, flint and steel, rope, pitons, torches, oil lamps - everything to keep you fed and lit while exploring.
|uOddities & Trinkets:|U Lucky charms, magnifying glasses, lockpicks, grappling hooks, vials of glowing moss, maps (some accurate, some less so) – |GTiber|n has a knack for finding the unusual.

|GTiber|n himself is a stout man with a perpetually grease-stained apron and a shrewd glint in his eye. He’s seen countless adventurers come and go, and can size up a customer with a single glance, knowing exactly how much they're willing to spend. He isn’t overly friendly, but he knows his wares and offers practical advice – often laced with a healthy dose of cynicism.

|GTiber|n’s is more than just a store; it’s a staging ground for adventure. It’s where heroes prepare to face their fears, and where survivors return to replenish their supplies – and perhaps boast about their triumphs (or lament their failures).
"""
    },
    (10, 7, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CMarket Square|n"
    },
    (12, 5): {
        "prototype_parent": "riverport_xyz_room",
        "key": "The Heartstone Tankard",
        "aliases": ["tavern"],
        "desc": """
The scent of woodsmoke, stale ale, and something vaguely fishy hangs thick as a morning mist around |CThe Heartstone Tankard|n. It’s not |iunpleasant|I, exactly, just… Riverport. Built practically into the bank of the Southrun River, the tavern leans slightly towards the water like a weary traveller seeking rest. Its timbers are dark with age and splashed with river spray, patched in places with mismatched planks salvaged from shipwrecks – you can almost smell the salt clinging to them even now.

|CThe Tankard|n takes its name from the grand |CHeartstone Fountain|n just a stone’s throw north, which is said to bring luck to the town. |GTorvin Stonehand|n, the tavern keeper, claims his tankards are blessed by proximity, though whether that blessing translates to fewer hangovers is debatable.

The building isn’t grand. It's long and low, with a thatched roof perpetually shedding bits of straw. A wide, welcoming doorway – often propped open in warmer months – leads into the main common room. Inside, it’s dimly lit by oil lamps swinging from rough-hewn rafters and the glow of the hearth that dominates one end of the room. The floor is packed earth, worn smooth by countless boots and liberally sprinkled with sawdust to soak up spills.

Tables are a motley collection – sturdy oak for the regulars, wobbly pine for newcomers, and a few scarred remnants of ships’ galleys. Benches, equally mismatched, line the walls alongside a scattering of well-worn chairs. Above the hearth hangs a particularly impressive boar's head, its glassy eyes seeming to follow your every move.

The bar itself is a long, polished slab of darkwood, worn smooth by years of elbows and tankards. Behind it, |GTorvin|n presides like a benevolent (if slightly grumpy) bear. He’s a man built like an oak tree, with hands calloused from hauling barrels and a beard that rivals the riverweed in length. His wife, |GBess|n, a woman whose smile could melt stone, handles most of the cooking – hearty stews, roasted fish fresh from the Southrun, and surprisingly good bread are her specialties.

|CThe Heartstone Tankard|n isn’t fancy. It doesn't boast silks or silver. But it |iis|I at Riverport’s heart. Fishermen swap tales of monstrous catches, merchants haggle over prices, riverboat captains boast of their voyages, and weary travellers find a warm fire and a strong drink. You can hear whispers of trade routes, rumours of bandits in the Blackwood Forest, and even the occasional snippet of courtly intrigue carried on the breeze from the capital.

It’s a place where fortunes are won and lost, secrets are traded, and friendships are forged – all over a pint of |GTorvin|n's best ale. Just be careful who you share your stories with; in Riverport, everyone has an ear to the ground, and nothing stays quiet for long.
""",
    },
    (12, 5, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": "To |CHeartstone Fountain|n"
    },
    (12, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Heartstone Fountain",
        "desc": """
The heart of Riverport isn't its bustling docks, nor its crowded |CMarket Square|n, but |CThe Heartstone Fountain|n. It stands not on paving stones, but a small rise of smoothed river-cobbles, as if the earth itself offered it up. |GOld Man Hemlock|n, who claims to remember when Riverport was just a scattering of fishing huts, says the rise |iis|I an ancient burial mound, and the fountain built upon the spirit of the river's first guardian. Whether that’s true or not, the fountain feels… old. Older than the stone walls of the keep, older even than the oldest oak in Whisperwood.

The basin itself is carved from a single block of grey-veined granite, so large it took twenty oxen to drag it from the Quarry of Silent Kings. It’s shaped like a blooming water lily, each petal subtly different, worn smooth by centuries of hands dipping for blessings and cool relief. But it's not the stone that truly captures the eye; it's what sits within.

At the fountain’s center rises the Heartstone itself – a sphere of polished obsidian, roughly the size of a man’s head. It doesn’t |ilook|I like obsidian, though. Within its depths swirl constellations of silver light, constantly shifting and reforming. Some say they mirror the night sky above, others claim they show glimpses of fortunes yet to come.

From the Heartstone springs the water. Not in a single jet, but in dozens of delicate streams that arc upwards, catching the sunlight and scattering it into rainbows. The water isn’t merely clear; it has a subtle luminescence, a pearly sheen that makes it seem almost alive. It tastes faintly of mint and river-stone, cool even on the hottest summer day.

Around the base of the lily bloom are carvings of Riverport's history: fishermen hauling nets brimming with silverfish, merchants bartering for spices from distant lands, knights defending the town against goblin raids. Each carving is worn, softened by time and weather, but still vibrant enough to tell its tale.

The fountain isn’t just a source of water; it’s Riverport's gathering place. Lovers whisper promises beside it, merchants haggle over prices within earshot, children splash and play in the spray. Old women come to draw water for healing potions, believing the Heartstone imbues it with restorative power. And on festival days, the fountain is draped with garlands of wildflowers and lit by a hundred flickering lanterns, its silver light seeming to dance with the joy of the town.

It’s said that if you toss a silver coin into |CThe Heartstone Fountain|n and make a wish for Riverport's good fortune, your wish will be granted – but only if it truly benefits the town as a whole. Selfish wishes tend to sink straight to the bottom, lost amongst the other offerings.
""",
    },
    (12, 6, 'n') : {
        "prototype_parent": "xyz_exit",
        "desc": "To |CHemlock Manor|n"
    },
    (12, 6, 'e') : {
        "prototype_parent": "xyz_exit",
        "desc": "To |CMid Sunstone Way|n"
    },
    (12, 7): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Hemlock Manor",
        "desc": """
|GOld Man Hemlock|n’s house stands as a testament to both longevity and practicality. It's situated just north of |CThe Heartstone Fountain|n, nestled amongst a small cluster of ancient willow trees whose branches weep towards the obsidian stone. Unlike many Riverport dwellings built quickly from whatever was at hand, |GHemlock|n’s home feels |igrown|I from the land itself.

The house is two stories tall, constructed primarily of river stone – smooth, grey stones hauled up from the Southrun over decades. Thick walls give it a solid, enduring quality, as if it could withstand any storm. Ivy climbs liberally across the stonework, softening its edges and blending it with the surrounding greenery. The roof is steeply pitched, covered in moss-covered shingles that have weathered to a silvery grey.

A winding path, paved with flat stones worn smooth by countless footsteps, leads up to the front door – a heavy oak affair reinforced with iron bands. Above the door hangs a carved wooden sign depicting a wise old owl perched on a branch, |GHemlock|n’s personal emblem.

The windows are small and numerous, set deep within the stone walls, giving the house a slightly watchful appearance. They're often filled with the warm glow of oil lamps or the flickering light of candles, even during daylight hours – |GHemlock|n prefers a cozy atmosphere. Each window sill is crowded with potted herbs: rosemary, thyme, lavender, and others whose scents mingle in the air around the house.

A small garden surrounds the home, bursting with medicinal plants and vegetables. |GHemlock|n has a knack for coaxing life from the soil, even in Riverport’s often damp climate. A weathered wooden bench sits beneath one of the willow trees, offering a perfect spot to observe the fountain and watch the comings and goings of the village.

Inside, the house is cluttered but comfortable. Bookshelves line every wall, overflowing with scrolls, tomes, and handwritten journals detailing Riverport’s history and |GHemlock|n's own observations. The air smells faintly of dried herbs, woodsmoke, and old parchment. It isn’t a grand house, but it radiates warmth, wisdom, and the quiet dignity of a life well-lived. It feels like a place where stories are born, and secrets are kept safe.
""",
    },
    (14, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Mid Sunstone Way",
        "desc": """
Just east of |CHeartstone Fountain|n, |CSunstone Way|n begins as a wide, well-maintained thoroughfare paved with large flagstones. It’s noticeably cleaner than the |CMarket Square|n, regularly swept by townspeople and merchants heading towards the eastern districts. The road is flanked on either side by sturdy wooden fences separating it from small gardens and modest homes – dwellings belonging to artisans and shopkeepers who benefit from the foot traffic flowing through Riverport.

The air here smells less of fish and spices, and more of woodsmoke from cooking fires and blooming honeysuckle climbing over garden walls. Sunlight streams down |CSunstone Way|n, giving it a brighter, warmer feel than the often-shadowed |CMarket Square|n.

Small stalls begin to appear along the road, though they’re less numerous and more specialized than those in the square. You might find a baker selling fresh bread, a cobbler repairing shoes, or a weaver displaying her colorful tapestries.

The buildings are generally two stories tall, constructed from wood and stone, with tiled roofs and small balconies overlooking the street. Many feature brightly painted shutters and flower boxes overflowing with blooms.

Just a short distance east of the fountain, |CSunstone Way|n splits into two smaller roads – one leading towards the docks along the Southrun River, and the other winding upwards towards the residential district perched on the hillside. But for now, right at the fountain’s edge, it's a lively but orderly street, bustling with activity as people go about their daily lives – a clear transition from the vibrant chaos of the |CMarket Square|n to the more settled rhythm of Riverport’s eastern districts.
"""
    },
    # (16, 2): {},
    (16, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Southrun Bridge",
        "desc": """
|CThe Southrun Bridge|n, just before |CSunstone Way|n splits northward, is Riverport's primary link to the eastern side of town and a vital artery for trade. It’s a sturdy structure built from grey stone, spanning the width of the Southrun River with three graceful arches. The stonework is weathered but well-maintained, showing signs of countless years enduring the river’s currents and the weight of passing traffic.

The bridge deck itself is wide enough to accommodate two wagons abreast, paved with cobblestones worn smooth by centuries of use. Low stone railings run along either side, offering a partial view of the Southrun River flowing beneath – often teeming with boats, barges, and even the occasional playful river serpent.

Small shrines dedicated to various water deities are built into the bridge’s arches, adorned with offerings of flowers, coins, and small trinkets left by grateful travelers and fishermen. Lanterns hang from iron brackets along the sides, illuminating the bridge at night and casting dancing reflections on the water below.

The air around the bridge is often filled with the sounds of river traffic – the creak of oars, the splash of paddles, the shouts of boatmen. The scent of fresh water mixes with the smells of woodsmoke and fish from nearby docks.

Guards are stationed at either end of the |CSouthrun Bridge|n, collecting tolls from merchants and travelers and keeping an eye out for trouble. It’s a busy, bustling place – a constant flow of people, goods, and animals moving between the two sides of Riverport. The bridge isn't just a way to cross the river; it’s a social hub, a meeting point, and a symbol of connection within the town.
"""
    },
    (16, 9): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Weaver's Run",
        "desc": """
The intersection where |CWeaver’s Run|n meets the small road leading down to |CBridge End|n isn’t a sharp corner; rather, it’s a gentle bend in both roads, creating a somewhat triangular space. The area feels much quieter and more peaceful than bustling |CBridge End|n – a welcome change for residents returning home.

|CWeaver's Run|n here is paved with flagstones, though they are often overgrown with moss and wildflowers. Houses line either side of the road, each with small gardens and picket fences. The architecture is generally simple but charming - two-story wooden homes with tiled roofs and brightly painted doors.

The intersection itself features a small stone well, providing fresh water for nearby residents. A baker’s shop occupies one corner, its windows filled with tempting loaves of bread and sweet pastries. Across from the bakery sits a small tailor's workshop, where you can often hear the rhythmic whir of a spinning wheel.

The road leading down to |CBridge End|n is steeper here, winding its way downwards towards the more commercial areas below. It’s frequently used by residents heading to market or visiting friends and family in town.

This intersection feels like the heart of the Hillside district – a place where neighbors gather, children play, and life moves at a slower pace. The air smells of baking bread, blooming flowers, and freshly laundered clothes. It’s a cozy, welcoming spot that embodies the charm and tranquility of Riverport's residential neighborhood.
"""
    },
    # (16, 10): {}, # temple
    # (18, 2): {},
    (18, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Bridge End",
        "desc": """
The crossroads just east of the |CSouthrun Bridge|n feels like a miniature hub of activity, a place where |CSunstone Way|n’s steady flow momentarily pauses and disperses. The junction isn't particularly grand – no ornate statues or impressive paving stones – but it’s well-worn and clearly defined.

|CSunstone Way|n continues eastward here, maintaining its wide cobblestone path, while the smaller road heading north is narrower and more winding, paved with a mix of flagstones and packed earth. A simple wooden signpost stands at the center of the crossroads, pointing the way: “To Hillside – Residential District” etched into the weathered wood.

The area around the junction is dominated by small shops catering to travelers and residents alike. A stable offering lodging for horses and mules, often accompanied by the scent of hay and manure, a fruit vendor who has set up a stall near the signpost, selling apples, pears, and other seasonal produce and a blacksmith’s that stands slightly further back, its forge sending plumes of smoke into the air and filling the area with the rhythmic clang of hammer on steel.

The crossroads is often crowded with people – travelers arriving from the east, residents heading up to the Hillside district, merchants unloading goods, and children playing amongst the bustle. It’s a lively, vibrant spot where different paths converge, creating a sense of energy and anticipation. You can feel the transition here - moving from the more commercial |CSunstone Way|n towards the quieter, more residential streets that climb upwards toward the hillside homes.

Locals refer to this crossroads as "|CBridge End|n." It's a simple, practical name reflecting its location – the point where |CSunstone Way|n meets the bridge and the road leading up to Hillside begins. While not officially designated on any town map, “Meet me at |CBridge End|n” is a common phrase amongst Riverport residents, understood by all. You’ll hear it used when arranging meetings, directing visitors, or simply describing where something happened. It’s become an informal but widely recognized landmark within the town.
"""
    },
    # (19, 4): {},
    # (22, 4): {},
    (23, 8): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Thorne's Table",
        "aliases": ["cook", "food"],
        "desc": """
|CThorne’s Table|n is as eccentric and charming as the cook herself, |GBriar Thorne|n. It isn’t grand or imposing – more like a cozy cottage expanded outwards over the years. The exterior is built from rough-hewn stone covered in climbing ivy, with smoke perpetually curling from its crooked chimney.

The windows are small and leaded glass, displaying an array of colorful jars filled with strange ingredients: shimmering mushrooms, dried dragon peppers, luminescent berries, and herbs that seem to glow faintly. A hand-painted sign above the door depicts a steaming pot surrounded by swirling magical energy.

Inside, |CThorne’s Table|n is warm and inviting, smelling of spices, roasted meats, and something subtly… magical. The main room is dominated by a large stone hearth where |GBriar|n does most of her cooking, constantly stirring pots and basting roasts with practiced ease.

Shelves line the walls, crammed with jars, bottles, and boxes containing all manner of ingredients. Dried herbs hang from the rafters, filling the air with their fragrant aroma. Tables are scattered throughout the room, covered in checkered cloths and set with mismatched pottery.

|GBriar|n herself is a stout woman with rosy cheeks and twinkling eyes, always wearing a stained apron and a mischievous grin. She’s known for her quick wit and her ability to assess a customer's needs with just a glance.

The menu isn’t written down; |GBriar|n simply asks what you need – strength, speed, clarity of mind – and crafts a meal accordingly. A simple stew might grant temporary endurance, while a spiced pie could sharpen your senses. It’s not cheap, but the benefits are well worth the price for adventurers, merchants, or anyone seeking an edge.
"""
    },
    (24, 6): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Sunstone and Border",
        "aliases": ["border road", "border"],
        "desc": """
The intersection of |CSunstone Way|n and |CBorder Road|n isn't a grand affair – it feels more like two roads simply running into each other than a carefully planned junction. The cobblestones of |CSunstone Way|n gradually give way to packed earth as it meets |CBorder Road|n, which is wider and straighter, designed for heavier traffic heading north and south.

A weathered wooden post stands at the intersection, bearing faded carvings indicating directions: “North to Hillside,” “South to Port.”

The area is less bustling than others, but still sees a fair amount of traffic – farmers bringing produce into town, merchants heading to neighboring villages, travelers venturing further afield. A small cart selling firewood sits on one corner, and a modest inn called “The Eastern Gate” offers respite for weary travelers.

|CBorder Road|n here feels more open, with fields stretching out on either side. The air smells of earth, hay, and livestock. You can see the beginnings of the surrounding countryside – rolling hills dotted with farms and forests in the distance.

A small stone shrine dedicated to the goddess of safe journeys stands slightly off to the north, where travelers often leave offerings before embarking on longer trips. The intersection is a point of transition - leaving Riverport’s relative safety behind and venturing into the wider world beyond its walls. It's a place of departures and arrivals, marking the edge between civilization and the wild.
"""
    },
    # (24, 7): {}
    (24, 8): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Weaver and Border",
        "desc": """
The section of |CBorder Road|n immediately before it intersects with |CWeaver’s Run|n feels distinctly more utilitarian than the charming residential stretch of |CWeaver’s Run|n itself. It’s a working part of Riverport, geared towards trade and transport rather than leisurely living.

|CBorder Road|n here is wide and relatively straight, well-worn by the constant passage of wagons, carts, and livestock heading to and from town. The road surface is mostly packed earth, though sections have been reinforced with larger stones where erosion is common.

On either side of |CBorder Road|n stand a collection of workshops and small businesses catering to farmers and travelers. A wheelwright’s shop stands prominently, the scent of wood shavings filling the air as he crafts new wheels for carts and wagons. Next door is a cart repair shop, often piled high with broken axles and splintered planks.

A stonecutter's yard occupies a larger space, showcasing finished gravestones and building materials alongside half-finished sculptures. The rhythmic chipping of hammers against stone provides a constant background noise.

Several small barns and storage sheds line the road, used by farmers to store hay, grain, and other produce before bringing it into town. You can often see chickens pecking around in the dirt or pigs rooting through piles of discarded vegetables.

The air here smells of woodsmoke, dust, and livestock – a more earthy aroma than the floral scents further west on |CWeaver’s Run|n. It's a practical, hardworking area - less picturesque but essential to Riverport’s economy. The feeling is one of constant activity, with workers bustling about their tasks and wagons constantly coming and going. This stretch of |CBorder Road|n isn’t about beauty; it’s about getting things done.

Just west of here is |CThorne's Table|n.
"""
    },
    (25, 7): {
        "prototype_parent": "riverport_xyz_room",
        "key": "Elara's Honeyfarm",
        "aliases": ["farm"],
        "desc": """
On |CBorder Road|n, just before it curves north from |CSunstone Way|n, lies |CElara’s Honeyfarm|n – though “farm” feels almost too grand a word for its charmingly haphazard layout. It's less a meticulously planned agricultural operation and more an extension of |GElara|n herself, sprawling organically across several acres.

The farm isn’t dominated by vast fields of crops, but rather by rows upon rows of brightly painted beehives – dozens of them, each adorned with whimsical designs: flowers, suns, even tiny portraits of |GElara|n's grumpy face. The air hums with the constant buzz of thousands of bees flitting between hives and nearby wildflower patches.

A rambling stone farmhouse sits at the center of it all, its walls covered in climbing roses and wisteria. A weathered wooden fence encloses a small vegetable garden bursting with herbs, tomatoes, and other produce used in |GElara|n’s honey-infused creations.

Scattered around the farm are various sheds and outbuildings – some neatly organized, others overflowing with beekeeping equipment, empty jars, and half-finished projects. Chickens peck freely amongst the hives, seemingly unbothered by their buzzing neighbors. A small orchard of apple trees provides pollen for the bees and fruit for |GElara|n’s honey cakes.

The farm feels lived-in and loved, a testament to |GElara|n's decades of dedication. It’s not the most efficient or modern operation, but it produces some of the sweetest, most flavorful honey in Riverport – often said to have subtle magical properties depending on which flowers the bees favored that season. The scent of honey hangs heavy in the air, mingling with the earthy aroma of wildflowers and damp soil. It's a peaceful, idyllic spot where time seems to slow down, and the simple pleasures of life are celebrated.
"""
    },
}

MAP_STR = """
                       1                   2                   3 
 + 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 

11                                                                                 
                                                                                    
10                                 H                                          
                                   |                                           
 9         o------------ΞBΞ--------R---------------o                        
           |                       |               |                          
 8         R-H                     o---o         ♨-R                     
           |                           |           |                      
 7         o---o   🜛   ⚔   ♔           |           R-⚶                
               |   |   |   |           |           |                 
 6         G---X---R---R---⇈---R--ΞBΞ--R-----------X    
               |       |   |   |                   |                 
 5             o---o   $   ♫   |             o-----R-H                  
                   |           o-o           |                         
 4               H-R             |       H   R-H                        
                   |             |       |   |                         
 3                 o-------------R--ΞBΞ--X---o                          
                                 |       |                               
 2                               | H   H |                              
                                 | |   | |                               
 1                               oΞBΞΞΞBΞo                              
                                                                                   
 0                                                                                

 + 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 
                       1                   2                   3 
"""

MAP_OPTIONS = {
    "map_visual_range": None, # None means display the whole map
    "map_align": "l",
    "map_separator_char": "|x~|n"
}

XYMAP_DATA = {
    "zcoord": "riverport",
    "map": MAP_STR,
    "legend": LEGEND,
    "prototypes": PROTOTYPES,
    "options": MAP_OPTIONS
}

