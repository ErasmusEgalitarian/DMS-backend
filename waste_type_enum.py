from enum import Enum


class WasteType(str, Enum):
    PAPER = "paper"
    PLASTIC = "plastic"
    GLASS = "glass"
    METAL = "metal"
    ORGANIC = "organic"
    TEXTILE = "textile"
    OTHER = "other"
