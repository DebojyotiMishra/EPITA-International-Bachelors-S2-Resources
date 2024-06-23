import os
import subprocess

tag_prefixes = [prefix + suffix
                for suffix in ['Hello',
                               'Vector',
                               'Distance',
                               'Matrix',
                               'SqMatrix',
                               'Determinant',
                               'RowOperations',
                               'Gaussian',
                               'GaussJordan',
                               'MetricSpace',
                               'Group',
                               'Field',
                               'VectorSpace',
                               'Norm',
                               'InnerProduct',
                               'Angle',
                               'Orthonormal',
                               'GramSchmidt',
                               'Coordinates',
                               'Eigenvalues'
                               ]
                for prefix in ['', 'Late-']]


def english_env():
    sub_env = os.environ.copy()
    sub_env['LC_CTYPE'] = 'en_US.UTF-8'
    sub_env['LC_ALL'] = 'en_US.UTF-8'
    sub_env['LANG'] = 'en_US.UTF-8'
    sub_env['LANGUAGE'] = 'en_US.UTF-8'
    return sub_env


def get_stdout(cmd):
    return subprocess.run(cmd, capture_output=True, env=english_env()).stdout.decode('utf-8').split()


def find_git():
    import shutil

    return shutil.which('git')


def remove_exiting_tags():
    for tag in get_stdout(['git', 'tag']):
        subprocess.run(['git', 'tag', '-d', tag], env=english_env())


def suggest_tag(prefix):
    import datetime
    #
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return prefix + '-' + now + '-' + get_stdout(['git', 'rev-parse', '--short', 'HEAD'])[0]


def call_with_print(cmd):
    print("(--------------------")
    print(f"cmd = {cmd}")
    sr = subprocess.run(cmd, env=english_env())
    if sr.stdout is not None:
        print(sr.stdout)
    if sr.returncode != 0:
        print(f"cmd returned [{sr.returncode}]")
    print(")--------------------")
    return sr.returncode == 0


def submit_for_grade(prefix:str):
    while prefix and (prefix[-1] == '-'):
        prefix = prefix[:-1]
    assert prefix in tag_prefixes, f"{prefix} is not a valid tag prefix:  valid tag prefixes are {tag_prefixes}"
    remove_exiting_tags()
    call_with_print(['git', 'commit', '-am', f"committing for tag {prefix}"])
    call_with_print(['git', 'branch'])
    call_with_print(['git', 'branch', '-r'])
    call_with_print(['git', 'remote', '-v'])
    call_with_print(['git', 'status'])
    tag = suggest_tag(prefix)
    print(f"Creating new tag: {tag}")
    call_with_print(['git', 'tag', tag])
    call_with_print(['git', 'push'])
    call_with_print(['git', 'push', '--tags'])


def git_branch():
    return get_stdout(['git', 'branch', '--show-current'])[0]


if __name__ == '__main__':
    assert find_git() is not None, "git: command not found"
    assert git_branch() == "submission", f"current branch is '{git_branch()}', expecting 'submission'"
    # verify submission branch
    submit_for_grade(input(f"Enter a tag prefix: "))
