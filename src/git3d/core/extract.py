from .init import init_config_dir, retrieve_config_path, retrieve_config_dir
from ..resources import load_config, export_yaml
from ..utils.parse import list_to_dict
import os, sys, shutil
from copy import copy
from .init import retrieve_git_root

TAG = ' # please_ignore_thank_you_S2'
always_ignore = {
    '.puzzle/repos': None
}

def extract_copy(dir: str, target: str, virtual_remote_repo: str, ignores: dict, root_dir: str = None) -> None:
    root_dir = root_dir or dir
    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
        item_rel_path = os.path.normpath(os.path.join(dir, item).removeprefix(root_dir+'/'))
        if not os.path.exists(os.path.join(virtual_remote_repo, item_rel_path)):
            continue
        target_path = os.path.join(target, item_rel_path)
        if os.path.isdir(item_path) and (item_rel_path in ignores.keys()):
            ...
        elif os.path.isdir(item_path):
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            extract_copy(item_path, target, virtual_remote_repo, ignores, root_dir=root_dir)
        elif item_rel_path not in ignores.keys():
            shutil.copyfile(item_path, target_path)
        else: # copy file without ignored parts.
            ignored_line_numbers = ignores[item_rel_path]
            if ignored_line_numbers is None:
                ...  # ignore all file
            else:
                if ignored_line_numbers == -1:
                    new_lines = []
                else:
                    with open(item_path, 'r') as original_file:
                        lines = original_file.readlines()
                        new_lines = copy(lines)
                        for numbers in ignored_line_numbers:
                            # TODO: check if there are some overlaps
                            if numbers == -1:
                                new_lines = []
                            elif isinstance(numbers, int):
                                new_lines[numbers-1] += TAG
                            elif isinstance(numbers, tuple):
                                for i in range(numbers[0]-1, numbers[1]):
                                    new_lines[i] += TAG
                trimmed_lines = [line for line in new_lines if not line.endswith(TAG)]
                with open(target_path, 'w+') as new_file:
                    new_file.writelines(trimmed_lines)


def extract_submodule():
    import subprocess
    config_path = retrieve_config_path()
    config_dir = retrieve_config_dir()
    local_repos = os.path.join(config_dir, 'repos')

    config = load_config(config_path) or {}
    submodules = config.get('submodules', [])
    git_root = retrieve_git_root()

    for submodule in submodules:
        repo = submodule['repo']
        ignore_list = submodule.get('ignore', []) or []
        for ign in ignore_list:
            ign['lines'] = ign.get('lines', None)
            if ign['lines'] is not None:
                ign['lines'] = [line if isinstance(line, int) else tuple(line) for line in ign['lines']]
        ignores = list_to_dict(ignore_list, key_field='name', value_field='lines')
        ignores.update(always_ignore)
        local_repo = os.path.normpath(os.path.join(git_root, submodule.get('path', '')))
        virtual_local_repo = os.path.join(local_repos, submodule['name'], 'local')
        virtual_remote_repo = os.path.join(local_repos, submodule['name'], 'remote')

        remote_config_path = os.path.join(virtual_remote_repo, '.puzzle', 'templateconfig')
        remote_config = load_config(remote_config_path) or {}
        remote_ign_list = remote_config.get('ignore', []) or []
        for ign in remote_ign_list:
            ign['lines'] = ign.get('lines', None)
            if ign['lines'] is not None:
                ign['lines'] = [line if isinstance(line, int) else tuple(line) for line in ign['lines']]
        remote_ignores = list_to_dict(remote_ign_list, key_field='name', value_field='lines')
        # skeleton_only_list = remote_config.get('skeleton-only', []) or []
        # remote_ignores.update({skl: -1 for skl in skeleton_only_list})

        extract_copy(virtual_remote_repo, virtual_local_repo, virtual_remote_repo, ignores=remote_ignores)
        extract_copy(local_repo, virtual_local_repo, virtual_remote_repo, ignores=ignores)

