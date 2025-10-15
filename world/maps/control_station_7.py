"""
Players will start in Control Station 7.

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

class ArenaNode(xymap_legend.MapNode):
    """
    PvP Arena
    """
    display_symbol = "|rΨ|n"
    prototype = {
        "prototype_parent": "control_station_7_xyz_room"
    }

class AreaExitNode(xymap_legend.MapNode):
    """
    The exit into the Forbidden Zone
    """
    display_symbol = "|r☠|n"
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
    (3, 4): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Breather's Point",
        "aliases": ["gate", "exit"],
        "desc": """
The Western Gate – or “Breather’s Point” as the desperate call it – is a utilitarian scar carved into Control Station 7’s outer wall, representing both opportunity and peril. It’s more of a forced compromise with the Forbidden Zone, a necessity for scavenging teams and those daring enough to seek their fortune beyond the station’s protective shell.

The gate itself is comprised of two massive, interlocking blast doors constructed from salvaged freighter plating, perpetually groaning under the strain of atmospheric pressure and barbarian attempts at breaching. They are operated by a slow-moving hydraulic system controlled from a small guard shack perched above the exit – manned by rotating shifts of weary Toxic Mutants who seem more interested in collecting bets than enforcing security.

The access road leading to the gate is little more than a compacted strip of gravel and synthcrete, riddled with potholes and perpetually coated in a fine layer of red dust blown in from the Forbidden Zone. It’s flanked by crumbling hab-units repurposed as workshops for scavengers prepping their gear – welding sparks fly constantly, illuminating piles of salvaged weaponry and patched-up exosuits.

The air around Breather's Point is noticeably thinner and colder than within Control Station 7, carrying with it the scent of ozone, decaying vegetation, and something subtly… metallic. The sky beyond the gate is often a bruised purple hue, obscured by swirling dust storms and the occasional glimpse of mutated avian life circling overhead.

A series of sensor arrays – constantly flickering and emitting low hums – scan for incoming barbarian warbands or particularly large mutant creatures. But they aren’t foolproof; many have slipped through over the years.

