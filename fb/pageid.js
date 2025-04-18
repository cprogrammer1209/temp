const axios = require('axios');

// Replace with your access token and the Facebook page name
const accessToken = 'EAAVb7ciGOKMBO4DEG7ICWNw35yCkp4KWFscgiMh31F4E2RadJOLgwbq99lw6QlDf8ZAp0SaHs7EaRB9qZAZBm4S7PpaaJtIXJQEXWzLmWpOGZBEPHCDiOSq78iotkDYv609ktZAai2fGaG4KqWuZAD96ZAGWRhdJ4hhB5aMQqTGF0NEnVsY6rhCaKg4iQ5KcPIwZBMXC318Fxt6XMIGQCNlCoviRBPePAsEg4xYZD'
const pageName = 'DrLeanaWen';

const url = `https://graph.facebook.com/${pageName}?access_token=${accessToken}`;

axios.get(url)
  .then(response => {
    const pageId = response.data.id;
    console.log(`Page ID for ${pageName}: ${pageId}`);
  })
  .catch(error => {
    console.error('Error fetching page data:', error);
  });
