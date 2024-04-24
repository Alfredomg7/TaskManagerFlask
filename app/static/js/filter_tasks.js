function filterTasks() {
    try {
        const dropdown = document.getElementById('task-filter-dropdown');
        const filter = dropdown.value;
        const today = new Date().toISOString().split('T')[0];
        const table = document.getElementById('tasks-table');
        const rows = table.getElementsByTagName('tr');

        const startOfWeek = new Date(today);
        startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1);  // Start of the week (Monday)

        const endOfWeek = new Date(today);
        endOfWeek.setDate(startOfWeek.getDate() + 6);

        const startOfMonth = new Date(today);
        startOfMonth.setDate(1);

        const endOfMonth = new Date(today);
        endOfMonth.setMonth(startOfMonth.getMonth() + 1);
        endOfMonth.setDate(0);

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const dueDateCell = row.getElementsByTagName('td')[2]
            
            if (dueDateCell) {
                const dueDate = dueDateCell.textContent.trim();
                let showRow = false;

                switch (filter) {
                    case 'all':
                        showRow = true;
                        break;

                    case 'today':
                        showRow = (dueDate === today);
                        break;
                
                    case 'this-week':
                        showRow = (dueDate >= today && dueDate <= endOfWeek.toISOString().split('T')[0]);
                        break;

                    case 'this-month':
                        showRow = (dueDate >= today && dueDate <= endOfMonth.toISOString().split('T')[0]);
                        break;

                    case 'upcoming':
                        showRow = (dueDate >= today);
                        break;

                    case 'expired':
                        showRow = (dueDate < today);
                        break;
                }
                
                row.style.display = showRow ? '' : 'none';
            }
        } 
    } catch (error) {
            console.log("No dropdown filter");  // Log the error for debugging
        }
}
document.getElementById('task-filter-dropdown').addEventListener('change', filterTasks);