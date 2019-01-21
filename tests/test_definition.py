import unittest
import xconfig


class DefinitionTest(unittest.TestCase):
    def setUp(self):
        d = xconfig.Definition()
        self.definition = d

    def test_option_properties(self):
        option = xconfig.Option('Root_Option1', value_type=xconfig.Boolean, default=False, required=False,
                                hidden=False, help="TEST ME")
        self.assertEqual(option.tag, 'Root_Option1')
        self.assertEqual(option.value_type, xconfig.Boolean)
        self.assertEqual(option.default_value, False)
        self.assertEqual(option.required, False)
        self.assertEqual(option.hidden, False)
        self.assertEqual(option.help, "TEST ME")

    def test_option_properties_changes(self):
        option = xconfig.Option('Root_Option1', value_type=xconfig.Boolean, default=False, required=False,
                                hidden=False, help="TEST ME")
        option.tag = 'Root_Option2'
        option.value_type = xconfig.String
        option.default_value = True
        option.required = True
        option.hidden = True
        option.help = "TEST ME 2"

        self.assertEqual(option.tag, 'Root_Option2')
        self.assertEqual(option.value_type, xconfig.String)
        self.assertEqual(option.default_value, True)
        self.assertEqual(option.required, True)
        self.assertEqual(option.hidden, True)
        self.assertEqual(option.help, "TEST ME 2")

    def test_option_properties_failure(self):
        with self.assertRaises(ValueError):
            xconfig.Option(None, xconfig.Boolean)
        with self.assertRaises(ValueError):
            xconfig.Option('Text', None)
