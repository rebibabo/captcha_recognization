# -*- coding: UTF-8 -*-
import os

''' dataset config '''
output_dir: str = "dataset"
image_size: tuple[int, int] = [140, 40]
dataset_num: int = 20000
split_ratio: list[float] = [0.8, 0.1, 0.1]
max_captcha_length: int = 4

train_dataset_path = os.path.join(output_dir, "train")
valid_dataset_path = os.path.join(output_dir, "valid")
test_dataset_path = os.path.join(output_dir, "test")

character_set = [str(i) for i in range(10)] + list('abcdefghijklmnopqrstuvwxyz')
charset_len = len(character_set)

''' train config '''
batch_size: int = 64
num_epochs: int = 100
learning_rate: float = 0.001

