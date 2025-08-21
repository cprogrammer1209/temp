const crypto = require('crypto');

function generateApiKey(length = 64) {
    return crypto.randomBytes(length).toString('hex');
}

// Example usage
const apiKey = generateApiKey(16); 
console.log("Generated API Key:", apiKey);
