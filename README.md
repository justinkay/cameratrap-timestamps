# cameratrap-timestamps
Extract timestamps from camera trap images using OCR. Currently only supports Reconyx-style images where the timestamp is in the header.

### Example Image & Output


## Setup
1. Install tesseract (OCR library)

```
sudo apt install tesseract-ocr
```

2. Install Python requirements

```
pip install -r requirements.txt
```

## Usage

Process a single image and return the timestamp:
```
python extract.py --img [path/to/image/img.jpg]
>>> 
```

Process a directory of images and write results to a CSV file:
```
python extract.py --dir [path/to/image/directory/] --out [path/to/output.csv]
```
