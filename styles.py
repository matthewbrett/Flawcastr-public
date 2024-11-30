"""
styles.py - Central styling configuration for Flawcastr

This module contains all styling-related constants and configurations used across
the application. It's organized by component type and usage context.
"""

# =============================================================================
# Primary Color Palette
# =============================================================================
COLORS = {
    # Base colors
    'background': "#E1ECF4",
    'input_field': "#EDF2F7",
    'accent': "#6C63FF",
    'grid': "#E9ECEF",
    'border': "#A5C4E0",
    'scrollbar': "#A5C4E0",
    
    # Text colors
    'text_primary': "#333333",
    'text_title': "#1a1a1a",
}

# =============================================================================
# Typography
# =============================================================================
TYPOGRAPHY = {
    'family': "Segoe UI",
    'size': {
        'normal': "12pt",
        'small': "11pt",
        'title': "14pt"
    }
}

# =============================================================================
# Plot Styling (Primary Definition)
# =============================================================================
PLOT_STYLES = {
    'colors': {
        'deterministic': '#6C63FF',
        'previous': '#00C896',
        'probabilistic': '#D3D3D3',
        'saved': '#FF6B6B',
        'grid': COLORS['grid']
    },
    'background': COLORS['background'],
    'grid': {
        'color': COLORS['grid'],
        'alpha': 0.2,
        'linestyle': '-',
        'linewidth': 0.25
    },
    'lines': {
        'deterministic': {
            'linewidth': 3,
            'alpha': 1.0
        },
        'previous': {
            'linewidth': 1,
            'alpha': 0.7
        },
        'probabilistic': {
            'linewidth': 1,
            'alpha': 0.25
        },
        'saved': {
            'linewidth': 2,
            'alpha': 0.7
        }
    }
}

# =============================================================================
# Widget Styling (Primary Definition)
# =============================================================================
WIDGET_STYLES = {
    'background': COLORS['background'],
    'plot_face': COLORS['background']
}

# =============================================================================
# Common StyleSheets (Primary Definition)
# =============================================================================
COMMON_STYLES = {
    'main_widget': f"""
        QWidget {{
            background-color: {COLORS['background']};
            font-family: {TYPOGRAPHY['family']};
            font-size: {TYPOGRAPHY['size']['normal']};
            color: {COLORS['text_primary']};
        }}
    """,
    
    'scroll_area': f"""
        QScrollArea {{ 
            border: none; 
            background-color: {COLORS['background']}; 
            padding-right: 20px;
        }}
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 6px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {COLORS['scrollbar']};
            min-height: 20px;
            border-radius: 3px;
            opacity: 0.7;
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollBar:horizontal {{
            height: 0px;
        }}
    """,
    
    'input_fields': f"""
        QLineEdit, QComboBox {{
            background-color: {COLORS['input_field']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 5px;
            font-family: {TYPOGRAPHY['family']};
            font-size: {TYPOGRAPHY['size']['normal']};
            color: {COLORS['text_primary']};
        }}
        QLabel {{
            margin-top: 10px;
            margin-bottom: 5px;
        }}
    """
}

# =============================================================================
# Button Style
# =============================================================================
BUTTON_STYLE = """
    QPushButton {
        background-color: #7FA5C4;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #6E94B3;
    }
    QPushButton:pressed {
        background-color: #5D83A2;
    }
"""

# =============================================================================
# Layout Constants
# =============================================================================
FORM_LAYOUT = {
    'spacing': {
        'divider': 20,
        'section': 10,
        'field': 5
    },
    'dimensions': {
        'label_width': 150,
        'tooltip_width': 20
    }
}

# =============================================================================
# Legacy/Compatibility Definitions (referencing primary definitions above)
# =============================================================================

# Legacy plot colors (referencing PLOT_STYLES)
COLORS.update({
    'plot_deterministic': PLOT_STYLES['colors']['deterministic'],
    'plot_previous': PLOT_STYLES['colors']['previous'],
    'plot_probabilistic': PLOT_STYLES['colors']['probabilistic'],
    'plot_saved': PLOT_STYLES['colors']['saved']
})

# Legacy widget styles (referencing WIDGET_STYLES)
WIDGET_STYLES.update({
    'splitter': WIDGET_STYLES['background'],
    'scrollarea': WIDGET_STYLES['background']
})

# Legacy tooltip and divider styles (using primary colors)
TOOLTIP_STYLE = """
    QLabel {
        color: blue;
        font-weight: bold;
        font-size: 12px;
        border: 1px solid black;
        border-radius: 5px;
        padding: 2px;
        background-color: #f0f0f0;
    }
    QLabel:hover {
        background-color: #e1e1e1;
    }
"""

DIVIDER_STYLE = {
    'color': COLORS['border'],
    'height': 1,
    'margin': 20
}

CLIENT_DETAILS_STYLE = f"""
    QLabel {{
        font-size: {TYPOGRAPHY['size']['title']};
        font-weight: bold;
        margin: 20px 0;
        color: {COLORS['text_primary']};
    }}
"""
