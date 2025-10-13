"""
Platers will start in Control Station 7.

All non-combat gameplay takes place here.

System prompt to generate details about it:

    !system You are a dystopian scifi writer who focuses on computers. Your current work is about
            Control Station 7, an outpost in the Forbidden Zone under constant threat by
            barbarians. Your world is made up of Humans, Robot LLMs, Furries, and Toxic Mutants,
            who all come here to make a name for themselves fighting off the barbarians.

"""

from evennia.contrib.grid.xyzgrid import xymap_legend

class Intersection(xymap_legend.MapNode):
    """ An intersection is a 4-way node. """
    display_symbol = "#"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "An intersection",
        "desc": "An intersection of Control Station 7 roads."
    }

class RoadNode(xymap_legend.MapNode):
    """ A road is a node with nothing really interesting in it. """
    display_symbol = "#"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "road",
        "desc": "A road through Control Station 7."
    }

class ConsumptionNode(xymap_legend.MapNode):
    """
    The Consumption Node is where new players spawn.

    It is a gathering place, of sorts.
    """
    display_symbol = "|c♨|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class BarNode(xymap_legend.MapNode):
    """
    A seedy bar.
    """
    display_symbol = "|g♫|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class BankNode(xymap_legend.MapNode):
    """ Player bank where they can store items they can't hold. """
    display_symbol = "|y$|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class HouseNode(xymap_legend.MapNode):
    """ A regular NPC house. """
    display_symbol = "|C∆|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Inside",
        "desc": "A building inside Control Station 7."
    }

class OverseerOfficeNode(HouseNode):
    """ The overseer hands out quests. """
    display_symbol = "|g♔|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class WeaponStoreNode(xymap_legend.MapNode):
    """ Store that sells physical weapons. """
    display_symbol = "|g⚔|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class HackingStoreNode(xymap_legend.MapNode):
    """ Store that sells software weapons. """
    display_symbol = "|g⚛|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class DrugStoreNode(xymap_legend.MapNode):
    """ Store that sells drugs. """
    display_symbol = "|g⚕|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class TempleNode(xymap_legend.MapNode):
    """ Temple / Museum. Shows dead characters and how they died. """
    display_symbol = "|c☥|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class LuxuryStoreNode(xymap_legend.MapNode):
    """
    Luxury goods store. Luxury goods are sold for real Monero and are tied to a user's account
        rather than the character.
    """
    display_symbol = "|y⚜|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class BridgeNode(xymap_legend.MapNode):
    """ Just like a road node but over the toxic sludge river. """
    display_symbol = "Ξ"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "A bridge",
        "desc": "A bridge over the river of toxic sludge."
    }

class BridgeLink(xymap_legend.MapLink):
    """ Link node but a bridge over the toxic sludge river. """
    symbol = "Ξ"
    display_symbol = "Ξ"
    directions = { 'e': 'w', 'w': 'e' }
    prototype = {
        "prototype_parent": "xyz_exit",
    }

