from flask import Flask, render_template, request, jsonify, send_file
import io
from PIL import Image

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.form['positivePrompts']
        image = Image.new('RGB', (100, 100), color='red')

        image_stream = io.BytesIO()
        image.save(image_stream, format='PNG')
        image_stream.seek(0)
        return send_file(image_stream, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)