Image-Quiz-Application

This is a simple window-application made in Python 3.7 with Arcade 2.3.5 library. Application is a simple quiz about
guessing correct characters from WH40k setting. User clicks on the portraits trying to select only characters aligned
to the chosen fraction. As long as his choices are correct, he can continue picking characters. When he makes a mistake,
quiz is restarted.

I was asked to make this application.

INSTALLATION AND RUN
You can download or clone whole project and run raw python file in console or any IDE, e.g. PyCharm.

1. Download or clone this repository.
2. Setup new virtual environment with Python 3.6.
3. Install requirements with: pip install -r requirements.txt
4. Run main.py in any IDE, e.g. PyCharm, or in Terminal go to dir when you downloaded project and type: python3 quiz.py

Or, you can download only a ready Windows-build zipped as 'WH40K_QUIZ.zip' folder. Unzip it and
run by double-clicking on WH40K_QUIZ shortcut to .exe file.

USE:

In directory **\images** are two subdirectories: **\correct** and **\incorrect**. You can replace dummy images with your own sets 
of images. Put into 'correct' images you want to be counted as good choices, and wrong-ones into the 'incorrect'. When
player mouse-clicks on 'correct' image, quiz continues until he picks all of them. If player choice is wrong, quiz 
terminates. In both cases - quiz can be started again with 'RESTART' button. Images are placed again in new positions.

Press 'ESC' keyboard key to quit application.

Config file: there is a config.txt file in application main directory. It contains one variable:
 _**required_correct_hits**_. You can edit it's value to decide how many correct guesses are 
 required to trigger win-condition. Do not set negative values nor values higher than number of
 images in both 'correct' and 'incorrect' directories! 

TO BE DONE:

1. Add 'stages' or 'turns' functionality: when player picks good image, new set is presented to him, instead of picking
from one, big set until all correct guesses are made.
2. Random (not rows and columns based) positions for images.
3. Animations and sounds.
4. Linux version.
