document.addEventListener('DOMContentLoaded', function() {
    // Set copyright year
    document.getElementById('copyright-year').textContent = new Date().getFullYear();
    
    // Demo modal functionality
    const demoButton = document.getElementById('demoButton');
    const playButton = document.querySelector('.play-button');
    const demoModal = document.getElementById('demoModal');
    const closeModal = document.querySelector('.close-modal');
    const videoPlaceholder = document.getElementById('videoPlaceholder');
    
    if (demoModal) {
        // Add animation class to demo button
        if (demoButton) {
            demoButton.classList.add('pulse-animation');
        }
        
        // Add animation and click functionality to play button in demo preview
        if (playButton) {
            // Animate play button on hover
            playButton.addEventListener('mouseover', function() {
                this.style.transform = 'scale(1.1)';
                this.style.backgroundColor = 'rgba(243, 156, 18, 1)';
            });
            
            playButton.addEventListener('mouseout', function() {
                this.style.transform = 'scale(1)';
                this.style.backgroundColor = 'rgba(243, 156, 18, 0.9)';
            });
            
            // Open modal when play button is clicked
            playButton.addEventListener('click', function() {
                openVideoModal();
            });
        }
        
        // Animate button on hover
        demoButton.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        demoButton.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
        
        // Function to open video modal with animation
        function openVideoModal() {
            demoModal.style.display = 'block';
            setTimeout(() => {
                demoModal.style.opacity = '1';
            }, 10);
            document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
            
            // Simulate loading a video
            if (videoPlaceholder) {
                videoPlaceholder.innerHTML = '<div class="loading-animation"><div></div><div></div><div></div><div></div></div><p>Loading presentation...</p>';
                
                // After a delay, show the video placeholder (in a real scenario, this would be where you'd embed the actual video)
                setTimeout(() => {
                    videoPlaceholder.innerHTML = `
                        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#f39c12" stroke-width="2"/>
                            <path d="M10 8L16 12L10 16V8Z" fill="#f39c12"/>
                        </svg>
                        <p style="margin-top: 20px; font-size: 1.2rem;"><span style="color: #f39c12;">Future</span><span style="color: #27AE60;">Data</span><span style="color: #2980b9;">AI</span> Product Demo</p>
                        <p style="margin-top: 10px; font-size: 0.9rem; max-width: 80%; text-align: center;">
                            This is where your product demonstration video would appear. For a personalized demo tailored to your business needs, please contact our team.
                        </p>
                    `;
                }, 1500);
            }
        }
        
        // Open modal when demo button is clicked
        if (demoButton) {
            demoButton.addEventListener('click', function() {
                openVideoModal();
            });
        }
        
        // Close modal with fade out animation
        const closeModalWithAnimation = () => {
            demoModal.style.opacity = '0';
            setTimeout(() => {
                demoModal.style.display = 'none';
                document.body.style.overflow = ''; // Restore scrolling
                // Reset the video placeholder for next time
                if (videoPlaceholder) {
                    videoPlaceholder.innerHTML = `
                        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#f39c12" stroke-width="2"/>
                            <path d="M10 8L16 12L10 16V8Z" fill="#f39c12"/>
                        </svg>
                        <p style="margin-top: 20px; font-size: 1.2rem;">Future Data AI Product Demo</p>
                        <p style="margin-top: 10px; font-size: 0.9rem; max-width: 80%; text-align: center;">
                            This is where your product demonstration video would appear. For a personalized demo tailored to your business needs, please contact our team.
                        </p>
                    `;
                }
            }, 300);
        };
        
        // Close modal when X is clicked
        if (closeModal) {
            closeModal.addEventListener('click', closeModalWithAnimation);
        }
        
        // Close modal when clicking outside of it
        window.addEventListener('click', function(event) {
            if (event.target === demoModal) {
                closeModalWithAnimation();
            }
        });
        
        // Close modal when ESC key is pressed
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && demoModal.style.display === 'block') {
                closeModalWithAnimation();
            }
        });
    }
    
    // Form validation for subscription form
    const subscriptionForm = document.getElementById('subscriptionForm');
    if (subscriptionForm) {
        subscriptionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('subscribeEmail').value.trim();
            if (!validateEmail(email)) {
                showError(document.getElementById('subscribeEmail'), 'Please enter a valid email address');
                return;
            }
            
            // Submit the form data
            fetch('/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    subscriptionForm.reset();
                    showAlert('Thank you for subscribing!', 'success');
                } else {
                    showAlert(data.message || 'There was a problem with your subscription. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('There was a problem with your subscription. Please try again.', 'error');
            });
        });
    }
    
    // Form validation for contact form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            let isValid = true;
            
            // Reset previous errors
            clearErrors();
            
            // Validate name
            if (!name) {
                showError(document.getElementById('name'), 'Name is required');
                isValid = false;
            }
            
            // Validate email
            if (!validateEmail(email)) {
                showError(document.getElementById('email'), 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate message
            if (!message) {
                showError(document.getElementById('message'), 'Message is required');
                isValid = false;
            }
            
            if (isValid) {
                // Submit the form data
                fetch('/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: name,
                        email: email,
                        phone: document.getElementById('phone').value.trim(),
                        message: message
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        contactForm.reset();
                        showAlert('Thank you! Your message has been sent successfully.', 'success');
                    } else {
                        showAlert(data.message || 'There was a problem sending your message. Please try again.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('There was a problem sending your message. Please try again.', 'error');
                });
            }
        });
    }
    
    // Helper functions
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
    
    function showError(inputElement, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = '#e74c3c';
        errorDiv.style.fontSize = '0.8rem';
        errorDiv.style.marginTop = '-0.5rem';
        errorDiv.style.marginBottom = '1rem';
        errorDiv.textContent = message;
        
        inputElement.style.borderColor = '#e74c3c';
        inputElement.parentNode.insertBefore(errorDiv, inputElement.nextSibling);
        
        // Remove error when input changes
        inputElement.addEventListener('input', function() {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
            inputElement.style.borderColor = '';
        }, { once: true });
    }
    
    function clearErrors() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(error => error.remove());
        
        const inputs = document.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.style.borderColor = '';
        });
    }
    
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert';
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
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 500);
        }, 5000);
    }
});