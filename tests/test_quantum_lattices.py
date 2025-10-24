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
        self.ql = spawn("dust_shard")[0]
        self.randint_patcher = patch("random.randint")
        self.mock_randint = self.randint_patcher.start()

    def tearDown(self):
        self.randint_patcher.stop()
        super().tearDown()

    def test_can_use(self):
        """ test dust shard can_use """
        bike = spawn("bike_lock")[0]
        dust_shard = DustShard(self.ql, bike)
        self.assertFalse(dust_shard.can_use())
        bike.tier = 2
        bike.save()
        self.assertFalse(dust_shard.can_use())
        bike.affixes.append("prefix_acidic")
        bike.save()
        self.assertTrue(dust_shard.can_use())

    def test_use(self):
        """ test using dust shard """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        bike.affixes.append("prefix_acidic")
        dust_shard = DustShard(self.ql, bike)
        self.mock_randint.return_value = 2
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            dust_shard.use(self.char1)
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
        self.ql = spawn("static_bloom")[0]

    def test_can_use(self):
        """ test static bloom can_use """
        bike = spawn("bike_lock")[0]
        static_bloom = StaticBloom(self.ql, bike)
        self.assertFalse(static_bloom.can_use())
        bike.tier = 2
        bike.save()
        self.assertFalse(static_bloom.can_use())
        bike.affixes.append("prefix_acidic")
        bike.save()
        self.assertTrue(static_bloom.can_use())

    def test_use(self):
        """ test using static bloom """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        bike.affixes.append("prefix_acidic")
        static_bloom = StaticBloom(self.ql, bike)
        with patch("world.quantum_lattices.EvMenu") as mock_ev_menu:
            static_bloom.use(self.char1)
            mock_ev_menu.assert_called_with(
                self.char1,
                {
                    "node_select_affix": static_bloom._node_select_affix,
                    "node_end_menu": static_bloom._node_end_menu,
                },
                startnode="node_select_affix",
                cmd_on_exit=None
            )
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            static_bloom._node_end_menu(self.char1, "")
            self.assertEqual(bike.affixes, ["prefix_acidic"])
            mock_at_post_use.assert_not_called()
            static_bloom._node_end_menu(self.char1, "", affix_to_remove="prefix_acidic")
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
        self.ql = spawn("echo_stone")[0]
        self.randint_patcher = patch("random.randint")
        self.mock_randint = self.randint_patcher.start()

    def tearDown(self):
        self.randint_patcher.stop()
        super().tearDown()

    def test_can_use(self):
        """ test echo stone can_use """
        bike = spawn("bike_lock")[0]
        echo_stone = EchoStone(self.ql, bike)
        self.assertFalse(echo_stone.can_use())
        bike.tier = 2
        bike.save()
        self.assertTrue(echo_stone.can_use())
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        self.assertFalse(echo_stone.can_use())

    def test_use(self):
        """ test using echo stone """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        echo_stone = EchoStone(self.ql, bike)
        self.mock_randint.return_value = 2
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            echo_stone.use(self.char1)
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
        self.ql = spawn("resonance_crystal")[0]

    def test_can_use(self):
        """ test resonance crystal can_use """
        bike = spawn("bike_lock")[0]
        resonance_crystal = ResonanceCrystal(self.ql, bike)
        self.assertTrue(resonance_crystal.can_use())
        bike.tier = 2
        bike.save()
        self.assertFalse(resonance_crystal.can_use())

    def test_use(self):
        """ test using resonance crystal """
        bike = spawn("bike_lock")[0]
        self.assertEqual(bike.tier, 1)
        resonance_crystal = ResonanceCrystal(self.ql, bike)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            resonance_crystal.use(self.char1)
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
        self.ql = spawn("singularity_shard")[0]

    def test_can_use(self):
        """ test singularity shard can_use """
        bike = spawn("bike_lock")[0]
        singularity_shard = SingularityShard(self.ql, bike)
        self.assertFalse(singularity_shard.can_use())
        bike.tier = 2
        bike.save()
        self.assertTrue(singularity_shard.can_use())

    def test_use(self):
        """ test using singularity shard """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        singularity_shard = SingularityShard(self.ql, bike)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            singularity_shard.use(self.char1)
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
        self.ql = spawn("phase_pearl")[0]

    def test_can_use(self):
        """ test phase pearl can_use """
        bike = spawn("bike_lock")[0]
        phase_pearl = PhasePearl(self.ql, bike)
        self.assertFalse(phase_pearl.can_use())
        bike.tier = 2
        bike.save()
        self.assertTrue(phase_pearl.can_use())
        bike.tier = 3
        bike.save()
        self.assertFalse(phase_pearl.can_use())
        bike.tier = 4
        bike.save()
        self.assertFalse(phase_pearl.can_use())

    def test_use(self):
        """ test using phase pearl """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.save()
        phase_pearl = PhasePearl(self.ql, bike)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            phase_pearl.use(self.char1)
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
        self.ql = spawn("void_spark")[0]

    def test_can_use(self):
        """ test void spark can_use """
        bike = spawn("bike_lock")[0]
        void_spark = VoidSpark(self.ql, bike)
        self.assertFalse(void_spark.can_use())
        bike.tier = 2
        bike.save()
        self.assertFalse(void_spark.can_use())
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        self.assertTrue(void_spark.can_use())

    def test_use(self):
        """ test using void spark """
        bike = spawn("bike_lock")[0]
        bike.tier = 2
        bike.affixes = ["prefix_acidic", "prefix_nucular"]
        bike.save()
        void_spark = VoidSpark(self.ql, bike)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            void_spark.use(self.char1)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |Mvoid spark|n crumbles away and transforms the |Cacidic nucular plasteel bike"
                " lock|n into |Ca plasteel bike lock|n."
            )

