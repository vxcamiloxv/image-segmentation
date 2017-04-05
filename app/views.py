"""views

Copyright (C) 2017 Camilo QS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from flask import render_template
from PIL import ImageEnhance, Image
import numpy as np
import cv2
import os

from app import app


@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/api/segmentation', methods=['GET'])
def segmentation():
    """ Read image from static directori and set segmentation """

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(APP_ROOT, 'static/images/')

    image_in = cv2.imread(os.path.join(IMAGE_PATH, 'input.jpg'))
    colors = [([18, 23, 187], [181, 183, 255])]

    # loop by color range
    for (min_r, max_r) in colors:
        # create color array
        min_r = np.array(min_r, dtype = 'uint8')
        max_r = np.array(max_r, dtype = 'uint8')

        print(min_r)

        # search color and create mask
        mask = cv2.inRange(image_in, min_r, max_r)
        mask = cv2.bitwise_and(image_in, image_in, mask = mask)

        # Set saturation
        image_sat = ImageEnhance.Color(Image.fromarray(image_in.copy()))
        image_sat = image_sat.enhance(0.0)
        image_in = cv2.cvtColor(np.array(image_sat), cv2.COLOR_RGB2BGR)

        # merge images
        image_out = image_in.copy()
        cv2.addWeighted(image_in, 1.0, mask, 1.0, 0.0, image_out);

        # save output
        cv2.imwrite(os.path.join(IMAGE_PATH, 'output.jpg'), image_out)

        return app.send_static_file('images/output.jpg')
