# -*- coding: utf-8 -*-
"""
将一张图片填充为正方形后切为9张图
Author: Alexlilihxq
"""

from PIL import Image
import os


def fill_image(image):
    """填充, 将图片填充为正方形"""
    width, height = image.size
    # 选取长和宽中较大值作为新图片的边长
    new_image_length = width if width > height else height
    # 生成新的底图图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    # 将之前的图粘贴在新图上，居中
    if width > height:  # 原图宽大于高，则填充图片的竖直维度
        # (x,y)二元组表示粘贴上图相对下图的左上角起始位置
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    return new_image


def cut_image_divided(image, n):
    """切割，将图片切割为n x n 的子图
    :param : n
    :type : int
    """
    width, height = image.size
    item_width = int(width / n)
    box_list = []
    # (left, upper, right , lower)
    for i in range(0, n):
        for j in range(0, n):
            # 计算图片切割的位置
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


def save_images(image_list, file_path):
    """保存, 将切割后的图片保存到指定目录"""
    index = 1
    file_name = os.path.basename(file_path)     # 优化图片保存方式
    file_name = file_name.split('.')[0]
    for image in image_list:
        image.save('./result/' + file_name + str(index) + '.png', 'PNG')
        index += 1


if __name__ == '__main__':
    file_list = ['GitNum.png', 'python.jpeg', 'Walker.jpeg', 'Programmer.png', 'PangHu.png']
    file_path = file_list[4]
    image = Image.open(file_path)
    image = fill_image(image)
    # image.show()
    image_list = cut_image_divided(image, 2)
    save_images(image_list, file_path)
