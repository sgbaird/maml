# coding: utf-8
import unittest

from maml.describers.matminer_wrapper import wrap_matminer_describer
from maml.utils import to_composition

try:
    from matminer.featurizers import composition
except ImportError:
    composition = None
from pymatgen.util.testing import PymatgenTest


@unittest.skipIf(composition is None, "matminer package is needed")
class TestWrapper(PymatgenTest):
    @classmethod
    def setUp(cls) -> None:
        cls.s_li2o = PymatgenTest.get_structure("Li2O")
        cls.s_lfp = PymatgenTest.get_structure("LiFePO4")

    def test_element_prop(self):
        ElementProperty = wrap_matminer_describer(
            "ElementProperty", composition.ElementProperty, to_composition, describer_type="composition"
        )
        ep = ElementProperty.from_preset("magpie")
        self.assertArrayAlmostEqual(ep.transform_one(self.s_li2o).values, ep.transform_one("Li2O").values)
        self.assertListEqual(ep._get_param_names(), ["data_source", "features", "stats"])

    def test_atomic_orbitals(self):

        AtomicOrbitals = wrap_matminer_describer(
            "AtomicOrbitals", composition.AtomicOrbitals, to_composition, describer_type="composition"
        )
        ao = AtomicOrbitals()
        for i, j in zip(ao.transform_one("LiFePO4").values, ao.transform_one(self.s_lfp).values):
            for k, l in zip(i, j):
                self.assertEqual(k, l)


if __name__ == "__main__":
    unittest.main()
