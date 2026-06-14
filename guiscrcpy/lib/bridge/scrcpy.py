import os
from subprocess import PIPE

from .base import Bridge
from ...lib.utils import open_process
from ...lib.scrcpy_version import capabilities_from_output, parse_scrcpy_version


class ScrcpyBridge(Bridge):
    name = "scrcpy"

    def post_init(self):
        if os.getenv("SCRCPY_LDD"):
            if os.getenv("LD_LIBRARY_PATH"):
                os.environ["LD_LIBRARY_PATH"] += os.getenv("SCRCPY_LDD")
            else:
                os.environ["LD_LIBRARY_PATH"] = os.getenv("SCRCPY_LDD")

    def start(self, args, stdout=PIPE, stderr=PIPE):
        proc = open_process(
            [self.path] + args,
            stdout=stdout,
            stderr=stderr,
        )
        return proc

    def version_output(self):
        proc = open_process([self.path, "--version"], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate(timeout=5)
        output = out.decode(errors="replace")
        if err:
            output += "\n" + err.decode(errors="replace")
        return output

    def version(self):
        return parse_scrcpy_version(self.version_output())

    def capabilities(self):
        return capabilities_from_output(self.version_output())
