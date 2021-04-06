"""
Module for handling DB connection and schema. 

.. note::
    
    This file imports pyodbc, despite it not being explicitly used. The connection 
    to the database uses pyodbc, as named in the local_config's DB uri string; pyodbc is included 
    here as an easy way of forcing pyinstaller to recognise it as a module to be built into the 
    exe file. 

"""
import sqlalchemy
from configparser import ConfigParser
import os
import sys
import click
import pyodbc  # Not explicitly used - see docstring
from curriculum_model.db.schema import Base


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller 

    From https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/44352931#44352931"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class DB():
    """Simple class for handling DB connection

    Parameters
    ----------
    uri : str
        SQLAlchemy connection string. 
    echo : boolean 
        Whether or not to output instructions sent to DB. 
    config_section : str
        Name of the section in the config file. 
    """

    def __init__(self, echo=False, config_section="PRODUCTION", config_name='local_config.ini'):
        fldr = resource_path(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))))
        self._config_file = os.path.join(fldr, config_name)
        self._cp = ConfigParser()
        self._cp.read(self._config_file)
        self.test_mode = True if "TEST" in config_section else False
        try:
            self.uri = self._cp[config_section]['uri']
        except KeyError:
            raise FileNotFoundError("Local config file not found.")
        self.echo = echo

    def __enter__(self):
        self.engine = sqlalchemy.create_engine(self.uri, echo=self.echo)
        self._sfactory = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.con = self.engine.connect()
        if self.test_mode:
            Base.metadata.create_all(self.engine)
        return self

    def __exit__(self, type, value, traceback):
        self.engine.dispose()
        pass

    def session(self):
        """
        Returns an SQLAlchemy session object, for ORM work. 
        """
        s = self._sfactory()
        return s

# Map taking string names to table objects


def table_map(sqlalchemy_base):
    """
    Returns a dictionary of table names to table objects. 

    Uses the given SQL Alchemy base 

    Parameters
    ----------
    sqlalchemy_base : 
        SQLAlchemy declarative base object. 

    Returns
    -------
    dict
        Map of tablename to corresponding object. 
    """
    tm = {}
    for model in sqlalchemy_base._decl_class_registry.values():
        if hasattr(model, '__tablename__'):
            tm[model.__tablename__] = model
    return tm
