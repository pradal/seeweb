""" Manage workspace associated with each user
"""
from os import chdir, getcwd, mkdir
from os.path import dirname, exists, join
from subprocess import PIPE, Popen

from seeweb.views.tools import source_pth


def workspace_pth(uid):
    root = dirname(dirname(dirname(dirname(__file__))))
    return join(root, "see_playground", uid)


def has_workspace(uid):
    """Check whether a given user already has a workspace
    """
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("conda info --envs\n")
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    envs = [line.split(" ")[0] for line in lines[3:-2]]

    return uid in envs


def create_workspace(uid):
    """Create a Python27 workspace environment
    for a given user.
    """
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("conda create -y -q -n %s python\n" % uid)
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]
    return ans


def remove_workspace(uid):
    """Create a Python27 workspace environment
    for a given user.
    """
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("conda remove -y -q -n %s --all\n" % uid)
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]
    return ans


def install_project(uid, pid):  # TODO dependencies
    """Install python project in current user workspace
    """
    cwd = getcwd()
    ppth = source_pth(pid)
    if not exists(ppth):
        raise UserWarning("no source directory")

    if not exists(join(ppth, "setup.py")):
        raise UserWarning("no setup.py found")

    chdir(ppth)
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("activate %s\n" % uid)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("python setup.py install\n")
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]

    chdir(cwd)
    return ans


def uninstall_project(uid, pid):  # TODO dependencies
    """Install python project in current user workspace
    """
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("activate %s\n" % uid)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("pip uninstall -y %s\n" % pid)
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]

    return ans


def exec_python_script(uid, script):
    """Execute a python script in user environment.
    """
    cwd = getcwd()
    wpth = workspace_pth(uid)
    if not exists(wpth):
        mkdir(wpth)

    chdir(wpth)
    with open("current_script.py", 'w') as f:
        f.write(script)

    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("activate %s\n" % uid)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("python current_script.py\n")
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]

    chdir(cwd)
    return ans


def launch_executable(uid, exename):
    """launch given executable in associated environment.
    """
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("activate %s\n" % uid)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("%s\n" % exename)
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]
    return ans


def compile_sources(uid, pid):
    """Compile sources using a given user environment.
    """
    cwd = getcwd()
    ppth = source_pth(pid)
    if not exists(ppth):
        raise UserWarning("no source directory")

    if not exists(join(ppth, "setup.py")):
        raise UserWarning("no setup.py found")

    chdir(ppth)
    pr = Popen("cmd", stdin=PIPE, stdout=PIPE)
    pr.stdin.write("activate %s\n" % uid)
    pr.stdin.write("echo azerty\n")
    res = pr.communicate("python setup.py bdist_egg\n")
    if res[1] is not None:
        raise UserWarning(res[1])

    lines = res[0].splitlines()
    while not lines[0].startswith("azerty"):
        lines.pop(0)

    ans = lines[3:-2]

    chdir(cwd)
    return ans
