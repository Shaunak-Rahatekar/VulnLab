from flask import Blueprint, render_template, request
from sqlalchemy import text
from config import VULN_MODE
from models import db, Product

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    columns = []
    results = []
    
    if query:
        if VULN_MODE.get("sqli", True):
            # VULNERABLE MODE
            # Vulnerable to UNION-Based SQL Injection
            # The query dynamically fetches whatever columns the SQL engine returns
            sql = f"SELECT name, price, description FROM products WHERE name LIKE '%{query}%'"
            
            # Execute raw SQL directly
            result_proxy = db.session.execute(text(sql))
            
            # Fetch dynamic column headers and rows (allows UNION to inject different columns seamlessly)
            columns = list(result_proxy.keys())
            results = result_proxy.fetchall()
            
        else:
            # PATCHED MODE
            # Use SQLAlchemy ORM with parameterized queries
            products = Product.query.filter(Product.name.contains(query)).all()
            
            # Format explicitly for the generic table
            columns = ['name', 'price', 'description']
            for p in products:
                results.append([p.name, p.price, p.description])

    return render_template('search.html', 
                           search_query=query, 
                           columns=columns, 
                           results=results,
                           vuln_mode=VULN_MODE.get("sqli", True))
