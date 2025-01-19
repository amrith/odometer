# odometer

A animated GIF generator to simulate an odometer display.

# Description

An odometer provides a digital display of a distance. Similar displays
include a hobbs meter or an old fashioned pedometer. In its most basic
form, an odometer consists of a number of decimal digits, counting
upwards.

A traditional counter of this kind has an analog least significant
digit, and the other digits are all digital. In other words, the least
significant digit moves slowly, and you get to see the transition from
one value to the next but the other digits snap from one to the next.

This odometer provides some flexibility in the output it generates,
allowing you to simulate a fully digital, fully analog, or
conventional display.

# Usage

usage: odometer.py [-h] [-r RATE] [-d DIGITS] [-s START] -f FINISH [-t TIME]
                   [--file FILE] [-m {DIGITAL,ANALOG,ANALOG_ALL}]
odometer.py: error: the following arguments are required: -f/--finish
Usage:
  python script.py -f <finish> [options]

Options:
  -r, --rate      Frame rate (default: 97 frames per second).
  -d, --digits    Number of digits to display (default: number of digits in finish).
  -s, --start     Start number (default: 0).
  -f, --finish    Finish number (required).
  -t, --time      Time per frame in milliseconds (default: 15).
      --file      Output file name (default: <finish>.gif).
  -m, --mode      Mode of the animation, one of DIGITAL, ANALOG, ANALOG_ALL (default: ANALOG).

# Sample

```
   python odometer.py --finish 200 --time 5 --mode DIGITAL --file 200.gif
```

Make a fully digital odometer starting at 0 counting up to 200 over 5
seconds in a file called 200.gif.

