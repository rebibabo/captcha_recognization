# -*- coding: UTF-8 -*-
import numpy as np
import torch
from torch.autograd import Variable
#from visdom import Visdom # pip install Visdom
import config
import my_dataset
from model import CNN

def main():
    cnn = CNN()
    cnn.eval()
    cnn.load_state_dict(torch.load('best_model.pkl'))
    print("load cnn net.")

    predict_dataloader = my_dataset.get_predict_data_loader()

    #vis = Visdom()
    for i, (images, labels) in enumerate(predict_dataloader):
        image = images
        vimage = Variable(image)
        output = cnn(vimage)

        predict_label = ''
        for i in range(config.max_captcha_length):
            c = config.character_set[np.argmax(output[0, i*config.charset_len:(i+1)*config.charset_len].data.numpy())]
            predict_label += c
        #vis.images(image, opts=dict(caption=c))
        print("predict_label:", predict_label)
        print("true_label:", labels[0])

if __name__ == '__main__':
    main()


