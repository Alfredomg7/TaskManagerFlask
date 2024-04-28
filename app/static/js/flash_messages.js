window.addEventListener('load', () => {
    try {
        const alerts = document.querySelectorAll('.alert');
    
        alerts.forEach((alert) => {
            setTimeout(() => {
                if (alert.style.opacity === '0') {
                    alert.remove();
                }
            }, 7000);
        });
    } catch (error) {
        console.log("No alerts messages");
    }
});