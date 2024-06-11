document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('prescription', document.getElementById('prescription-upload').files[0]);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const container = document.getElementById('medicine-container');
            container.innerHTML = ''; // Clear previous content
            
            data.medicines.forEach(medicine => {
                const medicineDiv = document.createElement('div');
                medicineDiv.className = 'medicine';
                
                const name = document.createElement('h3');
                name.textContent = medicine;
                medicineDiv.appendChild(name);
                
                const description = document.createElement('p');
                description.textContent = `Recommended Alternatives: ${data.recommendations[medicine].join(', ')}`;
                medicineDiv.appendChild(description);
                
                container.appendChild(medicineDiv);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
