from flask import Flask, render_template, request
import os
from LZW import LZW
import io
from base64 import encodebytes
from PIL import Image
import json
import mimetypes
import glob
from flask import send_file, safe_join

app = Flask(__name__, static_url_path = "/")
app.config['SECRET_KEY'] = 'dcdfbdgdvscdvfbdvs'
app.config['uploads'] = "static/uploads"


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/download/', methods = ["POST", "GET"])
def download():
    if request.method == "GET":
        # data = json.loads(request.data.decode(encoding='UTF-8'))
        # json_data = json.loads(str(request.data, encoding='utf-8'))
        # print(json_data)
        fl_path = "CompressedFiles/"
        filename = 'downloaded_file_name.lzw'
        rt = glob.glob(os.path.join(fl_path, '*.lzw'))
        print(rt)
        # fl = open(rt[0], 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        return send_file(fl_path + rt[0].split('/')[1], as_attachment=True)
        # response = HttpResponse(fl, content_type=mime_type)
        # response['Content-Disposition'] = "attachment; filename=%s" % filename

@app.route('/compress/', methods = ["POST", "GET"])
def compress():
  if request.method == "POST":
    if request.files:
      content_type = request.mimetype
      image = request.files['image']
      image.save(os.path.join(app.config['uploads'], image.filename))
      encoded_img = get_response_image(os.path.join(app.config['uploads'], image.filename))
      response = {"message": "saved", "encoded_img": encoded_img}
      return response, 200

def get_response_image(image_path):
    print(image_path)
    filesplit = image_path.split('.')
    filesplit1 = filesplit[0].split('/')

    print(filesplit1)
    compressor = LZW(image_path)
    compressor.compress()

    decompressor = LZW("CompressedFiles/" + filesplit1[2] + "Compressed.lzw")
    encoded_img = decompressor.decompress()
    
    pil_img = Image.open("DecompressedFiles/" + filesplit1[2] + "Decompressed.jpg", mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)
