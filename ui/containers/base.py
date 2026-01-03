from enum import Enum

import tkinter as tk
from tkinter import ttk

from typing import Optional


class ContainerType(Enum):
    BASE = 0
    SECTION = 1
    LOCATION = 2
    TASK = 3


class YWARContainer(ttk.Frame):
    """
    Base class for all containers in the YWAR UI.

    This class is responsible for:
    - Tracking semantic type (section/location/task)
    - Computing nesting depth relative to containers of the same type
    - Rendering visual structure:
        - Accent bar
        - Header area
        - Child container area

    Subclasses are expected to define:
    - Container type (using ContainerType enum class defined in this module)
    - Base container color
    - Specific styling for increased levels of depth
    """

    # placeholder virtual container attributes redefined by subclasses
    CONTAINER_TYPE: ContainerType = ContainerType.BASE
    BASE_COLOR: str = "#000000"
    DEPTH_STYLES: dict = {}                             # depth to style mapping

    def __init__(self, parent: tk.Frame, *, title = "", **kwargs):
        # initializing the parent frame itself
        super().__init__(parent, **kwargs)
        # referencing the parent container if applicable
        self.parent_container = parent if isinstance(parent, YWARContainer) else None

        self.title = title
        self.children_containers = []

        # computing nesting depth relative to containers of the same type
        self.depth = self._compute_relative_depth()

        # resolving styling based on depth
        self.style_tokens = self._resolve_style_tokens()

        # building visual structure
        self._build_structure()