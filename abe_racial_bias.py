from psychopy import visual, core, event
from numpy import random
import glob, os
import numpy as np

#global variables presented here



# get_keypress() - Takes no arguments and returns any possible keypresses. 
# If no keypress is detected, returns None
def get_keypress():
    keys = event.getKeys()
    if keys:
        return keys[0]
    else:
        return None

# shutdown(win) - Takes the current active window as an argument and 
# closes the window and cleanly exits the current script. Doesn't return
# a value
def shutdown(win):
    win.close()
    core.quit()

# init_window() - Takes no arguments and initializes the main active
# window to use for the experiment
def init_window():
    wd = visual.Window(
        size=[1400, 800],
        units="pix",
        fullscr=True 
    )
    return wd

# get_images(dir) - Takes a string argument for directory and returns
# a list of all JPEG images within that directory
# Requires: [dir] must be a valid directory
def get_images(dir):
    os.chdir(dir)
    imgList = []
    for file in glob.glob("*.jpg"):
        imgList.append(file)
    return imgList

# encoding_loop(win, stimImages) - Takes a window argument and a list of 
# images to use as stimuli. This function essentially runs the encoding 
# and detection tasks of the experiment. 
def encoding_loop(win, stimImages):
    #generates a red square
    redSq = visual.Rect(
        win=win,
        units="pix",
        width=10,
        height=10,
        fillColor=[1, -1, -1],
        lineColor=[1, -1, -1])
    #Below loop runs through each image in the stimImages argument and runs the procedure on it
    for stim in stimImages:
        img = visual.ImageStim(win=win, image=stim, units="pix") #Image presented as a Stim
        tex = np.array([
            [1, 0],
            [0, -1]
            ]) #numpy array used to make the texture for scrambled image
        scramble = visual.GratingStim(win, tex=tex, mask = None, size=256) #scrambled image
        
        clock = core.Clock()
        while clock.getTime() <= 1.0:
            key = get_keypress()
            if key == 'q':
                shutdown(win) #sets up q as 'escape' character to quit program
            if 0.0 <= clock.getTime() < .050:
                img.draw()
                win.flip()
            elif 0.050 <= clock.getTime() < 0.150:
                img.draw()
                redSq.draw() #target presented briefly (100ms)
                win.flip()
            elif 0.150 <= clock.getTime() < 0.2:
                img.draw()
                win.flip()
            else:
                scramble.draw() #scrambled image presented for remaining 800ms
                win.flip()

# main() - Takes no arguments and runs the main program
def main():
    win = init_window()
    oldImages = get_images("./Stimuli/Old_Images")
    encoding_loop(win, oldImages)

# Below two lines of python actually run the main function
if __name__ == "__main__":
    main()