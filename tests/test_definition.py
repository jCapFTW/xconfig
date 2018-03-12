import unittest
import xconfig


class IniTest(unittest.TestCase):
    def setUp(self):
        d = xconfig.Definition()
        self.definition = d

    def test_option_properties(self):
        option = xconfig.Option('Root_Option1', value_type=xconfig.Boolean, default=False, required=False,
                                force_write=False, help="TEST")
        assert(option.tag == 'Root_Option1')
        assert(option.value_type == xconfig.Boolean)
        assert(not option.default_value)
        assert(not option.is_required)
        assert(not option.force_write)
        assert(option.help == "TEST")


if __name__ == '__main__':
    unittest.main()
