import re
from dataclasses import dataclass
from typing import Optional, Tuple


VersionTuple = Tuple[int, int, int]


@dataclass(frozen=True)
class ScrcpyCapabilities:
    version: Optional[VersionTuple]
    audio: bool
    camera: bool
    virtual_display: bool
    flex_display: bool
    hid_input: bool
    gamepad: bool
    otg: bool


def parse_scrcpy_version(output: str) -> Optional[VersionTuple]:
    """Parse scrcpy version output into a comparable tuple."""
    match = re.search(r"\bscrcpy\s+(\d+)\.(\d+)(?:\.(\d+))?", output)
    if not match:
        return None

    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3) or 0)
    return major, minor, patch


def version_at_least(version: Optional[VersionTuple], minimum: VersionTuple) -> bool:
    return version is not None and version >= minimum


def capabilities_for_version(version: Optional[VersionTuple]) -> ScrcpyCapabilities:
    """Return feature gates for known scrcpy releases."""
    return ScrcpyCapabilities(
        version=version,
        audio=version_at_least(version, (2, 0, 0)),
        camera=version_at_least(version, (2, 2, 0)),
        virtual_display=version_at_least(version, (3, 1, 0)),
        flex_display=version_at_least(version, (4, 0, 0)),
        hid_input=version_at_least(version, (2, 0, 0)),
        gamepad=version_at_least(version, (3, 0, 0)),
        otg=version_at_least(version, (1, 24, 0)),
    )


def capabilities_from_output(output: str) -> ScrcpyCapabilities:
    return capabilities_for_version(parse_scrcpy_version(output))
