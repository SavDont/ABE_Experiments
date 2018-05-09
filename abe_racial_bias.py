from experiment import Experiment
from psychopy import visual, core, event, gui, event
from collections import defaultdict
from pandas import DataFrame
import glob, os
import numpy as np
import random
import image_slicer

#global variables presented here
colorRed = [1, -1, -1] 
colorGrn = [-1, 1, -1]

def shuffle_images(df):
    '''
    shuffle_images(df) - shuffles the images separately and joins them back 
    together in the original order
        Inputs: [df] is a python dataframe where the first columns is the image
        name, second column indicates whether image is a target, and last column
        indicates whether the image is black or not
        Returns: A shuffled dataframe in the original order of target/distractor
        and black/white conditions. However, the order of each subset of 
        conditions is different
    '''
    t_b = df[(df.t == 1) & (df.b == 1)]
    t_w = df[(df.t == 1) & (df.b == 0)]
    d_b = df[(df.t == 0) & (df.b == 1)]
    d_w = df[(df.t == 0) & (df.b == 0)]

    t_b = t_b.sample(frac=1).reset_index(drop=True)
    t_w = t_w.sample(frac=1).reset_index(drop=True)
    d_b = d_b.sample(frac=1).reset_index(drop=True)
    d_w = d_w.sample(frac=1).reset_index(drop=True)

    df.loc[(df.t == 1) & (df.b == 1), 'img'] = t_b['img'].values
    df.loc[(df.t == 1) & (df.b == 0), 'img'] = t_w['img'].values
    df.loc[(df.t == 0) & (df.b == 1), 'img'] = d_b['img'].values
    df.loc[(df.t == 0) & (df.b == 0), 'img'] = d_w['img'].values

    return df

def get_images(dir, group):
    '''
    get_images(dir, group) - finds the images required for the experiment and 
    classifies each image as a target or not
        Inputs: [dir] is a string representation of the directory to look at to 
        find the images. [group] is an integer representing the group number.
        Returns: A shuffled pandas DataFrame where the first column indicates
        the image name, the second column indicates whether the image is a 
        target and the last column indicates whether the image is a black face
        Requires: [dir] must be a valid directory
    '''
    #create a 2-d list where for each inner list, 1st element is image name
    #second element is whether it is target or not (boolean) and third
    # is whether or not it is a black face or not (boolean)
    img_list = []
    os.chdir(dir)
    
    whiteImages = []
    for file in glob.glob('w*.jpg'):
        whiteImages.append(file)
        
    blackImages = []
    for file in glob.glob('b*.jpg'):
        blackImages.append(file)
        
    if group == 1:
        #targets to appear on 70% of black faces and 30% of white
        targetBlackImages = random.sample(blackImages, 28)
        targetWhiteImages = random.sample(whiteImages, 12)
    else:
        #targets to appear on 30% of black faces and 70% of white
        targetBlackImages = random.sample(blackImages, 12)
        targetWhiteImages = random.sample(whiteImages, 28)

    for face in blackImages:
        if face in targetBlackImages:
            img_list.append([face, 1, 1])
        else:
            img_list.append([face, 0, 1])

    for face in whiteImages:
        if face in targetWhiteImages:
            img_list.append([face, 1, 0])
        else:
            img_list.append([face, 0, 0])

    random.shuffle(img_list)

    os.chdir('../..')
    return DataFrame(data=img_list, columns = ['img', 't', 'b'])

def create_scramble(images, dir, save_dir):
    '''
    create_scramble(images, dir, save_dir) - Creates a list of scrambled images
    where we split each 256px image into 16x16 tiles and randomly shuffling
        Inputs: [images] is a pandas dataframe where the inner elements have the 
        image names. [dir] is a string representing the base directory of the 
        images to be read. [save_dir] is a string representing the base 
        directory of the scrambled images to be saved.
        Requires: both [dir] and [sae_dir] must be valid directories
    '''
    for img in images['img']:
        tiles = image_slicer.slice(dir+img, 256, save=False)
        tiles_list = list(tiles)
        random.shuffle(tiles_list)
        count = 0
        for tile in tiles:
            tile.image = tiles_list[count].image
            count += 1
        scramble = image_slicer.join(tiles)
        scramble.save(save_dir+img)

def gen_square(win, color):
    '''
    gen_square(win, color) - generates a psychopy visual 10x10 square of the 
    specified color 
        Inputs: [win] is the active window. [color] is an RGB list.
        Returns: A psychopy visual stim rectangle
    '''
    return visual.Rect(
        win=win,
        units="deg",
        width=.5,
        height=.5,
        fillColor=color,
        lineColor=color)

