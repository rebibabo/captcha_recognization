# -*- coding: UTF-8 -*-
from captcha.image import ImageCaptcha  # pip install captcha
from PIL import Image
import random
import shutil
import os
from tqdm import tqdm
import config

def gen_captcha_text_and_image() -> None:
    if os.path.exists(config.output_dir):
        shutil.rmtree(config.output_dir)
    os.makedirs(config.train_dataset_path, exist_ok=True)
    os.makedirs(config.valid_dataset_path, exist_ok=True)
    os.makedirs(config.test_dataset_path, exist_ok=True)
 
    hash_set = set()
    image = ImageCaptcha(width=240, height=80)
    datasets = []
    for i in tqdm(range(config.dataset_num), desc="Generating captchas"):
        for _ in range(100):
            captcha_text = random.choices(config.character_set, k=config.max_captcha_length)
            captcha_text = ''.join(captcha_text)
            h = hash(captcha_text)
            if h not in hash_set:
                hash_set.add(h)
                captcha_image = Image.open(image.generate(captcha_text))
                captcha_image = captcha_image.resize(config.image_size)
                datasets.append((captcha_text, captcha_image))
                break
    
    random.shuffle(datasets)
    train_count = int(config.split_ratio[0] * config.dataset_num)
    valid_count = int(config.split_ratio[1] * config.dataset_num)
    for i, (captcha_text, captcha_image) in enumerate(datasets[:train_count]):
        filename = f"{i+1}_{captcha_text}.png"
        captcha_image.save(os.path.join(config.train_dataset_path, filename))
    for i, (captcha_text, captcha_image) in enumerate(datasets[train_count:train_count+valid_count]):
        filename = f"{i+1}_{captcha_text}.png"
        captcha_image.save(os.path.join(config.valid_dataset_path, filename))
    for i, (captcha_text, captcha_image) in enumerate(datasets[train_count+valid_count:]):
        filename = f"{i+1}_{captcha_text}.png"
        captcha_image.save(os.path.join(config.test_dataset_path, filename))
         
if __name__ == '__main__':
    gen_captcha_text_and_image()