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


###### TRY USING THESE FOR VIZ STYLING??? #########
qwidget_background_colour = "#FFFFFF"  # Pure white background
qsplitter_background_colour = "#F8F9FA"  # Light gray
qscrollarea_background_colour = "#FFFFFF"  # Pure white
init_plot_widget_facecolor = "#FFFFFF"  # Pure white
init_plot_widget_stylesheet_background_color = "#FFFFFF"  # Pure white

# Button colors
button_style = """
    QPushButton {
        background-color: #0D6EFD;  /* Bootstrap primary blue */
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #0B5ED7;  /* Slightly darker blue on hover */
    }
    QPushButton:pressed {
        background-color: #0A58CA;  /* Even darker blue when pressed */
    }
"""

# Color scheme variables - using darker blue background
BACKGROUND_COLOR = "#E1ECF4"      # Darker blue background for entire app
INPUT_FIELD_COLOR = "#EDF2F7"     # Slightly lighter blue for input fields
ACCENT_COLOR = "#6C63FF"          # Vibrant purple for primary actions
GRID_COLOR = "#E9ECEF"            # Lighter gray for grid lines

# Ensure ALL background color variables are set to the same blue
qwidget_background_colour = BACKGROUND_COLOR
qsplitter_background_colour = BACKGROUND_COLOR
qscrollarea_background_colour = BACKGROUND_COLOR
init_plot_widget_facecolor = BACKGROUND_COLOR
init_plot_widget_stylesheet_background_color = BACKGROUND_COLOR

