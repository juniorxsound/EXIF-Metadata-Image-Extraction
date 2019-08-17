
const apiRequest = require('./api')

const imageSelector = document.getElementById('img_selector')
const imagePreview  = document.getElementById('img_preview')

imageSelector.addEventListener('change', (e) => {
    const file = e.target.files[0]

    // Show the preview of the image
    imagePreview.src = file.path

    // Request the binary stream and hit the API for the exif metadata
    fetch(file.path).then(response => {
        response.blob().then(blob => {
            apiRequest('exif/json', blob).then(res => {
                console.log(res)
            })
        })
    })

})