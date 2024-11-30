# There is currently an issue with horizontal axis - it's fine right now but when benchmark age changes, the plot changes but the horizontal axis doesn't

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QScrollArea,
    QFrame,
    QCheckBox,
    QPushButton,
    QSizePolicy,
    QInputDialog,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QDesktopServices
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from calcs import simulate_annual_investment_balances
import config
import os
import numpy as np
import pandas as pd
from viz_widgets import init_input_widget
from styles import (
    COLORS, 
    PLOT_STYLES, 
    COMMON_STYLES, 
    BUTTON_STYLE, 
    TYPOGRAPHY, 
    FORM_LAYOUT
)
from viz_charts import ChartManager

# Use imported colors
BACKGROUND_COLOR = COLORS['background']
INPUT_FIELD_COLOR = COLORS['input_field']
GRID_COLOR = COLORS['grid']
FONT_FAMILY = "Segoe UI"          # Keep original font settings
FONT_COLOR = COLORS['text_primary']
TITLE_COLOR = COLORS['text_title']

# Use imported plot colors
plot_colors = PLOT_STYLES['colors']

# Keep original background color assignments
qwidget_background_colour = BACKGROUND_COLOR
qsplitter_background_colour = BACKGROUND_COLOR
qscrollarea_background_colour = BACKGROUND_COLOR
init_plot_widget_facecolor = BACKGROUND_COLOR
init_plot_widget_stylesheet_background_color = BACKGROUND_COLOR

def currency_formatter(x, pos):
    return "${:,.0f}".format(x)


def on_save_variables_button_clicked():
    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )  # Define BASE_DIR before using it
    csv_path = os.path.join(
        BASE_DIR, "default.csv"
    )  # Change the file extension to .csv
    save_config_to_excel(config, csv_path)


def save_config_to_excel(config_module, csv_path):
    # Create a DataFrame with two columns: Variable and Value
    data = {"Variable": [], "Value": []}

    # Add the configuration variables and their values to the DataFrame
    for var in dir(config_module):
        # Filter out built-in attributes and methods
        if not var.startswith("__") and not callable(getattr(config_module, var)):
            data["Variable"].append(var)
            data["Value"].append(getattr(config_module, var))

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Convert the 'Variable' column to the title case and replace underscores with spaces
    df["Variable"] = df["Variable"].str.replace("_", " ").str.title()

    # Write the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)

    print(f"Configuration saved to {csv_path}")


