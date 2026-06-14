import unittest

from guiscrcpy.lib.scrcpy_version import (
    capabilities_from_output,
    capabilities_for_version,
    parse_scrcpy_version,
    version_at_least,
)


class ScrcpyVersionTest(unittest.TestCase):
    def test_parses_major_minor_patch(self):
        self.assertEqual(parse_scrcpy_version("scrcpy 4.0\n"), (4, 0, 0))
        self.assertEqual(parse_scrcpy_version("scrcpy 3.3.4 <info>\n"), (3, 3, 4))

    def test_returns_none_for_unknown_output(self):
        self.assertIsNone(parse_scrcpy_version("not scrcpy"))

    def test_version_comparison_handles_unknown(self):
        self.assertFalse(version_at_least(None, (4, 0, 0)))
        self.assertTrue(version_at_least((4, 0, 0), (4, 0, 0)))
        self.assertTrue(version_at_least((4, 1, 0), (4, 0, 0)))
        self.assertFalse(version_at_least((3, 3, 4), (4, 0, 0)))

    def test_capabilities_for_scrcpy_4(self):
        capabilities = capabilities_from_output("scrcpy 4.0\n")

        self.assertEqual(capabilities.version, (4, 0, 0))
        self.assertTrue(capabilities.audio)
        self.assertTrue(capabilities.camera)
        self.assertTrue(capabilities.virtual_display)
        self.assertTrue(capabilities.flex_display)
        self.assertTrue(capabilities.hid_input)
        self.assertTrue(capabilities.gamepad)
        self.assertTrue(capabilities.otg)

    def test_capabilities_for_old_or_unknown_versions(self):
        old = capabilities_for_version((1, 23, 0))
        unknown = capabilities_for_version(None)

        self.assertFalse(old.audio)
        self.assertFalse(old.otg)
        self.assertFalse(unknown.audio)
        self.assertFalse(unknown.virtual_display)


if __name__ == "__main__":
    unittest.main()