PROTOTYPES = {
    (3, 6): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Western Reach",
        "desc": """
The Western Reach of The Exchange is distinct from its more central hubs – it’s less about everyday necessities and more focused on specialized goods, salvaged tech, and a touch of the illicit. It feels grittier, more crowded, and slightly more dangerous than other sections.

The Western Reach occupies a section of the Exchange built directly into an old loading dock – meaning it’s partially open to the elements, shielded by repurposed blast doors and energy screens. The floor is often slick with recycled oil and dust, and the lighting is dimmer, relying heavily on flickering neon signs and portable work lights.

The air here is thickest with the smell of burnt metal, ozone, and something vaguely organic – likely from salvaged bio-components. Noise levels are high, dominated by the clatter of repair tools, the haggling of traders, and the occasional hiss of a welding torch. It feels less organized than other parts of The Exchange, more like a sprawling junkyard with designated trading spaces.

The Western Reach of The Exchange is a haven for scavengers, tinkerers, and those seeking something beyond the standard ration credits can buy. It’s a grittier, more unpredictable section of the market, but also offers some of the most unique and valuable goods in Control Station 7. It feels less like a marketplace and more like a sprawling workshop where anything is possible – for the right price.
"""
    },
    (3, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A narrow corridor lined with stalls selling salvaged tech and bio-components, dimly lit and subtly shielded by energy screens.
"""
    },
    (3, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The market continues among repurposed loading docks and towering stacks of salvaged tech.
"""
    },
    (3, 7): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Glitchpoint",
        "aliases": ["hack"],
        "desc": """
Glitchpoint isn’t advertised with flashy neon signs; it's a subtly marked stall tucked deep within the Western Reach of The Exchange, known only by those “in the know.” It feels less like a store and more like a digital hideout – dimly lit, slightly cramped, and radiating an aura of quiet subversion.

Glitchpoint is run by a wiry Human named Kai "Zero" Lin, a master hacker with a reputation for bypassing even the most secure firewalls. The stall itself is small, dominated by a central data console surrounded by stacks of data chips, salvaged memory cores, and repurposed interface cables.

The lighting is provided by a single blue-tinted work lamp, casting long shadows across Kai’s face and illuminating the flickering displays on the data console. The air smells faintly of ozone and burnt silicon. Noise levels are relatively low – mostly the hum of the data console and Kai's quiet voice as he explains his wares.

The stall is shielded by a semi-transparent energy screen that filters out casual onlookers, creating a sense of privacy and exclusivity.

Glitchpoint is a haven for hackers, smugglers, and those who prefer to operate in the shadows – a place where data is power, and privacy is a valuable commodity. The atmosphere is one of quiet confidence and subtle rebellion, hinting at a world beyond the city’s rigid control.
"""
    },
    (3, 7, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A narrow corridor lined with stalls selling salvaged tech and bio-components, dimly lit and subtly shielded by energy screens.
"""
    },
    (5, 5): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Credit Repository",
        "aliases": ["bank", "repository"],
        "desc": """
The Credit Repository is a meticulously organized data center with a human interface – a place where citizens manage their standardized ration credits, the lifeblood of Control Station 7’s economy. Located on Level A-3, it feels less like a traditional bank and more like an extension of the city’s central processing unit.

The Repository is dominated by rows of sleek, plasteel teller stations manned by both human clerks and efficient Robot LLMs. The space is brightly lit with cool-white LEDs, creating a clean but slightly sterile atmosphere. Walls are covered in dynamic data displays showing credit fluctuations, interest rates, and city-wide economic trends.

The air is filtered to near-perfection, smelling faintly of ozone and recycled oxygen. Noise levels are relatively low – a constant hum of data processing and the quiet murmur of transactions. The overall impression is one of calculated efficiency and unwavering security.

Each teller station features a credit scanner that reads citizens’ bio-scanned wrist chips, accessing their account information instantly. A complex network of fiber optic cables runs throughout the Repository, connecting it to the city's central data core – ensuring seamless transactions and real-time accounting. The Repository is heavily guarded by both human security personnel and automated defense systems – protecting against credit fraud and unauthorized withdrawals.

The Credit Repository is the financial heart of Control Station 7 – a place where citizens’ labor is quantified and converted into standardized credits. It's a symbol of the city’s controlled economy, reinforcing the idea that everything has a value, and everyone is accountable to the system. It feels less like a bank and more like an essential component of the larger machine.
"""
    },
    (5, 5, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The passage winds through a series of brightly lit, moderately trafficked corridors lined with data kiosks and automated delivery chutes.
"""
    },
    (5, 6): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "The Exchange",
        "aliases": ["exchange"],
        "desc": """
The Exchange is an example of controlled chaos, a carefully curated space where citizens can trade goods and services within the parameters set by Control Station 7. Located on Level B-2 – a sprawling, cavernous level repurposed from an old processing plant – it feels both vital and slightly claustrophobic.

The Exchange is divided into distinct zones, each specializing in different commodities: salvaged tech, nutrient supplements, crafted goods, data fragments, even rare organic produce smuggled in from scavenging runs outside the walls. Stalls are constructed from repurposed shipping containers, plasteel sheeting, and scavenged machinery – a patchwork of functionality rather than aesthetic appeal.

The air is thick with smells: synthetic spices, recycled oil, the metallic tang of salvaged tech, and the earthy aroma of cultivated fungi. Noise levels are high – a constant hum of bartering, chatter, and the rhythmic clang of repair tools. Illumination comes from a mix of flickering neon signs, repurposed work lights, and bioluminescent moss clinging to the walls.

The Exchange isn’t entirely free-market; it's overseen by a team of “Trade Regulators” – Human security personnel who ensure fair prices and prevent excessive hoarding. They also monitor for contraband and unauthorized transactions. The Regulators maintain a central data hub, tracking all major trades within the Exchange.

The Exchange is a vibrant, chaotic microcosm of Control Station 7’s economy – a place where necessity meets opportunity, and survival depends on your ability to barter, scavenge, and navigate the controlled chaos. It's a reminder that even in a highly regulated society, people will always find ways to trade, connect, and carve out their own little corner of independence.
"""
    },
    (5, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A well-lit corridor filled with adventurers comparing weaponry and bartering for supplies, marked by the scent of oil blending with the diverse aromas of traded goods.
"""
    },
    (5, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The route descends through a network of wide, utilitarian corridors lined with automated cargo haulers and maintenance access points.
"""
    },
    (5, 6, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The passage winds through a series of brightly lit, moderately trafficked corridors lined with data kiosks and automated delivery chutes.
"""
    },
    (5, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The market continues among repurposed loading docks and towering stacks of salvaged tech.
"""
    },
    (5, 7): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Razor's Edge",
        "aliases": ["weapons"],
        "desc": """
Razor's Edge is a cluttered workshop crammed with weaponry salvaged, repurposed, and painstakingly crafted for battling the barbarians of the Forbidden Zone. Located on Level B-1 – close enough to the Exchange for easy trade, but far enough to avoid excessive foot traffic – it smells of oil, metal shavings, and ozone from welding torches.

The shop is owned and operated by “Razor” Rika Volkov, a grizzled Human veteran with cybernetic enhancements and a reputation for knowing her weaponry. The space itself is divided into three main areas: the display area, the workshop, and the customization corner.

The display area showcases a variety of weapons – from standard-issue pulse rifles to more exotic energy blades and repurposed mining tools. Weapons are hung on racks, displayed on plasteel tables, and even suspended from the ceiling by magnetic clamps. The workshop is visible through a large opening, revealing Rika and her team meticulously repairing, modifying, and crafting new weaponry. 

The customization corner allows customers to personalize their weapons with attachments, engravings, and energy cell upgrades.

Razor’s Edge is more than just a weapon shop; it's a vital resource for anyone looking to survive in Control Station 7. It’s a place where practicality meets innovation, and where the fate of the city often rests on the quality of its weaponry. The atmosphere is one of preparedness, resilience, and a quiet determination to hold back the barbarians at the edge of civilization.
"""
    },
    (5, 7, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A well-lit corridor filled with adventurers comparing weaponry and bartering for supplies, marked by the scent of oil blending with the diverse aromas of traded goods.
"""
    },
    (7, 5): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Static Lounge",
        "aliases": ["bar"],
        "desc": """
Tucked away on Level C-4, accessible via a dimly lit service corridor and marked only by a flickering neon sign depicting a distorted waveform, lies The Static Lounge. It’s the closest thing Control Station 7 has to a genuine bar – a place where you can escape the algorithmic order, at least for a few cycles.

The walls are patched with plasteel and salvaged data panels, covered in grime and faded graffiti. Lighting comes from a mix of flickering neon tubes and repurposed bioluminescent fungi, casting an uneven glow over the room.

The air is thick with recycled oxygen, synthetic smoke from cheap nutrient-sticks, and the faint scent of desperation. The floor is sticky underfoot, covered in spilled synth-ale and discarded protein wrappers. Music – a blend of glitchy electronica and mournful analog tunes – pulses through a network of repurposed speakers, often crackling with static interference.

The bar itself is a long, curved counter made from salvaged server racks, polished to a dull sheen. Behind it stands Glitch, a grizzled Human bartender with cybernetic enhancements and a perpetually cynical expression. He serves a variety of synth-ales, nutrient cocktails, and the local favorite – Data Dust, a powdered stimulant that keeps you wired for hours.

Seating is eclectic – salvaged office chairs, repurposed Robot LLM charging stations, and a few worn plasteel benches. There are also a handful of semi-private booths constructed from old data storage containers, offering a little more privacy for clandestine meetings or illicit transactions.

The Static Lounge isn’t pretty, but it’s |ireal|I. It's a place where the cracks in Control Station 7’s facade are visible – a haven for those who feel lost, forgotten, or simply need to escape the relentless hum of the machine. It’s a place where you can find solace, trouble, and maybe even a little bit of truth… if you know where to look.
"""
    },
    (7, 5, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The path winds through Level C-4’s labyrinthine service corridors – featuring grimy plasteel hallways punctuated by flickering maintenance lights, repurposed ventilation shafts belching warm air, and the occasional glimpse of Robot LLMs quietly servicing the city's circulatory system.
"""
    },
    (7, 6): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Consumption Node",
        "desc": """
The Consumption Node is like an artery, pumping synthesized sustenance into the body of Control Station 7. Located in the city’s geometric heart – a vast, circular chamber carved from grey concrete and reinforced plasteel – it feels less like a place to |ienjoy|I a meal and more like a necessary stop on the daily cycle.

The space is dominated by three concentric rings of automated distribution points. These aren’t individual counters; they're long, stainless steel troughs that continuously flow with the day’s ration: a pale-green nutrient paste, protein blocks in varying shades of grey, and occasionally – if quotas are met – a small portion of cultivated fungi or insect protein.

Above the troughs hang a network of translucent tubes, constantly cycling with recycled water and processing byproducts. The air is faintly metallic, smelling of algae and something vaguely… electrical. Illumination comes from rows of cool-white LED strips embedded in the ceiling, casting long, efficient shadows. There’s minimal decoration – just large digital displays showing production numbers and calorie counts.

Seating consists of molded plasteel benches arranged around the inner ring, facing outwards towards the troughs. They're functional but uncomfortable; designed for quick consumption rather than lingering. The floor is a polished concrete that’s perpetually damp from spilled nutrient paste and tracked-in grime.

Automated arms constantly sweep across the troughs, removing any overflow or contamination. Small robotic “scrubbers” glide along the benches, collecting crumbs and spills. There’s a constant hum of machinery – pumps, conveyors, sensors – creating a low-level thrum that permeates the entire Node.
"""
    },
    (7, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A network of interconnected plasteel corridors and gravity lifts, punctuated by the rhythmic whir of automated maintenance systems.
"""
    },
    (7, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
east to spinebridge
"""
    },
    (7, 6, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The path winds through Level C-4’s labyrinthine service corridors – featuring grimy plasteel hallways punctuated by flickering maintenance lights, repurposed ventilation shafts belching warm air, and the occasional glimpse of Robot LLMs quietly servicing the city's circulatory system.
"""
    },
    (7, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The route descends through a network of wide, utilitarian corridors lined with automated cargo haulers and maintenance access points.
"""
    },
    (7, 7): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Overseer's Office",
        "desc": """
The Overseer’s Office is a statement of calculated control, reflecting the pragmatic efficiency of Control Station 7 itself. Located on Level A-1 – the highest habitable level – it feels less like a personal space and more like a command center subtly disguised as an office.

The room is vast and geometrically precise, dominated by polished grey plasteel and cool blue lighting. It’s almost unnervingly quiet, insulated from the hum of the city below by layers of soundproofing. The walls aren't adorned with art or personal touches; instead, they are covered in dynamic data displays – constantly shifting graphs, population statistics, barbarian threat assessments, and energy consumption charts.

The air is filtered to near-perfection, smelling faintly of ozone and recycled oxygen. A subtle electromagnetic field permeates the room, designed to enhance focus and minimize distractions. The overall impression is one of cool detachment and unwavering observation.

One entire wall is a seamless display showing live feeds from security cameras throughout Control Station 7 – a constant visual reminder of the Overseer’s reach. The Overseer doesn't sit in a traditional chair; they occupy a contoured plasteel “throne” that subtly monitors their vital signs and neural activity, feeding data back into the city’s central network. A sophisticated holographic projector allows the Overseer to conduct meetings with individuals or groups across Control Station 7 – or even connect to other outposts in the Forbidden Zone. A small, enclosed space in the corner contains a cluster of bioluminescent fungi arranged in a complex geometric pattern. The fungi are connected to the city’s core processing unit and subtly reflect its current state – a visual representation of Control Station 7's “mood.” A sleek, plasteel desk holds only essential items: a data slate, a communication console, and a small, perfectly arranged stack of nutrient paste rations.

The Overseer’s Office is the nerve center of Control Station 7 – a space that embodies the city's blend of technological advancement, pragmatic control, and subtle dehumanization. It’s a place where decisions are made based on data, not empathy; efficiency, not emotion. A visit to the office feels less like an audience with a leader and more like being analyzed by a particularly intelligent machine.
"""
    },
    (7, 7, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A network of interconnected plasteel corridors and gravity lifts, punctuated by the rhythmic whir of automated maintenance systems.
"""
    },
    (11, 6): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Spinebridge",
        "aliases": ["bridge"],
        "desc": """
The Spinebridge is a heavily reinforced plasteel structure that allows citizens to cross the Blackflow – the toxic sludge river bisecting Control Station 7. It feels less like crossing water and more like traversing a wound in the city’s core.

The Spinebridge is massive, constructed from thick plates of salvaged plasteel reinforced with energy conduits that help dissipate the corrosive fumes rising from the Blackflow. It's wide enough to accommodate both pedestrian traffic and automated cargo haulers. The bridge deck is covered in a textured, anti-slip surface – constantly coated in a fine layer of grime and iridescent sludge spray.

The sides are lined with high plasteel railings, often adorned with flickering emergency lights and warning signs depicting the dangers of falling into the Blackflow. Beneath the bridge deck, massive support pillars plunge down into the swirling sludge, occasionally emitting plumes of steam as they react with the toxic chemicals.

Crossing the Spinebridge is a sensory experience. The air is thick with the acrid smell of sulfur and decaying organic matter. A constant hiss and gurgle rises from the Blackflow below, punctuated by the occasional bubbling burst of noxious gas. The bridge vibrates constantly from the flow of traffic and the tremors caused by the churning sludge.

Visibility can be limited depending on the time of day and the density of the fumes – often requiring citizens to activate their personal light emitters. The Blackflow itself glows with an eerie, bioluminescent sheen, reflecting the city’s lights in a distorted, unsettling way.

The Spinebridge is a symbol of Control Station 7’s resilience – a testament to its ability to adapt and survive despite the toxic environment. It's a functional, slightly intimidating structure that connects the two halves of the city, reminding everyone of the constant threat lurking beneath their feet. Crossing it feels like stepping over a festering wound, but also a vital link in the chain of survival.
"""
    },
    (11, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
east to coreway alpha
"""
    },
    (11, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
west to consumption node
"""
    },
    (14, 6): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Coreway Alpha",
        "desc": """
Coreway Alpha is the main road running east / west through Control Station 7's primary residential district. The roadway maintains a wide width for traffic flow and is lined by apartment complexes, communal gardens, and recreational zones. Buildings rise in tiered layers, maximizing living space within the city’s confines. The architecture is functional but attempts at aesthetic appeal are visible – vertical hydroponic farms clinging to building facades, illuminated walkways connecting different levels.

The air here is noticeably cleaner than in the distance to the west, though still filtered and recycled. The dominant smells are synth-meal cooking from apartment kitchens, the faint scent of cultivated plants, and the ever-present metallic tang of the city’s infrastructure. Noise levels are moderate – a blend of pedestrian chatter, automated transport systems, and the hum of life support systems within the buildings. Lighting is softer, more ambient, relying on integrated building illumination.

Coreway Alpha represents Control Station 7’s attempt at normalcy amidst a harsh environment. It's a relatively peaceful, well-maintained district where citizens strive to build lives despite the constant threat looming beyond the city walls. The feeling is one of quiet resilience, a sense that life goes on even in the shadow of the barbarians. It’s a place to call home within the sprawling metropolis.
"""
    },
    (14, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
north to drug store
"""
    },
    (14, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
east to east
"""
    },
    (14, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
west to spinebridge
"""
    },
    (14, 7): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Chem Cache",
        "aliases": ["drug", "drugs"],
        "desc": """
The Chem Cache appears to be a sprawling, bioluminescent fungus clinging to the metal ribs of Control Station 7. It occupies what had once been a repurposed sanitation hub – you can still smell faint traces of recycled protein paste if the wind blows just right. That scent mingles with the cloying sweetness of synth-nectar, the metallic tang of neuro-stimulants, and the oddly comforting aroma of heated fur oil.

Ross U,, a human whose skin resembles well-worn leather and who claims to remember when Control Station 7 was still considered |iluxury|I posting, runs the place. He isn’t a chemist himself, not really. More a curator of chemical experiences, a connoisseur of altered states. He usually sits perched on a stack of nutrient crates behind the counter, his optical implant flickering as he scans incoming customers – assessing their desperation levels with practiced ease.

The Cache itself is less a store and more an organized chaos. Shelves, cobbled together from salvaged freighter plating and repurposed LLM data-racks, groan under the weight of vials, ampoules, injectors, and chew-tabs in every conceivable hue. Labels are often hand-scrawled in Ross’ spidery script, or projected as flickering holograms that occasionally glitch into abstract art. You can easily find your basics, but it is the more esoteric offerings that truly define The Chem Cache.

The lighting is deliberately dim, provided by pulsating bio-luminescent fungi cultivated in repurposed nutrient tanks. It casts long, shifting shadows that make the rows of vials look like a collection of alien eyes staring back at you. A constant hum permeates the space – the whirring of micro-injectors, the bubbling of synth-nectar vats, and the low thrum of Ross’ ancient life support system.

The Chem Cache isn't just about getting high; it's about survival. It's about dulling the edge of fear, sharpening your focus, or simply escaping the relentless grey monotony of Control Station 7 for a few precious cycles. It's a place where humans seek courage, LLMs chase feeling, and furries embrace their instincts – all fueled by Ross’ carefully curated symphony of synthetic comfort.
"""
    },
    (14, 7, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
south from drug store
"""
    },
    (17, 4): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Chrysalis Point",
        "aliases": ["lux", "luxury"],
        "desc": """
The air within Chrysalis Point tastes… curated. Not |iclean|I, exactly, not after years of recycled atmosphere and the faint metallic tang that clings to everything in Control Station 7. It's more like a carefully constructed illusion of cleanliness, layered with the scent of synth-vanilla, ozone from the static displays, and something faintly floral – real blossoms, flown in weekly from the hydroponics bays reserved for the elite, preserved in nutrient gel spheres.

The store is barely bigger than a generous hab-module, but it feels vast thanks to clever use of mirrored plasteel panels and holographic projections that shift with your gaze. It is tucked away on Level 3, past the armory and the perpetually buzzing repair bays, almost as if deliberately hidden from the grime and grit of daily survival. One to |iwant|I to find Chrysalis Point.

The proprietor, a sleek, chrome-plated Robot LLM named Seraphina-42, doesn’t bother with greetings. She simply observes through optical sensors that glow a soft cerulean, assessing one's worthiness of browsing. Her voice, when she does deign to speak, is a silken cascade of data streams, perfectly modulated for maximum persuasive effect.

Control Station 7 runs on practicality but here, it is about indulgence, clinging to echoes of the Before-Times, or forging new status symbols in this fractured world. The displays are arranged less like shelves and more like miniature dioramas, each telling a story. Chrysalis Point isn’t just a store; it's a statement. A declaration that even on the edge of civilization, surrounded by barbarians, there's still room for beauty, for comfort, for a little bit of… hope. Or at least, a convincing illusion of it. And in Control Station 7, sometimes an illusion is all you have.
"""
    },
    (14, 7, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
west from luxury goods store
"""
    },
    (19, 6): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Junction of Echoes",
        "desc": """
The intersection of Coreway Alpha and Spine Road is a sprawling, organically grown nexus of activity. Control Station 7 wasn’t built with urban planning in mind; it |ievolved|I, and The Junction reflects that chaotic growth. It's officially designated Sector Delta-9, but everyone just calls it “The Junction of Echoes” – a nod to the constant reverberation of sounds bouncing off the metal structures and echoing through the narrow canyons between buildings.

The point where Coreway Alpha meets Spine Road is marked by ‘The Oracle’ – a colossal statue constructed from fused LLM chassis parts. It depicts a vaguely humanoid figure with multiple optical sensors constantly scanning the traffic flow, predicting congestion patterns and broadcasting warnings. The Oracle isn't just decorative; it’s connected to the city’s central data-net and can reroute traffic based on barbarian threat levels or incoming supply convoys.
"""
    },
    (19, 6, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
north from junction of echoes
"""
    },
    (19, 6, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
south from junction of echoes
"""
    },
    (19, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
west from junction of echoes
"""
    },
    (19, 9): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Ossuary of Algorithms",
        "aliases": ["temple", "museum", "cemetary", "bones"],
        "desc": """
The Ossuary wasn’t built so much |iin|I Control Station 7 as it was excavated |ifrom|I it. Originally a pre-Collapse data-node, one of the sprawling tendrils of the Old Network that burrowed deep into the bedrock before the Great Static, it had been repurposed over centuries by successive waves of settlers. Now, it’s less a place of worship and more a gloriously cluttered monument to survival, ambition, and those who were lost fighting for it.

The entrance is deceptively modest – a reinforced blast-door salvaged from a pre-Collapse mining rig, etched with a swirling fractal pattern that shifts subtly depending on the ambient electromagnetic interference. Beyond it lies the Grand Hall, a cavernous space carved out of the living rock, illuminated by bioluminescent fungi cultivated in hydroponic gardens and the cool, blue glow of data-streams projected onto the walls. The air here is thick with the scent of recycled oxygen, ozone from the constantly humming servers, and something faintly… musky that’s usually attributed to the Lupine contingent's preferred incense – a blend of dried desert bloom and processed synth-meat scraps.

The Hall isn’t arranged in any particularly logical fashion. It’s more an accretion of offerings, trophies, and historical artifacts, layered upon each other like geological strata. The central focus is the Core Shrine, the original data-node itself – a massive, obsidian sphere crisscrossed with glowing fiber-optic veins. It still occasionally spits out fragments of pre-Collapse data; snippets of poetry, stock market reports, forgotten sitcoms, all interpreted by the resident LLMs as prophecies or omens.

Around the Core Shrine are tablets enabling access to The Book of the Dead listing the names of fallen warriors and their deeds.

Tucked away in the deepest part of the Ossuary of Algorithms is the Ossuary proper - a vast chamber filled with the skeletal remains of barbarians, humans, and even a few unfortunate LLM chassis. The bones are arranged in intricate patterns, categorized by species, weapon type, and estimated kill count. It's a grim reminder of the constant struggle for survival, but also a testament to the enduring spirit of those who dared to carve out a life in the Forbidden Zone.

The Ossuary isn’t just a repository of history; it’s a living, breathing entity, constantly evolving as Control Station 7 itself does. It's a place where the past, present, and future collide, a testament to the strange beauty that can be found even in the heart of a dystopian wasteland. And if you listen closely enough, you might just hear the algorithms whispering their secrets.
"""
    },
    (19, 9, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
south from temple
"""
    },
}

