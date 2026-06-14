# Configuration

guiscrcpy places a configuration file called `guiscrcpy.json` in 

## Windows
`C:\Users\<username>\AppData\Local\guiscrcpy\guiscrcpy.json`

## Linux
`$XDG_CONFIG_HOME/guiscrcpy/guiscrcpy.json` Environment Variable, which, if not defined defaults
to `~/.config/guiscrcpy/guiscrcpy.json`

The CLI are placed in `~/.local/bin` by default (PyPI) 

## macOS
`~/.config/guiscrcpy/guiscrcpy.json`

# Sample Configuration file
The configuration file uses JavaScript Object Notation, to easily retrieve and write data. A user may also edit the configuration file to edit the default settings

```json
{
    "adb": "/usr/bin/adb",
    "bitrate": 8000,
    "cmx": "",
    "dimension": null,
    "dispRO": false,
    "extra": "",
    "fullscreen": false,
    "paths": [
        "bin",
        "/usr/bin",
        "~/.local/bin",
        "~/bin",
        "/usr/local/bin"
    ],
    "scrcpy": "/usr/bin/scrcpy",
    "scrcpy_options": {
        "video_codec": "h265",
        "max_fps": 60,
        "audio_source": "playback",
        "audio_dup": true,
        "keyboard": "uhid",
        "mouse": "uhid"
    },
    "scrcpy-server": null,
    "swtouches": false
}
```

## Modern scrcpy options

The `scrcpy_options` object maps directly to supported `scrcpy` command-line
options. Empty or missing keys are ignored, and the main window controls still
override their matching legacy options.

Useful examples:

```json
{
    "scrcpy_options": {
        "video_source": "camera",
        "camera_facing": "front",
        "camera_size": "1920x1080",
        "camera_fps": 60,
        "audio_source": "mic",
        "record": "camera.mp4"
    }
}
```

```json
{
    "scrcpy_options": {
        "new_display": "1920x1080/420",
        "flex_display": true,
        "keep_active": true,
        "start_app": "org.mozilla.firefox",
        "video_codec": "h265",
        "video_bit_rate": "16M"
    }
}
```

```json
{
    "scrcpy_options": {
        "keyboard": "uhid",
        "mouse": "uhid",
        "gamepad": "uhid",
        "otg": false
    }
}
```
