const crypto = require("crypto");

function encrypt(data, password) {
    var cipher = crypto.createCipher('aes-128-cbc', password);
    var new_data = cipher.update(data, 'utf8', 'hex')
    new_data += cipher.final('hex');
    return new_data;
}

function decrypt(data, password) {
    var cipher = crypto.createDecipher('aes-128-cbc', password);
    var new_data = cipher.update(data, 'hex', 'utf8')
    new_data += cipher.final('utf8');
    return new_data;
}


function encrypt(data, password) {
    var cipher = crypto.createCipher('aes-128-cbc', password);
    var new_data = cipher.update(data, 'utf8', 'hex')
    new_data += cipher.final('hex');
    return new_data;
}

function decrypt(data, password) {
    var cipher = crypto.createDecipher('aes-128-cbc', password);
    var new_data = cipher.update(data, 'hex', 'utf8')
    new_data += cipher.final('utf8');
    return new_data;
}

module.exports = {
    encrypt,
    decrypt
}