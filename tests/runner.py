import subprocess


def run(cmd):
    cmd = cmd.split()
    try:
        return subprocess.check_output(cmd)
    except Exception as e:
        pytest.fail(e)
