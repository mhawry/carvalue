import os.path
import re
import shutil
import click
from flask import current_app
from sqlalchemy import text

BASE_DB_SCHEMA_FILE = 'base_db_schema.sql'


def init_db():
    """Initialize the base database structure"""
    engine = current_app.config['DB_ENGINE']

    # note: the schema is idempotent (can be run multiple times)
    with engine.connect() as connection, current_app.open_resource(BASE_DB_SCHEMA_FILE) as f:
        connection.execute(text(f.read().decode('utf8')))
        connection.commit()


def process_market_data_file(filename: str) -> None:
    """Loads market data from a given file into the database

    Parameters
    ----------
    filename : str
        Path of the file to parse
    """

    # copy the input file in tmp, so we can manipulate it
    temp_file = os.path.join('/tmp/', os.path.basename(filename))
    shutil.copyfile(filename, temp_file)

    # get rid of the \" in the source file
    with open(temp_file, 'r+') as f:
        data = f.read()
        f.seek(0)
        f.write(re.sub("\\\"", "", data))
        f.truncate()

    engine = current_app.config['DB_ENGINE']

    # this is the fastest way to import the data into the table
    # TODO this breaks when uploading the same data twice (unique index on vin)
    with engine.connect() as connection:
        connection.execute(text(f"COPY cars FROM '{temp_file}' DELIMITER '|' CSV HEADER;"))
        connection.commit()


def process_purge_market_data() -> None:
    """Purge existing market data from the database"""
    engine = current_app.config['DB_ENGINE']

    with engine.connect() as connection:
        connection.execute(text('TRUNCATE TABLE cars;'))
        connection.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database')


@click.command('process-market-data-file')
@click.argument('filename', type=click.Path(exists=True))
def process_market_data_file_command(filename: str):
    click.echo(f'Processing market data file: {filename}')
    process_market_data_file(filename)
    click.echo('Market data file has been processed')


@click.command('purge-market-data')
def purge_market_data_command():
    click.echo('Purging existing market data')
    process_purge_market_data()
    click.echo('Market data has been purged')


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(process_market_data_file_command)
    app.cli.add_command(purge_market_data_command)
