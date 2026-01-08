document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const imagePreview = document.getElementById('imagePreview');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const results = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const submitBtn = document.getElementById('submitBtn');

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                imagePreview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
            };
            reader.readAsDataURL(file);
        }
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        results.style.display = 'none';
        errorDiv.style.display = 'none';
        
        loadingSpinner.style.display = 'block';
        submitBtn.disabled = true;
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            loadingSpinner.style.display = 'none';
            submitBtn.disabled = false;
            
            if (response.ok && data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred');
            }
            
        } catch (error) {
            loadingSpinner.style.display = 'none';
            submitBtn.disabled = false;
            showError('Network error: ' + error.message);
        }
    });

    function displayResults(data) {
        results.style.display = 'block';
        
        document.getElementById('resultImage').src = `/static/results/${data.result_image}`;
        
        document.getElementById('totalDetections').textContent = data.total_detections;
        
        const detectedFruitsDiv = document.getElementById('detectedFruits');
        detectedFruitsDiv.innerHTML = '';
        
        for (const [fruit, count] of Object.entries(data.class_counts)) {
            detectedFruitsDiv.innerHTML += `
                <div class="fruit-item">
                    <span>${fruit}</span>
                    <span><strong>${count}</strong></span>
                </div>
            `;
        }
        
        const predictionsListDiv = document.getElementById('predictionsList');
        predictionsListDiv.innerHTML = '';
        
        data.predictions.forEach((pred, index) => {
            const confidence = (pred.confidence * 100).toFixed(1);
            predictionsListDiv.innerHTML += `
                <div class="prediction-item">
                    <span class="prediction-class">${index + 1}. ${pred.class}</span>
                    <span class="prediction-confidence">${confidence}%</span>
                </div>
            `;
        });
        
        results.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }
});