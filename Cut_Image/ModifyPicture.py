# -*- coding: utf-8 -*-
"""
将9张图拼接并填充为适当比例
Author: Alexlilihxq
"""

from PIL import Image
import os


def fill_image(image_input):
    """填充, 将图片填充为适当比例"""
    width, height = image_input.size
    # 选取长和宽中较大值作为新图片的边长
    image_height = width if width < height else height
    new_width = image_height // 6 * 9
    # 生成新的底图图片[白底]
    new_image = Image.new(image_input.mode, (new_width, image_height), color='white')
    # 将之前的图粘贴在新图上，居中
    if width > height:  # 原图宽大于高，则填充图片的竖直维度
        # (x,y)二元组表示粘贴上图相对下图的左上角起始位置
        # new_image.paste(image_input, (0, int((image_height - height) )))
    # else:
        new_image.paste(image_input, (int((new_width - width) / 2), 0))
    return new_image


def save_images(image_list, file_path):
    """保存, 将切割后的图片保存到指定目录"""
    index = 1
    file_name = os.path.basename(file_path)  # 优化图片保存方式
    file_name = file_name.split('.')[0]
    image.save('./result/' + file_name + '.png', 'PNG')


if __name__ == '__main__':
    file_path = '宝贝美照2.jpg'
    image = Image.open(file_path)
    image = fill_image(image)
    # image.show()
    # image_list = cut_image_divided(image, 4)
    # image_list[0].show()
    save_images(image, file_path)
