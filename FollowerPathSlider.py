"""
Macro: FollowerPathSlider
Author: Tuza Adeyemi Olukan
Version: 1.0
Date: 2024-01-17
Description: This macro allows a follower object to be clamped to a path,
             and a slider is used to vary the position of the follower along the path.
             Tested with FreeCAD version 0.20.1.
"""



import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore

def load_initial_slider_value():
    """
    Load initial slider values from a file.
    You can change the file path where you want it to be saved. Default is your home directory.
    if you change it rember to also change the path for the "save_initial_slider_value(values)" below

    Returns:
        tuple or None: Tuple of (follower_name, curve_name, clamped_percentage, initial_value)
                       or None if the file doesn't exist or has incorrect data.
    """
    file_path = os.path.join(os.path.expanduser("~"), "initial_slider_value.txt")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                data = file.read().split(',')
                if len(data) == 4:
                    # Return as tuple (follower_name, curve_name, clamped_percentage, initial_value)
                    print('This is the last' + data[3])
                    return data[0], data[1], float(data[2]), float(data[3])
        except ValueError:
            print("Error: Unable to read values from file. Using default values.")
    return None

def save_initial_slider_value(values):
    """
    Save initial slider values to a file.

    Args:
        values (tuple): Tuple of (follower_name, curve_name, clamped_percentage, initial_value).
    """
    file_path = os.path.join(os.path.expanduser("~"), "initial_slider_value.txt")
    try:
        with open(file_path, "w") as file:
            file.write(','.join(map(str, values)))
    except OSError as e:
        print(f"Error: Unable to save initial slider values. {e}")

# Function to create a custom dialog for object names and clamped percentage
def get_object_names_and_clamped_percentage_dialog(all_object_labels, prev_values):
    """
    Display a dialog for selecting object names and clamped percentage.

    Args:
        all_object_labels (list): List of labels for all objects in the document.
        prev_values (tuple): Previous values to set as defaults in the dialog.

    Returns:
        tuple or None: Tuple of (sphere_name, curve_name, clamped_percentage)
                       or None if the user cancels the input.
    """
    dialog = QtGui.QDialog()
    dialog.setWindowTitle("Object Names and Clamped Percentage Input")
    dialog.setMinimumWidth(300)

    layout = QtGui.QVBoxLayout(dialog)

    follower_label = QtGui.QLabel("Select the name of the Follower:")
    follower_combobox = QtGui.QComboBox()

    curve_label = QtGui.QLabel("Select the name of the Path:")
    curve_combobox = QtGui.QComboBox()

    clamped_percentage_label = QtGui.QLabel("Enter the clamped percentage of curve length:")
    clamped_percentage_spinbox = QtGui.QDoubleSpinBox()
    clamped_percentage_spinbox.setRange(0, 100)  # Adjust the range as needed
    clamped_percentage_spinbox.setSuffix("%")

    ok_button = QtGui.QPushButton("OK")

    layout.addWidget(follower_label)
    layout.addWidget(follower_combobox)
    layout.addWidget(curve_label)
    layout.addWidget(curve_combobox)
    layout.addWidget(clamped_percentage_label)
    layout.addWidget(clamped_percentage_spinbox)
    layout.addWidget(ok_button)

    # Populate comboboxes with suggested names
    follower_combobox.addItems(all_object_labels)
    curve_combobox.addItems(all_sketch_labels)

    # Set previous values if available
    if prev_values:
        follower_combobox.setCurrentText(prev_values[0])
        curve_combobox.setCurrentText(prev_values[1])
        clamped_percentage_spinbox.setValue(prev_values[2])

    # Function to accept the input and close the dialog
    def accept_input():
        dialog.accept()

    ok_button.clicked.connect(accept_input)

    result = dialog.exec_()

    if result == QtGui.QDialog.Accepted:
        return (
            follower_combobox.currentText(),
            curve_combobox.currentText(),
            clamped_percentage_spinbox.value()
        )
    else:
        return None

# Get a list of all object names in the document
all_object_names = [obj.Name for obj in App.ActiveDocument.Objects]
all_object_labels = [obj.Label for obj in App.ActiveDocument.Objects]
all_sketch_labels = [obj.Label for obj in App.ActiveDocument.Objects if obj.isDerivedFrom("Sketcher::SketchObject")]

# Now, all_sketch_labels contains labels of sketch objects only

# Load previous values from the file
prev_values = load_initial_slider_value()

# Create the dialog and get user input for object names and clamped percentage
object_names_and_clamped_percentage = get_object_names_and_clamped_percentage_dialog(all_object_labels, prev_values)

if object_names_and_clamped_percentage:
    follower_name, curve_name, clamped_percentage = object_names_and_clamped_percentage
    # Save the current values to be used as previous values next time
    save_initial_slider_value([follower_name, curve_name, clamped_percentage, prev_values[3]])
else:
    print("User canceled input.")
    follower_name, curve_name, clamped_percentage = "Cube", "Sphere", 97  # Default value

def get_object_name_by_label(label):
    # Get the active document
    doc = App.ActiveDocument

    # Iterate through all objects in the document
    for obj in doc.Objects:
        # Check if the object has a label property
        if hasattr(obj, 'Label'):
            # Check if the label matches the specified label
            if obj.Label == label:
                # Return the object name
                return doc.getObject(obj.Name)

    # If no matching object is found, return None
    return None

# ... (rest of your code)

follower = get_object_name_by_label(follower_name)
curve = get_object_name_by_label(curve_name)

print(f"Follower object: {follower}")
print(f"Curve object: {curve}")

if follower and curve:
    curve_shp = curve.Shape
    edge = curve_shp.Edges[0]

    # Create a slider for controlling the position
    slider = QtGui.QSlider()
    slider.setOrientation(QtCore.Qt.Horizontal)
    slider.setRange(0, int(curve_shp.Length ))  # Adjust the multiplier based on your needs
    initial_value = load_initial_slider_value()
    raw_value = initial_value[3]
    slider.setValue(float(raw_value))  # Cast to int to set the initial value correctly
    display_val = str(round(raw_value/curve_shp.Length*100))
    # Create a label to display the slider value
    value_label = QtGui.QLabel("Parameter Value (t): {}".format(display_val))
    #value_label.setText(f"Parameter Value (t): {display_val}")
    print(display_val)

    def update_position(value):
        doc = App.ActiveDocument
        # Calculate clamped value based on the percentage
        clamped_value = (clamped_percentage / 100) * curve_shp.Length

        # Ensure the clamped value doesn't exceed the maximum
        clamped_value = min(value, clamped_value)

        t = edge.getParameterByLength(clamped_value )  # Adjust the multiplier based on your needs
        v = edge.valueAt(t)
        follower.Placement = App.Placement(v, App.Rotation(App.Vector(0.00, 0.00, 1.00), 0))
        doc.recompute()
        Gui.updateGui()
        t_display = round((clamped_value/curve_shp.Length)*100)
        # Update the label text with the current parameter value (t)
        value_label.setText(f"Parameter Value (t): {t_display}")
        save_initial_slider_value([follower_name, curve_name, clamped_percentage, value])

    slider.valueChanged.connect(update_position)

    # Show the slider and label in a separate dialog
    slider_dialog = QtGui.QDialog()
    layout = QtGui.QVBoxLayout(slider_dialog)
    layout.addWidget(slider)
    layout.addWidget(value_label)  # Add the label to the layout
    slider_dialog.exec_()

else:
    print("One or more objects not found in the active document.")
