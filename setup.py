"""
��Ŀ��ʼ��
"""

import os


def create_folders():
    try:
        os.mkdir("output")
        os.mkdir("dataset")
        print("�ļ��д����ɹ���")
    except FileExistsError:
        print("�ļ����Ѵ��ڡ�")


if __name__ == "__main__":
    create_folders()
