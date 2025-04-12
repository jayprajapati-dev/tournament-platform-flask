from app import create_app
import os

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Ensure the static and templates directories exist
    os.makedirs('app/static', exist_ok=True)
    os.makedirs('app/templates', exist_ok=True)
    os.makedirs('app/static/css', exist_ok=True)
    os.makedirs('app/static/js', exist_ok=True)
    
    # Run the application in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000) 