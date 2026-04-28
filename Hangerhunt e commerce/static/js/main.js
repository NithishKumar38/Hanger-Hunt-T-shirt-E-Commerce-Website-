// Handle dynamic display of file names on file input change
document.addEventListener("DOMContentLoaded", () => {
    
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const label = this.nextElementSibling;
            
            if (fileName && label) {
                // Keep original text but add filename
                if (!label.dataset.originalText) {
                    label.dataset.originalText = label.innerText;
                }
                label.innerText = `Selected: ${fileName}`;
                label.style.borderColor = 'var(--accent)';
                label.style.color = 'var(--accent)';
            }
        });
    });

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => alert.remove(), 500);
            });
        }, 3000);
    }
});
