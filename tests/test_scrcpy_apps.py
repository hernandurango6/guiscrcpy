import unittest

from guiscrcpy.lib.scrcpy_apps import AndroidApp, parse_scrcpy_apps


class ScrcpyAppsTest(unittest.TestCase):
    def test_parses_user_and_system_apps(self):
        output = """
scrcpy 4.0 <https://github.com/Genymobile/scrcpy>
[server] INFO: List of apps:
 * Configuración                  com.android.settings
 * Cámara                         com.android.camera
 - Brave                          com.brave.browser
 - Google Play Games              com.google.android.play.games
"""

        self.assertEqual(
            parse_scrcpy_apps(output),
            [
                AndroidApp(
                    name="Configuración",
                    package="com.android.settings",
                    system=True,
                ),
                AndroidApp(
                    name="Cámara",
                    package="com.android.camera",
                    system=True,
                ),
                AndroidApp(
                    name="Brave",
                    package="com.brave.browser",
                    system=False,
                ),
                AndroidApp(
                    name="Google Play Games",
                    package="com.google.android.play.games",
                    system=False,
                ),
            ],
        )

    def test_ignores_non_app_lines(self):
        output = """
INFO: ADB device found:
[server] INFO: Processing Android apps... (this may take some time)
D:/scrcpy/scrcpy-server: 1 file pushed
"""

        self.assertEqual(parse_scrcpy_apps(output), [])


if __name__ == "__main__":
    unittest.main()