# Plot colors - more distinct and vibrant
plot_colors = {
    'deterministic': '#6C63FF',    # Vibrant purple for main line
    'previous': '#00C896',         # Bright teal for previous line
    'probabilistic': '#D3D3D3',    # Light gray for probabilistic
    'saved_scenarios': '#FF6B6B',  # Coral red for saved scenarios
    'grid': GRID_COLOR            # Consistent grid color
}

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

        self.saved_scenarios = []
        self.validation_labels = {}
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # Create left side container
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        
        # Create buttons container with fixed height
        buttons_container = QWidget()
        buttons_container.setFixedHeight(80)  # Reduced from 100 to 80
        buttons_layout = QHBoxLayout(buttons_container)
        
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
        
        # Add buttons container to left layout
        left_layout.addWidget(buttons_container)
        
        # Initialize input widget
        self.config_var_format = {}
        init_input_widget(self)
        
        # Create scroll area for input widget
        scroll = QScrollArea()
        scroll.setStyleSheet(f"""
            QScrollArea {{ 
                border: none; 
                background-color: {qscrollarea_background_colour}; 
            }}
            QScrollBar:vertical {{
                border: none;
                background: lightgrey;
                width: 5px;
                opacity: 0.25;
            }}
            QScrollBar::handle:vertical {{
                background: lightgrey;
                min-height: 10px;
            }}
        """)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.input_widget)
        
        # Add scroll area to left layout
        left_layout.addWidget(scroll)
        
        # Initialize plot
        self.last_deterministic_balances = None
        self.init_plot_widget()
        
        # Add widgets to main layout
        main_layout.addWidget(left_container, 1)
        main_layout.addWidget(self.canvas, 2)
        
        self.setCentralWidget(main_widget)
        
        # Connect plot update signal
        self.plot_needs_update.connect(self.update_plot)
        self.update_plot()

        # Apply button styles
        save_button.setStyleSheet(button_style)
        clear_button.setStyleSheet(button_style)
        feedback_button.setStyleSheet(button_style)
        
        # Force background color on all widgets and style input fields with larger font
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BACKGROUND_COLOR};
                font-size: 12pt;  /* Increased base font size */
            }}
            QLabel {{
                font-size: 12pt;  /* Explicit font size for labels */
            }}
            QScrollArea {{ 
                background-color: {BACKGROUND_COLOR};
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {BACKGROUND_COLOR};
            }}
            QLineEdit {{
                background-color: {INPUT_FIELD_COLOR};
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                padding: 5px;
                font-size: 12pt;  /* Explicit font size for input fields */
            }}
            QComboBox {{
                background-color: {INPUT_FIELD_COLOR};
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                padding: 5px;
                font-size: 12pt;  /* Explicit font size for dropdowns */
            }}
            QPushButton {{
                font-size: 11pt;  /* Slightly smaller font for buttons */
                {button_style}
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
        """)
        
        main_widget.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")
        self.input_widget.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")
        
        # Update canvas background
        self.canvas.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")
        self.fig.patch.set_facecolor(BACKGROUND_COLOR)
        self.ax.set_facecolor(BACKGROUND_COLOR)

        # Reduce spacing in button layout
        buttons_layout.setContentsMargins(10, 5, 10, 5)  # Reduced vertical margins
        buttons_layout.setSpacing(10)  # Reduced spacing between buttons

    def init_plot_widget(self):
        self.fig = Figure(facecolor=init_plot_widget_facecolor)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet(
            f"background-color: {init_plot_widget_stylesheet_background_color};"
        )

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
            years = self.calculate_years()  # Recalculate the years
            self.clear_and_plot_previous_balances(years)
            self.plot_saved_scenarios(years)
            self.plot_probabilistic_balances(years)
            self.plot_deterministic_balances(years)
            self.set_plot_aesthetics()
        except Exception as e:
            # Handle or log the exception
            print(f"Error updating the plot: {e}")
            # Optionally, clear the plot or display an error message on the plot
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
            self.canvas.draw()  # Ensure the canvas is updated

    def calculate_years(self):
        years_to_model = config.age_to_follow_to - config.client1_age
        return np.arange(config.client1_age, config.client1_age + years_to_model + 1, 1)

    def clear_and_plot_previous_balances(self, years):
        self.ax.clear()
        if self.last_deterministic_balances:
            # Adjust 'years' to match the length of 'last_deterministic_balances'
            if len(years) != len(self.last_deterministic_balances):
                # If 'years' is shorter, assume it's missing the final year and extend it
                if len(years) < len(self.last_deterministic_balances):
                    years = np.arange(len(self.last_deterministic_balances))
                # If 'years' is longer, truncate it to match 'last_deterministic_balances'
                else:
                    years = years[: len(self.last_deterministic_balances)]

            # Add config.client1_age to 'years' for plotting
            adjusted_years = years + config.client1_age

            try:
                self.ax.plot(
                    adjusted_years,
                    self.last_deterministic_balances,
                    color="green",
                    linewidth=1,
                    label="Previous Deterministic",
                )
            except Exception as e:
                self.ax.text(
                    0.5,
                    0.5,
                    "Error: Invalid data for plotting",
                    transform=self.ax.transAxes,
                    ha="center",
                    va="center",
                )

        self.canvas.draw()  # Ensure the canvas is updated even if there's an error

    def plot_deterministic_balances(self, years):
        try:
            deterministic_balances, _, _ = simulate_annual_investment_balances()
            if len(years) != len(deterministic_balances):
                adjusted_years = np.arange(len(deterministic_balances)) + config.client1_age
            else:
                adjusted_years = years + config.client1_age

            self.ax.plot(
                adjusted_years,
                deterministic_balances,
                color=plot_colors['deterministic'],
                linewidth=3,
                label="Deterministic",
            )
            self.last_deterministic_balances = deterministic_balances
            self.max_deterministic_balance = max(deterministic_balances)

        except Exception as e:
            print(f"Error: {e}")
            self.ax.text(
                0.5, 0.5,
                "Error: Unable to simulate balances",
                transform=self.ax.transAxes,
                ha="center", va="center"
            )
        finally:
            self.canvas.draw()

    def plot_saved_scenarios(self, years):
        if self.validation_labels:
            for name, scenario in self.validation_labels.items():
                if len(years) != len(scenario):
                    adjusted_years = np.arange(len(scenario)) + config.client1_age
                else:
                    adjusted_years = years + config.client1_age

                self.ax.plot(
                    adjusted_years, 
                    scenario, 
                    color=plot_colors['saved_scenarios'], 
                    linewidth=2, 
                    alpha=0.7
                )

                last_x = adjusted_years[-1]
                last_y = scenario[-1]
                self.ax.text(last_x, last_y, name, fontsize=11)

    def plot_probabilistic_balances(self, years=None):
        if getattr(config, "investment_probabilistic_approach_yes_or_no", "no") == "no":
            return
        
        _, _, probabilistic_scenarios = simulate_annual_investment_balances()
        
        if years is None or len(years) != len(probabilistic_scenarios[0]):
            years = np.arange(len(probabilistic_scenarios[0]))
        
        adjusted_years = years + config.client1_age
        
        try:
            for scenario_balances in probabilistic_scenarios:
                self.ax.plot(
                    adjusted_years,
                    scenario_balances,
                    color=plot_colors['probabilistic'],
                    linewidth=1,
                    alpha=0.25,
                )
        except Exception as e:
            print(f"Error: {e}")
            self.ax.text(
                0.5, 0.5,
                "Error: Unable to plot probabilistic scenarios",
                transform=self.ax.transAxes,
                ha="center", va="center"
            )

    def set_plot_aesthetics(self):
        self.ax.set_xlabel(f"{config.client1_name}'s age")
        self.ax.set_ylabel("Investment assets")
        self.ax.set_ylim(bottom=0)

        if hasattr(self, "max_deterministic_balance"):
            self.ax.set_ylim(top=2 * self.max_deterministic_balance)

        self.ax.set_xlim(left=config.client1_age, right=config.age_to_follow_to)
        
        # Update grid style
        self.ax.grid(
            True,
            which="both",
            linestyle="--",
            linewidth=0.5,
            color=plot_colors['grid'],
            alpha=0.5
        )
        
        self.ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
        
        # Ensure plot background matches app background
        self.fig.patch.set_facecolor(BACKGROUND_COLOR)
        self.ax.set_facecolor(BACKGROUND_COLOR)
        
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
