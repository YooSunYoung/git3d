from .init import init_config_dir, retrieve_config_path, retrieve_config_dir
from ..resources import load_config, export_yaml
import os


def init_submodule_config() -> None:
    import os
    config_path = retrieve_config_path()
    if not os.path.exists(config_path):
        with open(config_path, 'w+') as file:
            file.write('')


def init_submodule_local_repo():
    config_dir = retrieve_config_dir()
    local_repos = os.path.join(config_dir, 'repos')
    if not os.path.exists(local_repos):
        os.mkdir(local_repos)


def clone_submodules():
    import subprocess
    init_config_dir()
    init_submodule_config()
    config_path = retrieve_config_path()
    config_dir = retrieve_config_dir()
    init_submodule_local_repo()
    local_repos = os.path.join(config_dir, 'repos')
    
    config = load_config(config_path) or {}
    submodules = config.get('submodules', [])
    for submodule in submodules:
        repo = submodule['repo']
        local_repo = os.path.join(local_repos, submodule['name'])
        if not os.path.exists(local_repo):
            os.mkdir(local_repo)
            os.mkdir(os.path.join(local_repo, 'remote'))
            os.mkdir(os.path.join(local_repo, 'local'))
        subprocess.getoutput(f"git clone {repo} {os.path.join(local_repo, 'remote')}")
                     

def add_submodule(name: str, repo: str):
    init_config_dir()
    init_submodule_config()
    config_path = retrieve_config_path()
    config = load_config(config_path) or {}
    if 'submodules' not in config:
        config['submodules'] = []
    if any(True if submodule['name'] == name else False for submodule in config['submodules']):
        print(f"Submodule {name} already exists. Skipping updating submodule config. ")
    else:
        config['submodules'].append({
            'name': name,
            'repo': repo
        })
        export_yaml(config, config_path, overwrite=True)

    clone_submodules()
