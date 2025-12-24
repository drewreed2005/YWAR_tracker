"""
app.py
------
Main Tkinter application window.

Responsibilities:
- Creating the Tk root
- Applying config and theme
- Laying out the major UI regions
- Starting the Tkinter event loop

All logic here is purely structural.
"""

import tkinter as tk
from tkinter import ttk

from config.config import CONFIG
from ui.theme import apply_theme


class YWARApp:
    def __init__(self):
        """
        Creates and stores the root, configures the window properties,
        applies the application theme, and builds the app layout.
        """
        
        # creating the main Tkinter window
        self.root = tk.Tk()
        
        # applying window metadata from config
        self._configure_window()
        
        # applying the theme and storing theme colors
        self.colors = apply_theme(self.root, CONFIG)
        
        # building the main UI layout
        self._build_layout(CONFIG)
    
    def _configure_window(self) -> None:
        """
        Configures basic window properties:
        - Title
        - Geometry
        - Resizability
        """
        
        app_config = CONFIG['app']
        window_config = CONFIG['window']
        
        # setting window title and initial width and height (formatted as geometry string)
        self.root.title(f'{app_config['title']} v{app_config['version']}')
        self.root.geometry(f'{window_config['width']}x{window_config['height']}')
        
        # setting minimum window size
        self.root.minsize(window_config['min_width'], window_config['min_height'])
        
        # allowing or disallowing resizing width and height respectively
        self.root.resizable(window_config['resizable'], window_config['resizable'])
        # (user may toggle window resizability to ensure the proper aspect ratio is kept;
        #  this could prevent accidental resizing that affects recording, monitoring, etc.)
        
        # allowing optional automatic fullscreen
        if window_config.get('fullscreen', False):
            self.root.attributes('-fullscreen', True)
    
    def _build_layout(self, config: dict) -> None:
        """
        Builds the top-level layout. Uses a horizontal PanedWindow so the left and
        right sections can be resized by the user.
        """
        
        # initializing the PanedWindow
        self.main_pane = ttk.PanedWindow(
            self.root,
            orient = tk.HORIZONTAL
        )
        self.main_pane.pack(fill = tk.BOTH, expand = True)
        
        # initializing and building the left panel (contains active route information)
        self.left_frame = ttk.Frame(self.main_pane)
        self._build_left_panel(self.left_frame)
        
        # initializing and building the right panel (contains timer, map, and task notes)
        self.right_frame = ttk.Frame(self.main_pane)
        self._build_right_panel(self.right_frame, config)
        
        # adding panes with weights (intended to start with close to equal width)
        self.main_pane.add(self.left_frame, weight = 3)
        self.main_pane.add(self.right_frame, weight = 4)
        
        # building the footer with the control buttons
        self._build_footer()
    
    def _build_left_panel(self, parent: ttk.Frame) -> None:
        """
        Builds the left-hand column, which is intended to display:
        - The current section header
        - The location hierarchy (emphasis on primary location)
        - The task list (with current task highlighted)
        """
        
        parent.pack(fill = tk.BOTH, expand = True)
        
        # adding placeholder content
        # TODO: review after further functionality implementation
        section_label = ttk.Label(
            parent,
            text = 'Current Section',
            style = 'Header.TLabel'
        )
        section_label.pack(anchor = 'w', padx = 12, pady = (12, 6))
        
        task_placeholder = ttk.Label(
            parent,
            text = 'Task list will appear here'
        )
        task_placeholder.pack(anchor = 'w', padx = 12, pady = 6)
    
    def _build_right_panel(self, parent: ttk.Frame, config: dict) -> None:
        """
        Builds the right-hand column, which is intended to display:
        - Timer and active timing information (top)
        - Map view with task markers (middle)
        - Task notes (bottom)
        """
        
        parent.pack(fill = tk.BOTH, expand = True)
        
        # adding placeholder content for all three sub-panels
        # TODO: review after further functionality implementation
        timer_label = ttk.Label(
            parent,
            text = '00:00:00.000' if config['timer']['precision_ms'] else '00:00:00',
            style = 'Timer.TLabel'
        )
        timer_label.pack(anchor = 'center', pady = (12, 18))
        
        map_placeholder = ttk.Label(
            parent,
            text = 'Map view placeholder'
        )
        map_placeholder.pack(expand = True)
        
        notes_placeholder = ttk.Label(
            parent,
            text = 'Task notes will appear here',
            wraplength = 400,
            justify = 'left'
        )
        notes_placeholder.pack(
            fill = tk.X,
            padx = 12,
            pady = 12
        )
    
    def _build_footer(self) -> None:
        """
        Builds the footer with main interaction buttons:
        - Complete task
        - Skip/defer task
        - Undo task
        """
        
        self.footer_frame = ttk.Frame(self.root)
        self.footer_frame.pack(fill = tk.X, side = tk.BOTTOM, pady = 6)
        
        # creating the complete task button
        self.complete_button = ttk.Button(
            self.footer_frame,
            text = f'Complete Task ({CONFIG['controls']['complete_task_1'].lower().capitalize()}/' + \
                    f'{CONFIG['controls']['complete_task_2'].lower().capitalize()})',
            command = self._on_complete_task
        )
        self.complete_button.pack(side = tk.LEFT, padx = 6)
        
        # skip task button
        self.skip_button = ttk.Button(
            self.footer_frame,
            text = f'Skip Task ({CONFIG['controls']['skip_task'].lower().capitalize()})',
            command = self._on_skip_task
        )
        self.skip_button.pack(side = tk.LEFT, padx = 6)
        
        # undo task button
        self.undo_button = ttk.Button(
            self.footer_frame,
            text = f'Undo Task ({CONFIG['controls']['undo_task'].lower().capitalize()})',
            command = self._on_undo_task
        )
        self.undo_button.pack(side = tk.LEFT, padx = 6)
    
    # --- placeholder callback methods ---
    # TODO: define once further functionality exists
    def _on_complete_task(self) -> None:
        print('Complete task pressed')
    
    def _on_skip_task(self) -> None:
        print('Skip task pressed')
    
    def _on_undo_task(self) -> None:
        print('Undo task pressed')
    
    
    def run(self) -> None:
        """
        Starts the Tkinter event loop.
        """
        self.root.mainloop()