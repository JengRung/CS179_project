# CS179_project
This is the repository for our project by team Snack Overflow
## Installation
Make sure you are running python 3.10.10 by using
```bash
python --version
```
Which can be installed using pyenv or conda (Or directly).
Next make sure you have PySide2 and Numpy using the following commands
```bash
pip install PySide2
pip install numpy
```
Now, you can change directories to our code base and run the code using
```bash
python gui.py
```
If the UI is wonky, open up GUI.py and change the SIZER value on line 18, which should look like this
```python
SIZER = 1
```
And do the same for SIZER in grid.py on line 8.
If this still doesn't work, please make an issue or email one of us.
