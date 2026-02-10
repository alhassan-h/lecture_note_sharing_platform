from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Note
from app.routes.auth import lecturer_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import io

lecturer_bp = Blueprint('lecturer', __name__, url_prefix='/lecturer')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def is_using_supabase():
    """Check if Supabase is configured"""
    return os.environ.get('SUPABASE_URL') and os.environ.get('SUPABASE_KEY')

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
        
        # Determine storage location
        file_path = None
        
        if is_using_supabase():
            # Upload to Supabase Storage
            try:
                from app.supabase_client import upload_to_supabase
                
                # Read file content
                file.seek(0)  # Ensure we're at the start of the file
                file_content = file.read()
                
                # Construct the path in Supabase storage
                supabase_path = f"uploads/{filename}"
                
                # Upload and get the public URL
                file_path = upload_to_supabase(file_content, supabase_path)
                
            except Exception as e:
                flash(f'Failed to upload file to Supabase: {str(e)}', 'error')
                return redirect(url_for('lecturer.upload'))
        else:
            # Save file to local filesystem
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_path = filepath
        
        # Create note record in database
        note = Note(
            course_title=course_title,
            course_code=course_code,
            filename=original_filename,
            file_path=file_path,  # This can be a local path or a Supabase URL
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
    
    # Delete file from storage
    if is_using_supabase():
        # Delete from Supabase Storage
        try:
            from app.supabase_client import delete_from_supabase
            
            # Extract the path from the stored file_path (which may be a full URL)
            # For Supabase URLs like: https://xxx.supabase.co/storage/v1/object/public/lecture-notes/uploads/file.pdf
            # We need to extract: uploads/file.pdf
            if 'supabase.co' in note.file_path:
                # Extract path from Supabase URL
                bucket_name = os.environ.get('SUPABASE_BUCKET_NAME', 'lecture-notes')
                # Find the position after the bucket name
                marker = f'/{bucket_name}/'
                if marker in note.file_path:
                    supabase_path = note.file_path.split(marker)[-1]
                    delete_from_supabase(supabase_path, bucket_name)
        except Exception as e:
            flash(f'Warning: Failed to delete file from Supabase: {str(e)}', 'warning')
    else:
        # Delete from local filesystem
        if os.path.exists(note.file_path):
            os.remove(note.file_path)
