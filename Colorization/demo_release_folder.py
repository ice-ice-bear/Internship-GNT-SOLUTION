import argparse
import matplotlib.pyplot as plt
import os

from colorizers import *

parser = argparse.ArgumentParser()
parser.add_argument('-d','--img_dir', type=str, default='imgs', help='directory containing the input images')
parser.add_argument('--use_gpu', action='store_true', help='whether to use GPU')
parser.add_argument('-o','--save_prefix', type=str, default='saved', help='will save into this file with {eccv16.png, siggraph17.png} suffixes')
parser.add_argument('-s','--save_dir', type=str, default='output', help='directory to save the colorized images')
opt = parser.parse_args()

# load colorizers
colorizer_eccv16 = eccv16(pretrained=True).eval()
colorizer_siggraph17 = siggraph17(pretrained=True).eval()
if(opt.use_gpu):
    colorizer_eccv16.cuda()
    colorizer_siggraph17.cuda()

# default size to process images is 256x256
img_files = [f for f in os.listdir(opt.img_dir) if f.endswith('.jpg') or f.endswith('.png')]
for i, img_file in enumerate(img_files):
    img_path = os.path.join(opt.img_dir, img_file)
    # grab L channel in both original ("orig") and resized ("rs") resolutions
    img = load_img(img_path)
    (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
    if(opt.use_gpu):
        tens_l_rs = tens_l_rs.cuda()

    # colorizer outputs 256x256 ab map
    # resize and concatenate to original L channel
    img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
    out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
    out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

    plt.imsave(os.path.join(opt.save_dir, f'{opt.save_prefix}_{i}_eccv16.png'), out_img_eccv16)
    plt.imsave(os.path.join(opt.save_dir, f'{opt.save_prefix}_{i}_siggraph17.png'), out_img_siggraph17)

