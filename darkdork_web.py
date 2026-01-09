#!/usr/bin/env python3
"""
DarkDork Web Application
Modern web-based interface for DarkDork with query builder and library
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Dict, List
import urllib.parse

try:
    from darkdork_library import DorkLibrary
    from darkdork_db import DarkDorkDatabase
    from darkdork_exports import ExportManager
except ImportError:
    DorkLibrary = None
    DarkDorkDatabase = None
    ExportManager = None


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize systems
library = DorkLibrary() if DorkLibrary else None
db = DarkDorkDatabase() if DarkDorkDatabase else None
exporter = ExportManager() if ExportManager else None


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/library/categories')
def get_categories():
    """Get all dork categories with counts"""
    if not library:
        return jsonify({'error': 'Library not available'}), 500

    categories = {}
    for dork in library.dorks:
        cat = dork.get('category', 'Uncategorized')
        categories[cat] = categories.get(cat, 0) + 1

    return jsonify({
        'categories': [
            {'name': cat, 'count': count}
            for cat, count in sorted(categories.items())
        ]
    })


@app.route('/api/library/dorks')
def get_dorks():
    """Get dorks with optional filtering"""
    if not library:
        return jsonify({'error': 'Library not available'}), 500

    category = request.args.get('category')
    severity = request.args.get('severity')
    search = request.args.get('search')
    tags = request.args.getlist('tags')

    dorks = library.search_dorks(
        query=search,
        category=category,
        tags=tags if tags else None,
        severity=severity
    )

    return jsonify({
        'dorks': dorks,
        'total': len(dorks)
    })


@app.route('/api/library/dork/<int:dork_id>')
def get_dork(dork_id):
    """Get specific dork by ID"""
    if not library:
        return jsonify({'error': 'Library not available'}), 500

    dork = library.get_by_id(dork_id)
    if not dork:
        return jsonify({'error': 'Dork not found'}), 404

    return jsonify(dork)


@app.route('/api/builder/build', methods=['POST'])
def build_query():
    """Build a dork query from parameters"""
    data = request.json

    parts = []

    # Site/domain
    if data.get('site'):
        parts.append(f"site:{data['site']}")

    # File type
    if data.get('filetype'):
        parts.append(f"filetype:{data['filetype']}")

    # In title
    if data.get('intitle'):
        if ' ' in data['intitle']:
            parts.append(f'intitle:"{data["intitle"]}"')
        else:
            parts.append(f"intitle:{data['intitle']}")

    # In URL
    if data.get('inurl'):
        parts.append(f"inurl:{data['inurl']}")

    # In text
    if data.get('intext'):
        if ' ' in data['intext']:
            parts.append(f'intext:"{data["intext"]}"')
        else:
            parts.append(f"intext:{data['intext']}")

    # Exact match
    if data.get('exact'):
        parts.append(f'"{data["exact"]}"')

    # Exclude
    if data.get('exclude'):
        for term in data['exclude'].split():
            parts.append(f"-{term}")

    query = ' '.join(parts)
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    return jsonify({
        'query': query,
        'url': search_url
    })


@app.route('/api/execute', methods=['POST'])
def execute_dork():
    """Execute a dork and record in database"""
    data = request.json
    query = data.get('query')
    target = data.get('target')
    project_id = data.get('project_id')

    if not query:
        return jsonify({'error': 'Query required'}), 400

    # Build search URL
    if target:
        query = f"site:{target} {query}"

    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    # Record in database
    search_id = None
    if db:
        search_id = db.record_search(
            query,
            project_id=project_id,
            target_domain=target,
            search_url=search_url
        )

    # Update dork usage statistics
    dork_id = data.get('dork_id')
    if library and dork_id:
        library.update_usage(dork_id)

    return jsonify({
        'query': query,
        'url': search_url,
        'search_id': search_id,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/history')
def get_history():
    """Get search history"""
    if not db:
        return jsonify({'error': 'Database not available'}), 500

    limit = request.args.get('limit', 50, type=int)
    project_id = request.args.get('project_id', type=int)

    searches = db.list_searches(project_id=project_id, limit=limit)

    return jsonify({
        'searches': searches,
        'total': len(searches)
    })


@app.route('/api/projects')
def get_projects():
    """Get all projects"""
    if not db:
        return jsonify({'error': 'Database not available'}), 500

    status = request.args.get('status')
    projects = db.list_projects(status=status)

    return jsonify({
        'projects': projects,
        'total': len(projects)
    })


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    if not db:
        return jsonify({'error': 'Database not available'}), 500

    data = request.json
    project_id = db.create_project(
        data.get('name'),
        data.get('description'),
        data.get('target_domain'),
        data.get('metadata')
    )

    return jsonify({
        'project_id': project_id,
        'message': 'Project created successfully'
    })


@app.route('/api/statistics')
def get_statistics():
    """Get overall statistics"""
    stats = {}

    if library:
        lib_stats = library.get_statistics()
        stats['library'] = lib_stats

    if db:
        db_stats = db.get_statistics()
        stats['database'] = db_stats

        # Get analytics
        analytics = db.get_analytics_summary(days=30)
        stats['analytics'] = analytics

    return jsonify(stats)


@app.route('/api/export', methods=['POST'])
def export_data():
    """Export data in various formats"""
    if not exporter:
        return jsonify({'error': 'Exporter not available'}), 500

    data_dict = request.json
    data = data_dict.get('data', [])
    format_type = data_dict.get('format', 'json')
    title = data_dict.get('title', 'DarkDork Export')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"darkdork_export_{timestamp}.{format_type}"

    success = False

    if format_type == 'json':
        success = exporter.export_to_json(data, filename)
    elif format_type == 'csv':
        success = exporter.export_to_csv(data, filename)
    elif format_type == 'html':
        success = exporter.export_to_html(data, filename, title)
    elif format_type == 'pdf':
        success = exporter.export_to_pdf(data, filename, title)
    elif format_type == 'docx':
        success = exporter.export_to_docx(data, filename, title)
    elif format_type == 'xml':
        success = exporter.export_to_xml(data, filename)
    elif format_type == 'markdown':
        success = exporter.export_to_markdown(data, filename, title)

    if success:
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'error': 'Export failed'}), 500


@app.route('/api/popular')
def get_popular_dorks():
    """Get most popular dorks"""
    if not library:
        return jsonify({'error': 'Library not available'}), 500

    limit = request.args.get('limit', 10, type=int)
    popular = library.get_popular_dorks(limit)

    return jsonify({
        'dorks': popular,
        'total': len(popular)
    })


@app.route('/api/tags')
def get_tags():
    """Get all available tags"""
    if not library:
        return jsonify({'error': 'Library not available'}), 500

    return jsonify({
        'tags': sorted(list(library.tags))
    })


@app.route('/api/search', methods=['POST'])
def search():
    """Search dorks by multiple criteria"""
    if not library:
        return jsonify({'error': 'Library not available'}), 500

    data = request.json
    results = library.search_dorks(
        query=data.get('query'),
        category=data.get('category'),
        tags=data.get('tags'),
        severity=data.get('severity')
    )

    return jsonify({
        'results': results,
        'total': len(results),
        'query': data.get('query')
    })


if __name__ == '__main__':
    # Create library if it doesn't exist
    if library and len(library.dorks) == 0:
        print("Initializing dork library...")
        from darkdork_library import create_comprehensive_library
        library = create_comprehensive_library()
        print(f"Library initialized with {len(library.dorks)} dorks")

    print("="*60)
    print("DarkDork Web Application")
    print("="*60)
    print("\nStarting server...")
    print("URL: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5000)
