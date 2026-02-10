from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Note
from app.routes.auth import lecturer_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime

lecturer_bp = Blueprint('lecturer', __name__, url_prefix='/lecturer')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@lecturer_bp.route('/dashboard')
@login_required
@lecturer_required
def dashboard():
    """Lecturer dashboard - list and manage notes"""
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(uploaded_by=current_user.id).order_by(Note.upload_date.desc()).paginate(page=page, per_page=10)
    return render_template('lecturer_dashboard.html', notes=notes)

@lecturer_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@lecturer_required
def upload():
    """Upload a new lecture note"""
    if request.method == 'POST':
        course_title = request.form.get('course_title', '').strip()
        course_code = request.form.get('course_code', '').strip()
        file = request.files.get('file')
        
        # Validation
        if not all([course_title, course_code, file]):
            flash('All fields are required.', 'error')
            return redirect(url_for('lecturer.upload'))
        
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('lecturer.upload'))
        
        if not allowed_file(file.filename):
            flash('Only PDF and DOCX files are allowed.', 'error')
            return redirect(url_for('lecturer.upload'))
        
        # Secure the filename
        original_filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + original_filename
        
        # Save file
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create note record in database
        note = Note(
            course_title=course_title,
            course_code=course_code,
            filename=original_filename,
            file_path=filepath,
            uploaded_by=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        
        flash('Lecture note uploaded successfully!', 'success')
        return redirect(url_for('lecturer.dashboard'))
    
    return render_template('upload.html')

@lecturer_bp.route('/delete/<int:note_id>', methods=['POST'])
@login_required
@lecturer_required
def delete_note(note_id):
    """Delete a lecture note"""
    note = Note.query.get_or_404(note_id)
    
    # Check if current user is the uploader
    if note.uploaded_by != current_user.id:
        flash('You do not have permission to delete this note.', 'error')
        return redirect(url_for('lecturer.dashboard'))
    
    # Delete file from filesystem
    if os.path.exists(note.file_path):
        os.remove(note.file_path)
    
    # Delete from database
    db.session.delete(note)
    db.session.commit()
    
    flash('Lecture note deleted successfully!', 'success')
    return redirect(url_for('lecturer.dashboard'))
