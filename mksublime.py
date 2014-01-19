#!/usr/bin/env python
import os
import argparse
import json


def parse_args():
    """ Parse and return the arguments

    Returns:
        args

    """
    parser = argparse.ArgumentParser(description="Creates a sublime project.")
    parser.add_argument('project_directory', help='The directory containing project data.')
    return parser.parse_args()


def main(args):
    """ Creates a sublime project file using args

    Args:
        args: the arguments passed to the script

    """
    project_directory = os.path.abspath(args.project_directory)
    project_name = getattr(args, 'name', None) or os.path.basename(project_directory)
    project_file = os.path.join(project_directory, project_name + '.sublime-project')

    data = {
        "folders":
        [
            {
                "follow_symlinks": True,
                "path": project_directory
            }
        ]
    }

    # Find if we're in a virtual env
    virtual_env = os.getenv('VIRTUAL_ENV', None)

    if virtual_env:
        interpreter = os.path.join(virtual_env, 'bin', 'python')
        data['settings'] = {
            "python_intepreter": interpreter
        }
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)

    # Write the data to the project file
    with open(project_file, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    args = parse_args()
    main(args)
