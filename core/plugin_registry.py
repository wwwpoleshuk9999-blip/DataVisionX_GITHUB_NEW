import json
import os
import time


REGISTRY_FILE = "data/plugin_registry.json"



def init_registry():

    os.makedirs(
        "data",
        exist_ok=True
    )

    if not os.path.exists(REGISTRY_FILE):

        with open(
            REGISTRY_FILE,
            "w"
        ) as f:

            json.dump(
                [],
                f,
                indent=4
            )



def load_registry():

    init_registry()

    with open(
        REGISTRY_FILE,
        "r"
    ) as f:

        return json.load(f)



def save_registry(data):

    with open(
        REGISTRY_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def register_plugin(
    plugin_id,
    name,
    version,
    path
):

    registry = load_registry()


    for plugin in registry:

        if plugin["id"] == plugin_id:

            return plugin



    item = {

        "id": plugin_id,

        "name": name,

        "version": version,

        "path": path,

        "installed": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "status": "INSTALLED"

    }


    registry.append(
        item
    )


    save_registry(
        registry
    )


    return item



def get_registry():

    return load_registry()



init_registry()
