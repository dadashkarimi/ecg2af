from flask import Flask, render_template, request, redirect, url_for, session
import os
from ecg_model import predict_af

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return "No file part", 400

    files = request.files.getlist('files')
    if not files:
        return "No selected files", 400

    # Initialize lists for valid and invalid files
    file_paths = []
    file_names = []
    invalid_files = []

    for file in files:
        if file.filename == '':
            return "No selected file", 400
        if file and file.filename.endswith('.hd5'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_paths.append(file_path)
            file_names.append(file.filename)  # Store the original file name
        else:
            # Add to the list of invalid files if format is incorrect
            invalid_files.append(file.filename)

    # If there are any invalid files, return an error message listing them
    if invalid_files:
        return jsonify({
            "status": "error",
            "message": "Invalid file format. Please upload .hd5 files only.",
            "invalid_files": invalid_files
        }), 400

    # Save valid file paths and names to session and redirect to /results
    session['file_paths'] = file_paths
    session['file_names'] = file_names
    return redirect(url_for('show_results'))

@app.route('/results')
def show_results():
    # Get file paths from session
    file_paths = session.get('file_paths', None)
    file_names = session.get('file_names', None)
    if not file_paths or not file_names:
        return redirect(url_for('index'))

    results = []
    combined_results = []  # List to hold combined results with file names
    for file_path, file_name in zip(file_paths, file_names):
        try:
            # Get predictions from each uploaded file
            predictions = predict_af(file_path)
            combined_results.append((predictions, file_name))  # Store as tuple
        except Exception as e:
            return f"An error occurred while processing the file: {e}", 500

    return render_template('results.html', combined_results=combined_results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


