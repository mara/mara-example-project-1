"""Set up Navigation, ACL & Logos"""

import flask
import mara_acl
import mara_acl.users
import mara_app
import mara_app.layout
import mara_data_explorer
import mara_db
import mara_metabase
import mara_metabase.acl
import mara_metabase.config
import mara_mondrian
import mara_mondrian.config
import mara_page.acl
import mara_pipelines
import mara_schema
from app.ui import start_page
from mara_app import monkey_patch
from mara_page import acl
from mara_page import navigation

blueprint = flask.Blueprint('ui', __name__, url_prefix='/ui', static_folder='static')


def MARA_FLASK_BLUEPRINTS():
    return [start_page.blueprint, blueprint]


# replace logo and favicon
monkey_patch.patch(mara_app.config.favicon_url)(lambda: flask.url_for('ui.static', filename='favicon.ico'))
monkey_patch.patch(mara_app.config.logo_url)(lambda: flask.url_for('ui.static', filename='logo.png'))


# add custom css
@monkey_patch.wrap(mara_app.layout.css_files)
def css_files(original_function, response):
    files = original_function(response)
    files.append(flask.url_for('ui.static', filename='styles.css'))
    return files


# define protected ACL resources
@monkey_patch.patch(mara_acl.config.resources)
def acl_resources():
    return [acl.AclResource(name='Documentation',
                            children=[mara_pipelines.MARA_ACL_RESOURCES().get('Pipelines'),
                                      mara_db.MARA_ACL_RESOURCES().get('DB Schema'),
                                      mara_schema.MARA_ACL_RESOURCES()['Schema']]),
            acl.AclResource(name='Data',
                            children=[*mara_data_explorer.MARA_ACL_RESOURCES().values(),
                                      *mara_metabase.MARA_ACL_RESOURCES().values(),
                                      *mara_mondrian.MARA_ACL_RESOURCES().values()
                                      ]),
            acl.AclResource(name='Admin',
                            children=[mara_app.MARA_ACL_RESOURCES().get('Configuration'),
                                      mara_acl.MARA_ACL_RESOURCES().get('Acl')])]


# activate ACL
monkey_patch.patch(mara_page.acl.current_user_email)(mara_acl.users.current_user_email)
monkey_patch.patch(mara_page.acl.current_user_has_permissions)(mara_acl.permissions.current_user_has_permissions)
monkey_patch.patch(mara_page.acl.user_has_permissions)(mara_acl.permissions.user_has_permissions)

monkey_patch.patch(mara_acl.config.whitelisted_uris)(lambda: ['/mara-app/navigation-bar', '/mondrian/saiku/authorize'])

# enable user and permission sync from mara acl to Metabase
mara_metabase.acl.enable_automatic_sync_of_users_and_permissions_to_metabase()


# navigation bar (other navigation entries will be automatically added)
@monkey_patch.patch(mara_app.config.navigation_root)
def navigation_root() -> navigation.NavigationEntry:
    return navigation.NavigationEntry(label='Root', children=[
        navigation.NavigationEntry(label='Welcome', icon='home', uri_fn=lambda: '/', description='Welcome !'),
        *mara_metabase.MARA_NAVIGATION_ENTRIES().values(),
        *mara_mondrian.MARA_NAVIGATION_ENTRIES().values(),
        *mara_data_explorer.MARA_NAVIGATION_ENTRIES().values(),
        *mara_schema.MARA_NAVIGATION_ENTRIES().values(),
        *mara_pipelines.MARA_NAVIGATION_ENTRIES().values(),
        *mara_db.MARA_NAVIGATION_ENTRIES().values(),
        navigation.NavigationEntry(
            'Settings', icon='cog', description='ACL & Configuration', rank=100,
            children=[*mara_app.MARA_NAVIGATION_ENTRIES().values(),
                      *mara_acl.MARA_NAVIGATION_ENTRIES().values()])])
