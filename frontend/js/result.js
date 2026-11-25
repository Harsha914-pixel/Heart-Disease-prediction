document.addEventListener('DOMContentLoaded', () => {
    const rawData = sessionStorage.getItem('latest_prediction');
    if (!rawData) {
        alert("No prediction data found. Redirecting to dashboard.");
        window.location.href = '/dashboard';
        return;
    }

    const data = JSON.parse(rawData);
    
    // Set text values
    document.getElementById('val-name').innerText = data.patient_name;
    document.getElementById('val-age-gender').innerText = `${data.age} / ${data.gender}`;
    document.getElementById('val-bp').innerText = `${data.input_data.trestbps} mm Hg`;
    document.getElementById('val-chol').innerText = `${data.input_data.chol} mg/dl`;
    document.getElementById('val-sugar').innerText = data.input_data.fbs === 1 ? '> 120 mg/dl' : '<= 120 mg/dl';
    document.getElementById('val-hr').innerText = `${data.input_data.thalach} bpm`;

    // Process prediction status and probability
    const resultBox = document.getElementById('result-box');
    const resultStatus = document.getElementById('result-status');
    const resultProb = document.getElementById('result-prob');
    const severityContainer = document.getElementById('result-severity-container');
    const severityClass = document.getElementById('result-severity-class');

    const hasDisease = data.class > 0;
    
    if (hasDisease) {
        resultBox.className = "result-box detected";
        resultStatus.innerText = "Heart Disease Detected";
        severityContainer.classList.remove('d-none');
        severityClass.innerText = `Class ${data.class}`;
    } else {
        resultBox.className = "result-box no-disease";
        resultStatus.innerText = "No Heart Disease";
        severityContainer.classList.add('d-none');
    }

    if (data.probability !== null) {
        resultProb.innerText = `${(data.probability * 100).toFixed(1)}%`;
    } else {
        resultProb.innerText = "N/A";
    }

    // Set up PDF download button
    const downloadBtn = document.getElementById('download-pdf-btn');
    downloadBtn.addEventListener('click', () => {
        window.location.href = `/api/report/${data.id}`;
    });
});
