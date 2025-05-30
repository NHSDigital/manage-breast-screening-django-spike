from typing import Sequence


def exclude_axe_violations(axe_response: dict, exclude_ids: Sequence) -> None:
    """
    Modify an axe response to exclude specific violations.
    """
    axe_response["violations"] = [
        violation
        for violation in axe_response["violations"]
        if violation["id"] not in exclude_ids
    ]


def exclude_axe_targets(axe_response: dict, exclude_targets: Sequence) -> None:
    """
    Modify an axe response to exclude specific targets
    """
    exclude_targets_set = set(exclude_targets)
    for violation in axe_response["violations"]:
        violation["nodes"] = [
            node
            for node in violation["nodes"]
            if not set(node["target"]).issubset(exclude_targets_set)
        ]
