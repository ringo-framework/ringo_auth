#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from tedega_view import create_application
from tedega_storage.rdbms import (
    init_storage,
    get_storage
)
from tedega_storage.rdbms.crud import (
    create as _create,
)
from tedega_share import (
    init_logger,
    get_logger,
    monitor_connectivity,
    monitor_system
)

import tedega_auth.model

package_directory = os.path.dirname(os.path.abspath(__file__))


def build_app(servicename):
    # Define things we want to happen of application creation. We want:
    # 1. Initialise out fluent logger.
    # 2. Initialise the storage.
    # 3. Start the monitoring of out service to the "outside".
    # 4. Start the monitoring of the system every 10sec (CPU, RAM,DISK).
    run_on_init = [(init_logger, servicename),
                   (init_storage, None),
                   (monitor_connectivity, [("www.google.com", 80)]),
                   (monitor_system, 10)]
    application = create_application(servicename, run_on_init=run_on_init)
    log = get_logger()
    with get_storage() as storage:
        user = _create(storage, tedega_auth.model.user.User, dict(name="admin", password="secret"))
        storage.create(user)
        log.info("Create default user 'admin' with password 'secret'")
    
    return application

if __name__ == "__main__":
    application = build_app("tedega_auth")
    application.run()
