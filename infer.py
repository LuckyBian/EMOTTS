import matplotlib.pyplot as plt
import IPython.display as ipd

import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from text import text_to_sequence2

from scipy.io.wavfile import write


hps = utils.get_hparams_from_file("/home/weizhenbian/vits_emo/configs/cantonese_base.json")
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).cuda()
_ = net_g.eval()

_ = utils.load_checkpoint("/home/weizhenbian/vits_emo/model/G_69000.pth", net_g, None)

def get_text(text,emo,hps):
    text_norm = text_to_sequence(text)
    emo_norm = text_to_sequence2(emo)
    text_norm = text_norm + emo_norm
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

stn_tst = get_text("老师还有什么要做的？","语气中满是疑惑，带有些许的不解和迷惑",hps)

with torch.no_grad():
    x_tst = stn_tst.cuda().unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()

# Save audio to file instead of playing it in IPython
audio_path = "/home/weizhenbian/vits_emo/output/output.wav"
write(audio_path, hps.data.sampling_rate, audio)
print(f"Audio saved to {audio_path}")
