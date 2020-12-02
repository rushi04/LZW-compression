from flask import Flask, render_template, request
import os
from LZW import LZW
import io
from base64 import encodebytes
from PIL import Image

app = Flask(__name__, static_url_path = "/")
app.config['SECRET_KEY'] = 'dcdfbdgdvscdvfbdvs'
app.config['uploads'] = "static/uploads"


@app.route('/')
def index():
	return render_template('index.html')

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

    decompressor = LZW("CompressedFiles/" +filesplit1[2] +"Compressed.lzw")
    encoded_img = decompressor.decompress()
    
    pil_img = Image.open("DecompressedFiles/" + filesplit1[2] + "Decompressed.jpg", mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)
