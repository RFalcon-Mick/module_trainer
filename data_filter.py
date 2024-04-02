"""
���ݴ���
���˹���ͼ��
����ͼ�񳤿�����һ������
"""

from PIL import Image
import os

dataset_root_path = "dataset"

min = 200   # �̱�
max = 2000  # ����
ratio = 0.5 # �̱� / ����

delete_list = [] # �н�����ͼƬ�ĳ�������
for root,dirs,files in os.walk(dataset_root_path):
    for file_i in files:
        file_i_full_path = os.path.join(root, file_i)
        img_i = Image.open(file_i_full_path)
        img_i_size = img_i.size  # ��ȡ����ͼ��ĳ���

        # ɾ�����߹��̵�ͼƬ
        if img_i_size[0]<min or img_i_size[1]<min:
            print(file_i_full_path, " ������Ҫ��")
            delete_list.append(file_i_full_path)

        # ɾ�����߹�����ͼƬ
        if img_i_size[0] > max or img_i_size[1] > max:
            print(file_i_full_path, " ������Ҫ��")
            delete_list.append(file_i_full_path)

        # ɾ����߱���������ͼƬ
        long = img_i_size[0] if img_i_size[0] > img_i_size[1] else img_i_size[1]
        short = img_i_size[0] if img_i_size[0] < img_i_size[1] else img_i_size[1]

        if short / long < ratio:
            print(file_i_full_path, " ������Ҫ��",img_i_size[0],img_i_size[1])
            delete_list.append(file_i_full_path)


# print(delete_list)
for file_i in delete_list:
    try:
        print("����ɾ��",file_i)
        os.remove(file_i)
    except:
        pass
