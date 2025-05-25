document.addEventListener('DOMContentLoaded', function() {
    // Navigation scroll effect
    const navbar = document.querySelector('.navbar');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.navbar-menu');
    const navLinks = document.querySelectorAll('.navbar-menu a');
    
    // Navbar background change on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    });
    
    // Close mobile menu when clicking a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            document.body.classList.remove('no-scroll');
        });
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Form validation
    const contactForm = document.getElementById('contactForm');
    const subscriptionForm = document.getElementById('subscriptionForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');
            let isValid = true;
            
            // Reset error messages
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            
            // Validate name
            if (!name.value.trim()) {
                displayError(name, 'Name is required');
                isValid = false;
            }
            
            // Validate email
            if (!validateEmail(email.value.trim())) {
                displayError(email, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate message
            if (!message.value.trim()) {
                displayError(message, 'Message is required');
                isValid = false;
            }
            
            if (isValid) {
                // Submit the form data using Fetch API
                fetch('/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: name.value.trim(),
                        email: email.value.trim(),
                        phone: document.getElementById('phone').value.trim(),
                        message: message.value.trim()
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        contactForm.reset();
                        showAlert('Thank you! Your message has been sent successfully.', 'success');
                    } else {
                        showAlert('There was a problem sending your message. Please try again.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('There was a problem sending your message. Please try again.', 'error');
                });
            }
        });
    }
    
    if (subscriptionForm) {
        subscriptionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const subscribeEmail = document.getElementById('subscribeEmail');
            let isValid = true;
            
            // Reset error messages
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            
            // Validate email
            if (!validateEmail(subscribeEmail.value.trim())) {
                displayError(subscribeEmail, 'Please enter a valid email address');
                isValid = false;
            }
            
            if (isValid) {
                // Submit the subscription form data
                fetch('/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: subscribeEmail.value.trim()
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        subscriptionForm.reset();
                        showAlert('Thank you for subscribing!', 'success');
                    } else {
                        showAlert('There was a problem with your subscription. Please try again.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('There was a problem with your subscription. Please try again.', 'error');
                });
            }
        });
    }
    
    // Helper functions
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
    
    function displayError(inputElement, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = '#e74c3c';
        errorDiv.style.fontSize = '0.9rem';
        errorDiv.style.marginTop = '5px';
        errorDiv.textContent = message;
        
        inputElement.parentNode.appendChild(errorDiv);
        inputElement.style.borderColor = '#e74c3c';
        
        // Remove error when input changes
        inputElement.addEventListener('input', function() {
            errorDiv.remove();
            inputElement.style.borderColor = '';
        });
    }
    
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert ' + type;
        alertDiv.textContent = message;
        
        // Style the alert
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.padding = '15px 30px';
        alertDiv.style.borderRadius = '5px';
        alertDiv.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        alertDiv.style.zIndex = '9999';
        
        if (type === 'success') {
            alertDiv.style.backgroundColor = '#2ecc71';
            alertDiv.style.color = '#fff';
        } else {
            alertDiv.style.backgroundColor = '#e74c3c';
            alertDiv.style.color = '#fff';
        }
        
        document.body.appendChild(alertDiv);
        
        // Remove the alert after 5 seconds
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            alertDiv.style.transition = 'opacity 0.5s';
            setTimeout(() => {
                alertDiv.remove();
            }, 500);
        }, 5000);
    }
});
