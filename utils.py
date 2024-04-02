"""
����dataloader
"""

import torch
from PIL import Image

import torchvision.transforms as transforms
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from torch.utils.data import Dataset

# ���ݹ�һ�����׼��

transform_BZ= transforms.Normalize(
    mean=[0.52225417, 0.4851904, 0.42605346],# ȡ�������ݼ�
    std=[0.20513351, 0.20246686, 0.20748332]
)


class LoadData(Dataset):
    def __init__(self, txt_path, train_flag=True):
        self.imgs_info = self.get_images(txt_path)
        self.train_flag = train_flag
        self.img_size = 512

        self.train_tf = transforms.Compose([
                transforms.Resize(self.img_size),
                transforms.RandomHorizontalFlip(),#��ͼƬ���������ˮƽ��ת
                transforms.RandomVerticalFlip(),#����Ĵ�ֱ��ת
                transforms.ToTensor(),#��ͼƬ��ΪTensor��ʽ
                transform_BZ#ͼƬ��׼���Ĳ���
            ])
        self.val_tf = transforms.Compose([##�򵥰�ͼƬѹ���˱��Tensorģʽ
                transforms.Resize(self.img_size),
                transforms.ToTensor(),
                transform_BZ#��׼������
            ])

    def get_images(self, txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            imgs_info = f.readlines()
            imgs_info = list(map(lambda x:x.strip().split('\t'), imgs_info))
        return imgs_info#����ͼƬ��Ϣ

    def padding_black(self, img):   # ����ߴ�̫С��������
        w, h  = img.size
        scale = self.img_size / max(w, h)
        img_fg = img.resize([int(x) for x in [w * scale, h * scale]])
        size_fg = img_fg.size
        size_bg = self.img_size
        img_bg = Image.new("RGB", (size_bg, size_bg))
        img_bg.paste(img_fg, ((size_bg - size_fg[0]) // 2,
                              (size_bg - size_fg[1]) // 2))
        img = img_bg
        return img

    def __getitem__(self, index):#���������뷵�صĶ���
        img_path, label = self.imgs_info[index]
        img = Image.open(img_path)#��ͼƬ
        img = img.convert('RGB')#ת��ΪRGB ��ʽ
        img = self.padding_black(img)
        if self.train_flag:
            img = self.train_tf(img)
        else:
            img = self.val_tf(img)
        label = int(label)

        return img, label

    def __len__(self):
        return len(self.imgs_info)

def WriteData(fname, *args):
    with open(fname, 'a+') as f:
        for data in args:
            f.write(str(data)+"\t")
        f.write("\n")


if __name__ == "__main__":
    train_dataset = LoadData("train.txt", True)
    print("���ݸ�����", len(train_dataset))
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=10,
                                               shuffle=True)
    for image, label in train_loader:
        print("image.shape = ", image.shape)
        # print("image = ",image)
        print("label = ",label)

