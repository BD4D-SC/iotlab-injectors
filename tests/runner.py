import subprocess


def run(cmd):
    cmd = cmd.split()
    try:
        return subprocess.check_output(cmd,
                   stderr=subprocess.STDOUT)
    except Exception as e:
        raise e
