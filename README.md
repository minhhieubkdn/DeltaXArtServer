# Delta X Art Software User Guide

Welcome to the Delta X Art Software tutorial. This guide will walk you through the process of setting up and using the software to create stunning drawings with your Delta X robot.

## Step-by-Step Instructions

### Step 1: Download `Delta X Art` Software 

Visit the [Delta X Art GitHub repository](https://github.com/minhhieubkdn/DeltaXArtServer/) to download the latest version of the software.

### Step 2: Run the Python Server Code

1. Ensure that Python is installed on your system.
2. Install the required libraries by running the command `pip install -r requirements.txt`.
3. Execute the main.py file to start the server code.

### Step 3: Open Delta X Art Software

1. Launch the Delta X Art Software.
2. Log in using the default credentials: Username: admin, Password: 123456.
3. Open a pre-existing project by clicking the Folder icon under the Open Recent section.
4. Select the `Rose.json` project.
5. Expand the menu toolbar by clicking the `<` button on the right side.
6. Click `Export G-code` button to navigate to Export Gcode Screen.
7. Click the `Move` icon at the bottom-left of the screen to enable moving and scaling actions. Use the `left mouse` button to` drag and drop`, and the `mouse wheel` to `scale` the drawing. Click the `Move` icon again to disable drawing movement.
8. Choose the right robot model (D400, D600 or D800).
9. Install the pen and pen holder onto the moving base.
10. Use the `Delta X Software` to lower the pen until it is nearly touching the drawing plane. Take note of this Z position and add 15 to obtain the Z_SAFE parameter. Enter this value in the Z Safe box.
11. Map the robot coordinates to the drawing plane by touching three points on the drawing. Record the positions of these points and enter them in the `Right Menu`.
12. Once all settings are configured, click the `Export Gcodes` icon in the `Left Tool Bar`.
13. Copy the generated G-code and paste it into the `Delta X Software` to initiate the drawing process.

![Rose](/imgs/rose.png)