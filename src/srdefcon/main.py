#!/usr/bin/env python
# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause

from .core import Core
import time
from PIL import Image, ImageDraw, ImageFont
import colorsys

try:
    import unicornhathd

    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicornhathd

FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf", 10)

COLOR_MAPPING = {
    5: (0, 0, 255),
    4: (0, 255, 0),
    3: (0xff, 0xff, 0x00),
    2: (0xff, 0x75, 0x00),
    1: (255, 0, 0),
    0: (0, 0, 0),
}
font = ImageFont.truetype(*FONT)


def drawText(lines, bgcolor):
    print("Drawing %r" % lines)
    text_x = u_width
    text_y = 2

    font_file, font_size = FONT

    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = u_width, 0

    for line in lines:
        w, h = font.getsize(line)
        text_width += w + u_width
        text_height = max(text_height, h)

    text_width += u_width + text_x + 1

    image = Image.new("RGB", (text_width, max(16, text_height)), bgcolor)
    draw = ImageDraw.Draw(image)

    offset_left = 0

    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, (255 - bgcolor[0], 255 - bgcolor[1], 255 - bgcolor[2]),
                  font=font)

        offset_left += font.getsize(line)[0] + u_width

    for scroll in range(text_width - u_width):
        for x in range(u_width):
            for y in range(u_height):
                pixel = image.getpixel((x + scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(u_width - 1 - x, y, r, g, b)

        unicornhathd.show()
        time.sleep(0.1)


def getColor(d):
    return COLOR_MAPPING[d]


def getScore():
    return Core().score()


def getDefcon():
    return Core().defcon()


def getInstances():
    r = Core().instances()
    # print "Found {} instances".format(r)
    if r is None or len(r) == 0:
        return [":)"]
    else:
        return r


def setColor(r, g, b):
    for x in range(0, u_width):
        for y in range(0, u_height):
            unicornhathd.set_pixel(x, y, r, g, b)
    unicornhathd.show()


unicornhathd.rotation(0)
u_width, u_height = unicornhathd.get_shape()

try:
    while True:
        print("Getting defcon")
        defcon = getDefcon()
        print("Defcon {}".format(defcon))
        color = getColor(defcon)
        print("Color {}".format(color))
        drawText(getInstances(), color)
except KeyboardInterrupt:
    unicornhathd.off()
