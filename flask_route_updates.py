
# Add these routes to your Flask app for enhanced UX features

@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

# Enhanced error handlers with better UX
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
