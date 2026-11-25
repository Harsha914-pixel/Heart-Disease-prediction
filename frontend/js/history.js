document.addEventListener('DOMContentLoaded', () => {
    fetchHistory();
});

function fetchHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('history-table-body');
            tbody.innerHTML = ''; // clear loading state
            
            if (!Array.isArray(data) || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted py-4">No prediction records found.</td></tr>';
                return;
            }

            data.forEach(row => {
                const tr = document.createElement('tr');
                
                const formattedDate = new Date(row.prediction_date).toLocaleString();
                
                const statusBadge = row.prediction_status === 'Heart Disease Detected'
                    ? `<span class="badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1">Detected</span>`
                    : `<span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">No Disease</span>`;
                
                const probText = row.probability ? `${(row.probability * 100).toFixed(1)}%` : 'N/A';
                const classText = row.predicted_class > 0 ? `Class ${row.predicted_class}` : '0';

                tr.innerHTML = `
                    <td>#${row.id}</td>
                    <td><strong>${escapeHtml(row.patient_name)}</strong></td>
                    <td>${row.age}</td>
                    <td>${escapeHtml(row.gender)}</td>
                    <td>${formattedDate}</td>
                    <td>${statusBadge}</td>
                    <td><span class="badge bg-secondary-subtle text-secondary px-2 py-1">${classText}</span></td>
                    <td>${probText}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary me-1 btn-view" data-id="${row.id}"><i class="fas fa-eye me-1"></i>View</button>
                        <a href="/api/report/${row.id}" class="btn btn-sm btn-primary-custom"><i class="fas fa-download me-1"></i>PDF</a>
                    </td>
                `;

                // Add event listener to view button
                tr.querySelector('.btn-view').addEventListener('click', () => {
                    const inputDataParsed = JSON.parse(row.input_data);
                    const viewData = {
                        id: row.id,
                        prediction: row.prediction_status,
                        class: row.predicted_class,
                        probability: row.probability,
                        patient_name: row.patient_name,
                        age: row.age,
                        gender: row.gender,
                        input_data: inputDataParsed
                    };
                    sessionStorage.setItem('latest_prediction', JSON.stringify(viewData));
                    window.location.href = '/result';
                });

                tbody.appendChild(tr);
            });
        })
        .catch(err => {
            console.error("Error fetching history:", err);
            const tbody = document.getElementById('history-table-body');
            tbody.innerHTML = '<tr><td colspan="9" class="text-center text-danger py-4">Error loading prediction history.</td></tr>';
        });
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}
