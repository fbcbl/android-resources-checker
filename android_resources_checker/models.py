from dataclasses import dataclass
from enum import Enum

from typing import Dict, Set


class ResourceType(Enum):
    drawable = "drawable"
    color = "color"
    anim = "anim"
    raw = "raw"
    dimen = "dimen"
    string = "string"
    style = "style"


@dataclass(frozen=True)
class PackagingType(Enum):
    file = "file"
    entry = "entry"


@dataclass(frozen=True)
class ResourceReference:
    name: str
    resource_type: ResourceType


@dataclass(frozen=True)
class PackagedResource:
    resource: ResourceReference
    packaging_type: PackagingType
    filepath: str
    size: int


@dataclass(frozen=True)
class AnalysisBreakdown:
    project_name: str
    used_resources: Dict[ResourceType, Set[PackagedResource]]
    unused_resources: Dict[ResourceType, Set[PackagedResource]]
    unused_size_bytes: int


class ReportType(Enum):
    csv = "csv"
    stdout = "stdout"
