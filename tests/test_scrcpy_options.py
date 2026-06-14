import unittest

from guiscrcpy.lib.scrcpy_options import ScrcpyOptions


class ScrcpyOptionsTest(unittest.TestCase):
    def test_builds_current_gui_basics(self):
        options = ScrcpyOptions(
            serial="abc123",
            max_size=1080,
            video_bit_rate="8M",
            fullscreen=True,
            always_on_top=True,
            show_touches=True,
            turn_screen_off=True,
        )

        self.assertEqual(
            options.to_args(),
            [
                "--serial",
                "abc123",
                "--max-size",
                "1080",
                "--video-bit-rate",
                "8M",
                "--fullscreen",
                "--always-on-top",
                "--show-touches",
                "--turn-screen-off",
            ],
        )

    def test_builds_camera_audio_and_recording_options(self):
        options = ScrcpyOptions(
            video_source="camera",
            camera_facing="front",
            camera_size="1920x1080",
            camera_fps=60,
            audio_source="mic",
            audio_codec="aac",
            record="capture.mp4",
            record_format="mp4",
        )

        self.assertEqual(
            options.to_args(),
            [
                "--video-source",
                "camera",
                "--audio-source",
                "mic",
                "--audio-codec",
                "aac",
                "--camera-size",
                "1920x1080",
                "--camera-facing",
                "front",
                "--camera-fps",
                "60",
                "--record",
                "capture.mp4",
                "--record-format",
                "mp4",
            ],
        )

    def test_builds_virtual_display_and_hid_options(self):
        options = ScrcpyOptions(
            tcpip="192.168.1.20:5555",
            new_display="1920x1080/420",
            flex_display=True,
            keep_active=True,
            start_app="+org.mozilla.firefox",
            keyboard="uhid",
            mouse="uhid",
            gamepad="uhid",
        )

        self.assertEqual(
            options.to_args(),
            [
                "--tcpip=192.168.1.20:5555",
                "--new-display=1920x1080/420",
                "--flex-display",
                "--start-app",
                "+org.mozilla.firefox",
                "--keyboard",
                "uhid",
                "--mouse",
                "uhid",
                "--gamepad",
                "uhid",
                "--keep-active",
            ],
        )

    def test_rejects_invalid_choices(self):
        with self.assertRaisesRegex(ValueError, "video_codec"):
            ScrcpyOptions(video_codec="vp9").to_args()

    def test_rejects_conflicting_camera_selection(self):
        with self.assertRaisesRegex(ValueError, "camera_id and camera_facing"):
            ScrcpyOptions(
                video_source="camera",
                camera_id="0",
                camera_facing="front",
            ).to_args()

    def test_rejects_conflicting_device_selection(self):
        with self.assertRaisesRegex(ValueError, "serial cannot"):
            ScrcpyOptions(serial="abc123", tcpip="192.168.1.20").to_args()


if __name__ == "__main__":
    unittest.main()
