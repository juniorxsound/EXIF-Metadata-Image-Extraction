
require('dotenv').config() // Loads process.env enviorment variables

const request = (route = 'exif/json', img) => {
    // Create the form and append the image file
    const formData  = new FormData()
    formData.append('file', img)
    
    // Make the request
    return fetch(`http://${process.env.HOST}:${process.env.PORT}/${route}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        body: formData
    })
} 

module.exports = request