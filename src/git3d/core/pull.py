from .init import init_config_dir, retrieve_config_path, retrieve_config_dir
from .add import init_submodule_config
from ..resources.loaders import load_config

import os
from .extract import extract_submodule
import subprocess

def pull_submodules():
    config_path = retrieve_config_path()
    config_dir = retrieve_config_dir()
    local_repos = os.path.join(config_dir, 'repos')
    
    config = load_config(config_path) or {}
    submodules = config.get('submodules', [])
    for submodule in submodules:
        virtual_remote_repo = os.path.join(local_repos, submodule['name'], 'remote')
        subprocess.getoutput(f"cd {virtual_remote_repo} && git pull ")
    # extract_submodule()
