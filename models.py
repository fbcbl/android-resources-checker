from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    drawable = "drawable",
    color = "color",
    anim = "anim",
    raw = "raw"


@dataclass(frozen=True)
class ResourceReference:
    name: str
    type: ResourceType


@dataclass(frozen=True)
class PackagedResource:
    resource: ResourceReference
    size: int


@dataclass(frozen=True)
class AnalysisBreakdown:
    project_name: str
    used_resources: dict[ResourceType, set[ResourceReference]]
    unused_resources: dict[ResourceType, set[ResourceReference]]
    unused_size_bytes: int

