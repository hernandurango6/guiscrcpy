"""
GUISCRCPY by srevinsaju
Get it on : https://github.com/srevinsaju/guiscrcpy
Licensed under GNU Public License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from guiscrcpy.ux import Ui_SettingsWindow


class InterfaceSettings(QMainWindow, Ui_SettingsWindow):
    # there was a Dialog in the bracket
    def __init__(self, parent):
        QMainWindow.__init__(self)
        Ui_SettingsWindow.__init__(self)
        self.setupUi(self)
        self.parent = parent
        self.commands = []
        self.checkboxes = {
            self.a1: [[None], "--always-on-top", 0],
            self.a2: [[self.a2c1, self.a2c2], "--crop {}:{}", 1],
            self.a3: [[self.a3e1], "--max-fps {}"],
            self.a4: [[None], "--prefer-text"],
            self.a5: [[self.a5c1], "--push-target {}"],
            self.a6: [[self.a6c1], "--record {}"],
            self.a8: [[self.a8c1], "--serial {}"],
            self.a9: [[None], "--window-borderless"],
            self.b0: [[self.b0c1], "--window-title {}"],
            self.b1: [[self.b1c1, self.b1c1], "--window-x {} --window-y {}"],
            self.b2: [[self.b2c1, self.b2c2], "--window-width {} --window-height {}"],
        }
        self._build_scrcpy4_panel()

    def _build_scrcpy4_panel(self):
        self.resize(760, 760)
        self.modern_group = QGroupBox("scrcpy 4.0", self.centralwidget)
        self.modern_group.setGeometry(0, 425, 740, 285)
        layout = QGridLayout(self.modern_group)

        self.video_source = QComboBox(self.modern_group)
        self.video_source.addItems(["", "display", "camera"])
        self.video_codec = QComboBox(self.modern_group)
        self.video_codec.addItems(["", "h264", "h265", "av1"])
        self.max_fps = QSpinBox(self.modern_group)
        self.max_fps.setRange(0, 240)

        self.disable_audio = QCheckBox("Disable audio", self.modern_group)
        self.audio_source = QComboBox(self.modern_group)
        self.audio_source.addItems(
            [
                "",
                "output",
                "playback",
                "mic",
                "mic-unprocessed",
                "mic-camcorder",
                "mic-voice-recognition",
                "mic-voice-communication",
                "voice-call",
                "voice-call-uplink",
                "voice-call-downlink",
                "voice-performance",
            ]
        )
        self.audio_codec = QComboBox(self.modern_group)
        self.audio_codec.addItems(["", "opus", "aac", "flac", "raw"])
        self.audio_dup = QCheckBox("Audio dup", self.modern_group)

        self.camera_facing = QComboBox(self.modern_group)
        self.camera_facing.addItems(["", "front", "back", "external"])
        self.camera_size = QLineEdit(self.modern_group)
        self.camera_size.setPlaceholderText("1920x1080")
        self.camera_fps = QSpinBox(self.modern_group)
        self.camera_fps.setRange(0, 240)
        self.camera_torch = QCheckBox("Torch", self.modern_group)

        self.enable_new_display = QCheckBox("New display", self.modern_group)
        self.new_display = QLineEdit(self.modern_group)
        self.new_display.setPlaceholderText("1920x1080/420")
        self.flex_display = QCheckBox("Flex", self.modern_group)
        self.keep_active = QCheckBox("Keep active", self.modern_group)
        self.start_app = QLineEdit(self.modern_group)
        self.start_app.setPlaceholderText("org.mozilla.firefox")

        self.keyboard_mode = QComboBox(self.modern_group)
        self.keyboard_mode.addItems(["", "sdk", "uhid", "aoa", "disabled"])
        self.mouse_mode = QComboBox(self.modern_group)
        self.mouse_mode.addItems(["", "sdk", "uhid", "aoa", "disabled"])
        self.gamepad_mode = QComboBox(self.modern_group)
        self.gamepad_mode.addItems(["", "uhid", "aoa", "disabled"])
        self.otg = QCheckBox("OTG", self.modern_group)
        self.list_apps_button = QPushButton("Apps", self.modern_group)
        self.list_cameras_button = QPushButton("Cameras", self.modern_group)
        self.list_displays_button = QPushButton("Displays", self.modern_group)
        self.list_encoders_button = QPushButton("Encoders", self.modern_group)

        layout.addWidget(QLabel("Video source"), 0, 0)
        layout.addWidget(self.video_source, 0, 1)
        layout.addWidget(QLabel("Video codec"), 0, 2)
        layout.addWidget(self.video_codec, 0, 3)
        layout.addWidget(QLabel("Max FPS"), 0, 4)
        layout.addWidget(self.max_fps, 0, 5)

        layout.addWidget(self.disable_audio, 1, 0)
        layout.addWidget(QLabel("Audio source"), 1, 1)
        layout.addWidget(self.audio_source, 1, 2)
        layout.addWidget(QLabel("Audio codec"), 1, 3)
        layout.addWidget(self.audio_codec, 1, 4)
        layout.addWidget(self.audio_dup, 1, 5)

        layout.addWidget(QLabel("Camera facing"), 2, 0)
        layout.addWidget(self.camera_facing, 2, 1)
        layout.addWidget(QLabel("Camera size"), 2, 2)
        layout.addWidget(self.camera_size, 2, 3)
        layout.addWidget(QLabel("Camera FPS"), 2, 4)
        layout.addWidget(self.camera_fps, 2, 5)
        layout.addWidget(self.camera_torch, 3, 0)

        layout.addWidget(self.enable_new_display, 4, 0)
        layout.addWidget(self.new_display, 4, 1, 1, 2)
        layout.addWidget(self.flex_display, 4, 3)
        layout.addWidget(self.keep_active, 4, 4)
        layout.addWidget(QLabel("Start app"), 5, 0)
        layout.addWidget(self.start_app, 5, 1, 1, 5)

        layout.addWidget(QLabel("Keyboard"), 6, 0)
        layout.addWidget(self.keyboard_mode, 6, 1)
        layout.addWidget(QLabel("Mouse"), 6, 2)
        layout.addWidget(self.mouse_mode, 6, 3)
        layout.addWidget(QLabel("Gamepad"), 6, 4)
        layout.addWidget(self.gamepad_mode, 6, 5)
        layout.addWidget(self.otg, 7, 0)
        layout.addWidget(QLabel("List from device"), 7, 1)
        layout.addWidget(self.list_apps_button, 7, 2)
        layout.addWidget(self.list_cameras_button, 7, 3)
        layout.addWidget(self.list_displays_button, 7, 4)
        layout.addWidget(self.list_encoders_button, 7, 5)

    def init(self):
        self._load_scrcpy4_options()
        self.updatebutton.clicked.connect(self.complete)
        self.a6d1.clicked.connect(self.file_chooser)
        self.list_apps_button.clicked.connect(
            lambda: self._show_scrcpy_info("Apps", ["--list-apps"])
        )
        self.list_cameras_button.clicked.connect(
            lambda: self._show_scrcpy_info("Cameras", ["--list-cameras"])
        )
        self.list_displays_button.clicked.connect(
            lambda: self._show_scrcpy_info("Displays", ["--list-displays"])
        )
        self.list_encoders_button.clicked.connect(
            lambda: self._show_scrcpy_info("Encoders", ["--list-encoders"])
        )
        self.show()

    def _show_scrcpy_info(self, title, args):
        try:
            output = self.parent.scrcpy.run_info(args)
        except Exception as err:
            QMessageBox.warning(self, title, "Could not run scrcpy: {}".format(err))
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(720, 420)
        layout = QVBoxLayout(dialog)
        text = QTextEdit(dialog)
        text.setReadOnly(True)
        text.setPlainText(output.strip() or "No output")
        layout.addWidget(text)
        dialog.exec_()

    @staticmethod
    def _set_combo(combo, value):
        index = combo.findText(value or "")
        combo.setCurrentIndex(index if index >= 0 else 0)

    @staticmethod
    def _combo_value(combo):
        value = combo.currentText().strip()
        return value or None

    def _load_scrcpy4_options(self):
        options = self.parent.config.get("scrcpy_options", {})
        self._set_combo(self.video_source, options.get("video_source"))
        self._set_combo(self.video_codec, options.get("video_codec"))
        self.max_fps.setValue(int(options.get("max_fps") or 0))

        self.disable_audio.setChecked(bool(options.get("no_audio")))
        self._set_combo(self.audio_source, options.get("audio_source"))
        self._set_combo(self.audio_codec, options.get("audio_codec"))
        self.audio_dup.setChecked(bool(options.get("audio_dup")))

        self._set_combo(self.camera_facing, options.get("camera_facing"))
        self.camera_size.setText(options.get("camera_size") or "")
        self.camera_fps.setValue(int(options.get("camera_fps") or 0))
        self.camera_torch.setChecked(bool(options.get("camera_torch")))

        new_display = options.get("new_display")
        self.enable_new_display.setChecked(new_display is not None)
        self.new_display.setText(new_display or "")
        self.flex_display.setChecked(bool(options.get("flex_display")))
        self.keep_active.setChecked(bool(options.get("keep_active")))
        self.start_app.setText(options.get("start_app") or "")

        self._set_combo(self.keyboard_mode, options.get("keyboard"))
        self._set_combo(self.mouse_mode, options.get("mouse"))
        self._set_combo(self.gamepad_mode, options.get("gamepad"))
        self.otg.setChecked(bool(options.get("otg")))

    def _collect_scrcpy4_options(self):
        options = {}

        for key, value in {
            "video_source": self._combo_value(self.video_source),
            "video_codec": self._combo_value(self.video_codec),
            "audio_source": self._combo_value(self.audio_source),
            "audio_codec": self._combo_value(self.audio_codec),
            "camera_facing": self._combo_value(self.camera_facing),
            "camera_size": self.camera_size.text().strip() or None,
            "start_app": self.start_app.text().strip() or None,
            "keyboard": self._combo_value(self.keyboard_mode),
            "mouse": self._combo_value(self.mouse_mode),
            "gamepad": self._combo_value(self.gamepad_mode),
        }.items():
            if value:
                options[key] = value

        for key, value in {
            "max_fps": self.max_fps.value(),
            "camera_fps": self.camera_fps.value(),
        }.items():
            if value:
                options[key] = value

        for key, value in {
            "no_audio": self.disable_audio.isChecked(),
            "audio_dup": self.audio_dup.isChecked(),
            "camera_torch": self.camera_torch.isChecked(),
            "flex_display": self.flex_display.isChecked(),
            "keep_active": self.keep_active.isChecked(),
            "otg": self.otg.isChecked(),
        }.items():
            if value:
                options[key] = value

        if self.enable_new_display.isChecked():
            options["new_display"] = self.new_display.text().strip()

        return options

    def file_chooser(self):
        dialog = QFileDialog()
        dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
        dialog.setDefaultSuffix("mp4")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["H.264 (*.mp4)", "MKV (*.mkv)"])
        if dialog.exec_() == QDialog.Accepted:
            self.a6c1.setText(dialog.selectedFiles()[0])

    def checkboxes_act(self, args):
        pass

    def complete(self):
        x = []
        for i in self.checkboxes:
            if i.isChecked():
                box = self.checkboxes[i]
                cmd = box[1]
                cmd_args = []
                for j in box[0]:
                    if j is None:
                        break
                    else:
                        try:
                            arg = j.text()
                            print(arg)
                        except (AttributeError, NameError, ValueError):
                            arg = j.value()
                            print(arg)
                        cmd_args.append(arg)
                else:
                    cmd = cmd.format(*cmd_args)
                print(cmd)
                x.append(cmd)
        print(x)
        self.hide()
        self.parent.cmx = x
        self.parent.config["scrcpy_options"] = self._collect_scrcpy4_options()
        self.parent.config_manager.update_config(self.parent.config)
        self.parent.config_manager.write_file()

    def cancel(self):
        pass
