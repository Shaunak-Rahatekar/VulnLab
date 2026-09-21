from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import VULN_MODE
from models import db, Comment

xss_bp = Blueprint('xss', __name__)

@xss_bp.route('/comments', methods=['GET', 'POST'])
def comments():
    vuln_mode = VULN_MODE.get("xss", True)
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        text = request.form.get('comment', '')
        
        if name and text:
            # No server-side sanitization on save in either mode.
            # We strictly treat this XSS as an output-encoding problem.
            new_comment = Comment(name=name, text=text)
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment posted successfully!", "success")
        else:
            flash("Name and comment are required.", "error")
            
        return redirect(url_for('xss.comments'))
        
    # Fetch all comments in reverse chronological order
    all_comments = Comment.query.order_by(Comment.created_at.desc()).all()
    
    return render_template('comments.html', 
                           comments=all_comments, 
                           vuln_mode=vuln_mode)

@xss_bp.route('/search_reflected', methods=['GET'])
def search_reflected():
    # The vulnerability depends purely on the frontend template logic (using | safe).
    # The backend simply reflects the input back to the template.
    query = request.args.get('query', '')
    vuln_mode = VULN_MODE.get("xss", True)
    
    return render_template('search_reflected.html',
                           search_query=query,
                           vuln_mode=vuln_mode)
