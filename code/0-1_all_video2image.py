import cv2
import os

def video_to_frames(video, path_output_dir):
    # extract frames from a video and save to directory as 'x.png' where 
    # x is the frame index
    vidcap = cv2.VideoCapture(video)
    count = 0
    while vidcap.isOpened():
        
        success, image = vidcap.read()
        if success:
            cv2.imwrite(path_output_dir+'{}.png'.format(str(count).zfill(4)), image)
            count += 1

        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()


def read_video_names(jaad_split_videos_path, split_v):
    
    with open(jaad_split_videos_path+split_v) as f:
        video_names = f.readlines()
    
    video_names = [video_name.rstrip('\n') for video_name in video_names]

    return video_names
    



jaad_path = '/media/taemi/Elements/JAAD/'

jaad_path_cplips = jaad_path + 'JAAD_clips/'

jaad_split_videos_path = jaad_path + 'split_ids/all_videos/'

split_list = ['test.txt', 'train.txt', 'val.txt']

for split_v in split_list:
    
    save_path = '../datas/'+split_v[:-4]
    os.mkdir(save_path)

    video_names = read_video_names(jaad_split_videos_path, split_v)
    for video_name in video_names:
        frame_save_path = save_path +'/'+ video_name
        print(frame_save_path)
        os.mkdir(frame_save_path)

        video_to_frames(jaad_path_cplips+video_name+'.mp4', frame_save_path+'/')




# video_name = 'demo_filled.avi'
# os.mkdir('./images/{}'.format(video_name[:-4]))
# video_to_frames('./result_videos/{}'.format(video_name), './images/{}'.format(video_name[:-4]))