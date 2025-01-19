#
# progressive.py
#
# A simple animated GIF generator to produce a somewhat realistic
# rendering of an odometer.
#
# Amrith
#

from PIL import Image, ImageDraw, ImageFont
import argparse
import glob
import math
import numpy as np
import os
import random
import sys

# the three possible progressive settings
DIGITAL_MODES=['DIGITAL', 'ANALOG', 'ANALOG_ALL']

# make the debug directory, and clean it up if it already exists.
DEBUG_DIR="debug/"
def make_debug_dir():
    os.makedirs(DEBUG_DIR, exist_ok=True)
    files = glob.glob(DEBUG_DIR + "*")
    for f in files:
        os.remove(f)

# frame rate and default simulation time for the animated GIF.
FRAME_RATE=97 # number of frames per second
SIMULATION_TIME = 5 # default 5 seconds

# font, font size, font name and things related to the font.
DIGIT_HEIGHT = 1 # in inches
DIGIT_DPI = 70
# font size in pixels is font height times DPI
FONT_SIZE = DIGIT_DPI * DIGIT_HEIGHT
FONT_NAME = "/System/Library/Fonts/Keyboard.ttf"
FONT = ImageFont.truetype(FONT_NAME, FONT_SIZE)

# the cylinder has 10 digits, each of height DIGIT_HEIGHT
# pixels. Assuming that there's a border around each, the radius of
# the cylinder can be computed below. oddly enough this is a cylinder
# radius in pixels.

BORDER_SIZE = 0.05
CYLINDER_RADIUS = int((FONT_SIZE * (1 + BORDER_SIZE) * 10) / (2 * math.pi))

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def nearest_prime(n):
    if is_prime(n):
        return n

    lower = n - 1
    upper = n + 1

    while True:
        if is_prime(lower):
            return lower
        if is_prime(upper):
            return upper

        lower -= 1
        upper += 1

# The values to be shown in the animation are computed here. A start
# and end value are used to determine the various values that need to
# be inserted into the animation. Since you can't do a for loop on
# floats using range(), use np.arange. But that means you force back
# to a float. The array is guaranteed to start with 'start' but we
# force it to end with finish.
def make_values_array(start, finish, count):
    values = []

    step = nearest_prime(int(finish - start)/count)

    for v in np.arange(start, finish, step):
        values.append(float(v))

    if values[-1] != finish:
        values.append(float(finish))

    return values

# each digit has a different width and height, and renders at a
# different position relative to the baseline. Figure the size of the
# digit bounding box next.
def get_digit_dimensions(font):
    max_width = 0

    # each font has a defined ascent and descent - the amounts above
    # and below the baseline. The bounding box should be at least that
    # high.
    ascent, descent = font.getmetrics()
    max_height = ascent + descent

    for digit in "0123456789":
        bbox = font.getbbox(digit)
        width = bbox[2] - bbox[0] # right - left.

        if width > max_width:
            max_width = width

    return max_width, max_height

#
# the coordinate system has an origin at the top left, and x increases
# right, and y increases down.
#
# there are N digits in the display. The x dimension of the image is
# therefore (N+1) borders and N digit_widths. The y dimension is twice
# the border and the digit height.
#
# The location(s) of the digits is computed along with the bounding
# boxes.
#
def get_digit_layout(digits):
    # first get the dimensions of the digits
    digit_width, digit_height = get_digit_dimensions(FONT)

    # the borders around each box are based on the height and width
    xborder = int(digit_width * BORDER_SIZE)
    yborder = int(digit_height * BORDER_SIZE)

    # the locations array is an array of the top left corners of each
    # digit in the rendering.
    locations = []

    # the bounding boxes start from the locations, and have
    # digit_width and digit_height
    boxes = []

    # since we compute the digits to render based on the modulo after
    # division by 10, the locations array is computed in backwards
    # order. The first entry in the locations array should relate to
    # the furthest left digit.
    for i in reversed(range(digits)):
        x = xborder + i * (digit_width + xborder)
        locations.append([x, yborder])
        boxes.append([x, yborder, x + digit_width, yborder + digit_height])

    def get_image_size():
        return digits * (digit_width + xborder) + xborder, \
            digit_height + 2 * yborder

    image_size = get_image_size()

    return digit_width, digit_height, locations, image_size, boxes

