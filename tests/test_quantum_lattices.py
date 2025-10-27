""" test quantum lattice use behavior """

from unittest.mock import patch

from evennia.prototypes.spawner import spawn
from evennia.utils.test_resources import EvenniaTest

from world.quantum_lattices import (
    DustShard,
    StaticBloom,
    EchoStone,
    ResonanceCrystal,
    SingularityShard,
    PhasePearl,
    VoidSpark,
    ChromaticHeart,
    NexusDiamond
)
from world.utils import rainbow

class TestDustShard(EvenniaTest):
    """ test dust shards """
    def setUp(self):
        super().setUp()
        self.ql = DustShard(spawn("dust_shard")[0])
        self.randint_patcher = patch("random.randint")
        self.mock_randint = self.randint_patcher.start()

    def tearDown(self):
        self.randint_patcher.stop()
        super().tearDown()

    def test_can_use(self):
        """ test dust shard can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertFalse(self.ql.can_use(bike))
        bike.affixes.append("prefix_acidic")
        bike.save()
        self.assertTrue(self.ql.can_use(bike))

    def test_use(self):
        """ test using dust shard """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        bike.affixes.append("prefix_acidic")
        self.mock_randint.return_value = 2
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.affixes, ["prefix_nucular"])
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |xdust shard|n crumbles away and transforms the |Cacidic plasteel bike lock|n"
                " into |Ca nucular plasteel bike lock|n."
            )

# we need to call protected members here to test the menu functionality
# pylint: disable=protected-access
class TestStaticBloom(EvenniaTest):
    """ test static blooms """
    def setUp(self):
        super().setUp()
        self.ql = StaticBloom(spawn("static_bloom")[0])

    def test_can_use(self):
        """ test static bloom can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertFalse(self.ql.can_use(bike))
        bike.affixes.append("prefix_acidic")
        bike.save()
        self.assertTrue(self.ql.can_use(bike))

    def test_use(self):
        """ test using static bloom """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        bike.affixes.append("prefix_acidic")
        with patch("world.quantum_lattices.EvMenu") as mock_ev_menu:
            self.ql.use(self.char1, bike)
            mock_ev_menu.assert_called_with(
                self.char1,
                {
                    "node_select_affix": self.ql._node_select_affix,
                    "node_end_menu": self.ql._node_end_menu,
                },
                startnode="node_select_affix",
                cmd_on_exit=None,
                item=bike,
            )
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql._node_end_menu(self.char1, "", item=bike)
            self.assertEqual(bike.affixes, ["prefix_acidic"])
            mock_at_post_use.assert_not_called()
            self.ql._node_end_menu(self.char1, "", item=bike, affix_to_remove="prefix_acidic")
            self.assertEqual(bike.affixes, [])
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |cstatic bloom|n crumbles away and transforms the |Cacidic plasteel bike"
                " lock|n into |Ca plasteel bike lock|n."
            )

class TestEchoStone(EvenniaTest):
    """ test echo stones """
    def setUp(self):
        super().setUp()
        self.ql = EchoStone(spawn("echo_stone")[0])
        self.randint_patcher = patch("random.randint")
        self.mock_randint = self.randint_patcher.start()

    def tearDown(self):
        self.randint_patcher.stop()
        super().tearDown()

    def test_can_use(self):
        """ test echo stone can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertTrue(self.ql.can_use(bike))
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        self.assertFalse(self.ql.can_use(bike))

    def test_use(self):
        """ test using echo stone """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        self.mock_randint.return_value = 2
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.affixes, ["prefix_nucular"])
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |Gecho stone|n crumbles away and transforms the |Cplasteel bike lock|n into"
                " |Ca nucular plasteel bike lock|n."
            )

class TestResonanceCrystal(EvenniaTest):
    """ test resonance crystals """
    def setUp(self):
        super().setUp()
        self.ql = ResonanceCrystal(spawn("resonance_crystal")[0])

    def test_can_use(self):
        """ test resonance crystal can_use """
        bike = spawn("bike_lock")[0]
        self.assertTrue(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertFalse(self.ql.can_use(bike))

    def test_use(self):
        """ test using resonance crystal """
        bike = spawn("bike_lock")[0]
        self.assertEqual(bike.tier, 1)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.tier, 2)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |yresonance crystal|n crumbles away and transforms the |xplasteel bike lock|n"
                " into |Ca plasteel bike lock|n."
            )

class TestSingularityShard(EvenniaTest):
    """ test singularity shards """
    def setUp(self):
        super().setUp()
        self.ql = SingularityShard(spawn("singularity_shard")[0])

    def test_can_use(self):
        """ test singularity shard can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertTrue(self.ql.can_use(bike))

    def test_use(self):
        """ test using singularity shard """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.tier, 1)
            self.assertEqual(bike.affixes, [])
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |[x|Xsingularity shard|n crumbles away and transforms the |Cacidic nucular"
                " plasteel bike lock|n into |xa plasteel bike lock|n."
            )

