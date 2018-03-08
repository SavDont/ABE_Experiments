from psychopy import visual, core, event, gui, event
import glob, os
import numpy as np
import random
import pprint

#global variables presented here
colorRed = [1, -1, -1] 
colorGrn = [-1, 1, -1]
textureMask = np.array([
            [1, 0],
            [0, -1]
            ]) #numpy array used to make the texture for scrambled image


# get_keypress() - Takes no arguments and returns any possible keypresses. 
# If no keypress is detected, returns None
def get_keypress():
    keys = event.getKeys()
    if keys:
        return keys[0]
    else:
        return None

# user_input() - Takes no argument and it displays a user input dialog
# requesting for subject number
# Requires: User input must be an int
def user_input():
    dlg = gui.Dlg()
    dlg.addField("Subject Num:")
    
    dlg.show()
    try:
        return int(dlg.data[0])
    except ValueError:
        print "ERROR: No input entered for subject number"
        core.quit()

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

# get_images(dir) - Takes a string argument for directory and a boolean argument 
# for group number and returns a shuffled tuple list for all the JPEG images within
# that directory where the first element of the tuple is the file name and the 
# second element is a boolean value indicating whether this image is a target or
# not.
# Requires: [dir] must be a valid directory
def get_images(dir, groupOne):
    os.chdir(dir)
    
    whiteImages = []
    for file in glob.glob("w*.jpg"):
        whiteImages.append(file)
        
    blackImages = []
    for file in glob.glob("b*.jpg"):
        blackImages.append(file)
        
    if groupOne:
        #targets to appear on 70% of black faces and 30% of white
        targetBlackImages = random.sample(blackImages, 28)
        targetWhiteImages = random.sample(whiteImages, 12)
    else:
        #targets to appear on 30% of black faces and 70% of white
        targetBlackImages = random.sample(blackImages, 12)
        targetWhiteImages = random.sample(whiteImages, 28)
        
    allImages = whiteImages + blackImages
    imgList = []
    for face in allImages:
        if face in targetBlackImages or face in targetWhiteImages:
            imgList.append((face, True))# target image so we set True
        else:
            imgList.append((face, False))
    
    random.shuffle(imgList)
    os.chdir("../..")
    return imgList

# meta_data_write(win, data, subjectNum, groupOne, meta) - Takes the window,
# array of all data, subject number, and group number as arguments
# This function writes the data to a file named to identify the group
# number and the subject number as well as whether or not this is meta data or 
# stimulus data from the experiment
def data_write(win, data, subjectNum, groupOne, meta):
    if meta:
        data_path = ("./Data/P"+str(subjectNum)+"_ABE_Racial_Bias_Exp_Meta_Group"+
            str((not groupOne)+1)+".txt")# labels the file
    else:
        data_path = ("./Data/P"+str(subjectNum)+"_ABE_Racial_Bias_Exp_Data_Group"+
        str((not groupOne)+1)+".txt")
    if not os.path.exists(data_path):
        file = open(data_path, "w")
        textString = ""
        for line in data:
            lineString = ""
            for element in line:
                lineString += str(element)+'\t'
            file.write(lineString+'\n')
        file.close()
    else:
        print "ERROR: Filename "+data_path+" already exists"
        shutdown(win)

# gen_square(win, color) - Takes a window argument and a color
# to create a 10x10 px visual square of the color provided
# Requires: [color] must be a three value list representing color
# as documented in the psychopy library
def gen_square(win, color):
    return visual.Rect(
        win=win,
        units="pix",
        width=10,
        height=10,
        fillColor=color,
        lineColor=color)

# encoding_loop(win, stimImages) - Takes a window argument and a list of 
# images to use as stimuli. It also takes two boolean values representing the
# group number and the target stimulus to use. Lastly, takes in a string
# representing the base directory for the images. This function essentially runs 
# the encoding and detection tasks of the experiment. 
def encoding_loop(win, stimImages, groupOne, redTarget, subjectNum, base_dir):
    redSq = gen_square(win, colorRed) #generates a red square
    greenSq = gen_square(win, colorGrn) #generates a green square
    
    scramble = visual.GratingStim(win, tex=textureMask, mask = None, size=256) #scrambled image
    detectionData = []
    clock = core.Clock()
    #Below loop runs through each image in the stimImages argument and runs the procedure on it
    for (stim, target) in stimImages:
        img = visual.ImageStim(win=win, image=base_dir+stim, units="pix") #Image presented as a Stim
        
        reactionTimes = [] #times when user reacted to the stim
        
        img.draw()
        win.flip() #we want to immediately present the stim and note down the presentation time
        
        stimPresentation = clock.getTime()
        stimExit = 0.0
        stimTimer = core.Clock()
        while stimTimer.getTime() <= 1.0:
            key = get_keypress()
            if key =='escape':
                data_write(win, detectionData, subjectNum, groupOne, False) #writes data before quitting
                shutdown(win) #sets up 'Esc' as a character to quit program
            elif key == 'space':
                reactionTimes.append(clock.getTime())
            
            if 0.0 <= stimTimer.getTime() < .050:
                img.draw()
                win.flip()
            elif 0.050 <= stimTimer.getTime() < 0.150:
                img.draw()
                if (target and redTarget) or (not target and not redTarget):
                    redSq.draw()
                else:
                    greenSq.draw()
                win.flip() #target/distractor presented for 100ms
            elif 0.150 <= stimTimer.getTime() < 0.2:
                img.draw()
                win.flip()
                stimExit = clock.getTime()
            else:
                scramble.draw() #scrambled image presented for remaining 800ms
                win.flip()
        #attach results of experiment to dataset
        detectionData.append(
            [
                stim,
                target,
                stimPresentation,
                stimExit
            ])
        detectionData[len(detectionData)-1].extend(reactionTimes)
    data_write(win, detectionData, subjectNum, groupOne, False)

# main() - Takes no arguments and runs the main program
def main():
    subjectNum = user_input()
    win = init_window()
    
    if subjectNum % 4 <= 1:
        groupOne = True
    else:
        groupOne = False
    oldImages = get_images("./Stimuli/Old_Images", groupOne)
    
    metaData = []
    for (stim, target) in oldImages:
        metaData.append(
            [
                stim,
                target
            ]
        )
    data_write(win, metaData, subjectNum, groupOne, True)
    
    if subjectNum % 2 == 1:
        redTarget = True
    else:
        redTarget = False
    encoding_loop(win, oldImages, groupOne, redTarget, subjectNum, "./Stimuli/Old_Images/")
    #insert shuffling code here

# Below two lines of python actually run the main function
if __name__ == "__main__":
    main()