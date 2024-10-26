from flask import Flask, render_template, request, redirect, url_for, session
import os
from ecg_model import predict_af

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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

        # Save file path to session and redirect to /results
        session['file_path'] = file_path
        return redirect(url_for('show_results'))
    else:
        return "Invalid file format. Please upload an .hd5 file.", 400

@app.route('/results')
def show_results():
    # Get file path from session and process predictions
    file_path = session.get('file_path', None)
    if not file_path:
        return redirect(url_for('index'))
    
    try:
        # Get predictions from the uploaded file
        predictions = predict_af(file_path)
        return render_template('results.html', **predictions)
    except Exception as e:
        return f"An error occurred while processing the file: {e}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

