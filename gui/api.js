
require('dotenv').config() // Loads process.env enviorment variables

const IsJson = (str) => {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

const hexToBase64 = (str) => {
    return btoa(String.fromCharCode.apply(null, str.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" ")));
}

const request = (route = 'exif/json', img) => {
    return new Promise((resolve, reject) => {
        const req = new XMLHttpRequest()
        req.open('POST', `http://${process.env.HOST}:${process.env.PORT}/${route}`, true)
        req.onerror = (e) => reject(req.statusText)
        req.onloadend = (e) => {
            if (IsJson(req.response)) {
                resolve(JSON.parse(req.response)[0])
            } else {
                resolve(`data:image/jpeg;base64,${hexToBase64(req.response)}`)
            } 
        }

        req.send(img)
    })
    
}

module.exports = request