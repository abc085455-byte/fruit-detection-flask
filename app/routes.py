from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
import os
from app.utils import detect_fruits, allowed_file, cleanup_old_files

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
    
    try:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        result_data = detect_fruits(
            upload_path, 
            current_app.config['RESULT_FOLDER']
        )
        
        cleanup_old_files(current_app.config['UPLOAD_FOLDER'], max_age_hours=24)
        cleanup_old_files(current_app.config['RESULT_FOLDER'], max_age_hours=24)
        
        return jsonify(result_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/result/<filename>')
def result(filename):
    result_path = url_for('static', filename=f'results/{filename}')
    return render_template('result.html', image_path=result_path)