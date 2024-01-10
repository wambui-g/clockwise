document.addEventListener('DOMContentLoaded', function() {
    // Login Button
    document.getElementById('loginBtn').addEventListener('click', function() {
        window.location.href = '/login';  // Redirect to the login page
    });

    // Create Account Button
    document.getElementById('createAccountBtn').addEventListener('click', function() {
        window.location.href = '/create-account';  // Redirect to the create account page
    });

    // Request Demo Button
    document.getElementById('requestDemoBtn').addEventListener('click', function() {
        window.location.href = '/request-demo';  // Redirect to the request demo page
    });
});

