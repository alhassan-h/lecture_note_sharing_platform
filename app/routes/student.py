from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models import Note
from app.routes.auth import student_required
import os

student_bp = Blueprint('student', __name__, url_prefix='/student')

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
    
    # Check if file exists
    if not os.path.exists(note.file_path):
        flash('File not found.', 'error')
        return redirect(url_for('student.dashboard'))
    
    try:
        return send_file(
            note.file_path,
            as_attachment=True,
            download_name=note.filename
        )
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('student.dashboard'))
