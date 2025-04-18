const CryptoJS = require('crypto-js');

const password = "Welcome@123";

const secretKey = "bf3c199c2470cb477d907b1e0917c17b";

const encryptedPassword = CryptoJS.AES.encrypt(JSON.stringify(password), secretKey).toString();

console.log("Encrypted Password:", encryptedPassword);

const decryptedBytes = CryptoJS.AES.decrypt(encryptedPassword, secretKey);
const decryptedPassword = decryptedBytes.toString(CryptoJS.enc.Utf8);

console.log("Decrypted Password:", decryptedPassword);