def encoding_loop(exp, stim_images, red_target, stim_dir, scramble_dir):
    '''
    encoding_loop(exp, stim_images, red_target, stim_dir, scramble_dir) - Runs 
    the encoding and detection task loops and saves the data
        Inputs: [exp] is an Experiment class. [stim_images] is a pandas
        dataframe with columns indicating image name, target, and race of 
        individual's face. [red_target] is a boolean value indicating whether or 
        not red is the target color. [stim_dir] is the base directory for the 
        stim images. [scramble_dir] is the base directory for the scrambled 
        images.
        Requires: [stim_dir] and [scramble_dir] are valid directories and every
        row in [stim_images] must contain non-NAN values.
    '''
    
    exp.text_box.text = "Recognition and Encoding Tasks:\
        \nYou will see a series of images in the following task.\
        \nPress the spacebar whenever you see a " + ("red" if red_target
        else "green") + " square.\
        \nPress the spacebar to continue."

    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])
    
    redSq = gen_square(exp.win, colorRed) #generates a red square
    greenSq = gen_square(exp.win, colorGrn) #generates a green square
    
    detection_data = []

    exp.text_box.text = "Block 1 will start now.\
            \nPress the spacebar to continue."
    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    clock = core.Clock()
    for i in range(10):

        shuffled_images = shuffle_images(stim_images)
        #loop runs through each image in shuffled_images argument for procedure
        targets_responded = 0
        non_targets_responded = 0
        #response_times used to calculate median response time
        response_times = []
        for index, row in shuffled_images.iterrows():
            #creates image and scramble for procedure
            img = visual.ImageStim(win=exp.win, image=stim_dir+row['img'],
                units='deg')
            scramble = visual.ImageStim(win=exp.win,
                image=scramble_dir+row['img'], units='deg')

            reaction_times = [] #times when user reacted to the stim

            img.draw()
            exp.win.flip() #immediately presents stim and records time

            stim_presentation = clock.getTime()
            stim_exit = 0.0
            space_pressed = False

            stim_timer = core.Clock()
            while stim_timer.getTime() <= 1.0:
                key = exp.get_keypress()
                if key == 'escape':
                    exp.data_write(detection_data, './Data/', 'Encoding')
                    exp.shutdown()
                elif key == 'space':
                    reaction_times.append(clock.getTime())
                    #Check to make sure this is the first time  the spacebar
                    #has been pressed and depending on whether the image
                    #is a target or not, add up the appropriate statistic
                    if (not space_pressed) and row['t']:
                        space_pressed = True
                        targets_responded += 1
                        response_times.append(stim_timer.getTime())
                    elif (not space_pressed) and not row['t']:
                        space_pressed = True
                        non_targets_responded += 1
                        response_times.append(stim_timer.getTime())

                if 0.0 <= stim_timer.getTime() < 0.050:
                    img.draw()
                    exp.win.flip()
                elif 0.050 <= stim_timer.getTime() < 0.150:
                    img.draw()
                    if((row['t'] and red_target) or 
                        (not row['t'] and not red_target)):
                        redSq.draw()
                    else:
                        greenSq.draw()
                    exp.win.flip()
                elif 0.150 <= stim_timer.getTime() < 0.2:
                    img.draw()
                    exp.win.flip()
                    stim_exit = clock.getTime()
                else:
                    scramble.draw() #scrambled image presented for 800ms
                    exp.win.flip()

            #attach results of experiment to dataset
            detection_data.append(
                [
                    exp.subject_data['subject_num'],
                    exp.subject_data['group'],
                    len(detection_data)+1,
                    row['img'],
                    row['t'],
                    row['b'],
                    red_target,
                    stim_presentation,
                    stim_exit
                ])
            detection_data[len(detection_data)-1].extend(reaction_times)

        median_response = np.median([i for i in response_times if i >= 0.050])
        if (i+1) < 10:
            exp.text_box.text = "Block %i complete. Here are your results:\
                \nPercentage of targets you responded to: %.2f %%\
                \nNumber of times you responded to non-targets: %i\
                \nMedian response time: %.4f s\
                \nBlock %i will start now.\
                \nPress the spacebar to continue." % (i+1, 
                    (float(targets_responded)/40.0)*100.0, non_targets_responded,
                    median_response, i+2)
        else:
            exp.text_box.text = "Block %i complete. Here are your results:\
                \nPercentage of targets you responded to: %.2f %%\
                \nNumber of times you responded to non-targets: %i\
                \nMedian response time: %.4f s\
                \nPress the spacebar to continue." % (i+1, 
                    (float(targets_responded)/40.0)*100.0, non_targets_responded,
                    median_response)
        exp.text_box.draw()
        exp.win.flip()
        event.waitKeys(keyList = ["space"])

    exp.data_write(detection_data, './Data/', 'Encoding')


