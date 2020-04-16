
require('dotenv').config() // Loads process.env enviorment variables

/**
 * An XML HTTP Request Promise wrapper
 * @param {String} route - What is the route this request should be made to? (default is `exif/json`)
 * @param {String} img - Base64 encoded img string
 * @param {String} method - What request method should be used (default is POST)
 * @returns {Promise} promise
 */
module.exports = (route = 'exif/json', img, method = 'POST') => {
    if (!img) {
        console.error('Must provide an img argument to make a request')
        return
    }

    return new Promise((resolve, reject) => {
        const req = new XMLHttpRequest()
        req.open(method, `http://${process.env.HOST}:${process.env.PORT}/${route}`, true)
        req.setRequestHeader('Content-Type', 'application/json')

        req.onerror = (e) => reject(req.statusText)
        req.onloadend = (e) => resolve(req.response)

        req.send(JSON.stringify({
            'image': img
        }))
    })
}
