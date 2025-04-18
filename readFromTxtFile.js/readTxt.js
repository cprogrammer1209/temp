const fs = require('fs');
const { json } = require('stream/consumers');



// Reading file synchronously
try {
  const data = fs.readFileSync('temp.txt', 'utf8');
  const singleLine = data.replace(/\r?\\n/g, '\n'); // Replace newlines with spaces
//   singleLine = JSON.parse(singleLine);
  console.log(singleLine);
  console.log(typeof singleLine);
} catch (err) {
  console.error('Error reading the file:', err);
}
