# -*- coding: UTF-8 -*-
import numpy as np
import config

char2pos = {c: pos for pos, c in enumerate(config.character_set)}
pos2char = {pos: c for pos, c in enumerate(config.character_set)}

def encode(text):
    vector = np.zeros(config.charset_len * config.max_captcha_length, dtype=float)
    for i, c in enumerate(text):
        idx = i * config.charset_len + char2pos[c]
        if idx >= vector.shape[0]:
            print(f"Error: captcha text is over length limit: {config.max_captcha_length}")
            exit()
        vector[idx] = 1.0
    return vector

def decode(vec):
    char_pos = vec.nonzero()[0]
    text = ''
    for c in char_pos:
        char_idx = c % config.charset_len
        text += pos2char[char_idx]
    return "".join(text)

if __name__ == '__main__':
    e = encode("2657DSADasflihqlwe34")
    print(decode(e))