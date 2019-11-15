import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path


class SearchImages:

    def run(self, sim, qty):

        set_template = 'image/dragonball.jpg'
        #set_template = 'image/Game_of_Thrones_Hardhome.mp4'
        similar = []
        image_type = self.initial_template_type(set_template)
        if image_type == "image":
            for bd_image in self.get_files():
                if bd_image[1] == "image":
                    img_string = str(bd_image[0])
                    similarity = self.similarity(
                        img_string, set_template, bd_image[1])
                    if similarity >= sim:
                        similar.append((str(bd_image[0]), similarity))

                if bd_image[1] == "video":
                    video_string = str(bd_image[0])
                    cap = cv2.VideoCapture(video_string, 0)
                    while (cap.isOpened()):
                        similarity_value = 0.0
                        ret, frame = cap.read()
                        if ret == True:
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            img = gray.copy()
                            similarity = self.similarity(
                                img, set_template, bd_image[1])
                            if similarity >= sim:
                                if similarity > similarity_value:
                                    similarity_value = similarity

                        else:
                            if similarity_value > similarity:
                                similar.append(
                                    (str(bd_image[0]), similarity_value))
                            break

        elif image_type == "video":

            cap_video = cv2.VideoCapture(set_template, 0)
            get_files = self.get_files()
            while (cap_video.isOpened()):
                ret_video, template_video = cap_video.read()
                if ret_video == True:
                    gray_video = cv2.cvtColor(
                        template_video, cv2.COLOR_BGR2GRAY)
                    set_template_video = gray_video.copy()

                    for bd_image in get_files:
                        if bd_image[1] == "image":
                            img_string = str(bd_image[0])
                            similarity = self.similarity(
                                img_string, set_template_video, bd_image[1])
                            if similarity >= sim:
                                similar.append((str(bd_image[0]), similarity))

                        if bd_image[1] == "video":
                            video_string = str(bd_image[0])
                            cap = cv2.VideoCapture(video_string, 0)
                            while (cap.isOpened()):
                                similarity_value = 0.0
                                ret, frame = cap.read()
                                if ret == True:
                                    gray = cv2.cvtColor(
                                        frame, cv2.COLOR_BGR2GRAY)
                                    img = gray.copy()
                                    similarity = self.similarity(
                                        img, set_template_video, bd_image[1])
                                    if similarity >= sim:
                                        if similarity > similarity_value:
                                            similarity_value = similarity
                                        similar.append(
                                            (str(bd_image[0]), similarity_value))
                                else:
                                    break

                else:
                    break

        else:
            return "Formato não permitido"

        pre_similar = sorted(similar, key=lambda i: i[1], reverse=True)
        return pre_similar[:qty]

    def get_files(self):
        list_files = []
        path = Path('bd_images')
        for filepath in path.glob('*'):
            list_files.append((filepath, self.type_file(filepath.suffix)))

        return list_files

    def type_file(self, ext):
        is_image = ['.jpg', '.jpeg', '.bmp', '.png', ]
        is_video = ['.mp4', '.3gp', '.mpeg', '.avi', ]
        if ext in is_image:
            return "image"
        elif ext in is_video:
            return "video"
        else:
            return "undefined"

    def initial_template_type(self, get_file):
        finfo = open(get_file)
        explod_file = finfo.name.split('.')
        extension_file = explod_file[-1]
        return self.type_file("."+extension_file)

    def similarity(self, set_image, set_template, set_type_image):
        if set_type_image == "video":
            img2 = set_image
        else:
            img = cv2.imread(set_image, 0)
            img2 = img.copy()

        if type(set_template) is str:
            template = cv2.imread(set_template, 0)
        else:
            template = set_template

        w, h = template.shape[::-1]
        methods = ['cv2.TM_CCOEFF_NORMED']

        for meth in methods:
            method = eval(meth)

            img3 = img2.copy()
            res = cv2.matchTemplate(img3, template, method)
            min_val, similaridade, min_loc, max_loc = cv2.minMaxLoc(res)

        return round(similaridade*100, 2)


if __name__ == "__main__":
    search = SearchImages()

    similaridade = float(input('Percentual de similaridade(em decimal):'))
    quantidade = int(input('Quantidade de resuldados:'))
    print(search.run(similaridade, quantidade))
