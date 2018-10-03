import numpy as np
import cv2
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str)
parser.add_argument('--width', type=int, default=100)
parser.add_argument("--height", type=int, default=100)
parser.add_argument('--exponent', type=float, default=2)
parser.add_argument('--stddev', type=float, default=0.1)
parser.add_argument('--invert', action="store_true")
args = parser.parse_args()

ascii_codes = [
    "01!2\"3#4$5%6&7'8(9)-=^~\\",
    "|qQwWeErRtTyYuUiIoOpP@`[",
    "{aAsSdDfFgGhHjJkKlL;+:*]",
    "}zZxXcCvVbBnNmMmM,<.>/?_",
    "123456789012345678901234"
]

ascii_codes_image = cv2.imread("ascii_codes.png")
ascii_codes_image = cv2.cvtColor(ascii_codes_image, cv2.COLOR_BGR2GRAY)
ascii_codes_image = ascii_codes_image.astype(np.float32) / 255.0

h = ascii_codes_image.shape[0] // 5
w = ascii_codes_image.shape[1] // 24

brightnesses = sorted([
    (ascii_codes[j][i], np.mean(ascii_codes_image[j * h: (j + 1) * h, i * w:(i + 1) * w]))
    for j in range(5) for i in range(24)
], key=lambda item: item[1])


def linear_search(target_brightness):
    for i, (_, brightness) in enumerate(brightnesses):
        if brightness > target_brightness:
            break
    return brightnesses[int(np.clip(np.random.normal(loc=i, scale=args.stddev), 0, len(brightnesses) - 1))][0]


image = cv2.imread(args.filename)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.bitwise_not(image) if args.invert else image
image = image.astype(np.float32) / 255.0
image = image ** args.exponent

h = image.shape[0] // args.height
w = image.shape[1] // args.width

ascii_art = ["".join([linear_search(np.mean(image[j * h: (j + 1) * h, i * w:(i + 1) * w]))
                      for i in range(args.width)]) for j in range(args.height)]

for line in ascii_art:
    print(line)
