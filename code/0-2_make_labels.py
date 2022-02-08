import cv2
from xml.etree.ElementTree import parse
import sys
import pickle
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
        if x.attrib['label'] == 'pedestrian':
            new_annotations.append(x)
            
    return new_annotations
   


def read_video_names(jaad_split_videos_path, split_v):
  
   with open(jaad_split_videos_path+split_v) as f:
       video_names = f.readlines()
  
   video_names = [video_name.rstrip('\n') for video_name in video_names]
 
   return video_names




def save_labels(split_v, video_names, jaad_path):
    '''
    split_v : test.txt or train.txt or val.txt
    '''

    # make split_v dir
    split_path = './data/{}'.format(split_v)
    os.makedirs(split_path, exist_ok=True)

    for video_name in video_names:
        # make video_name dir
        os.makedirs(split_path+'/'+video_name, exist_ok=True)
        annotations = parsing_annotation(jaad_path+"annotations/", video_name+'.xml') 
        for track in annotations:
            for box in track:
                # print(box.attrib['frame'], box.attrib['xbr'], box.attrib['xtl'], box.attrib['ybr'], box.attrib['ytl'])
                # save txt
                sys.stdout = open(./split_path/'{}'.format(video_name).txt,'w')
                 
        
    
    
    # annotations = parsing_annotation(vid_path+"annotations/", vid_name+'.xml') 
    # checking the existence of a person
    # if not len(annotations):
    #     print("'{}' doesn't have person".format(vid_name))
    #     return
    
    # for track in annotations:
    #     for box in track:
            # print(box.attrib['frame'], box.attrib['xbr'], box.attrib['xtl'], box.attrib['ybr'], box.attrib['ytl'])
            # 66 1919.0 1839.0 1079.0 498.0 [example]

    


def start(vid_path, vid_name):
   
    '''
    [lrgc] - str

    [mnm] - str
    '''

    jaad_path = '/home/msis/Desktop/project/JAAD/'
    
    jaad_split_videos_path = jaad_path + 'split_ids/all_videos/'
    
    split_list = ['test.txt', 'train.txt', 'val.txt']
    
      
    for split_v in split_list:
        video_names = read_video_names(jaad_split_videos_path, split_v)
        
        save_labels(split_v, video_names, jaad_path)
    


if __name__ == "__main__":
    # JAAD path
    VID_PATH = '/home/msis/Desktop/project/JAAD/' 
    # VID_NAME = 'video_0001'
    for num in range(346):
        VID_NAME = 'video_{0:04}'.format(num+1)
        start(VID_PATH, VID_NAME)
        break


# test_txt = "/home/msis/Desktop/project/JAAD/split_ids/all_videos"