class MyWindow(QMainWindow):
    plot_needs_update = pyqtSignal()  # Create a signal to update plot

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Flawcastr")
        self.setWindowState(Qt.WindowMaximized)
        
        # Initialize ChartManager first
        self.chart_manager = ChartManager()
        
        # Use chart_manager's canvas instead of creating our own
        self.fig = self.chart_manager.fig
        self.ax = self.chart_manager.ax
        self.canvas = self.chart_manager.canvas
        
        # Keep these as they're used by other methods
        self.saved_scenarios = self.chart_manager.saved_scenarios
        self.validation_labels = self.chart_manager.validation_labels
        self.last_deterministic_balances = self.chart_manager.last_deterministic_balances
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Padding around entire window
        main_layout.setSpacing(0)  # Set to 0 for no space between columns
        
        # Create right side container
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)  # No internal padding
        right_layout.setSpacing(0)  # No extra spacing
        
        # Add the canvas to the right container
        right_layout.addWidget(self.canvas)
        
        # Create left side container (chart)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)  # No internal padding
        left_layout.setSpacing(0)  # No extra spacing
        
        # Create scroll area container for input widgets
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(20, 20, 40, 20)
        scroll_layout.setSpacing(12)
        
        # Initialize input widget
        self.config_var_format = {}
        init_input_widget(self)
        
        # Create scroll area for input widget
        scroll = QScrollArea()
        scroll.setStyleSheet(COMMON_STYLES['scroll_area'])
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.input_widget)
        
        # Add scroll area to scroll container
        scroll_layout.addWidget(scroll)
        
        # Create buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(20, 10, 20, 20)  # Add consistent padding around buttons
        buttons_layout.setSpacing(10)
        
        # Add buttons
        save_button = QPushButton("Save scenario for comparison")
        save_button.clicked.connect(self.on_save_scenario_clicked)
        clear_button = QPushButton("Clear saved scenarios")
        clear_button.clicked.connect(self.on_clear_scenarios_clicked)
        feedback_button = QPushButton("Leave feedback")
        feedback_button.clicked.connect(self.open_email_client)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(clear_button)
        buttons_layout.addWidget(feedback_button)
        
        # Apply button styles
        save_button.setStyleSheet(BUTTON_STYLE)
        clear_button.setStyleSheet(BUTTON_STYLE)
        feedback_button.setStyleSheet(BUTTON_STYLE)
        
        # Add widgets to left layout
        left_layout.addWidget(scroll_container, 1)  # Add stretch factor
        left_layout.addWidget(buttons_container, 0)  # No stretch
        
        # Add containers to main layout in reverse order
        main_layout.addWidget(left_container, 1)   # Now first
        main_layout.addWidget(right_container, 2)  # Now second
        
        # Now apply all styles
        self.setStyleSheet(COMMON_STYLES['main_widget'])
        
        # Apply plot styling
        self.fig.patch.set_facecolor(PLOT_STYLES['background'])
        self.ax.set_facecolor(PLOT_STYLES['background'])
        
        # Apply scroll area styling
        scroll.setStyleSheet(COMMON_STYLES['scroll_area'])
        
        # Apply input styling
        self.input_widget.setStyleSheet(COMMON_STYLES['input_fields'])
        
        # Apply button styles
        save_button.setStyleSheet(BUTTON_STYLE)
        clear_button.setStyleSheet(BUTTON_STYLE)
        feedback_button.setStyleSheet(BUTTON_STYLE)

        # Set button layout spacing
        buttons_layout.setContentsMargins(10, 5, 10, 5)
        buttons_layout.setSpacing(FORM_LAYOUT['spacing']['field'])
        
        self.setCentralWidget(main_widget)
        
        # Connect plot update signal
        self.plot_needs_update.connect(self.update_plot)
        self.update_plot()

    def init_plot_widget(self):
        self.update_plot()

    def open_email_client(self):
        email = "sonnie.bailey@outlook.com"
        subject = "Flawcastr feedback"
        body = ""

        QDesktopServices.openUrl(
            QUrl(f"mailto:{email}?subject={subject}&body={body}", QUrl.TolerantMode)
        )

    def on_save_scenario_clicked(self):
        # Open a dialog box for the user to input the scenario name
        scenario_name, ok = QInputDialog.getText(
            self, "Save Scenario", "Enter scenario name:"
        )
        if ok:
            # Save the current deterministic balances as a scenario
            try:
                deterministic_balances, _, _ = simulate_annual_investment_balances()
                self.saved_scenarios.append(deterministic_balances)
                self.validation_labels[scenario_name] = deterministic_balances
                self.update_plot()
                # Update the scenario name label
                self.scenario_name_label.setText(
                    f"Scenario Name: {scenario_name}"
                )  # Include "Scenario Name: "
            except Exception as e:
                print(f"Error")

    def on_clear_scenarios_clicked(self):
        # Clear the saved scenarios and update the plot
        self.saved_scenarios.clear()
        self.validation_labels.clear()
        self.update_plot()

    def update_plot(self):
        try:
            years = self.chart_manager.calculate_years()
            self.chart_manager.clear_and_plot_previous_balances(years)
            self.chart_manager.plot_saved_scenarios(years)
            self.chart_manager.plot_probabilistic_balances(years)
            self.chart_manager.plot_deterministic_balances(years)
            self.chart_manager.set_plot_styling()
        except Exception as e:
            print(f"Error updating the plot: {e}")
            self.ax.clear()
            self.ax.text(
                0.5,
                0.5,
                "Error: Unable to update the plot",
                transform=self.ax.transAxes,
                ha="center",
                va="center",
            )
        finally:
            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
