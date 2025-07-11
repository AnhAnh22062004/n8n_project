from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import base64

app = Flask(_name_)

# Thư mục lưu ảnh
UPLOAD_FOLDER = "/home/n8nuser/n8n_project/temp_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/add-text", methods=["POST"])
def add_text():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400

    file = request.files['file']
    text = request.form.get('text', '')

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    # Lấy các tham số bổ sung từ form
    try:
        font_size = int(request.form.get('font_size', 30))
    except ValueError:
        font_size = 30

    try:
        position_y = int(request.form.get('position_y', -1))
    except ValueError:
        position_y = -1

    font_path = request.form.get('font_path', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    
    color = request.form.get('color')
    if not color:
        color = '#D9E006'

    try:
        # Mở ảnh và chuẩn bị vẽ
        img = Image.open(file.stream).convert("RGB")
        draw = ImageDraw.Draw(img)

        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
            line_height = font_size + 5
        except Exception as e:
            font = ImageFont.load_default()
            line_height = 35

        # Wrap text
        lines = textwrap.wrap(text, width=40)
        total_height = len(lines) * line_height - 5
        position_x = img.width // 2

        if position_y == -1:
            position_y = int(img.height * 0.9)

        y_text = position_y - total_height // 2

        # Vẽ text
        for line in lines:
            if hasattr(draw, "textbbox"):
                line_bbox = draw.textbbox((0, 0), line, font=font)
                line_width = line_bbox[2] - line_bbox[0]
            else:
                line_width, _ = draw.textsize(line, font=font)

            x_text = position_x - line_width // 2
            draw.text((x_text, y_text), line, font=font, fill=color)
            y_text += line_height

        # Lưu file
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        img.save(save_path)

        # Encode base64
        with open(save_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        return jsonify({
            "status": "success",
            "filename": file.filename,
            "font_size": font_size,
            "position_y": position_y,
            "font_path": font_path,
            "color": color,
            "base64": encoded
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)