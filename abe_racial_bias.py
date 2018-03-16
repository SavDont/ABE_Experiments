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
        units="pix",
        width=10,
        height=10,
        fillColor=color,
        lineColor=color)

def encoding_loop(exp, stim_images, red_target, stim_dir, scramble_dir):
    '''
    encoding_loop(exp, stim_images, red_target, stim_dir, scramble_dir) - Runs 
    the encoding and detection task loops and saves the data
        Inputs: [exp] is an Experiment class. [stim_images] is a 2-D array with
        the first element in each inner list being the image name and the 
        second element indicating whether or not it is a target. [red_target] is
        a boolean value indicating whether or not red is the target color. 
        [stim_dir] is the base directory for the stim images. [scramble_dir] is
        the base directory for the scrambled images.
        Requires: [stim_dir] and [scramble_dir] are valid directories and every
        element in stim_images must be a two element lists.
    '''
    redSq = gen_square(exp.win, colorRed) #generates a red square
    greenSq = gen_square(exp.win, colorGrn) #generates a green square
    
    detection_data = []
    clock = core.Clock()
    for i in range(10):
        shuffled_images = shuffle_images(stim_images)
        #loop runs through each image in shuffled_images argument for procedure
        for index, row in shuffled_images.iterrows():
            #creates image and scramble for procedure
            img = visual.ImageStim(win=exp.win, image=stim_dir+row['img'],
                units='pix')
            scramble = visual.ImageStim(win=exp.win,
                image=scramble_dir+row['img'], units='pix')

            reaction_times = [] #times when user reacted to the stim

            img.draw()
            exp.win.flip() #immediately presents stim and records time

            stim_presentation = clock.getTime()
            stim_exit = 0.0
            stim_timer = core.Clock()
            while stim_timer.getTime() <= 1.0:
                key = exp.get_keypress()
                if key == 'escape':
                    exp.data_write(detection_data, './Data/')
                    exp.shutdown()
                elif key == 'space':
                    reaction_times.append(clock.getTime())

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
    exp.data_write(detection_data, './Data/')

def main():
    exp = Experiment([1400, 800], True, {}, 'ABE_Racial_Bias')
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

    encoding_loop(exp, old_images, red_target, './Stimuli/Old_Images/', 
        './Stimuli/Scrambled_Old_Images/')

if __name__ == "__main__":
    main()