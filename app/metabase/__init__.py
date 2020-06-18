
def MARA_CONFIG_MODULES():
    from . import config
    return [config]

def MARA_CLICK_COMMANDS():
    from . import cli
    return [cli.setup, cli.sync_acl]

from . import acl
acl.patch_acl_methods()