def memory_loop(exp, old_imgs, new_imgs, old_imgs_dir, new_imgs_dir):
    '''
    memory_loop(exp, old_imgs, new_imgs, old_imgs_dir, new_imgs_dir) - Runes
    the recognition memory task loop and saves the data
        Inputs: [exp] is the Experiment class. [old_imgs] is a 2-D pandas 
        dataframe with columns indicating the image name, target, and race of 
        individuals face. This dataframe represents all old images presented
        during the encoding tasks. [new_imgs] is a similar dataframe with new
        images instead of old. [old_imgs_dir] is a string representing the 
        directory that the old images were taken from. [new_imgs_dir] is a
        string representing the directory that the new images were taken from.
        Requires: [old_imgs_dir] and [new_imgs_dir] are valid directories and
        every row in [old_imgs] and [new_imgs] must contain non-NAN values.
    '''
    
    exp.text_box.text = "Recognition Memory Tasks:\
        \nYou will see a series of images in the following task.\
        \nPress \'z\' key if you think it was presented previously \
        \nand press the \'x\' key if you think it is a new image.\
        \nFor each image also rate your confidence by pressing \
        \na number key from 1-7. Press spacebar to continue."
    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])
    
    image_sequence = []
    #accumulate all images and their directories into tuples where first 
    #element is image name and second element is whether it is a new image or 
    #not
    for index, row in old_imgs.iterrows():
        image_sequence.append((row['img'], 1))
      
    for index, row in new_imgs.iterrows():
        image_sequence.append((row['img'], 0))

    random.shuffle(image_sequence)

    memory_data = []

    clock = core.Clock()

    for (index, img) in enumerate(image_sequence, 1):
        img_stim = visual.ImageStim(win=exp.win, 
            image= (old_imgs_dir if img[1] else new_imgs_dir)+ img[0],
             units='deg')
        exp.text_box.text = "Old image or new image?"
        img_stim.draw()
        exp.text_box.draw()
        exp.win.flip()
        img_present_time = clock.getTime()

        img_keys = event.waitKeys(keyList = ['z', 'x', 'escape'], 
            timeStamped=clock)
   
        if img_keys[0][0] == 'escape':
            exp.shutdown()

        exp.text_box.text = "Confidence Level:\
                    \n1\t2\t3\t4\t5\t6\t7"
        exp.text_box.draw()
        exp.win.flip()
        confidence_present_time = clock.getTime()
        
        confidence_keys = event.waitKeys(
            keyList = ['1','2','3','4','5','6','7'], timeStamped=clock)
        
        exp.text_box.text = "+" if ((img_keys[0][0] == 'z') == img[1]) else "-"
        exp.text_box.color = "Green" if ((img_keys[0][0] == 'z') == img[1]) else "Red"
        exp.text_box.height = 3.0
        exp.text_box.draw()
        exp.win.flip()

        
        core.wait(0.3)
        exp.text_box.color = "Black"
        exp.text_box.height = 0.75
        
        memory_data.append(
            [
                exp.subject_data['subject_num'],
                exp.subject_data['group'],
                len(memory_data)+1,
                img[0],
                img[1],
                img_present_time,
                img_keys[0][0] == 'z', #should be 1 if user chose old image
                img_keys[0][1],
                confidence_present_time,
                int(confidence_keys[0][0]),
                confidence_keys[0][1]
            ])
        if index % 20 == 0:
            exp.text_box.text = "%i / %i images complete.\
                \nPress spacebar to continue." % (index, len(image_sequence))
            exp.text_box.draw()
            exp.win.flip()
            event.waitKeys(keyList = ["space"])
            
    exp.data_write(memory_data, './Data/', 'Memory')


if __name__ == "__main__":
    exp = Experiment([1400, 800], True, {}, 'ABE_Racial_Bias', 'testMonitor')
    
    exp.win.flip()
    
    if exp.subject_data['subject_num'] % 4 <= 1:
        exp.subject_data['group'] = 1
    else:
        exp.subject_data['group'] = 2

    old_images = get_images('./Stimuli/Old_Images', exp.subject_data['group'])

    create_scramble(old_images, './Stimuli/Old_Images/', 
        './Stimuli/Scrambled_Old_Images/')
    
    if exp.subject_data['subject_num'] % 2 == 1:
        red_target = True
    else:
        red_target = False

    #encoding_loop(exp, old_images, red_target, './Stimuli/Old_Images/', 
    #    './Stimuli/Scrambled_Old_Images/')
    
    new_images = get_images('./Stimuli/New_Images', exp.subject_data['group'])
    memory_loop(exp, old_images, new_images, 
        './Stimuli/Old_Images/', './Stimuli/New_Images/')
    exp.text_box.text = "Thank you for participating in this experiment.\
    \nYour response has been recorded"
    exp.text_box.draw()
    event.waitKeys(keyList=["space"])
    exp.win.flip()