class TestChromaticHeart(EvenniaTest):
    """ test chromatic hearts """
    def setUp(self):
        super().setUp()
        self.ql = spawn("chromatic_heart")[0]

    def test_can_use(self):
        """ test chromatic heart can_use """
        bike = spawn("bike_lock")[0]
        chromatic_heart = ChromaticHeart(self.ql, bike)
        self.assertFalse(chromatic_heart.can_use())
        bike.tier = 2
        bike.save()
        self.assertFalse(chromatic_heart.can_use())
        bike.tier = 3
        bike.save()
        self.assertTrue(chromatic_heart.can_use())
        bike.tier = 4
        bike.save()
        self.assertFalse(chromatic_heart.can_use())

    def test_use(self):
        """ test using chromatic heart """
        bike = spawn("bike_lock")[0]
        bike.tier = 3
        bike.save()
        chromatic_heart = ChromaticHeart(self.ql, bike)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            chromatic_heart.use(self.char1)
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
        self.ql = spawn("nexus_diamond")[0]

    def test_can_use(self):
        """ test nexus diamond can_use """
        bike = spawn("bike_lock")[0]
        nexus_diamond = NexusDiamond(self.ql, bike)
        self.assertTrue(nexus_diamond.can_use())
        bike.tier = 2
        bike.save()
        self.assertTrue(nexus_diamond.can_use())
        bike.tier = 3
        bike.save()
        self.assertTrue(nexus_diamond.can_use())
        bike.tier = 4
        bike.save()
        self.assertFalse(nexus_diamond.can_use())

    def test_use(self):
        """ test using nexus diamond """
        bike = spawn("bike_lock")[0]
        bike.save()
        nexus_diamond = NexusDiamond(self.ql, bike)
        with patch("typeclasses.objects.QuantumLatticeObject.at_post_use") as mock_at_post_use:
            nexus_diamond.use(self.char1)
            self.assertEqual(bike.tier, 4)
            mock_at_post_use.assert_called_once_with(
                self.char1,
                "The |[w|xnexus diamond|n crumbles away and transforms the |xplasteel bike lock|n"
                " into |ga plasteel bike lock|n."
            )
