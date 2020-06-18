import click


@click.command()
def setup():
    """Configures the metabase instance"""
    from . import setup
    setup.setup()


@click.command()
def sync_acl():
    """Syncs users, groups & data set permissions from mara to metabase"""
    from . import acl
    acl.sync()