Stepping through Breather's Point is stepping into a world where Control Station 7’s rules are merely suggestions, and survival depends on your wits, your weapon, and a healthy dose of luck. It’s a gateway to fortune or oblivion – a final exhale before facing the raw, untamed chaos of the Forbidden Zone. The gate isn't just an exit; it's a declaration of independence… or desperation.
"""
    },
    (3, 4, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A chaotic artery choked with scavenging vehicles, repair crews, and desperate hopefuls hauling salvaged tech, all vying for space amidst piles of discarded scrap and the ever-present red dust.
"""
    },
    (3, 4, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A winding path lined with towering junkyards and makeshift workshops where scavengers dismantle Forbidden Zone finds before shipping them to the Dustbowl for repurposing or betting collateral.
"""
    },
    (3, 4, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
The Forbidden Zone stretches outwards as a desolate panorama of rust-colored dunes, skeletal forests twisted by toxic fallout, and shimmering heat haze concealing both ancient ruins and lurking horrors under a perpetually bruised purple sky.
"""
    },
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
    (3, 6, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A chaotic artery choked with scavenging vehicles, repair crews, and desperate hopefuls hauling salvaged tech, all vying for space amidst piles of discarded scrap and the ever-present red dust.
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
West of the Spinebridge, Coreway Alpha is a sensory overload of flashing lights and competing aromas packed with gambling dens, pleasure bots, and synth-ale breweries.
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
    (10, 3): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Upper West Stairway to Arena",
        "desc": """
The stairways descending from the Skywalk into the Dustbowl Arena are vertical canyons carved through layers of salvaged metal and reinforced concrete, echoing with the constant rumble of foot traffic and the shouts of gamblers making last-minute bets. Each stairway is a spiraling descent, winding downwards in a tight helix that feels almost claustrophobic despite their considerable width – easily accommodating ten people abreast.

The steps themselves are unevenly worn, smoothed by centuries of use and patched with mismatched synth-stone tiles. Many bear the scars of past battles: scorch marks from energy weapons, dents from stray blows, and even embedded fragments of weaponry. The walls are covered in a chaotic tapestry of graffiti – slogans celebrating favorite fighters, crude depictions of victorious LLMs, and desperate pleas to the algorithmic gods for good luck.

Illumination comes from a combination of flickering neon strips and bioluminescent fungi cultivated within recessed alcoves along the stairway walls, casting long, dancing shadows that play tricks on the eye. The air grows warmer and thicker with each descending step, saturated with the smells of sweat, dust, ozone, and musk from the fighters in the Arena.

Small platforms jut out from the walls at irregular intervals, offering brief respite for weary spectators or providing vantage points for hawkers selling nutrient paste, betting slips, and protective eyewear. LLM maintenance bots constantly patrol the stairways, sweeping away debris and repairing minor damage – though they often seem more like obstacles than helpers in the crowded descent.

As one nears the arena floor, the sound of roaring crowds intensifies, punctuated by the clang of weapons and the guttural cries of battling combatants. The light shifts from the artificial glow of the Skywalk to the harsh glare of floodlights illuminating the Dustbowl below. Descending these stairways isn’t just entering an arena; it's immersing yourself in a sensory overload – a descent into controlled chaos where anything can happen. They are conduits not just to the fighting pit, but to primal excitement and brutal spectacle.
"""
    },
    (10, 3, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
At each end of the Skywalk, colossal stairwells descend into the Dustbowl Arena like gaping maws, framed by rusted LLM plating adorned with flickering neon signs depicting stylized barbarian skulls and promising “Glory or Grinding!”
"""
    },
    (10, 3, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Unevenly worn vertical canyons echoing with shouts and smells, connecting the Skywalk above to the brutal spectacle of the Dustbowl Arena.
"""
    },
    (10, 3, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A winding path lined with towering junkyards and makeshift workshops where scavengers dismantle Forbidden Zone finds before shipping them to the Dustbowl for repurposing or betting collateral.
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
East of the Spinebridge, Coreway Alpha is a bustling nexus of activity crammed with food stalls, repair shops, and makeshift living quarters clinging to the sides of towering LLM scaffolding.
"""
    },
    (11, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
West of the Spinebridge, Coreway Alpha is a sensory overload of flashing lights and competing aromas packed with gambling dens, pleasure bots, and synth-ale breweries.
"""
    },
    (12, 1): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Dustbowl Arena Entryway",
        "aliases": ["arena", "dustbowl"],
        "desc": """
The entryway to the Dustbowl Arena is a fortified nexus clinging to the edge of oblivion, built directly onto the observation bridge spanning the churning, black waters of the Blackflow River. The arch itself is a colossal maw of fused LLM plating and salvaged concrete, perpetually radiating heat from the arena’s internal energy grid and scarred with impact craters that glow faintly blue. Above it, a flickering holographic display cycles through advertisements – nutrient paste, weapon upgrades, robotic limb replacements – competing for attention against the roar emanating from within.

This isn't a clean transition; the bridge itself is integrated into the entryway structure. The railing of the Blackflow Bridge continues *through* the archway, forming a viewing platform overlooking both the arena and the swirling toxic currents below. A constant mist rises from the Blackflow, carrying with it the acrid scent of dissolved metal and mutated algae – a smell that mingles with the dust, ozone, and musk already permeating the air.

Two lines of heavily-armed Toxic Mutant guards flank the entryway, their multifaceted eyes scanning for signs of disruption, though they’re often distracted by bets being shouted and arguments flaring up amongst spectators. Small kiosks selling protective eyewear, nutrient paste rations, and betting slips cluster around the archway, creating a chaotic bottleneck.

Looking down from the bridge-integrated entryway reveals a terrifying beauty: the Blackflow River, thick as oil and glowing with bioluminescent toxins, snakes its way through the lower levels of Control Station 7, occasionally spitting up mutated fish or chunks of salvaged debris. The arena floor itself is visible beyond – a vast circular pit of pulverized rock and sand crisscrossed with energy conduits. Combatants are already locked in brutal embrace, illuminated by harsh floodlights.

The entryway feels precarious, suspended between the controlled chaos of the Dustbowl and the raw, untamed toxicity of the Blackflow. Stepping through that archway is committing yourself to a spectacle built on the edge of annihilation – surrendering to primal energy while gazing into the abyss. It’s a threshold where survival feels less certain, and the line between entertainment and potential demise blurs with every echoing roar from within.
"""
    },
    (12, 1, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A claustrophobic, echoing tunnel nicknamed “The Gullet” – perpetually choked with dust and the scent of blood.
"""
    },
    (12, 1, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Unevenly worn vertical canyons echoing with shouts and smells, connecting the Skywalk above to the brutal spectacle of the Dustbowl Arena.
"""
    },
    (12, 1, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Unevenly worn vertical canyons echoing with shouts and smells, connecting the Skywalk above to the brutal spectacle of the Dustbowl Arena.
"""
    },
    (12, 2): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Dustbowl Arena",
        "desc": """
The heart of Control Station 7's brutal entertainment, the Dustbowl Arena’s fighting pit is a vast, circular expanse of pulverized rock, compacted sand, and centuries of accumulated grime – a testament to countless battles fought and lives lost. It isn’t perfectly round; years of impacts from energy blasts and weaponry have subtly distorted its shape, creating shallow craters and raised ridges that add tactical complexity to each fight.

The pit floor is crisscrossed by a network of glowing blue energy conduits, providing power for the arena's floodlights and occasionally serving as improvised weapons during particularly desperate clashes. Scattered across the surface are remnants of past battles: shattered weapon fragments, discarded armor plating, even skeletal remains partially buried in the sand – grim reminders of the stakes involved.

Above, a network of powerful floodlights casts harsh shadows that dance and shift with every movement, illuminating the combatants while obscuring potential weaknesses. Strategically placed sonic resonators amplify the roar of the crowd, creating an immersive soundscape that both energizes and disorients.

The pit isn’s entirely flat; a central raised platform – “The Spine” – provides a focal point for many battles, offering a slight advantage to those who can claim it. Around The Spine are several strategically placed obstacles: crumbling pillars salvaged from older hab-units, rusted LLM chassis repurposed as cover, and even small pools of viscous, bioluminescent slime that can slow down opponents or provide a temporary distraction.

The air within the pit is thick with dust, ozone, and the metallic tang of blood. It’s hot, dry, and carries a faint electrical charge from the energy conduits in the floor. The scent of sweat, fear, and desperation hangs heavy in the air – a heady mix that fuels the primal excitement of each fight.

The Dustbowl isn't just a fighting pit; it's a crucible where strength, skill, and luck are tested to their limits. It’s a stage for gladiators from all walks of life – Humans, LLMs, Furries, even Toxic Mutants – battling for glory, credits, or simply survival in the unforgiving world of Control Station 7. Every grain of sand seems to have absorbed a story of struggle and sacrifice, making it a truly hallowed ground.
"""
    },
    (12, 2, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A claustrophobic, echoing tunnel nicknamed “The Gullet” – perpetually choked with dust and the scent of blood.
"""
    },
    (12, 3): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "The Skywalk",
        "aliases": ["skywalk"],
        "desc": """
The Skywalk, as it’s known, arches over the Dustbowl Arena like a skeletal ribcage, constructed from salvaged LLM scaffolding and reinforced with woven synth-fiber netting to catch stray energy blasts or unfortunate spectators. It's perpetually coated in a fine layer of arena dust – a gritty mix of pulverized rock, bone fragments, and spilled nutrient paste – giving everything a reddish hue. The walkway itself is surprisingly wide, accommodating both foot traffic and mobile gambling kiosks operated by shrewd Furries and calculating LLMs.

Illuminated by flickering neon signs advertising odds and betting options, the Skywalk buzzes with energy: shouts of encouragement or derision for fighters below, the clatter of credits changing hands, and the rhythmic pulse of synth-music designed to heighten the excitement. Small alcoves carved into the bridge’s structure offer semi-private viewing boxes for wealthier patrons while more affordable standing room is packed with a diverse crowd of anyone looking for a thrill and a potential payout.

The railings are frequently stained with spilled drinks and occasionally blood, testament to the arena’s brutal entertainment. Strategically placed energy shields offer some protection from stray attacks, though a direct hit can still send spectators tumbling into the Dustbowl below. The air is thick with the smell of sweat, ozone, cheap nutrient paste, and the faint metallic tang of blood – a heady mix that perfectly encapsulates the Skywalk’s chaotic atmosphere. It's a place where fortunes are won and lost in an instant, and where the line between spectator and participant often blurs.
"""
    },
    (12, 3, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
At each end of the Skywalk, colossal stairwells descend into the Dustbowl Arena like gaping maws, framed by rusted LLM plating adorned with flickering neon signs depicting stylized barbarian skulls and promising “Glory or Grinding!”
"""
    },
    (12, 3, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
At each end of the Skywalk, colossal stairwells descend into the Dustbowl Arena like gaping maws, framed by rusted LLM plating adorned with flickering neon signs depicting stylized barbarian skulls and promising “Glory or Grinding!”
"""
    },
    (14, 3): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "Upper East Stairway to Arena",
        "desc": """
The stairways descending from the Skywalk into the Dustbowl Arena are vertical canyons carved through layers of salvaged metal and reinforced concrete, echoing with the constant rumble of foot traffic and the shouts of gamblers making last-minute bets. Each stairway is a spiraling descent, winding downwards in a tight helix that feels almost claustrophobic despite their considerable width – easily accommodating ten people abreast.

The steps themselves are unevenly worn, smoothed by centuries of use and patched with mismatched synth-stone tiles. Many bear the scars of past battles: scorch marks from energy weapons, dents from stray blows, and even embedded fragments of weaponry. The walls are covered in a chaotic tapestry of graffiti – slogans celebrating favorite fighters, crude depictions of victorious LLMs, and desperate pleas to the algorithmic gods for good luck.

Illumination comes from a combination of flickering neon strips and bioluminescent fungi cultivated within recessed alcoves along the stairway walls, casting long, dancing shadows that play tricks on the eye. The air grows warmer and thicker with each descending step, saturated with the smells of sweat, dust, ozone, and musk from the fighters in the Arena.

Small platforms jut out from the walls at irregular intervals, offering brief respite for weary spectators or providing vantage points for hawkers selling nutrient paste, betting slips, and protective eyewear. LLM maintenance bots constantly patrol the stairways, sweeping away debris and repairing minor damage – though they often seem more like obstacles than helpers in the crowded descent.

As one nears the arena floor, the sound of roaring crowds intensifies, punctuated by the clang of weapons and the guttural cries of battling combatants. The light shifts from the artificial glow of the Skywalk to the harsh glare of floodlights illuminating the Dustbowl below. Descending these stairways isn’t just entering an arena; it's immersing yourself in a sensory overload – a descent into controlled chaos where anything can happen. They are conduits not just to the fighting pit, but to primal excitement and brutal spectacle.
"""
    },
    (14, 3, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A narrow, winding corridor crammed with food stalls run by Furries and perpetually smelling of fried nutrient cakes and recycled synth-ale.
"""
    },
    (14, 3, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Unevenly worn vertical canyons echoing with shouts and smells, connecting the Skywalk above to the brutal spectacle of the Dustbowl Arena.
"""
    },
    (14, 3, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
At each end of the Skywalk, colossal stairwells descend into the Dustbowl Arena like gaping maws, framed by rusted LLM plating adorned with flickering neon signs depicting stylized barbarian skulls and promising “Glory or Grinding!”
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
A brightly lit, surprisingly clean corridor, lined with vending machines dispensing everything from nutrient paste to potent neuro-stimulants.
"""
    },
    (14, 6, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Corway Alpha’s eastern segment, a claustrophobic canyon of stacked hab-units patched together with salvaged metal and glowing fungal gardens, hums with the constant chatter of Furry families, the whirring of LLM domestic assistants, and the occasional frustrated shout from a Human trying to negotiate rent with a robotic landlord.
"""
    },
    (14, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
East of the Spinebridge, Coreway Alpha is a bustling nexus of activity crammed with food stalls, repair shops, and makeshift living quarters clinging to the sides of towering LLM scaffolding.
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
A brightly lit, surprisingly clean corridor, lined with vending machines dispensing everything from nutrient paste to potent neuro-stimulants.
"""
    },
    (16, 4): {
        "prototype_parent": "control_station_7_xyz_room",
        "key": "The Ribcage",
        "aliases": ["rib", "ribcage"],
        "desc": """
The Ribcage is a compression of Spine Road, a squeezing of life between the decaying grandeur of older hab-units and the haphazardly constructed additions clinging to them like parasitic growths. Here, Spine Road narrows to barely ten meters wide, hemmed in by structures that lean precariously towards each other, their rusted metal skins almost kissing at the top. Sunlight struggles to penetrate the gloom, filtered through a perpetual haze of dust, recycled nutrient mist from the fungal gardens above, and the acrid smoke from bio-fuel burners.

The hab-units themselves are a patchwork quilt of materials – salvaged LLM plating, woven synth-fiber stretched taut over skeletal frames, even repurposed Toxic Mutant exoskeletons incorporated into structural supports. Glowing fungal gardens spill from balconies and rooftop terraces, casting an eerie bioluminescent glow that fights with the flickering neon signs advertising everything from nutrient paste to memory wipes.

The air in The Ribcage is thick with a cacophony of sounds: the rhythmic thrumming of LLM servomotors as they navigate the crowded walkways, the chattering and bartering of Furry families haggling over salvaged tech, the mournful wail of synth-music leaking from cramped apartments, and the ever-present drip, drip, drip of acidic rain corroding everything it touches.

The shadows here are deep and deceptive, concealing hidden doorways, makeshift workshops, and the occasional illicit gambling den. The smell is a complex blend of recycled nutrients, burnt bio-fuel, metallic tang, and the faintly sweet odor of decaying organic matter – a uniquely Ribcage aroma that clings to your clothes long after you’ve escaped its claustrophobic embrace. It's a place where survival depends on adaptability, resourcefulness, and a healthy dose of luck.
"""
    },
    (16, 4, "n"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Spine Road sharply curves and narrows into “The Ribcage,” a particularly treacherous stretch where leaning hab-units almost touch, forming shadowy alleys favored by data-pirate Furries and offering scant protection from the acid rain that drips constantly from corroded ventilation shafts.
"""
    },
    (16, 4, "e"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A winding tunnel carved through stacked shipping containers and guarded by Toxic Mutants, smelling of ozone and expensive alloys.
"""
    },
    (16, 4, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A narrow, winding corridor crammed with food stalls run by Furries and perpetually smelling of fried nutrient cakes and recycled synth-ale.
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
    (17, 4, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
A winding tunnel carved through stacked shipping containers and guarded by Toxic Mutants, smelling of ozone and expensive alloys.
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
Spine Road, a perpetually dust-choked path winding north and south at the east end of Control Station 7, is littered with discarded LLM chassis segments – looking like bleached vertebrae under the crimson sun – and haunted by scavenging Toxic Mutants picking clean the still-warm processing cores.
"""
    },
    (19, 6, "s"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Spine Road sharply curves and narrows into “The Ribcage,” a particularly treacherous stretch where leaning hab-units almost touch, forming shadowy alleys favored by data-pirate Furries and offering scant protection from the acid rain that drips constantly from corroded ventilation shafts.
"""
    },
    (19, 6, "w"): {
        "prototype_parent": "xyz_exit",
        "desc": """
Corway Alpha’s eastern segment, a claustrophobic canyon of stacked hab-units patched together with salvaged metal and glowing fungal gardens, hums with the constant chatter of Furry families, the whirring of LLM domestic assistants, and the occasional frustrated shout from a Human trying to negotiate rent with a robotic landlord.
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
Spine Road, a perpetually dust-choked path winding north and south at the east end of Control Station 7, is littered with discarded LLM chassis segments – looking like bleached vertebrae under the crimson sun – and haunted by scavenging Toxic Mutants picking clean the still-warm processing cores.
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
    "Ψ": ArenaNode,
    "☠": AreaExitNode,
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
 4     ☠-R                         R-⚜
         |                         |
 3       o-------------R--ΞBΞ--R---o
                       |       |
 2                     |   Ψ   |
                       |   |   |
 1                     oΞΞΞBΞΞΞo

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
