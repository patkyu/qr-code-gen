from flask import Flask, request, send_file, send_from_directory
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    text = request.form.get('text', '')
    color = request.form.get('color', '#000000')
    logo = request.files.get('logo')

    if not text:
        return "No text provided", 400

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color="white").convert("RGB")

    # Add logo if provided
    if logo:
        logo_img = Image.open(logo).convert("RGBA")
        logo_size = int(min(img.size) / 4)  # Logo is 1/4th of the QR code size
        logo_img = logo_img.resize((logo_size, logo_size), Image.LANCZOS)

        # Position the logo at the center
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(logo_img, pos, mask=logo_img)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
