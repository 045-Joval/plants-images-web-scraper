let controller = null; // Variable to store the AbortController instance

function getImages() {
    const query = document.getElementById('query').value;
    const licenseType = document.getElementById('licenseType').value;
    const numOfImages = document.getElementById('numOfImages').value;
    const imageWidth = document.getElementById('imageWidth').value;
    const imageHeight = document.getElementById('imageHeight').value;

    // Abort the existing request if it exists
    if (controller) {
        controller.abort();
    }

    // Create a new AbortController instance
    controller = new AbortController();

    // Show loading animation
    document.getElementById('loading').style.display = 'block';

    // Clear the existing images
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    // Fetch new images
    fetch('http://127.0.0.1:5000/api/getimages', {
        method: 'POST',
        signal: controller.signal,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query,
            license_type: parseInt(licenseType),
            number_of_images: parseInt(numOfImages),
            image_width: parseInt(imageWidth),
            image_height: parseInt(imageHeight),
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.length > 0) {
            data.forEach(item => {
                const imgElement = document.createElement('img');
                imgElement.src = `${item[0]}?${Date.now()}`; // Append a unique query parameter to the image URL
                imgElement.alt = 'Image';
                resultDiv.appendChild(imgElement);

                const jsonLink = document.createElement('a');
                jsonLink.href = item[1]; // JSON path
                jsonLink.target = '_blank';
                resultDiv.appendChild(jsonLink);

                resultDiv.appendChild(document.createElement('br'));
            });
        } else {
            resultDiv.innerText = 'No images found.';
        }

        // Hide loading animation
        document.getElementById('loading').style.display = 'none';
    })
    .catch(error => {
        // Check if the error is due to the request being aborted
        if (error.name !== 'AbortError') {
            console.error('Error:', error);
        }

        // Hide loading animation in case of an error
        document.getElementById('loading').style.display = 'none';
    });
}



function cancelRequest() {
    // Abort the request if it exists
    if (controller) {
        controller.abort();
        controller = null;
        document.getElementById('loading').style.display = 'none';
    }
}
