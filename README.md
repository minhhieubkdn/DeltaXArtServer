# Delta X Art software tutorial

## Preparation

### Step 1: Download Software at [HERE](https://github.com/minhhieubkdn/DeltaXArtServer/tree/master/download)

### Step 2: Run python server code (main.py)

* Make sure Python is installed
* Install requirement libs by command `pip install -r requirements.txt`.
* Run the `main.py` file to start the server code.

### Step 3: Open Delta X Art Software

* Login with default account `admin` and password `123456`.
* Open pre-project by click icon `Folder` button under `Open Recent`.
* Open `Rose.json` project.
* Click the `<` Expand button in the right side to open `Menu Tool Bar`.
* Click `Export G-code` button to move to Export Gcode Menu Screen.
* Click `Move` icon button at the left - bottom of the screen to enable moving and scaling action. Now use the left mouse to drag and drop, mouse wheel to scale the drawing. Click `Move` icon button again to disable drawing movement.
* Choose the right robot model (D400, D600 or D800)
* Install Pen and pen holder to moving base. Then use `Delta X Software` to move the pen down to almost touch the drawing plane. Taking that Z position and adding 15 we will get the Z_SAFE parameter. Then put it in `Z Safe` box.
* Then we map the robot coordinates with the drawing plane by 3 points. Move the pen to touch 3 points in drawing plane and get the positions, then fill 3 points parameters in the `Right Menu`.
* After you done everything, just clicking `Export Gcodes` icon button in the `Right Tool Bar`. Copy that G-code and paste it in `Delta X Software` to start drawing.
