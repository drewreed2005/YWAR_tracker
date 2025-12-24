"""
theme.py
--------
Centralized theme and styling logic for Tkinter app.

Responsibilities:
- Defining colors, fonts, and spacing in one place
- Applying them consistently when creating widgets

This file translates config values into concrete Tkinter styling.
"""

import tkinter as tk
from tkinter import ttk


def _get_colors_from_theme(config: dict) -> dict:
    # resolving the theme from the UI settings (if absent, defaulting to light theme)
    theme_name = config['ui'].get('theme', 'light')
    
    # obtaining color palettes for the given theme from theme config info
    theme_config = config['themes'][theme_name]
    return {
        'bg': theme_config['background'],
        'fg': theme_config['foreground'],
        'panel_bg': theme_config['panel_bg'],
        'accent': theme_config['accent'],
        'highlight': theme_config['highlight'],
        'border': theme_config['border']
    }


def _configure_frame_style(style: ttk.Style, panel_bg: str) -> None:
    style.configure(
        'TFrame',
        background = panel_bg
    )

def _configure_label_style(style: ttk.Style, panel_bg: str, fg: str, font_family: str, font_size: int) -> None:
    style.configure(
        'TLabel',
        # background = panel_bg,
        foreground = fg,
        font = (
            font_family,
            font_size
        )
    )

def _configure_button_style(style: ttk.Style, font_family: str, font_size: int, padding: int) -> None:
    style.configure(
        'TButton',
        font = (
            font_family,
            font_size
        ),
        padding = padding
    )

def _configure_header_style(style: ttk.Style, font_family: str, header_font_size: int) -> None:
    style.configure(
        'Header.TLabel',
        font = (
            font_family,
            header_font_size,
        )
    )

def _configure_highlight_style(style: ttk.Style, highlight: str, font_family: str, font_size: int) -> None:
    style.configure(
        'Highlight.TLabel',
        foreground = highlight,
        font = (
            font_family,
            font_size,
            'bold'
        )
    )

def _configure_timer_style(style: ttk.Style, monospace_font_family: str, timer_font_size: int) -> None:
    style.configure(
        'Timer.TLabel',
        font = (
            monospace_font_family,
            timer_font_size,
            'bold'
        )
    )


def apply_theme(root: tk.Tk, config: dict) -> dict:
    """
    Applies theme settings to the Tk root window and ttk styles.
    
    Returns a dictionary of resolved colors/fonts that the rest of the UI
    can reference when creating widgets.
    """
    
    # getting colors dictionary from theme info in config
    colors = _get_colors_from_theme(config)
    
    # applying the background color to the root window
    # (only affects widgets that inherit the root background)
    root.configure(bg = colors['bg'])
    
    # initializing the ttk style system
    style = ttk.Style(root)
    # using the platform-native theme as a base
    style.theme_use(style.theme_use())
    
    # configuring a generic frame style
    panel_bg = colors['panel_bg']
    _configure_frame_style(style, panel_bg = panel_bg)
    
    # configuring labels, buttons, etc.
    font_family = config['ui']['font']['family']
    font_size = config['ui']['font']['size']
    
    _configure_label_style(
        style, panel_bg = panel_bg, fg = colors['fg'],
        font_family = font_family, font_size = font_size
    )
    _configure_button_style(
        style, font_family = font_family, font_size = font_size, padding = 6
    )
    _configure_header_style(
        style, font_family = font_family,
        header_font_size = config['ui']['font']['header_size']
    )
    _configure_highlight_style(
        style, highlight = colors['highlight'], font_family = font_family,
        font_size = font_size
    )
    _configure_timer_style(
        style, monospace_font_family = config['ui']['font']['monospace_family'],
        timer_font_size = config['ui']['font']['timer_size']
    )
    
    return colors