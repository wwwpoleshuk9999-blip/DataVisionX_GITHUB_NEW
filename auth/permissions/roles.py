ROLES = {

    "admin": {
        "users": [
            "read",
            "create",
            "update",
            "delete"
        ],
        "plugins": [
            "read",
            "write"
        ],
        "data": [
            "read",
            "write"
        ]
    },


    "operator": {
        "users": [
            "read"
        ],
        "plugins": [
            "read",
            "write"
        ],
        "data": [
            "read",
            "write"
        ]
    },


    "viewer": {
        "users": [
            "read"
        ],
        "plugins": [
            "read"
        ],
        "data": [
            "read"
        ]
    }

}


def has_permission(role, resource, action):

    if role not in ROLES:
        return False

    if resource not in ROLES[role]:
        return False

    return action in ROLES[role][resource]
