# Macro-FollowerPathSlider
 This macro allows a follower object to be clamped to a path,              and a slider is used to vary the position of the follower along the path.              Tested with FreeCAD version 0.20.1.

 # I am working on the video Demo

 # Follower Path Slider Macro for FreeCAD

## Overview

The Follower Path Slider macro for FreeCAD allows you to attach a follower object to a B-spline path and control its position using a slider. This README provides instructions on how to use the macro and explains its features.

## Usage

1. **Run the Macro:**
   - Open FreeCAD.
   - Load the FollowerPathSlider.FCMacro file into FreeCAD.
   - Run the macro.

2. **Select Follower Object:**
   - Click "Select the name of the Follower:" and choose the desired follower object (e.g., bodies, sketches, etc.).

3. **Select Curve Object:**
   - Click "Select the name of the Path:" and choose the B-spline sketch object that will act as the path.

4. **Set Clamped Value:**
   - Enter the clamped percentage of the curve length. This value determines how far the follower will move along the path. Be cautious to avoid divergence issues in some cases.

5. **Click OK:**
   - Click the "OK" button to apply your selections.

6. **Adjust Position:**
   - A slider will appear. Adjust the slider to control the position of the follower along the path.

7. **Save Settings:**
   - The macro will remember your last selection. You can close and reopen FreeCAD, and the software will retain your previous choices.

## Notes

- The follower object can be any FreeCAD object, such as bodies or sketches.
- The curve object must be a B-spline sketch object.
- Be mindful of the clamped value to prevent divergence issues.

## Author

- **Tuza Adeyemi Olukan**
- **Version: 1.0**
- **Date: 2024-01-17**

## License

This macro is provided under the GNU 3.0 specified in the repository.

Feel free to report issues or contribute to the development of this macro.

