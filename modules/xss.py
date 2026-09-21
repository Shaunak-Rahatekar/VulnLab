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
