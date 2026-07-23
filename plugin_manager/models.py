from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PluginInfo:
    id: str
    name: str
    version: str
    author: str
    description: str
    api_version: str
    path: str

    permissions: Dict[str, bool] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)

    status: str = "STOPPED"