# make_counter_frame is used to draw a single frame of the
# counter. Here, value is a floating point number. Each frame consists
# of many digits. Each digit has a fixed width which was determined
# earlier using get_digit_width. first, let's look at the x coordinate
# of each digit.
def make_counter_frame(digits, v, digit_width, digit_height, locations,
                       image_size, boxes, mode):
    img = Image.new("RGBA", image_size, "black")
    draw = ImageDraw.Draw(img)

    mask = Image.new("L", image_size, 0)
    mask_draw = ImageDraw.Draw(mask)

    # begin with an integer value
    value = v

    for d in range(digits):
        digit = int(value % 10)

        dtext = str(digit)
        # the digit should be rendered at the yoffset

        if mode == 'DIGITAL' or (mode == 'ANALOG' and d != 0):
            yoffset = 0
        else:
            yoffset = ((value % 10) - digit) * digit_height

        l = [locations[d][0], locations[d][1] - yoffset]
        draw.text(l, dtext, font=FONT, fill="white")

        if yoffset != 0:
            dtext = str((digit + 1) % 10)
            l[1] += digit_height
            draw.text(l, dtext, font=FONT, fill="white")

        # then draw the box around each digit and the mask
        draw.rectangle(boxes[d], outline="gray")
        mask_draw.rectangle(boxes[d], fill=255)

        value = value / 10

    img.putalpha(mask)
    return img

def make_counter_gif(digits=8, start=0, finish=1000000,
                     nseconds = SIMULATION_TIME, file="sim.gif",
                     mode='DIGITAL', rate=FRAME_RATE):

    if mode not in DIGITAL_MODES:
        print(f"Invalid mode: {mode}. Must be one of {DIGITAL_MODES}")

    # add 1 to make the number of frames not some nice power of 10
    nframes = nseconds * rate + 1

    # get the values to simulate
    values = make_values_array(start, finish, nframes)

    # compute the layout of the digit display
    digit_width, digit_height, locations, \
        image_size, boxes = get_digit_layout(digits)

    frames = []

    # compute the image size
    for v in values:
        # print(f"Make image for value {v}")
        img = make_counter_frame(digits, v, digit_width, digit_height,
                                 locations, image_size, boxes, mode)
        filename = f"{DEBUG_DIR}/{v:.2f}.gif"
        img.save(filename, "GIF")
        frames.append(img)

    frames[0].save(f"{file}", save_all=True,
                   append_images=frames[1:],
                   duration=int(nseconds * 1000 / len(frames)))
    print(f"Generated {file} with %d frames." % len(frames))

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse command-line arguments for the application.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Define arguments
    parser.add_argument('-r', '--rate', type=int, default=FRAME_RATE, help="Frame rate (/s).")
    parser.add_argument('-d', '--digits', type=int, help="Number of digits to display.")
    parser.add_argument('-s', '--start', type=int, default=0, help="Start number.")
    parser.add_argument('-f', '--finish', type=int, required=True, help="Finish number (required).")
    parser.add_argument('-t', '--time', type=int, default=15, help="Time per frame in milliseconds.")
    parser.add_argument('--file', type=str, help="Output file name.")
    parser.add_argument('-m', '--mode', type=str, choices=['DIGITAL', 'ANALOG', 'ANALOG_ALL'],
                        default='ANALOG', help="Mode of the animation.")

    args = parser.parse_args()

    # Handle default for digits
    if args.digits is None:
        args.digits = len(str(args.finish))

    # Handle default for file
    if args.file is None:
        args.file = f"{args.finish}.gif"

    return args

def usage():
    return """\
Usage:
  python script.py -f <finish> [options]

Options:
  -r, --rate      Frame rate (default: %d frames per second).
  -d, --digits    Number of digits to display (default: number of digits in finish).
  -s, --start     Start number (default: 0).
  -f, --finish    Finish number (required).
  -t, --time      Time per frame in milliseconds (default: 15).
      --file      Output file name (default: <finish>.gif).
  -m, --mode      Mode of the animation, one of DIGITAL, ANALOG, ANALOG_ALL (default: ANALOG).
""" % (FRAME_RATE)

def main():
    try:
        args = parse_args()
    except SystemExit as e:  # Catch argparse's error handling
        print(usage())
        sys.exit(e.code)

    make_debug_dir()
    make_counter_gif(digits=args.digits,
                     start=args.start,
                     finish=args.finish,
                     nseconds=args.time,
                     file=args.file,
                     mode=args.mode,
                     rate=args.rate)

if __name__ == "__main__":
    main()
