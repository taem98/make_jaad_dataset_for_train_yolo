import cv2
from xml.etree.ElementTree import parse
import sys
import pickle
import math
import os


def parsing_annotation(path, name):
    '''
    - xtl : x top
    - ytl : y top
    - xbr : x lower
    - ybr : y lower

    - look : looking / non-looking
    - action : standing / warking
    '''
    tree = parse(path+name)
    root = tree.getroot()

    annotations = root.findall("track") # read pedestrian , ped
    new_annotations = []
    
    # removed ped

    for x in annotations:
        if (x.attrib['label'] == 'pedestrian') or (x.attrib['label'] == 'ped'):
            new_annotations.append(x)
            
    return new_annotations
   


def read_video_names(jaad_split_videos_path, split_v):
  
   with open(jaad_split_videos_path+split_v) as f:
       video_names = f.readlines()
  
   video_names = [video_name.rstrip('\n') for video_name in video_names]
 
   return video_names


def save_labels(split_v, video_names, jaad_path, jaad_video_path):
    '''
    split_v : test.txt or train.txt or val.txt
    '''

    # make split_v dir
    split_path = '../datas/{}'.format(split_v[:-4])
    print(split_path)
    os.makedirs(split_path, exist_ok=True)

    for video_name in video_names:
        # make video_name dir
        os.makedirs(split_path+'/'+video_name, exist_ok=True)

        annotations = parsing_annotation(jaad_path+"annotations/", video_name+'.xml') 
        
        print(jaad_path+"annotations/", video_name+'.xml')
        
        if not len(annotations):
            print("'{}' doesn't have person".format(video_name))
            continue

        # get video width and height
        # jaad_video_path + video_name
        vcap = cv2.VideoCapture(jaad_video_path+video_name+'.mp4')
        video_width = vcap.get(3) # float width
        video_height = vcap.get(4) # float height

        # print(video_name) 
        for track in annotations:
            for box in track:
                with open(split_path+'/'+video_name+'/{}.txt'.format(box.attrib['frame'].zfill(4)), 'a') as f:
                    xtl = float(box.attrib['xtl'])
                    xbr = float(box.attrib['xbr'])
                    ytl = float(box.attrib['ytl'])
                    ybr = float(box.attrib['ybr'])

                    x_mid = xtl + ((xbr - xtl) / 2 )
                    y_mid = ytl + ((ybr - ytl) / 2 )
                    box_width = xbr - xtl
                    box_height = ybr - ytl

                    # recude between 0 to 1
                    x_mid = x_mid / video_width
                    y_mid = y_mid / video_height
                    box_width = box_width / video_width
                    box_height = box_height / video_height

                    if x_mid < 0: x_mid = 0
                    elif x_mid > 1: x_mid = 1

                    if y_mid < 0: y_mid = 0
                    elif y_mid > 1: y_mid = 1

                    if box_width < 0: box_width = 0
                    elif box_width > 1: box_width = 1
                    
                    if box_height < 0: box_height = 0
                    elif box_height > 1: box_height = 1
                    
                    data = "0 "+str(x_mid)+" "+str(y_mid)+" "+str(box_width)+" "+str(box_height)
                    f.write(data+'\n')
            

def start(JAAD_path):
   
    '''
    [lrgc] - str

    [mnm] - str
    '''
    
    jaad_split_videos_path = JAAD_path + 'split_ids/all_videos/'
    jaad_video_path =  JAAD_path + 'JAAD_clips/'
    
    split_list = ['test.txt', 'train.txt', 'val.txt']
    
      
    for split_v in split_list:
        video_names = read_video_names(jaad_split_videos_path, split_v)
        
        save_labels(split_v, video_names, JAAD_path, jaad_video_path)
        # break
    


if __name__ == "__main__":
    # JAAD path
    JAAD_PATH ='/media/taemi/Elements/JAAD/'

    start(JAAD_PATH)
