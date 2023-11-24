import os
import subprocess
import click

@click.command()
@click.option('-d', '--directory', type=click.Path(exists=True), help='Directory to process')
def git_add_and_commit(directory):
    # Change to the specified directory
    os.chdir(directory)

    # Get the list of untracked files
    untracked_files = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()

    # Add untracked files to Git
    if untracked_files:
        subprocess.run(['git', 'add'] + untracked_files)

    # Get the list of modified files
    modified_files = subprocess.check_output(['git', 'ls-files', '--modified', '--exclude-standard'], text=True).splitlines()

    # Add modified files to Git
    if modified_files:
        subprocess.run(['git', 'add'] + modified_files)

    # Construct the commit message
    commit_message = construct_commit_message(untracked_files, modified_files)

    # Commit changes
    subprocess.run(['git', 'commit', '-m', commit_message])

def construct_commit_message(untracked_files, modified_files):
    message = "Update and modify files for the project\n- Add new files:\n"
    message += "\n".join(["  - {}".format(file) for file in untracked_files]) + "\n" if untracked_files else "None\n"

    message += "- Update files:\n"
    message += "\n".join(["  - {}".format(file) for file in modified_files]) + "\n" if modified_files else "None\n"

    return message

if __name__ == "__main__":
    git_add_and_commit()
