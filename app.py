import json
import tempfile

import cv2
from flask import Flask, request
from pytesseract import pytesseract

from cordinates.Cordinates import Cordinates

app = Flask(__name__)


@app.route('/', methods=['POST'])
def ocr_image_by_cordinates():
    cordinates_list = get_cordinates_request(request)

    file_path = save_file(request)
    image = cv2.imread(file_path)

    length = len(cordinates_list)
    ocr_texts = []
    for count in range(0, length):
        coordinates = cordinates_list[count]
        image_block = image[coordinates.startY:coordinates.endY, coordinates.startX:coordinates.endX]

        text = pytesseract.image_to_string(image_block, lang='pol')
        ocr_texts.append(text)

    return ocr_texts[0]


def save_file(request):
    fileContent = request.files['fileContent']
    file_name = request.values["fileName"]
    temp_dir = tempfile.gettempdir()
    tmp_file_name = temp_dir + "/" + file_name
    fileContent.save(tmp_file_name)
    return tmp_file_name


def get_cordinates_request(request):
    cordinates_list = []
    count = 0
    while True:
        try:
            startx = request.values["data[%s][coordinates][startX]" % count]
            endX = request.values["data[%s][coordinates][endX]" % count]
            startY = request.values["data[%s][coordinates][startY]" % count]
            endY = request.values["data[%s][coordinates][endY]" % count]
            count = count + 1
            cordinates_list.append(
                Cordinates(startx, endX, startY, endY))
        except:
            break
    return cordinates_list


if __name__ == '__main__':
    app.run(debug=True)
