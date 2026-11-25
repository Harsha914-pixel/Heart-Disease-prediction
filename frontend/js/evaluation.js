document.addEventListener('DOMContentLoaded', () => {
    fetchEvaluationData();
});

function fetchEvaluationData() {
    fetch('/api/evaluation')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Evaluation metrics not found. Please train models first.");
                return;
            }

            // Populate general info
            document.getElementById('val-dataset-size').innerText = data.dataset_size;
            document.getElementById('val-train-samples').innerText = data.training_samples;
            document.getElementById('val-test-samples').innerText = data.testing_samples;
            document.getElementById('val-selected-model').innerText = data.selected_algorithm;

            // Render table
            const tbody = document.getElementById('evaluation-table-body');
            tbody.innerHTML = '';

            const performances = data.model_performances;
            for (const [modelName, metrics] of Object.entries(performances)) {
                const tr = document.createElement('tr');
                const isSelected = modelName === data.selected_algorithm;
                
                if (isSelected) {
                    tr.className = "table-primary fw-medium";
                }

                tr.innerHTML = `
                    <td>
                        ${modelName} 
                        ${isSelected ? '<span class="badge bg-primary ms-2">Active</span>' : ''}
                    </td>
                    <td>${(metrics.accuracy * 100).toFixed(2)}%</td>
                    <td>${(metrics.precision * 100).toFixed(2)}%</td>
                    <td>${(metrics.recall * 100).toFixed(2)}%</td>
                    <td>${(metrics.f1_score * 100).toFixed(2)}%</td>
                `;
                tbody.appendChild(tr);
            }
        })
        .catch(err => {
            console.error("Error loading evaluation stats:", err);
            const tbody = document.getElementById('evaluation-table-body');
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger py-4">Error loading evaluation metrics.</td></tr>';
        });
}
