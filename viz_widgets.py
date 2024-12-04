from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QFrame,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QCheckBox,
)
from PyQt5.QtCore import Qt
import config
from styles import (
    TOOLTIP_STYLE,
    COMMON_STYLES,
    FORM_LAYOUT,
    CLIENT_DETAILS_STYLE,
)
from viz_widgets_config import section_titles, config_var_list  # Add this line

# Layout Constants
SECTION_LAYOUT_MARGINS = (0, 0, 0, 0)
SECTION_LAYOUT_SPACING = 5
CONTENT_LAYOUT_MARGINS = (10, 0, 0, 0)
CONTENT_LAYOUT_SPACING = 5

# Spacing Constants
CLIENT_DETAILS_SPACING = 20
EXPAND_BUTTON_SPACING = 10
TEXT_EXPLANATION_SPACING = 5
SPACER_SIZE = 20  # For QSpacerItem

# Widget Styling
CONTENT_WIDGET_STYLE = """
    QWidget {
        min-height: 25px;
    }
"""

SECTION_TOGGLE_BUTTON_STYLE = """
    QPushButton {
        text-align: left;
        padding: 2px;
        border: none;
        background-color: transparent;
        font-weight: bold;
    }
"""

EXPAND_ALL_BUTTON_STYLE = """
    QPushButton {
        padding: 5px;
        font-weight: bold;
        background-color: transparent;
        border: 1px solid #ccc;
        border-radius: 3px;
        max-width: 100px;
    }
    QPushButton:hover {
        background-color: #f0f0f0;
    }
"""

# Divider Configuration
DIVIDER_STYLE = {
    'shape': QFrame.HLine,
    'shadow': QFrame.Sunken
}

class CollapsibleSection(QWidget):
    def __init__(self, title):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(*SECTION_LAYOUT_MARGINS)
        self.layout.setSpacing(SECTION_LAYOUT_SPACING)
        
        # Header button
        self.toggle_button = QPushButton(f"▶ {title}")
        self.toggle_button.setStyleSheet(SECTION_TOGGLE_BUTTON_STYLE)
        
        # Content widget
        self.content = QWidget()
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content.setStyleSheet(CONTENT_WIDGET_STYLE)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(*CONTENT_LAYOUT_MARGINS)
        self.content_layout.setSpacing(CONTENT_LAYOUT_SPACING)
        self.content.setVisible(False)
        
        # Add to main layout
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.content)
        
        # Connect toggle
        self.toggle_button.clicked.connect(self.toggle_section)
    
    def toggle_section(self):
        is_visible = not self.content.isVisible()
        self.content.setVisible(is_visible)
        self.toggle_button.setText(f"{'▼' if is_visible else '►'} {self.toggle_button.text()[2:]}")
    
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        self.content_layout.addLayout(layout)


def update_client_details_label(window):
    if getattr(config, "individual_or_couple", "individual") == "individual":
        # For an individual, use this format
        client1_name = getattr(config, "client1_name", "")
        client1_age = getattr(config, "client1_age", "")
        client_details_text = (
            f"<b>Flawcast assumptions for {client1_name} ({client1_age}):</b>"
        )
    else:
        # For a couple, use a different format
        client1_name = getattr(config, "client1_name", "")
        client1_age = getattr(config, "client1_age", "")
        client2_name = getattr(config, "client2_name", "")
        client2_age = getattr(config, "client2_age", "")
        client_details_text = f"<b>Flawcast assumptions for {client1_name} ({client1_age}) and {client2_name} ({client2_age}):</b>"

    window.client_details_label.setText(client_details_text)


def add_combobox(window, var_name, options):
    h_layout = QHBoxLayout()
    label = QLabel(var_name.replace("_", " ").capitalize() + ":")
    combobox = QComboBox()
    combobox.addItems(options)
    combobox.currentIndexChanged.connect(
        lambda index, var=var_name, cb=combobox: on_combobox_changed(window, var, cb)
    )
    window.config_fields[var_name] = combobox

    h_layout.addWidget(label)
    h_layout.addWidget(combobox)
    window.input_layout.addLayout(h_layout)

    # Check the state of the 'explanations' variable
    explanations_enabled = getattr(config, "explanations", "yes") == "yes"
    combobox.setVisible(explanations_enabled)
    label.setVisible(explanations_enabled)


def on_combobox_changed(window, var_name, combobox):
    new_value = combobox.currentText()
    setattr(config, var_name, new_value)
    window.plot_needs_update.emit()


