
const apiRequest = require('./api')

const imageSelector = document.getElementById('img_selector')
const imagePreview  = document.getElementById('img_preview')

imageSelector.addEventListener('change', (e) => {
    const tempPath = event.target.files[0]
    const reader = new FileReader()
    
    // Preview the image and make the api request
    reader.addEventListener('load', () => {
        console.log(event.target.files[0])
        apiRequest('exif/json', reader.result)
            .then(res => {
                res.json().then(obj => {
                    console.log(obj)
                })
            })
            .catch(err => {
                console.error(err)
            })
    }, false);

    reader.readAsDataURL(tempPath)

})