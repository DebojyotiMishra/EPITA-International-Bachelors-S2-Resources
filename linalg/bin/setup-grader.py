import sys
import os
import subprocess
import datetime

testing = False
# jim.newton@git.forge.epita.fr:p/epita-pi-cs-bachelor/2024-linear-algebra/epita-pi-cs-bachelor-2024-linear-algebra-jim.newton.git
# prefixed by name of current user
# suffixed by name of the person whose repository you want to reference

# must start with @ and end with -
repo_infix = "@git.forge.epita.fr:p/epita-pi-cs-bachelor/2024-linear-algebra/epita-pi-cs-bachelor-2024-linear-algebra-"
required_directory = 'linear-algebra-student'


def create_tmp_dir():
    import tempfile
    temp_dir = tempfile.TemporaryDirectory()
    os.makedirs(temp_dir.name, exist_ok=True)
    return temp_dir.name


def get_stdout(cmd):
    return subprocess.run(cmd, capture_output=True).stdout.decode('utf-8').split()


def find_git():
    import shutil

    return shutil.which('git')


def english_env():
    sub_env = os.environ.copy()
    sub_env['LC_CTYPE'] = 'en_US.UTF-8'
    sub_env['LC_ALL'] = 'en_US.UTF-8'
    sub_env['LANG'] = 'en_US.UTF-8'
    sub_env['LANGUAGE'] = 'en_US.UTF-8'
    return sub_env


def remove_exiting_tags():
    for tag in get_stdout(['git', 'tag']):
        subprocess.run(['git', 'tag', '-d', tag], env=english_env(), capture_output=True)


def call_with_print(cmd, suppress=False, cwd=None, ignore_exit_status=False):
    print(f"cmd = {cmd}")
    sr = subprocess.run(cmd, env=english_env(), cwd=cwd, capture_output=ignore_exit_status)
    if suppress:
        pass
    elif sr.stdout is not None:
        for line in sr.stdout.decode('utf-8').split('\n'):
            print(line)
    if ignore_exit_status:
        pass
    elif sr.returncode != 0:
        print(f"cmd returned [{sr.returncode}]")
    return sr.returncode == 0


def grader_repo(user_name):
    if not testing:
        return f"{user_name}{repo_infix}{user_name}.git"
    local_repo = create_tmp_dir() + datetime.datetime.now().isoformat().replace(':', '-')
    os.makedirs(local_repo, exist_ok=True)
    call_with_print(['git', 'init', '--bare', '--initial-branch=master'], cwd=local_repo)
    return local_repo


def setup_grader(user_name):
    assert '.' in user_name, f"user name {user_name} in wrong format, should be name.name"
    repo = grader_repo(user_name)
    #    pierre.dupont@git.forge.epita.fr:p/epita-pi-cs-bachelor/2024-linear-algebra/epita-pi-cs-bachelor-2024-linear-algebra-pierre.dupont.git
    #    git ls-remote MY-GRADER-REPOSITORY
    if get_stdout(['git', 'ls-remote', repo]):
        # TODO need to merge unrelated histories if necessary
        print(f"repository not empty: {repo}")
        exit(1)

    # cd linear-algebra-student
    call_with_print(['git', 'commit', '-am', 'Initial commit'], ignore_exit_status=True)
    call_with_print(['git', 'remote', 'rm', 'grader'], ignore_exit_status=True)
    call_with_print(['git', 'remote', 'add', 'grader', repo])
    # TODO need to merge unrelated histories if necessary
    assert call_with_print(['git', 'fetch', 'grader'])
    call_with_print(['git', 'checkout', 'main'])
    call_with_print(['git', 'branch', '--delete', 'submission'], ignore_exit_status=True)
    call_with_print(['git', 'branch', 'submission'])
    call_with_print(['git', 'checkout', 'submission'])
    remove_exiting_tags()
    assert call_with_print(['git', 'push', 'grader', 'submission:master'])
    assert call_with_print(['git', 'branch', '--set-upstream-to=grader/master', 'submission'])
    assert call_with_print(['git', 'config', 'push.default', 'upstream'])
    remove_exiting_tags()


if __name__ == '__main__':
    wd = os.getcwd()

    assert required_directory in wd, f"must be run in {required_directory}, not in {wd}"
    assert find_git() is not None, "git: command not found"

    setup_grader(input(f"User name [first.last]: "))
