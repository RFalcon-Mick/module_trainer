"""
������������
��������������ͼ
����ͼ��ֱ���ɢ��ͼ
"""

import os
import PIL.Image as Image
import matplotlib.pyplot as plt
import numpy as np


def plot_resolution(dataset_root_path):
    img_size_list = []  # �н�����ͼƬ�ĳ�������
    for root, dirs, files in os.walk(dataset_root_path):
        for file_i in files:
            file_i_full_path = os.path.join(root, file_i)
            img_i = Image.open(file_i_full_path)
            img_i_size = img_i.size  # ��ȡ����ͼ��ĳ���
            img_size_list.append(img_i_size)

    print(img_size_list)  #

    width_list = [img_size_list[i][0] for i in range(len(img_size_list))]
    height_list = [img_size_list[i][1] for i in range(len(img_size_list))]

    # print(width_list)   # 640
    # print(height_list)    # 346

    plt.rcParams["font.sans-serif"] = ["SimHei"]  # ������������
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.unicode_minus"] = False  # �������ͼ���еġ�-�����ŵ���������

    plt.scatter(width_list, height_list, s=1)
    plt.xlabel("��")
    plt.ylabel("��")
    plt.title("ͼ���߷ֲ�")
    plt.show()


#   ��������ͼ
def plot_bar(dataset_root_path):
    file_name_list = []
    file_num_list = []
    for root, dirs, files in os.walk(dataset_root_path):
        if len(dirs) != 0:
            for dir_i in dirs:
                file_name_list.append(dir_i)
        file_num_list.append(len(files))

    file_num_list = file_num_list[1:]
    # ���ֵ�����Ѿ�ֵ�Ժ�����ʽ��ʾ����
    mean = np.mean(file_num_list)
    print("mean = ", mean)

    bar_positions = np.arange(len(file_name_list))

    fig, ax = plt.subplots()  # ���廭��������ӻ�
    ax.bar(bar_positions, file_num_list, 0.5)  # ����ͼ������������ľ��룬����ֵ�����Ŀ��

    ax.plot(bar_positions, [mean for i in bar_positions], color="red")  # ��ʾƽ��ֵ

    plt.rcParams["font.sans-serif"] = ["SimHei"]  # ������������
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.unicode_minus"] = False  # �������ͼ���еġ�-�����ŵ���������

    ax.set_xticks(bar_positions)  # ����x��Ŀ̶�
    ax.set_xticklabels(file_name_list, rotation=90)  # ����x��ı�ǩ
    ax.set_ylabel("�������")
    ax.set_title("���ݷֲ�ͼ")
    plt.show()


if __name__ == '__main__':
    dataset_root_path = "dataset"

    plot_resolution(dataset_root_path)

    # plot_bar(dataset_root_path)
