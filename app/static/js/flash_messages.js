window.addEventListener('load', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            if (alert.style.opacity === '0') {
                alert.remove();
            }
        }, 2500);
    });
});