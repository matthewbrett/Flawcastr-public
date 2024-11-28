"""
viz_charts.py - Chart Management Module for Flawcastr
"""
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter
import numpy as np
from calcs import simulate_annual_investment_balances
import config
from styles import COLORS, PLOT_STYLES, COMMON_STYLES, BUTTON_STYLE, TYPOGRAPHY

# Remove duplicate color definitions and use imported styles
BACKGROUND_COLOR = COLORS['background']
plot_colors = PLOT_STYLES['colors']
BORDER_COLOR = COLORS['border']
FONT_FAMILY = TYPOGRAPHY['family']
FONT_COLOR = COLORS['text_primary']

def currency_formatter(x, pos):
    return "${:,.0f}".format(x)

class ChartManager:
    def __init__(self):
        # Mirror exactly the same attributes from MyWindow
        self.fig = Figure(facecolor=BACKGROUND_COLOR)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.saved_scenarios = []
        self.validation_labels = {}
        self.last_deterministic_balances = None
        self.max_deterministic_balance = None
        
        # Set initial styling exactly as in MyWindow
        self.canvas.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")
        self.fig.patch.set_facecolor(BACKGROUND_COLOR)
        self.ax.set_facecolor(BACKGROUND_COLOR)

    def calculate_years(self):
        years_to_model = config.age_to_follow_to - config.client1_age
        return np.arange(config.client1_age, config.client1_age + years_to_model + 1, 1)

    def clear_and_plot_previous_balances(self, years):
        self.ax.clear()
        if self.last_deterministic_balances:
            if len(years) != len(self.last_deterministic_balances):
                if len(years) < len(self.last_deterministic_balances):
                    years = np.arange(len(self.last_deterministic_balances))
                else:
                    years = years[: len(self.last_deterministic_balances)]

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

        self.canvas.draw()

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

    def set_plot_styling(self):
        self.ax.set_xlabel(
            f"{config.client1_name}'s age", 
            fontsize=12, 
            fontweight='normal',
            color=FONT_COLOR, 
            fontfamily=FONT_FAMILY
        )
        self.ax.set_ylabel(
            "Investment assets", 
            fontsize=12, 
            fontweight='normal',
            color=FONT_COLOR, 
            fontfamily=FONT_FAMILY
        )
        self.ax.set_ylim(bottom=0)

        if hasattr(self, "max_deterministic_balance"):
            self.ax.set_ylim(top=2 * self.max_deterministic_balance)

        self.ax.set_xlim(left=config.client1_age, right=config.age_to_follow_to)
        
        self.ax.tick_params(axis='both', labelsize=12)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_fontfamily(FONT_FAMILY)
            label.set_color(FONT_COLOR)
        
        self.ax.grid(
            True,
            which="both",
            linestyle="--",
            linewidth=0.5,
            color=plot_colors['grid'],
            alpha=0.5
        )
        
        self.ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
        
        self.fig.patch.set_facecolor(BACKGROUND_COLOR)
        self.ax.set_facecolor(BACKGROUND_COLOR)
        
        for spine in self.ax.spines.values():
            spine.set_color(BORDER_COLOR)
            spine.set_linewidth(1.0)
        
        self.canvas.draw()

    def add_scenario(self, name, scenario_data):
        """Add a new scenario with validation"""
        self.validation_labels[name] = scenario_data
        self.saved_scenarios.append(scenario_data)
        self.canvas.draw()

    def clear_scenarios(self):
        """Clear all saved scenarios"""
        self.saved_scenarios.clear()
        self.validation_labels.clear()
        self.canvas.draw()