#!/usr/bin/env python
import os
import argparse
import json


def parse_args():
    """ Parse and return the arguments

    Returns:
        args: the args namespace

    """
    parser = argparse.ArgumentParser(description="Creates a sublime project.")
    parser.add_argument('project_data_directory',
                        help='The directory containing project data.')
    return parser.parse_args()


def main(args):
    """ Creates a sublime project file using args

    Args:
        args: the arguments passed to the script

    """
    # If SUBLIME_PROJECTS_DIR is set, then it takes precedence
    sublime_projects_dir = os.path.normpath(os.getenv('SUBLIME_PROJECTS_DIR'))
    project_data_directory = os.path.abspath(args.project_data_directory)
    project_storage_directory = sublime_projects_dir or project_data_directory

    # Get the name of the project either from the name arg or
    # the project data dir
    project_name = (getattr(args, 'name', None)
                    or os.path.basename(project_data_directory))
    project_file = os.path.join(project_storage_directory,
                                project_name + '.sublime-project')

    # The project settings, eventually output as json.
    data = {
        "folders":
        [
            {
                "follow_symlinks": True,
                "path": project_data_directory
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
    if not os.path.exists(project_storage_directory):
        os.makedirs(project_storage_directory)

    # Write the data to the project file
    with open(project_file, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    args = parse_args()
    main(args)
