# -*- coding: UTF-8 -*-
import os
from torch.utils.data import DataLoader,Dataset
import torchvision.transforms as transforms
from PIL import Image
import one_hot_encoding as ohe
import config

class mydataset(Dataset):
    def __init__(self, folder, transform=None):
        self.file_paths = [os.path.join(folder, image_file) for image_file in os.listdir(folder)]
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        image_root = self.file_paths[idx]
        image_name = image_root.split(os.path.sep)[-1]
        image = Image.open(image_root)
        if self.transform is not None:
            image = self.transform(image)
        label = ohe.encode(image_name.split('_')[1].split('.')[0])
        return image, label

transform = transforms.Compose([
    # transforms.ColorJitter(),
    transforms.Grayscale(),
    transforms.ToTensor(),
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
def get_train_data_loader():
    dataset = mydataset(config.train_dataset_path, transform=transform)
    return DataLoader(dataset, batch_size=config.batch_size, shuffle=True)

def get_valid_data_loader():
    dataset = mydataset(config.valid_dataset_path, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=False)

def get_test_data_loader():
    dataset = mydataset(config.test_dataset_path, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=False)