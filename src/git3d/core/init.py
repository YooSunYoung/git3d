import os

def retrieve_git_root() -> str:
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().removesuffix('\n')


def init_config_dir() -> str:
    git_root = retrieve_git_root()
    config_dir = os.path.join(git_root, '.puzzle')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    elif os.path.exists(config_dir) and not os.path.isdir(config_dir):
        raise Exception('.puzzle already taken...!')


def retrieve_config_dir() -> str:
    git_root = retrieve_git_root()
    return os.path.join(git_root, '.puzzle')


def retrieve_config_path() -> str:
    from ..resources import load_config
    return os.path.join(retrieve_config_dir(), 'submodule.pzl')


def retrieve_template_config() -> str:
    from ..resources import load_config
    template_config_path = os.path.join(retrieve_config_dir(), 'templateconfig')
    template_config = load_config(template_config_path)
    template_config


