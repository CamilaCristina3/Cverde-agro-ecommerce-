// Login Page Scripts - Optimized

(function() {
    'use strict';

    // Cache frequently accessed DOM elements
    const toggleBtn = document.querySelector('.toggle-password');
    const passwordField = document.querySelector('#id_password');
    const deleteButtons = document.querySelectorAll('.notification .delete');

    // Event delegation for notification close buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete')) {
            const notification = e.target.closest('.notification');
            if (notification) {
                notification.remove();
            }
        }
    });

    // Toggle password visibility - with early return
    if (toggleBtn && passwordField) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const isPassword = passwordField.type === 'password';
            passwordField.type = isPassword ? 'text' : 'password';
            
            // Update icon efficiently
            toggleBtn.innerHTML = isPassword ? 
                '<i class="fas fa-eye-slash"></i>' : 
                '<i class="fas fa-eye"></i>';
        });
    }

    // Focus effects with CSS class (define in CSS for better performance)
    const inputFields = document.querySelectorAll('input[type="text"], input[type="password"], input[type="email"]');
    
    inputFields.forEach(input => {
        input.addEventListener('focus', function() {
            this.classList.add('is-focused');
        });
        
        input.addEventListener('blur', function() {
            this.classList.remove('is-focused');
        });
    });
})();