def add_toggle(window, var_name, toggled_items, item_dict, section=None):
    h_layout = QHBoxLayout()
    label_text = item_dict.get("label", var_name.replace("_", " ").capitalize())

    toggle = QCheckBox(label_text)
    window.config_fields[var_name] = toggle

    # Set the checkbox state based on the config value
    if var_name == "individual_or_couple":
        initial_state = getattr(config, var_name) == "couple"
    else:
        initial_state = getattr(config, var_name) == "yes"
    toggle.setChecked(initial_state)

    h_layout.addWidget(toggle)
    
    # Add to section if provided, otherwise add to main layout
    if section:
        section.add_layout(h_layout)
    else:
        window.input_layout.addLayout(h_layout)

    # Connect the signal to the on_toggle_changed function
    toggle.stateChanged.connect(
        lambda state, var=var_name, items=toggled_items: on_toggle_changed(
            window, var, state, items
        )
    )

    # Set initial state and create fields if necessary
    on_toggle_changed(window, var_name, toggle.checkState(), toggled_items)

    # Add tooltip label for explanation if provided
    if "explanation" in item_dict:
        tooltip_text = item_dict["explanation"]
        tooltip_label = QLabel("?")
        tooltip_label.setStyleSheet(TOOLTIP_STYLE)
        tooltip_label.setToolTip(tooltip_text)
        h_layout.addWidget(tooltip_label)
        h_layout.addItem(
            QSpacerItem(SPACER_SIZE, SPACER_SIZE, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

    # Check the state of the 'explanations' variable
    explanations_enabled = getattr(config, "explanations", "yes") == "yes"
    toggle.setVisible(explanations_enabled)


def update_config_and_plot(window, var_name, state, items):
    new_value = "yes" if state == Qt.Checked else "no"
    setattr(config, var_name, new_value)  # Update the config variable
    window.plot_needs_update.emit()


def on_toggle_changed(window, var_name, state, items):
    if var_name == "individual_or_couple":
        if state == Qt.Unchecked:
            new_value = "individual"
        elif state == Qt.Checked:
            new_value = "couple"
    else:
        new_value = "yes" if state == Qt.Checked else "no"

    setattr(config, var_name, new_value)

    update_field_visibility(window)

    window.plot_needs_update.emit()


def update_text_visibility(window, explanations_state):
    explanations_enabled = explanations_state == "yes"
    for key, widget in window.config_fields.items():
        if key.startswith("text_"):
            widget.setVisible(explanations_enabled)


def add_client_info(window, client):
    h_layout = QHBoxLayout()
    label_name = QLabel("Name:")
    field_name = QLineEdit(str(getattr(config, f"{client}_name")))
    field_name.setStyleSheet(COMMON_STYLES['input_fields'])
    window.config_fields[f"{client}_name"] = field_name

    h_layout.addWidget(label_name)
    h_layout.addWidget(field_name)

    label_age = QLabel("Age:")
    field_age = QLineEdit(str(getattr(config, f"{client}_age")))
    field_age.setStyleSheet(COMMON_STYLES['input_fields'])
    window.config_fields[f"{client}_age"] = field_age

    h_layout.addWidget(label_age)
    h_layout.addWidget(field_age)
    window.input_layout.addLayout(h_layout)


# Helper function to add dividers
def add_divider(window):
    window.input_layout.insertSpacing(window.input_layout.count(), FORM_LAYOUT['spacing']['divider'])
    divider = QFrame()
    divider.setFrameShape(DIVIDER_STYLE['shape'])
    divider.setFrameShadow(DIVIDER_STYLE['shadow'])
    window.input_layout.addWidget(divider)
    window.input_layout.insertSpacing(window.input_layout.count(), FORM_LAYOUT['spacing']['divider'])


def add_input_field(window, var_name, item_dict, section=None):
    h_layout = QHBoxLayout()

    label_text = item_dict.get("label", var_name.replace("_", " ").capitalize() + ":")
    label = QLabel(label_text)

    field = QLineEdit()
    field.setStyleSheet(COMMON_STYLES['input_fields'])

    # Store references to the label and field using unique keys
    label_key = f"{var_name}_label"
    field_key = f"{var_name}_field"
    window.config_fields[label_key] = label
    window.config_fields[field_key] = field

    # Set the initial value for the field
    if var_name in [
        "investment_returns_under_threshold",
        "investment_returns_over_threshold",
        "retirement_expenditure_annual_reduction",
    ]:
        # Convert the decimal to a whole number percentage for display
        initial_value = str(round(getattr(config, var_name, 0) * 100, 2))
    else:
        initial_value = str(getattr(config, var_name, ""))
    field.setText(initial_value)

    h_layout.addWidget(label)
    h_layout.addWidget(field)

    # Add tooltip label if there's an explanation
    tooltip_text = item_dict.get("explanation", "")
    if tooltip_text:
        tooltip_label = QLabel("?")
        tooltip_label.setStyleSheet(TOOLTIP_STYLE)
        tooltip_label.setToolTip(tooltip_text)
        h_layout.addWidget(tooltip_label)

    if section:
        section.add_layout(h_layout)
    else:
        window.input_layout.addLayout(h_layout)

    # Connect the editingFinished signal to the on_field_edit_finish function
    field.editingFinished.connect(lambda: on_field_edit_finish(window, var_name, field))

    # Set visibility for field and label
    set_field_and_label_visibility(window, var_name, item_dict)


def add_text_with_explanation(window, text, explanation="", section=None):
    h_layout = QHBoxLayout()
    text_label = QLabel(text)
    h_layout.addWidget(text_label)

    if explanation:
        explanation_button = QLabel("[?]")
        explanation_button.setToolTip(explanation)
        explanation_button.setStyleSheet(TOOLTIP_STYLE)
        h_layout.addWidget(explanation_button)
        h_layout.addStretch(1)

    h_layout.setSpacing(TEXT_EXPLANATION_SPACING)

    if section:
        section.add_layout(h_layout)
    else:
        window.input_layout.addLayout(h_layout)


def add_multi_input_field(window, item_dict, section=None):
    h_layout = QHBoxLayout()

    for index in range(1, 3):
        var_name_key = f"var_name{index}"
        label_key = f"label_{item_dict[var_name_key]}"

        if var_name_key in item_dict:
            var_name = item_dict[var_name_key]
            label_text = item_dict.get(
                label_key, var_name.replace("_", " ").capitalize() + ":"
            )

            label = QLabel(label_text)
            field = QLineEdit(str(getattr(config, var_name, "")))
            field.setStyleSheet(COMMON_STYLES['input_fields'])

            window.config_fields[f"{var_name}_label"] = label
            window.config_fields[var_name] = field

            field.editingFinished.connect(
                lambda var=var_name, fld=field: on_field_edit_finish(window, var, fld)
            )

            h_layout.addWidget(label)
            h_layout.addWidget(field)

    # Add to section if provided, otherwise add to main layout
    if section:
        section.add_layout(h_layout)
    else:
        window.input_layout.addLayout(h_layout)


def set_field_and_label_visibility(window, var_name, item_dict):
    field_visible = True  # Default visibility
    label_key = f"{var_name}_label"
    field_key = f"{var_name}_field"

    # Check for conditional visibility
    if "conditional_on" in item_dict and not item_dict["conditional_on"]():
        field_visible = False

    if label_key in window.config_fields:
        window.config_fields[label_key].setVisible(field_visible)
    if field_key in window.config_fields:
        window.config_fields[field_key].setVisible(field_visible)

def toggle_all_sections(window, button):
    is_expanding = button.text() == "Expand All"
    for section in window.sections:
        section.content.setVisible(is_expanding)
        section.toggle_button.setText(f"{'▼' if is_expanding else '▶'} {section.toggle_button.text()[2:]}")
    button.setText("Collapse All" if is_expanding else "Expand All")

def init_input_widget(window):
    window.input_widget = QWidget()
    window.input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    window.input_layout = QVBoxLayout()
    window.input_layout.setAlignment(Qt.AlignTop)
    window.config_fields = {}
    window.sections = []  # Track all sections

    # Add client details label
    window.input_layout.addSpacing(CLIENT_DETAILS_SPACING)
    window.client_details_label = QLabel()
    window.client_details_label.setStyleSheet(CLIENT_DETAILS_STYLE)
    window.input_layout.addWidget(window.client_details_label)
    update_client_details_label(window)
    window.input_layout.addSpacing(CLIENT_DETAILS_SPACING)

    # Add Expand/Collapse All button
    expand_all_button = QPushButton("Expand All")
    expand_all_button.setStyleSheet(EXPAND_ALL_BUTTON_STYLE)
    expand_all_button.clicked.connect(lambda: toggle_all_sections(window, expand_all_button))
    window.input_layout.addWidget(expand_all_button)
    window.input_layout.addSpacing(EXPAND_BUTTON_SPACING)
    
    current_section = None
    section_count = 0

    # Process config_var_list
    for item_dict in config_var_list:
        item_type = item_dict.get("type")
        
        # Create new section at each divider
        if item_type == "divider":
            section_count += 1
            current_section = CollapsibleSection(section_titles.get(section_count, f"Section {section_count}"))
            window.sections.append(current_section)  # Add section to tracking list
            window.input_layout.addWidget(current_section)
            continue
            
        # Create layout for the item
        if item_type == "multi_input":
            add_multi_input_field(window, item_dict, current_section)
        elif item_type == "toggle":
            var_name = item_dict.get("var_name")
            toggled_items = item_dict.get("toggled_items", [])
            add_toggle(window, var_name, toggled_items, item_dict, current_section)
        elif item_type == "input":
            var_name = item_dict.get("var_name")
            add_input_field(window, var_name, item_dict, current_section)
        elif item_type == "text":
            text = item_dict.get("text", "")
            explanation = item_dict.get("explanation", "")
            add_text_with_explanation(window, text, explanation, current_section)

    update_field_visibility(window)
    window.input_widget.setLayout(window.input_layout)


def add_widget_based_on_type(window, widget_type, var_name, item_dict):
    explanations_enabled = getattr(config, "explanations", "yes") == "yes"

    field_key = f"{var_name}_field"
    label_key = f"{var_name}_label"

    if widget_type == "toggle":
        toggled_items = item_dict.get("toggled_items", [])
        add_toggle(window, var_name, toggled_items)
    elif widget_type == "combobox":
        options = item_dict.get("options", [])
        add_combobox(window, var_name, options)
    elif widget_type == "multi_input":
        add_multi_input_field(window, item_dict)
    elif widget_type == "input":
        add_input_field(window, var_name, item_dict)

        # Set initial visibility for input fields and labels
        if field_key in window.config_fields:
            window.config_fields[field_key].setVisible(explanations_enabled)
        if label_key in window.config_fields:
            window.config_fields[label_key].setVisible(explanations_enabled)


def on_field_edit_finish(window, var_name, field):
    new_value = field.text()

    # Inline validation for specific fields
    if var_name == "savings_rate_change_age":
        client1_current_age = getattr(config, "client1_age", 0)
        if int(new_value) <= client1_current_age:
            field.setText(str(getattr(config, var_name, "")))
            return

    if var_name == "savings_rate_change2_age":
        savings_rate_change_age = getattr(config, "savings_rate_change_age", 0)
        if int(new_value) <= int(savings_rate_change_age):
            field.setText(str(getattr(config, var_name, "")))
            return

    try:
        # Special handling for percentage fields
        if var_name in [
            "investment_returns_under_threshold",
            "investment_returns_over_threshold",
            "retirement_expenditure_annual_reduction",
        ]:
            # Convert user input percentage back to decimal
            updated_value = float(new_value) / 100
        elif var_name.endswith("_age") or var_name == "number_of_children":
            # Update age-related fields and number of children as integers
            updated_value = int(new_value)
        else:
            # Update other fields as floats
            updated_value = float(new_value)

        # Update the configuration variable
        setattr(config, var_name, updated_value)
    except ValueError:
        # If invalid input, reset the field to its previous value
        field.setText(str(getattr(config, var_name, "")))

    field.setModified(False)  # Reset the modified state

    # Update field visibility if the number of children has changed
    if var_name == "number_of_children":
        update_field_visibility(window)

    # Emit signal to update the plot
    window.plot_needs_update.emit()


def update_field_visibility(window):
    for item in config_var_list:
        if "var_name" in item and "conditional_on" in item:
            conditional_visibility_func = item["conditional_on"]
            is_visible = conditional_visibility_func()

            field_key = f"{item['var_name']}_field"
            label_key = f"{item['var_name']}_label"
            if field_key in window.config_fields:
                window.config_fields[field_key].setVisible(is_visible)
            if label_key in window.config_fields:
                window.config_fields[label_key].setVisible(is_visible)

        elif item["type"] == "multi_input" and "conditional_on" in item:
            is_visible = item["conditional_on"]()
            for index in range(1, 3):
                var_name_key = f"var_name{index}"
                if var_name_key in item:
                    var_name = item[var_name_key]
                    field_key = var_name
                    label_key = f"{var_name}_label"
                    if field_key in window.config_fields:
                        window.config_fields[field_key].setVisible(is_visible)
                    if label_key in window.config_fields:
                        window.config_fields[label_key].setVisible(is_visible)


def update_config_var(window, var_name, new_value):
    try:
        # If the variable is 'investment_probabilistic_number_of_scenarios', ensure it's an integer
        if var_name == "investment_probabilistic_number_of_scenarios":
            new_value = int(new_value)
        else:
            new_value = float(new_value)

        setattr(config, var_name, new_value)
        window.plot_needs_update.emit()
    except ValueError:
        # Handle the error for invalid input
        pass

def add_spacer(layout):
    layout.addItem(QSpacerItem(SPACER_SIZE, SPACER_SIZE, QSizePolicy.Expanding, QSizePolicy.Minimum))