import click
import sys
import os
from importlib import import_module as imp
from curriculum_model._version import __version__ as v


class Config(object):

    def __init__(self, verbose=False, echo=False, environment='PRODUCTION'):
        self.verbose = verbose
        self.echo = echo
        self.environment = environment.upper()

    def verbose_print(self, str, bold=False):
        """
        Wraps click echo, for consistent handling of verbose messages.
        """
        if self.verbose:
            click.secho(str, fg='green', bold=bold)


def add_subcommands(parent, file, package):
    """
    Add click subcommands according to directory structure.

    Parameters
    ----------
    parent : function
        Parent function which has commands added to it.
    file : str
        Filepath of current file (use __file__).
    package : str
        Name of the current package (use __package__).
    """
    p = os.path.dirname(file)
    files = os.listdir(p)
    this_package = sys.modules[package].__name__
    modules = [imp(this_package+"."+f.replace(".py", ""), )
               for f in files if f[0] != "_"]
    commands = [getattr(module, module.__name__[module.__name__.rfind(".")+1:])
                for module in modules]
    for _ in commands:
        parent.add_command(_)


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Print more information to the console.")
@click.option("--echo", "-e", is_flag=True, help="Print SQL run against database.")
@click.option("--dbenv", "-d", type=str, help="Specify a DB environment (must correspond to section in config).", default="PRODUCTION")
@click.pass_context
def cm(config, verbose, dbenv, echo):
    """
    Entry point for the CLI.
    """
    # Define config object to be passed to subcommands via click.pass_obj
    config.obj = Config(verbose, echo, dbenv)
    config.obj.verbose_print(f"Running Curriculum Model {v} CLI", True)


add_subcommands(cm, __file__, __package__)
