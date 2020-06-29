import click


@click.command()
def setup():
    """Configures the metabase instance"""
    from . import setup
    setup.setup()

@click.command()
def update_metadata():
    """Sync schema definitions from Mara to Metabase"""
    from . import metadata
    metadata.update_metadata()


@click.command()
def sync_acl():
    """Syncs users, groups & data set permissions from mara to metabase"""
    from . import acl
    acl.sync()
