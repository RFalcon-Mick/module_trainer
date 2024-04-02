"""
��ͼ����
"""

import torch
from torchvision.models import resnet18
from PIL import Image
import torchvision.transforms as transforms
import os

transform_BZ= transforms.Normalize(
    mean=[0.46402064, 0.45047238, 0.37801373],  # ȡ�������ݼ�
    std=[0.2007732, 0.196271, 0.19854763]
)


def padding_black(img,img_size = 512):  # ����ߴ�̫С��������
    w, h = img.size
    scale = img_size / max(w, h)
    img_fg = img.resize([int(x) for x in [w * scale, h * scale]])
    size_fg = img_fg.size
    size_bg = img_size
    img_bg = Image.new("RGB", (size_bg, size_bg))
    img_bg.paste(img_fg, ((size_bg - size_fg[0]) // 2,
                          (size_bg - size_fg[1]) // 2))
    img = img_bg
    return img

if __name__=='__main__':

    img_path = r''  # ���ô���ͼ��·��

    val_tf = transforms.Compose([  # �򵥰�ͼƬѹ���˱��Tensorģʽ
        transforms.Resize(512),
        transforms.ToTensor(),
        transform_BZ  # ��׼������
    ])



    # ����Կ����ã������Կ�����ѵ��
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")
    classes = 55  # ָ��������
    finetune_net = resnet18(num_classes=classes).to(device)

    state_dict = torch.load(r"output/resnet18_e_1e-3_best.pth")
    # print("state_dict = ",state_dict)
    finetune_net.load_state_dict(state_dict)
    finetune_net.eval()
    with torch.no_grad():

        # finetune_net.to(device)
        img = Image.open(img_path)  # ��ͼƬ
        img = img.convert('RGB')  # ת��ΪRGB ��ʽ
        img = padding_black(img)
        img = val_tf(img)
        img_tensor = torch.unsqueeze(img, 0)    # N,C,H,W, ; C,H,W

        img_tensor = img_tensor.to(device)
        result = finetune_net(img_tensor)
        # print("result = ",result.argmax(1))


        id = result.argmax(1).item()

        file_list=[]
        for a,b,c in os.walk("dataset"):
            if len(b) != 0:
                file_list = b
                print("Ԥ����Ϊ��", file_list[id])
