import os
import subprocess
import cv2
from os.path import join
import json

#利用cv2进行取帧
def extract_frames(data_path, output_path ,frame_total, method="cv2"):
    """Method to extract frames, either with ffmpeg or opencv. FFmpeg won't
    start from 0 so we would have to rename if we want to keep the filenames
    coherent."""
    os.makedirs(output_path, exist_ok=True)
    if method == "ffmpeg":
        subprocess.check_output(
            "ffmpeg -i {} {}".format(data_path, join(output_path, "%04d.png")),
            shell=True,
            stderr=subprocess.STDOUT,
        )
    elif method == "cv2":
        reader = cv2.VideoCapture(data_path)
        frame_num = 0
        while reader.isOpened():
            success, image = reader.read()
            if not success:
                break
            cv2.imwrite(join(output_path, '{:04}_mask.png'.format(frame_num)), image)
            frame_num += 1
            if frame_num == frame_total:    #这里设置为最多取frame_total帧
                break
        reader.release()
    else:
        raise Exception("Wrong extract frames method: {}".format(method))

origin_manipulation = ['Deepfakes','Face2Face','FaceSwap','NeuralTextures']
target_manipulation = ['FF-DF','FF-F2F','FF-FS','FF-NT']

def extract_frame_from_fake(file_name, frame_total):
    for i, j in enumerate(origin_manipulation):
        process_path = 'D:\FF_Mask_Download\manipulated_sequences\\' + j + '\\masks\\videos\\'
        target_path = 'D:\ProjectDevelop\SLADD-Learning\data\FF\mask\\'+target_manipulation[i]+'\\'
        if not os.path.exists(target_path + file_name):  #判断是否有该目录
            os.mkdir(target_path + file_name)
        if(os.path.lexists('{}'.format(process_path+file_name+'.mp4'))):   #判断要取帧的视频是否存在
            #print('{}'.format(process_path+file_name+'.mp4') + '存在')
            if(not os.listdir(target_path+file_name)):  #判断该目录是否为空,若为空则取帧并存放文件
                #将指定的视频进行取帧并存放到对应的位置
                data_path = process_path + file_name + '.mp4'
                output_path = target_path + file_name
                extract_frames(data_path,output_path,frame_total)   #需要时解除这行注释

modes = ['train','test','valid']
required_frame_num = {'test': 25, 'valid': 10, 'train': 30}  #低配版,正常来讲这里应该是25,10,270

for mode in modes:
    split_json_path = 'D:\\ProjectDevelop\\SLADD-Learning\\data\\FF\\config\\'+mode+'.json'
    with open(split_json_path) as json_file:
        json_list = json.load(json_file)
        #print(type(json_list), len(json_list),split_json_path)
        for item in json_list:
            file_name = item[0] + '_' + item[1]
            extract_frame_from_fake(file_name,required_frame_num[mode])
    print(mode+' complete')