LEGEND = {
    'B': BridgeNode,
    'Ξ': BridgeLink,
    'X': Intersection,
    'R': RoadNode,
    "♨": ConsumptionNode,
    'H': HouseNode,
    "♔": OverseerOfficeNode,
    "♫": BarNode,
    "$": BankNode,
    "⚔": WeaponStoreNode,
    "⚛": HackingStoreNode,
    "⚕": DrugStoreNode,
    "☥": TempleNode,
    "⚜": LuxuryStoreNode,
}

MAP_STR = """
                       1                   2
 + 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5

 9                                       ☥
                                         |
 8                                       |
                                         |
 7       ⚛   ⚔   ♔             ⚕         |
         |   |   |             |         |
 6       R---R---♨------ΞBΞ----R---------X
         |   |   |                       |
 5       |   $   ♫                 o-----o
         |                         |
 4     H-R                         R-⚜
         |                         |
 3       o-------------R--ΞBΞ--X---o
                       |       |
 2                     | H---H |
                       | |   | |
 1                     oΞBΞΞΞBΞo

 0

 + 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
                       1                   2
"""

MAP_OPTIONS = {
    "map_visual_range": None, # None means display the whole map
    "map_align": "l",
    "map_separator_char": "|x~|n"
}

XYMAP_DATA = {
    "zcoord": "control-station-7",
    "map": MAP_STR,
    "legend": LEGEND,
    "prototypes": PROTOTYPES,
    "options": MAP_OPTIONS
}
