from flask import Flask, render_template, request, redirect, url_for
import os
from ecg_model import predict_af

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and file.filename.endswith('.hd5'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        try:
            # Get the predictions and plot URL
            predictions = predict_af(file_path)
            return render_template('results.html', **predictions)
        except Exception as e:
            return f"An error occurred while processing the file: {e}", 500
    else:
        return "Invalid file format. Please upload an .hd5 file.", 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

