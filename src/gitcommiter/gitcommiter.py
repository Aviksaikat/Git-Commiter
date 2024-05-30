#!/usr/bin/python3
import subprocess
from pathlib import Path
import os
import click


def print_banner():
    click.echo(
        click.style(
            r"""
            ████████  ██   ██           ██████                                   ██   ██
         ██░░░░░░██░░   ░██          ██░░░░██                                 ░░   ░██
        ██      ░░  ██ ██████       ██    ░░   ██████  ██████████  ██████████  ██ ██████  █████  ██████
        ░██         ░██░░░██░  █████░██        ██░░░░██░░██░░██░░██░░██░░██░░██░██░░░██░  ██░░░██░░██░░█
        ░██    █████░██  ░██  ░░░░░ ░██       ░██   ░██ ░██ ░██ ░██ ░██ ░██ ░██░██  ░██  ░███████ ░██ ░
        ░░██  ░░░░██░██  ░██        ░░██    ██░██   ░██ ░██ ░██ ░██ ░██ ░██ ░██░██  ░██  ░██░░░░  ░██
         ░░████████ ░██  ░░██        ░░██████ ░░██████  ███ ░██ ░██ ███ ░██ ░██░██  ░░██ ░░██████░███
          ░░░░░░░░  ░░    ░░          ░░░░░░   ░░░░░░  ░░░  ░░  ░░ ░░░  ░░  ░░ ░░    ░░   ░░░░░░ ░░░
            """,
            fg="red",
        )
    )


def construct_commit_message(untracked_files, modified_files, deleted_files):
    message = "Updated and modified files for the project\n"

    if untracked_files:
        message += "- Added new files:\n"
        message += "\n".join(["  - {}".format(file) for file in untracked_files]) + "\n"

    if modified_files:
        message += "- Updated files:\n"
        message += "\n".join(["  - {}".format(file) for file in modified_files]) + "\n"

    if deleted_files:
        message += "- Deleted files:\n"
        message += "\n".join(["  - {}".format(file) for file in deleted_files]) + "\n"

    return (
        message.strip()
    )  # Remove trailing newline if no new, modified, or deleted files


@click.command()
@click.option(
    "-d", "--directory", type=click.Path(exists=True), help="Directory to process"
)
@click.option("-p", "--push", is_flag=True, help="Push changes to the remote repository")
@click.option("-nv", "--no-verify", is_flag=True, help="Ignore pre-commit hooks")
@click.option("-h", "--help", is_flag=True, help="Print help message")
def git_add_and_commit(directory, push, no_verify, help):
    if help:
        print_banner()
        click.echo("Automatically add and commit new, modified, and deleted files to Git and write super cool commit messages")
        click.echo("\nUsage:")
        click.echo("  gitcommiter -d /path/to/your/directory [-p]")
        click.echo("\nOptions:")
        click.echo("  -d, --directory  Directory to process")
        click.echo("  -p, --push       Push changes to the remote repository")
        click.echo("  -nv, --no-verify Ignore pre-commit hooks")
        click.echo("  -h, --help       Print this message")
        click.get_current_context().exit()

    if not directory:
        click.echo("Please provide a directory using the -d/--directory option.")
        click.echo("For example: gitcommiter -d /path/to/your/directory")
        click.get_current_context().exit()

    # Change to the specified directory
    directory_path = Path(directory)
    os.chdir(directory_path)

    # Get the list of untracked files
    untracked_files = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], text=True
    ).splitlines()

    # Add untracked files to Git
    if untracked_files:
        subprocess.run(["git", "add"] + untracked_files)

    # Get the list of modified files
    modified_files = subprocess.check_output(
        ["git", "ls-files", "--modified", "--exclude-standard"], text=True
    ).splitlines()

    # Add modified files to Git
    if modified_files:
        subprocess.run(["git", "add"] + modified_files)

    # Get the list of deleted files
    deleted_files = subprocess.check_output(
        ["git", "ls-files", "--deleted"], text=True
    ).splitlines()

    # Add deleted files to Git
    if deleted_files:
        subprocess.run(["git", "add"] + deleted_files)

    # Construct the commit message
    commit_message = construct_commit_message(
        untracked_files, modified_files, deleted_files
    )

    # Commit changes
    if commit_message:
        if no_verify:
            subprocess.run(["git", "commit", "-m", commit_message, "--no-verify"])
        else:
            subprocess.run(["git", "commit", "-m", commit_message])

    # Push changes if the -p/--push option is passed
    if push:
        subprocess.run(["git", "push"])



if __name__ == "__main__":
    git_add_and_commit()
