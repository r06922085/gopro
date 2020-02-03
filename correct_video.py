import cv2
import os
import numpy as np
import argparse


class correct_video():
    def __init__(self):
        '''correct_video.py
        1 will convert
        0 will still the same
        -1 will cancle the last choose and stop the programe

        you can specify single video name that you want it to be inverted 
        '''
        self.video_folder_path = "gopro/"
        self.video_folder_path_new = os.path.join(self.video_folder_path, "corrected1/")
        self.save_path = os.path.join(self.video_folder_path, 'invert_list.npy')
        self.data_type_list = ['.mp4', '.MP4']
        self.args = self.parse_args()
        self.run()

    def run(self):
        video_path_list = self.get_video_path_list()

        if os.path.isfile(self.save_path):
            invert_list = np.load(self.save_path).tolist()
            if len(invert_list) != len(video_path_list):
                invert_list = self.get_invert_list(invert_list)
        else:
            invert_list = self.get_invert_list()
        print(video_path_list)
        if invert_list is None:
            return

        cap_try = cv2.VideoCapture(video_path_list[0])
        # out_all = cv2.VideoWriter(self.video_folder_path_new+"*.mp4", cv2.CAP_FFMPEG, cv2.VideoWriter_fourcc(*'mp4v'), cap_try.get(cv2.CAP_PROP_FPS), (int(cap_try.get(3)), int(cap_try.get(4))))

        for i, video_path in enumerate(video_path_list):
            print(video_path + " is proccessing")
            cap = cv2.VideoCapture(video_path)
            frame = 0
            video_name = os.path.basename(video_path).split('.')[0]
            out = cv2.VideoWriter(self.video_folder_path_new+video_name+".mp4", cv2.CAP_FFMPEG, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (int(cap.get(3)), int(cap.get(4))))
            while True:
                ret, inp = cap.read()
                if ret:
                    frame += 1
                    if invert_list[i] == "1":
                        inp = cv2.rotate(inp, cv2.ROTATE_180)
                    out.write(inp)
                    #out_all.write(inp)
                elif frame > 30:
                    break
            cap.release()
            out.release()
        #out_all.release()

        cv2.destroyAllWindows()

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--invert_video', type=str, default=None)
        return parser.parse_args()

    def get_invert_list(self, invert_list=[]):
        video_path_list = self.get_video_path_list()
        for i in range(len(invert_list), len(video_path_list)):
            video_path = video_path_list[i]
            cap = cv2.VideoCapture(video_path)
            invert = ""
            while invert != "1" and invert != "0" and invert != "-1":
                _, inp = cap.read()
                cv2.imshow("", cv2.resize(inp, (300, 300)))
                cv2.waitKey(700)
                cv2.destroyAllWindows()
                invert = input("Invert?(1 is yes and 0 is no): ")
            if invert != "-1":
                invert_list.append(invert)
                np.save(self.save_path, np.asarray(invert_list))
            else:
                invert_list.pop()
                np.save(self.save_path, np.asarray(invert_list))
                return

        return invert_list

    def get_video_path_list(self):
        list = []
        if self.args.invert_video is not None:
            list.append(os.path.join(self.video_folder_path, self.args.invert_video))
            return list

        for item in os.listdir(self.video_folder_path):
            if os.path.isfile(os.path.join(self.video_folder_path, item)):
                if any(k in item for k in self.data_type_list):
                    list.append(os.path.join(self.video_folder_path, item))
        list.sort()
        return list


if __name__ == "__main__":
    c = correct_video()
