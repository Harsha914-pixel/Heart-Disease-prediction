document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoader = document.getElementById('btn-loader');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Custom check validity
        if (!form.checkValidity()) {
            e.stopPropagation();
            form.classList.add('was-validated');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        btnText.innerText = "Processing...";
        btnLoader.classList.remove('d-none');

        // Build Payload
        const payload = {
            patient_name: document.getElementById('patient_name').value,
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            cp: parseInt(document.getElementById('cp').value),
            trestbps: parseFloat(document.getElementById('trestbps').value),
            chol: parseFloat(document.getElementById('chol').value),
            fbs: parseInt(document.getElementById('fbs').value),
            restecg: parseInt(document.getElementById('restecg').value),
            thalach: parseFloat(document.getElementById('thalach').value),
            exang: parseInt(document.getElementById('exang').value),
            oldpeak: parseFloat(document.getElementById('oldpeak').value),
            slope: parseInt(document.getElementById('slope').value),
            ca: parseInt(document.getElementById('ca').value),
            thal: parseInt(document.getElementById('thal').value)
        };

        // Post request to prediction endpoint
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.error || "Server Error"); });
            }
            return response.json();
        })
        .then(data => {
            // Save response to sessionStorage to display on result page
            sessionStorage.setItem('latest_prediction', JSON.stringify({
                ...data,
                patient_name: payload.patient_name,
                age: payload.age,
                gender: payload.gender,
                input_data: payload
            }));
            
            // Redirect to result page
            window.location.href = '/result';
        })
        .catch(err => {
            alert("Error: " + err.message);
            // Restore button state
            submitBtn.disabled = false;
            btnText.innerHTML = '<i class="fas fa-heartbeat me-2"></i>Predict';
            btnLoader.classList.add('d-none');
        });
    });
});
