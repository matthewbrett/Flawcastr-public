# Flawcastr Interface Requirements

This document specifies function signatures and critical interfaces that must be maintained across all Flawcastr modules.

Before making any change to code, please check that the function signatures and data structures are compatible with the existing code. If you identify a discrepancy, please bring this to the attention of whomever you are working with as a priority.

## calcs.py
Must maintain these function signatures:
- display_results(years: int, result_data: dict) -> None
- simulate_annual_investment_balances() -> Tuple[List[float], List[float], List[List[float]]]
- update_and_display_results() -> dict
- calculate_retirement_expenditures() -> List[float]
- calculate_savings() -> List[float]
- calculate_nz_super() -> List[float]
- calculate_periodic_expenditure() -> List[float]
- calculate_one_off_items() -> List[float]
- calculate_one_off_item_impact() -> List[float]
- children_one_off_assistance() -> List[float]
- children_educational_assistance() -> List[float]
- calculate_deterministic_balances() -> List[float]
- calculate_probabilistic_balances() -> List[List[float]]
- get_rate(balance: float) -> float
Note: All calculation functions must maintain compatibility with config variables

## viz_charts.py
ChartManager class must maintain these method signatures:
- __init__() -> None
- calculate_years() -> np.array
- clear_and_plot_previous_balances(years: np.array) -> None
- plot_deterministic_balances(years: np.array) -> None
- plot_saved_scenarios(years: np.array) -> None
- plot_probabilistic_balances(years: np.array = None) -> None
- set_plot_styling() -> None
- add_scenario(name: str, scenario_data: np.array) -> None
- clear_scenarios() -> None
Note: All plotting methods must maintain matplotlib/PyQt widget compatibility

## viz_widgets.py
Must maintain these function signatures:
- init_input_widget(window: MyWindow) -> None
- update_client_details_label(window: MyWindow) -> None
- add_input_field(window: MyWindow, var_name: str, item_dict: dict, section: Optional[QWidget] = None) -> None
- add_toggle(window: MyWindow, var_name: str, toggled_items: list, item_dict: dict, section: Optional[QWidget] = None) -> None
- on_field_edit_finish(window: MyWindow, var_name: str, field: QLineEdit) -> None
- update_field_visibility(window: MyWindow) -> None
- toggle_all_sections(window: MyWindow, button: QPushButton) -> None
Note: Must maintain PyQt widget hierarchy and trigger plot updates appropriately

## flawcastr.py
ClientInfoDialog class must maintain:
- get_data() -> dict
- update_client2_visibility() -> None

Must maintain these function signatures:
- check_expiry() -> bool
- apply_initial_window_data_to_config(client_info: dict) -> None
- update_config_from_csv(csv_path: str, config_module: Any, initial_load: bool = False, skip_vars: List[str] = []) -> List[str]
- load_initial_configuration() -> None

## config.py
Must maintain all variable definitions with specified types:
- Dates as datetime.date
- Numbers as int or float
- Text as str
- Booleans as "yes"/"no" strings for toggles

## validation.py
Must maintain these function signatures:
- generate_base_table() -> dict
- modify_variable(var_name: str, original_value: Any) -> Any
- adjust_year_column(dataframe: pd.DataFrame, base_year_col: str = "Age1") -> pd.DataFrame
- run_validation() -> None

## collate.py
Must maintain these function signatures:
- natural_sort_key(s: str) -> List[Union[int, str]]
Note: Must maintain ability to collect and combine .md and .py files

## styles.py
Must maintain these constant dictionaries:
- COLORS: Dict[str, str]
- TYPOGRAPHY: Dict[str, Union[str, Dict[str, str]]]
- PLOT_STYLES: Dict[str, Dict]
- WIDGET_STYLES: Dict[str, str]
- COMMON_STYLES: Dict[str, str]
- BUTTON_STYLE: str
- FORM_LAYOUT: Dict[str, Dict[str, int]]
- TOOLTIP_STYLE: str
- DIVIDER_STYLE: Dict[str, Any]
- CLIENT_DETAILS_STYLE: str

## viz_widgets_config.py
Must maintain these data structures:
- section_titles: Dict[int, str]
- config_var_list: List[Dict[str, Any]]
Note: Dictionary structures must maintain all currently used key types

## Global Notes:
1. All functions that update config variables must emit window.plot_needs_update.emit()
2. All numerical input fields must maintain proper type conversion
3. All matplotlib/PyQt widgets must maintain proper parent-child relationships
4. Error handling must preserve existing error message display methods