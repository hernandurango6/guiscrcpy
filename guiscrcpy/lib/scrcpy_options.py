from dataclasses import dataclass
from typing import List, Optional


_VIDEO_CODECS = {"h264", "h265", "av1"}
_AUDIO_CODECS = {"opus", "aac", "flac", "raw"}
_AUDIO_SOURCES = {
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
}
_VIDEO_SOURCES = {"display", "camera"}
_CAMERA_FACING = {"front", "back", "external"}
_INPUT_MODES = {"disabled", "sdk", "uhid", "aoa"}
_GAMEPAD_MODES = {"disabled", "uhid", "aoa"}
_RECORD_FORMATS = {"mp4", "mkv", "m4a", "mka", "opus", "aac", "flac", "wav"}
_RENDER_FITS = {"letterbox", "unscaled", "stretched"}
_DISPLAY_IME_POLICIES = {"local", "fallback"}


def _append_value(args: List[str], flag: str, value: Optional[object]) -> None:
    if value is not None and value != "":
        args.extend([flag, str(value)])


def _validate_choice(name: str, value: Optional[str], choices: set) -> None:
    if value is not None and value not in choices:
        raise ValueError(
            "{} must be one of: {}".format(name, ", ".join(sorted(choices)))
        )


@dataclass
class ScrcpyOptions:
    """Build scrcpy command-line arguments from structured options."""

    serial: Optional[str] = None
    select_usb: bool = False
    select_tcpip: bool = False
    tcpip: Optional[str] = None

    max_size: Optional[int] = None
    video_bit_rate: Optional[str] = None
    max_fps: Optional[int] = None
    video_codec: Optional[str] = None
    video_encoder: Optional[str] = None
    video_source: str = "display"
    crop: Optional[str] = None
    capture_orientation: Optional[str] = None
    display_orientation: Optional[str] = None
    record_orientation: Optional[str] = None
    angle: Optional[float] = None
    display_id: Optional[int] = None
    no_downsize_on_error: bool = False
    min_size_alignment: Optional[int] = None

    no_audio: bool = False
    require_audio: bool = False
    audio_source: Optional[str] = None
    audio_codec: Optional[str] = None
    audio_encoder: Optional[str] = None
    audio_bit_rate: Optional[str] = None
    audio_buffer: Optional[int] = None
    audio_output_buffer: Optional[int] = None
    audio_dup: bool = False
    no_audio_playback: bool = False

    camera_id: Optional[str] = None
    camera_size: Optional[str] = None
    camera_facing: Optional[str] = None
    camera_ar: Optional[str] = None
    camera_fps: Optional[int] = None
    camera_high_speed: bool = False
    camera_torch: bool = False
    camera_zoom: Optional[float] = None

    new_display: Optional[str] = None
    flex_display: bool = False
    no_vd_system_decorations: bool = False
    no_vd_destroy_content: bool = False
    display_ime_policy: Optional[str] = None
    start_app: Optional[str] = None

    keyboard: Optional[str] = None
    mouse: Optional[str] = None
    gamepad: Optional[str] = None
    otg: bool = False
    no_control: bool = False
    no_mouse_hover: bool = False
    mouse_bind: Optional[str] = None

    record: Optional[str] = None
    record_format: Optional[str] = None
    time_limit: Optional[int] = None
    no_playback: bool = False
    no_video: bool = False
    no_video_playback: bool = False
    no_window: bool = False

    fullscreen: bool = False
    always_on_top: bool = False
    window_title: Optional[str] = None
    window_borderless: bool = False
    window_x: Optional[int] = None
    window_y: Optional[int] = None
    window_width: Optional[int] = None
    window_height: Optional[int] = None
    background_color: Optional[str] = None
    render_fit: Optional[str] = None
    disable_screensaver: bool = False

    show_touches: bool = False
    turn_screen_off: bool = False
    stay_awake: bool = False
    keep_active: bool = False
    power_off_on_close: bool = False
    no_power_on: bool = False

    list_apps: bool = False
    list_cameras: bool = False
    list_camera_sizes: bool = False
    list_displays: bool = False
    list_encoders: bool = False
    print_fps: bool = False

    def validate(self) -> None:
        _validate_choice("video_codec", self.video_codec, _VIDEO_CODECS)
        _validate_choice("audio_codec", self.audio_codec, _AUDIO_CODECS)
        _validate_choice("audio_source", self.audio_source, _AUDIO_SOURCES)
        _validate_choice("video_source", self.video_source, _VIDEO_SOURCES)
        _validate_choice("camera_facing", self.camera_facing, _CAMERA_FACING)
        _validate_choice("keyboard", self.keyboard, _INPUT_MODES)
        _validate_choice("mouse", self.mouse, _INPUT_MODES)
        _validate_choice("gamepad", self.gamepad, _GAMEPAD_MODES)
        _validate_choice("record_format", self.record_format, _RECORD_FORMATS)
        _validate_choice("render_fit", self.render_fit, _RENDER_FITS)
        _validate_choice(
            "display_ime_policy",
            self.display_ime_policy,
            _DISPLAY_IME_POLICIES,
        )

        if self.camera_id and self.camera_facing:
            raise ValueError("camera_id and camera_facing cannot be used together")
        if self.camera_size and (self.max_size or self.camera_ar):
            raise ValueError(
                "camera_size cannot be combined with max_size or camera_ar"
            )
        if self.serial and (self.select_usb or self.select_tcpip or self.tcpip):
            raise ValueError(
                "serial cannot be combined with select_usb, select_tcpip or tcpip"
            )
        if self.select_usb and self.select_tcpip:
            raise ValueError("select_usb and select_tcpip cannot both be enabled")

    def to_args(self) -> List[str]:
        self.validate()
        args: List[str] = []

        _append_value(args, "--serial", self.serial)
        if self.select_usb:
            args.append("--select-usb")
        if self.select_tcpip:
            args.append("--select-tcpip")
        if self.tcpip is not None:
            args.append(
                "--tcpip" if self.tcpip == "" else "--tcpip={}".format(self.tcpip)
            )

        _append_value(args, "--max-size", self.max_size)
        _append_value(args, "--video-bit-rate", self.video_bit_rate)
        _append_value(args, "--max-fps", self.max_fps)
        _append_value(args, "--video-codec", self.video_codec)
        _append_value(args, "--video-encoder", self.video_encoder)
        if self.video_source != "display":
            _append_value(args, "--video-source", self.video_source)
        _append_value(args, "--crop", self.crop)
        _append_value(args, "--capture-orientation", self.capture_orientation)
        _append_value(args, "--display-orientation", self.display_orientation)
        _append_value(args, "--record-orientation", self.record_orientation)
        _append_value(args, "--angle", self.angle)
        _append_value(args, "--display-id", self.display_id)
        _append_value(args, "--min-size-alignment", self.min_size_alignment)
        if self.no_downsize_on_error:
            args.append("--no-downsize-on-error")

        if self.no_audio:
            args.append("--no-audio")
        if self.require_audio:
            args.append("--require-audio")
        _append_value(args, "--audio-source", self.audio_source)
        _append_value(args, "--audio-codec", self.audio_codec)
        _append_value(args, "--audio-encoder", self.audio_encoder)
        _append_value(args, "--audio-bit-rate", self.audio_bit_rate)
        _append_value(args, "--audio-buffer", self.audio_buffer)
        _append_value(args, "--audio-output-buffer", self.audio_output_buffer)
        if self.audio_dup:
            args.append("--audio-dup")
        if self.no_audio_playback:
            args.append("--no-audio-playback")

        _append_value(args, "--camera-id", self.camera_id)
        _append_value(args, "--camera-size", self.camera_size)
        _append_value(args, "--camera-facing", self.camera_facing)
        _append_value(args, "--camera-ar", self.camera_ar)
        _append_value(args, "--camera-fps", self.camera_fps)
        _append_value(args, "--camera-zoom", self.camera_zoom)
        if self.camera_high_speed:
            args.append("--camera-high-speed")
        if self.camera_torch:
            args.append("--camera-torch")

        if self.new_display is not None:
            args.append(
                "--new-display"
                if self.new_display == ""
                else "--new-display={}".format(self.new_display)
            )
        if self.flex_display:
            args.append("--flex-display")
        if self.no_vd_system_decorations:
            args.append("--no-vd-system-decorations")
        if self.no_vd_destroy_content:
            args.append("--no-vd-destroy-content")
        _append_value(args, "--display-ime-policy", self.display_ime_policy)
        _append_value(args, "--start-app", self.start_app)

        _append_value(args, "--keyboard", self.keyboard)
        _append_value(args, "--mouse", self.mouse)
        _append_value(args, "--gamepad", self.gamepad)
        if self.otg:
            args.append("--otg")
        if self.no_control:
            args.append("--no-control")
        if self.no_mouse_hover:
            args.append("--no-mouse-hover")
        _append_value(args, "--mouse-bind", self.mouse_bind)

        _append_value(args, "--record", self.record)
        _append_value(args, "--record-format", self.record_format)
        _append_value(args, "--time-limit", self.time_limit)
        if self.no_playback:
            args.append("--no-playback")
        if self.no_video:
            args.append("--no-video")
        if self.no_video_playback:
            args.append("--no-video-playback")
        if self.no_window:
            args.append("--no-window")

        if self.fullscreen:
            args.append("--fullscreen")
        if self.always_on_top:
            args.append("--always-on-top")
        _append_value(args, "--window-title", self.window_title)
        if self.window_borderless:
            args.append("--window-borderless")
        _append_value(args, "--window-x", self.window_x)
        _append_value(args, "--window-y", self.window_y)
        _append_value(args, "--window-width", self.window_width)
        _append_value(args, "--window-height", self.window_height)
        _append_value(args, "--background-color", self.background_color)
        _append_value(args, "--render-fit", self.render_fit)
        if self.disable_screensaver:
            args.append("--disable-screensaver")

        if self.show_touches:
            args.append("--show-touches")
        if self.turn_screen_off:
            args.append("--turn-screen-off")
        if self.stay_awake:
            args.append("--stay-awake")
        if self.keep_active:
            args.append("--keep-active")
        if self.power_off_on_close:
            args.append("--power-off-on-close")
        if self.no_power_on:
            args.append("--no-power-on")

        if self.list_apps:
            args.append("--list-apps")
        if self.list_cameras:
            args.append("--list-cameras")
        if self.list_camera_sizes:
            args.append("--list-camera-sizes")
        if self.list_displays:
            args.append("--list-displays")
        if self.list_encoders:
            args.append("--list-encoders")
        if self.print_fps:
            args.append("--print-fps")

        return args
