const axios = require('axios');

const url = 'https://graph.facebook.com/v20.0/466172739909250/messages';
const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer EAAQUxzRaX1oBO0Pty09gjHpm8lBcPCpLl4d0XxZCwlvCpc4dwH9eZAmTtsZB1gjCG3TAyud0YpJDRQrj5IwcxZCIX8qSlkQTBhxShPeKeFyIwFzvHScgZBY4bgKWAVQoMdzo2fQtyyczw89F5jZBkeXJsAKyFnPUVkWffG6fYzlcMXmRAAAnIfTHNqgk3d7hg4mQZDZD',
};

const data = {
    messaging_product: "whatsapp",
    recipient_type: "individual",
    to: "919042456776",
    type: "template",
    template: {
        name: "fleet_compliance_template",
        language: { code: "en_US" },
        components: [
            {
                type: "header",
                parameters: [
                    {
                        type: "document",
                        document: {
                            link: "https://demo-fs.aiqod.com:3443/Fileeca1e580129cfddf5435cc400a7dd92c_Tax4-31-May-2025.pdf"
                        }
                    }
                ]
            },
            {
                type: "body",
                parameters: [
                    { type: "text", text: "Permit Certificate" },
                    { type: "text", text: "MMVDG02291124" },
                    { type: "text", text: "MH12QG3434" },
                    { type: "text", text: "07/03/2025" }
                ]
            },
            {
                type: "button",
                sub_type: "url",
                index: "0",
                parameters: [
                    { type: "text", text: "67ab50a5677b90dd6480af4a" }
                ]
            }
        ]
    }
};

axios.post(url, data, { headers })
    .then(response => {
        console.log('Response:', response.data);
    })
    .catch(error => {
        console.error('Error:', error.response ? error.response.data : error.message);
    });
