
const apiRequest = require('./api')

const imageSelector = document.getElementById('img_selector')
const imagePreview  = document.getElementById('img_preview')
const depth_preview = document.getElementById('depth_preview')
const logger        = document.getElementById('log_box')

imageSelector.addEventListener('change', (e) => {
    const file = e.target.files[0]
    const fileReader = new FileReader()

    imagePreview.src = file.path

    fileReader.onloadend = (e) => {
        if (depth_preview.src) {
            depth_preview.src = ''
        }

        apiRequest('exif/json', fileReader.result)
            .then(response => {
                const jsonResponse = JSON.parse(response)[0]
                logger.innerHTML = JSON.stringify(jsonResponse)
                // This means that it's an iOS device in portrait mode
                if (jsonResponse.MPImage2 && jsonResponse.DeviceManufacturer === 'Apple Computer Inc.') {
                    apiRequest('exif/depth/iphone', fileReader.result)
                        .then(imgResponse => {
                            const imgObject = JSON.parse(imgResponse)
                            if (imgObject.image) {
                                depth_preview.src = imgObject.image
                            }
                        })
                        .catch(err => {
                            depth_preview.src = ''
                            console.error(err)
                        })
                }
                // Or Google's Pixel in portait mode
                else if (jsonResponse.Data && jsonResponse.DeviceManufacturer === 'Google') {
                    apiRequest('exif/depth/pixel', fileReader.result)
                        .then(imgResponse => {
                            const imgObject = JSON.parse(imgResponse)
                            if (imgObject.image) {
                                depth_preview.src = imgObject.image
                            }
                        })
                        .catch(err => {
                            console.error(err)
                        })
                }
                // Or if we don't have a depth map map clean out the depth preview
                else {
                    depth_preview.src = ''
                }
            })
            .catch(err => {
                console.error(err)
            })
    }
    
    fileReader.readAsDataURL(file)
})