class TestPhasePearl(EvenniaTest):
    """ test phase pearls """
    def setUp(self):
        super().setUp()
        self.ql = PhasePearl(spawn("phase_pearl")[0])

    def test_can_use(self):
        """ test phase pearl can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertTrue(self.ql.can_use(bike))
        bike.tier = 3
        bike.save()
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 4
        bike.save()
        self.assertFalse(self.ql.can_use(bike))

    def test_use(self):
        """ test using phase pearl """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.tier, 3)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |530phase pearl|n crumbles away and transforms the |Cplasteel bike lock|n into"
                " |Ya plasteel bike lock|n."
            )

class TestVoidSpark(EvenniaTest):
    """ test void sparks """
    def setUp(self):
        super().setUp()
        self.ql = VoidSpark(spawn("void_spark")[0])

    def test_can_use(self):
        """ test void spark can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertFalse(self.ql.can_use(bike))
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        self.assertTrue(self.ql.can_use(bike))

    def test_use(self):
        """ test using void spark """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |Mvoid spark|n crumbles away and transforms the |Cacidic nucular plasteel bike"
                " lock|n into |Ca plasteel bike lock|n."
            )

class TestChromaticHeart(EvenniaTest):
    """ test chromatic hearts """
    def setUp(self):
        super().setUp()
        self.ql = ChromaticHeart(spawn("chromatic_heart")[0])

    def test_can_use(self):
        """ test chromatic heart can_use """
        bike = spawn("bike_lock")[0]
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertFalse(self.ql.can_use(bike))
        bike.tier = 3
        bike.save()
        self.assertTrue(self.ql.can_use(bike))
        bike.tier = 4
        bike.save()
        self.assertFalse(self.ql.can_use(bike))

    def test_use(self):
        """ test using chromatic heart """
        bike = spawn("bike_lock")[0]
        bike.tier = 3
        bike.save()
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.tier, 4)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                f"The {rainbow('chromatic heart')} crumbles away and transforms the |Yplasteel bike"
                " lock|n into |ga plasteel bike lock|n."
            )

class TestNexusDiamond(EvenniaTest):
    """ test nexus diamionds """
    def setUp(self):
        super().setUp()
        self.ql = NexusDiamond(spawn("nexus_diamond")[0])

    def test_can_use(self):
        """ test nexus diamond can_use """
        bike = spawn("bike_lock")[0]
        self.assertTrue(self.ql.can_use(bike))
        bike.tier = 2
        bike.save()
        self.assertTrue(self.ql.can_use(bike))
        bike.tier = 3
        bike.save()
        self.assertTrue(self.ql.can_use(bike))
        bike.tier = 4
        bike.save()
        self.assertFalse(self.ql.can_use(bike))

    def test_use(self):
        """ test using nexus diamond """
        bike = spawn("bike_lock")[0]
        bike.save()
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            self.ql.use(self.char1, bike)
            self.assertEqual(bike.tier, 4)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |[w|xnexus diamond|n crumbles away and transforms the |xplasteel bike lock|n"
                " into |ga plasteel bike lock|n."
            )
