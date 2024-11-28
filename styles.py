"""
styles.py - Central styling configuration for Flawcastr

This module contains all styling-related constants and configurations used across
the application. It's organized by component type and usage context.
"""

# =============================================================================
# Color Palette
# =============================================================================
COLORS = {
    # Base colors
    'background': "#E1ECF4",      # Main application background
    'input_field': "#EDF2F7",     # Form input backgrounds
    'accent': "#6C63FF",          # Primary accent color
    'grid': "#E9ECEF",            # Grid lines in charts
    'border': "#A5C4E0",          # Border colors
    'scrollbar': "#A5C4E0",       # Scrollbar styling
    
    # Text colors
    'text_primary': "#333333",    # Primary text color
    'text_title': "#1a1a1a",      # Title text color
    
    # Plot-specific colors
    'plot_deterministic': '#6C63FF',    # Main line in plots
    'plot_previous': '#00C896',         # Previous scenario line
    'plot_probabilistic': '#D3D3D3',    # Probabilistic scenarios
    'plot_saved': '#FF6B6B',            # Saved scenarios
}

# =============================================================================
# Typography
# =============================================================================
TYPOGRAPHY = {
    'family': "Segoe UI",    # Main font family
    'size': {
        'normal': "12pt",
        'small': "11pt",
        'title': "14pt"
    }
}

# =============================================================================
# Plot Styling
# =============================================================================
PLOT_STYLES = {
    'colors': {
        'deterministic': '#6C63FF',    # Main line in plots
        'previous': '#00C896',         # Previous scenario line
        'probabilistic': '#D3D3D3',    # Probabilistic scenarios
        'saved_scenarios': '#FF6B6B',  # Saved scenarios
        'grid': COLORS['grid']
    },
    'background': COLORS['background'],
    'grid': {
        'color': COLORS['grid'],
        'alpha': 0.2,                  # Reduced from 0.5 to be less prominent
        'linestyle': '-',              # Changed from '--' to solid line
        'linewidth': 0.25              # Reduced from 0.5 for finer grid
    },
    'lines': {
        'deterministic': {
            'linewidth': 3,            # Match original
            'alpha': 1.0
        },
        'previous': {
            'linewidth': 1,
            'alpha': 0.7
        },
        'probabilistic': {
            'linewidth': 1,
            'alpha': 0.25              # Keep transparency for multiple lines
        },
        'saved': {
            'linewidth': 2,
            'alpha': 0.7
        }
    }
}

# =============================================================================
# Widget Styling
# =============================================================================
WIDGET_STYLES = {
    'background': COLORS['background'],
    'splitter': COLORS['background'],
    'scrollarea': COLORS['background'],
    'plot_face': COLORS['background'],
}

# =============================================================================
# Button Styling
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
# Common Widget StyleSheets
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

# Form Layout Constants
FORM_LAYOUT = {
    'spacing': {
        'divider': 20,          # Spacing around dividers
        'section': 10,          # Spacing between sections
        'field': 5             # Spacing between fields
    },
    'dimensions': {
        'label_width': 150,    # Fixed width for labels
        'tooltip_width': 20    # Width for tooltip buttons
    }
}

# Explanation Button Style
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

# Divider Style
DIVIDER_STYLE = {
    'color': COLORS['border'],
    'height': 1,
    'margin': 20
}

# Client Details Label Style
CLIENT_DETAILS_STYLE = """
    QLabel {
        font-size: 14pt;
        font-weight: bold;
        margin: 20px 0;
        color: #333333;
    }
"""
