# Color palette for the application
COLORS = {
    'accent': '#FD0363',  # Primary accent color
    'accent_dark_1': '#CC095D',
    'accent_dark_2': '#9C1057',
    'accent_dark_3': '#6B1650',
    'accent_dark_4': '#3B1D4A',
    'background': '#0A2344',  # Main background color
}

# Additional color utilities
def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgba(hex_color, alpha=1.0):
    """Convert hex color to RGBA tuple"""
    rgb = hex_to_rgb(hex_color)
    return (*rgb, alpha) 