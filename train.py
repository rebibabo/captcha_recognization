# -*- coding: UTF-8 -*-
import torch
import torch.nn as nn
from torch.autograd import Variable
import my_dataset
from model import CNN
from tqdm import tqdm
import numpy as np
import one_hot_encoding
import config

def evaluate(model, valid_dataloader):
    model.eval()
    correct = 0
    total = 0
    for images, labels in tqdm(valid_dataloader, desc='Validating', total=len(valid_dataloader)):
        image = images
        vimage = Variable(image)
        output = model(vimage)

        # c0 = config.character_set[np.argmax(predict_label[0, 0:config.charset_len].data.numpy())]
        # c1 = config.character_set[np.argmax(predict_label[0, 1*config.charset_len:2*config.charset_len].data.numpy())]
        # c2 = config.character_set[np.argmax(predict_label[0, 2*config.charset_len:3*config.charset_len].data.numpy())]
        # c3 = config.character_set[np.argmax(predict_label[0, 3*config.charset_len:4*config.charset_len].data.numpy())]
        # print(c0, c1, c2, c3)
        # predict_label = '%s%s%s%s' % (c0, c1, c2, c3)
        
        predict_label = ''
        for i in range(config.max_captcha_length):
            c = config.character_set[np.argmax(output[0, i*config.charset_len:(i+1)*config.charset_len].data.numpy())]
            predict_label += c
        true_label = one_hot_encoding.decode(labels.numpy()[0])
        print((predict_label, true_label))
        total += labels.size(0)
        if(predict_label == true_label):
            correct += 1
    acc = correct / total
    print(f"Test Accuracy of the model on the {total} test images: {acc:.2f} %")
    return acc

def train():
    model = CNN()
    criterion = nn.MultiLabelSoftMarginLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)

    train_dataloader = my_dataset.get_train_data_loader()
    valid_dataloader = my_dataset.get_valid_data_loader()
    for epoch in range(config.num_epochs):
        bar = tqdm(train_dataloader, total=len(train_dataloader))
        total_loss = 0
        best_acc = 0
        model.train()
        for i, (images, labels) in enumerate(bar):
            images = Variable(images)
            labels = Variable(labels.float())
            predict_labels = model(images)
            loss = criterion(predict_labels, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            bar.set_description(f"Epoch: {epoch+1}, Loss: {total_loss/(i+1):.4f}")
        acc = evaluate(model, valid_dataloader)
        if acc > best_acc:
            best_acc = acc
        torch.save(model.state_dict(), "./best_model.pkl")   #current is best_model.pkl
        print("save last model")

if __name__ == '__main__':
    train()


