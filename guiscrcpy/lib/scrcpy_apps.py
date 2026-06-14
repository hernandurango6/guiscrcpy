import re
from dataclasses import dataclass
from typing import List


_APP_LINE_RE = re.compile(r"^\s*([*-])\s+(.+?)\s{2,}([\w.]+)\s*$")


@dataclass(frozen=True)
class AndroidApp:
    """Android app entry reported by scrcpy --list-apps."""

    name: str
    package: str
    system: bool = False


def parse_scrcpy_apps(output: str) -> List[AndroidApp]:
    """Parse scrcpy --list-apps output."""
    apps: List[AndroidApp] = []
    for line in output.splitlines():
        match = _APP_LINE_RE.match(line)
        if not match:
            continue

        marker, name, package = match.groups()
        apps.append(
            AndroidApp(
                name=name.strip(),
                package=package.strip(),
                system=marker == "*",
            )
        )
    return apps
