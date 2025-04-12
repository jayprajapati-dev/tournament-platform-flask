// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    // Add balance form validation
    const addBalanceForm = document.querySelector('form[action*="topup_wallet"]');
    if (addBalanceForm) {
        addBalanceForm.addEventListener('submit', function(e) {
            const amount = parseFloat(this.querySelector('input[name="amount"]').value);
            if (amount <= 0) {
                e.preventDefault();
                alert('Please enter a valid amount greater than 0.');
            }
        });
    }

    // Withdrawal form validation
    const withdrawalForm = document.querySelector('form[action*="request_withdrawal"]');
    if (withdrawalForm) {
        withdrawalForm.addEventListener('submit', function(e) {
            const amount = parseFloat(this.querySelector('input[name="amount"]').value);
            const minAmount = parseFloat(this.querySelector('input[name="amount"]').min);
            const maxAmount = parseFloat(this.querySelector('input[name="amount"]').max);
            
            if (amount < minAmount) {
                e.preventDefault();
                alert(`Minimum withdrawal amount is ₹${minAmount}`);
            } else if (amount > maxAmount) {
                e.preventDefault();
                alert('Insufficient wallet balance');
            }
        });
    }

    // Auto-hide flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Tournament Countdown Timer
function startCountdown(endDate, elementId) {
    const countdownElement = document.getElementById(elementId);
    if (!countdownElement) return;

    const end = new Date(endDate).getTime();
    
    const timer = setInterval(function() {
        const now = new Date().getTime();
        const distance = end - now;
        
        if (distance < 0) {
            clearInterval(timer);
            countdownElement.innerHTML = "Tournament Started!";
            return;
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }, 1000);
}

// Image Preview for Result Submission
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (!preview) return;

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Responsive Table Handling
function makeTableResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    makeTableResponsive();
    
    // Initialize countdown timers
    const countdownElements = document.querySelectorAll('[data-countdown]');
    countdownElements.forEach(element => {
        startCountdown(element.dataset.countdown, element.id);
    });
});

// Main JavaScript file for Tournament Platform

// Handle flash message dismissal
document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        var closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                alert.style.display = 'none';
            });
        }
    });
}); 