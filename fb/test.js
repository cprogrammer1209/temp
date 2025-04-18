const axios = require('axios');

const accessToken = 'EAAS4ha4joZCABO1slpAynA5sE99l0mfJU0jDPUKjWbPH3VK5liqpUsK1ILs9UcdPCTYbORR2GsEOFH9SsNYUjM0lfKohQE8D3HLTZC6qeP8AczPfU2DovZA32w4ZCASqZAZCoKZAXeGcddos106RIfO8EGBbfg7WVgWgoigZBPjBJ9QWHDKpOki1Pq0zsyMvqHjuWcpnlPzkIzVZCN88SXaIYmauIAyIZD'
const pageId = '100044240659241'; // Replace with the Facebook page ID (or page username)

const getPosts = async () => {
  try {
    const response = await axios.get(`https://graph.facebook.com/${pageId}/posts`, {
      params: {
        access_token: accessToken,
        fields: 'id,message,created_time,story,attachments',
        limit: 5 // Number of posts to retrieve
      }
    });
    
    console.log('Posts:', response.data);
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
};

getPosts();
