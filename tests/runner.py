import subprocess
import pytest


def run(cmd):
    cmd = cmd.split()
    try:
        return subprocess.check_output(cmd)
    except Exception as e:
        print(e.output)
        pytest.fail(e)
