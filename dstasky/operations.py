from __future__ import annotations

import os

import yaml

from dstasky.git import create_commit
from dstasky.tasks import ObjectEntry
from dstasky.utils import get_data_directory
from dstasky.utils import find_file

def create_object(obj: ObjectEntry) -> None:
    title = f"create({obj.objtype.value}): {obj.title}"

    uuid_str = str(obj.objuuid)
    body = f"Reference: {uuid_str}"

    data_dir = get_data_directory()
    objs_dir = os.path.join(data_dir, 'objects')
    obj_filename = f"{uuid_str}.yml"

    if find_file(obj_filename, objs_dir):
        raise AssertionError('This object file already exists!')

    obj_path = os.path.join(objs_dir, obj_filename)

    with open(obj_path, 'w', encoding='utf8') as file:
        file.write('---\n\n')
        yaml.dump(obj.to_dict(), file)

    obj_git_path = os.path.join('objects', obj_filename)
    try:
        create_commit(title, body, files=[obj_git_path])
    except RuntimeError as re:
        os.remove(obj_path)
        raise re
