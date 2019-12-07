"""Use this script to initialize the database.

This script will create the required database model
"""
import os
import sys

import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars


from .. import get_config
from ..models import get_engine, get_session_factory, get_tm_session
from ..models.meta import Base


def usage(argv):
    """Give feedback on commandline usage."""
    cmd = os.path.basename(argv[0])
    print(
        "usage: %s <config_uri> [var=value]\n"
        '(example: "%s development.ini")' % (cmd, cmd)
    )
    sys.exit(1)


def main(argv=sys.argv):
    """Initiliaze database.
    Standard database permissions and an admin user is added to the database.
    """
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings = get_config(settings=settings).get_settings()
    engine = get_engine(settings)

    if options.get("drop_all", "f").lower().startswith("t"):
        print("Dropping schema!")
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)

    # roles = ["admin", "superuser", "reporting-api"]
    # with transaction.manager:
    #     session = get_tm_session(session_factory, transaction.manager)
    #     user = session.query(User).limit(1).one_or_none()
    #     if not user:
    #         user = User(name="admin", email="admin@example.com")
    #         user.password = "admin"
    #         session.add(user)
    #         session.flush()
    #         session.refresh(user)

    #         roles = {role: Role(name=role) for role in roles}
    #         session.add_all(roles.values())
    #         user.roles = [roles["admin"]]
    print("Database filled!")
