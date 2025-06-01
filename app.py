import os
import logging
from flask import Flask, render_template_string, request, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Sample database for storing form submissions (in production, use a real database)
subscriptions = []
messages = []

@app.route('/')
def index():
    """Render the main page of the website."""
    with open("index.html") as f:
        return render_template_string(f.read())

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle newsletter subscription requests."""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            app.logger.error("Invalid subscription data received")
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
        
        email = data['email']
        
        # Validate email (basic validation)
        if not email or '@' not in email:
            app.logger.error(f"Invalid email format: {email}")
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Check if email already exists
        if email in [sub['email'] for sub in subscriptions]:
            app.logger.info(f"Email already subscribed: {email}")
            return jsonify({'success': True, 'message': 'Email already subscribed'})
        
        # Add to subscriptions
        subscriptions.append({'email': email})
        app.logger.info(f"New subscription: {email}")
        
        # In a real application, you might want to:
        # 1. Store this in a database
        # 2. Send a confirmation email
        # 3. Add to a mailing list service
        
        return jsonify({'success': True, 'message': 'Subscription successful'})
    
    except Exception as e:
        app.logger.error(f"Error processing subscription: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions."""
    try:
        data = request.get_json()
        
        if not data:
            app.logger.error("Invalid contact form data received")
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
        
        # Extract form data
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        message_text = data.get('message', '')
        
        # Validate required fields
        if not name or not email or not message_text:
            app.logger.error("Missing required contact form fields")
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Validate email format (basic)
        if '@' not in email:
            app.logger.error(f"Invalid email format in contact form: {email}")
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Add message to storage
        new_message = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message_text
        }
        messages.append(new_message)
        
        app.logger.info(f"New contact form submission from: {name} ({email})")
        
        # In a real application, you might want to:
        # 1. Store this in a database
        # 2. Send an email notification to administrators
        # 3. Send a confirmation email to the user
        
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    
    except Exception as e:
        app.logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5001, debug=True)
