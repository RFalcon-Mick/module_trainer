"""
ѵ��ģ�ͣ�Resnet18��
"""

import time
import torch
from torch import nn
from torch.utils.data import DataLoader
from utils import LoadData, WriteData

from torchvision.models import resnet18


def train(dataloader, model, loss_fn, optimizer, device):
    size = len(dataloader.dataset)
    avg_loss = 0
    # �����ݼ������ж�ȡbatch��һ�ζ�ȡ�����ţ�������������X(ͼƬ����)��y��ͼƬ��ʵ��ǩ����
    for batch, (X, y) in enumerate(dataloader):  # �̶���ʽ��batch���ڼ������ݣ��������δ�С����X��y������ֵ������
        # �����ݴ浽�Կ�
        X, y = X.to(device), y.to(device)
        # �õ�Ԥ��Ľ��pred
        pred = model(X)
        loss = loss_fn(pred, y)
        avg_loss += loss
        # ���򴫲�������ģ�Ͳ���
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # ÿѵ��10�Σ����һ�ε�ǰ��Ϣ
        if batch % 10 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

    # ��һ��epoch���˺󷵻�ƽ�� loss
    avg_loss /= size
    avg_loss = avg_loss.detach().cpu().numpy()
    return avg_loss


def validate(dataloader, model, loss_fn, device):
    size = len(dataloader.dataset)
    # ��ģ��תΪ��֤ģʽ
    model.eval()
    # ��ʼ��test_loss �� correct�� ����ͳ��ÿ�ε����
    test_loss, correct = 0, 0
    # ����ʱģ�Ͳ������ø��£�����no_gard()
    # ��ѵ���� �������õ�
    with torch.no_grad():
        # �������ݼ��������õ������X��ͼƬ���ݣ���y(��ʵ��ǩ��
        for X, y in dataloader:
            # ������ת��GPU
            X, y = X.to(device), y.to(device)
            # ��ͼƬ���뵽ģ�͵��оͣ��õ�Ԥ���ֵpred
            pred = model(X)
            # ����Ԥ��ֵpred����ʵֵy�Ĳ��
            test_loss += loss_fn(pred, y).item()
            # ͳ��Ԥ����ȷ�ĸ���(��Է���)
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= size
    correct /= size
    print(f"correct = {correct}, Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
    return correct, test_loss


if __name__ == '__main__':
    batch_size = 5

    # # ��ѵ�����Ͳ��Լ��ֱ𴴽�һ�����ݼ�������
    train_data = LoadData("train.txt", True)
    valid_data = LoadData("test.txt", False)

    train_dataloader = DataLoader(dataset=train_data, num_workers=4, pin_memory=True, batch_size=batch_size,
                                  shuffle=True)
    valid_dataloader = DataLoader(dataset=valid_data, num_workers=4, pin_memory=True, batch_size=batch_size)

    # ����Կ����ã������Կ�����ѵ��
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")
    classes = 55  # ָ��������
    model = resnet18(num_classes=classes)  # num_classes ����ָ������

    model = model.to(device)

    # ������ʧ���������������٣������أ�
    loss_fn = nn.CrossEntropyLoss()

    # �����Ż���������ѵ��ʱ���Ż�ģ�Ͳ���������ݶ��½���
    learning_rate = 1e-3
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    epochs = 500
    loss_ = 10
    save_root = "output/"

    for t in range(epochs):
        print(f"Epoch {t + 1}\n-------------------------------")
        time_start = time.time()
        avg_loss = train(train_dataloader, model, loss_fn, optimizer, device)
        time_end = time.time()
        print(f"train time: {(time_end - time_start)}")
        # (dataloader, model, loss_fn, device)jif
        val_accuracy, val_loss = validate(valid_dataloader, model, loss_fn, device)
        # д������
        WriteData(save_root + "resnet18_no_pretrain.txt",
                  "epoch", t,
                  "train_loss", avg_loss,
                  "val_loss", val_loss,
                  "val_accuracy", val_accuracy)
        if t % 5 == 0:
            torch.save(model.state_dict(),
                       save_root + "resnet18_no_pretrain_epoch" + str(t) + "_loss_" + str(avg_loss) + ".pth")

        torch.save(model.state_dict(), save_root + "resnet18_no_pretrain_last.pth")

        if avg_loss < loss_:
            loss_ = avg_loss
            torch.save(model.state_dict(), save_root + "resnet18_no_pretrain_best.pth")
