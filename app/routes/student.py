from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from app.models import Note
from app.routes.auth import student_required
import os
import io

student_bp = Blueprint('student', __name__, url_prefix='/student')

def is_using_supabase():
    """Check if Supabase is configured"""
    return os.environ.get('SUPABASE_URL') and os.environ.get('SUPABASE_KEY')

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard - list and download notes"""
    page = request.args.get('page', 1, type=int)
    search_course = request.args.get('search', '', type=str).strip()
    
    query = Note.query
    
    # Filter by course code if search term provided
    if search_course:
        query = query.filter(
            (Note.course_code.ilike(f'%{search_course}%')) |
            (Note.course_title.ilike(f'%{search_course}%'))
        )
    
    notes = query.order_by(Note.upload_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('student_dashboard.html', notes=notes, search_course=search_course)

@student_bp.route('/download/<int:note_id>')
@login_required
@student_required
def download_note(note_id):
    """Download a lecture note"""
    note = Note.query.get_or_404(note_id)
    
    try:
        if is_using_supabase():
            # Download from Supabase Storage
            from app.supabase_client import download_from_supabase
            
            # Extract the path from the stored file_path (which may be a full URL)
            if 'supabase.co' in note.file_path:
                # Extract path from Supabase URL
                bucket_name = os.environ.get('SUPABASE_BUCKET_NAME', 'lecture-notes')
                marker = f'/{bucket_name}/'
                if marker in note.file_path:
                    supabase_path = note.file_path.split(marker)[-1]
                    file_content = download_from_supabase(supabase_path, bucket_name)
                    
                    # Return the file as an attachment
                    return send_file(
                        io.BytesIO(file_content),
                        as_attachment=True,
                        download_name=note.filename
                    )
            
            # If we couldn't extract the path, try to use the URL directly
            # This shouldn't normally happen, but fall back to the URL
            flash('File path format unexpected. Please contact support.', 'error')
            return redirect(url_for('student.dashboard'))
        else:
            # Download from local filesystem
            if not os.path.exists(note.file_path):
                flash('File not found.', 'error')
                return redirect(url_for('student.dashboard'))
            
            return send_file(
                note.file_path,
                as_attachment=True,
                download_name=note.filename
            )
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('student.dashboard'))
