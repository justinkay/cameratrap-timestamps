import argparse
import glob
import os
import cv2
import pytesseract as tes
import pandas as pd
from tqdm import tqdm


def do_im(img):
    """
    Args:
        img: (str) path to image file
    Return:
        pandas.Timestamp
    """
    # grab the header
    im = cv2.imread(img)[:30,:750,:]
    
    # invert and add a border; greatly improves results of OCR
    im = (255-im)
    im = cv2.copyMakeBorder(im, 20, 20, 20, 20, cv2.BORDER_CONSTANT, None, value = (255,255,255))

    # try to get text to optimal character height; see: https://groups.google.com/g/tesseract-ocr/c/Wdh_JJwnw94/m/24JHDYQbBQAJ
    im = cv2.resize(im, (int(im.shape[1]*.75), int(im.shape[0]*.75)))
    
    # psm 7: assume 1 line of text
    # tesseract_dt.conf: includes character whitelist and regex-type pattern
    ocr = tes.image_to_string(im, config='--psm 7 tesseract_dt.conf').replace("\n\x0c","")

    try:
        ts = pd.Timestamp(ocr)
        return ts
    except:
        print("Error", img, ocr)
        return None

def do_dir(path):
    """
    Args:
        path: (str) path to directory of images
    Return:
        pandas.DataFrame, filename -> pd.Timestamp
    """
    imgs = glob.glob(path + "/*.jpg") + glob.glob(path + "/*.JPG") + glob.glob(path + "/*.png")
    
    entries = []
    for img in tqdm(imgs):
        ocr = do_im(img)
        entries.append({
            'filename': os.path.basename(img),
            'datetime': ocr
        })
    
    df = pd.DataFrame(entries)
    return df

def main(args):
    if args.dir is not None:
        df = do_dir(args.dir)
        df.to_csv(args.out)
        print(df)
    elif args.img is not None:
        print(do_im(args.img))
    else:
        print("You must specify --dir or --img to run this script.")

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=None, help="Path to directory of image files to process. Use --dir XOR --img.")
    parser.add_argument("--img", default=None, help="Path to image file to process. Use --img XOR --dir.")
    parser.add_argument("--out", default="output.csv", help="Path to CSV output. Only valid if using --dir. Default: ./output.csv")
    return parser

if __name__ == "__main__":
    args = argument_parser().parse_args()
    main(args)