// const axios = require('axios')

// let input = {
//     url:"https://automation.aiqod.com:3333/scrapper/playwright",
//   method: 'POST',
//   headers: { 'Content-Type': 'application/json' },
//   body: '{"input":{"route":[{"_id":"680834c429f6e10eff4ada7f","redBusSource":"Pune","redBusDestination":"nagpur","abhiBusSource":"Pune","abhiBusDestination":"nagpur","paytmBusSource":"Pune","paytmBusDestination":"nagpur","orgId":"67fc8c23deeb69d26c679105","subscriberId":"67fc8c23deeb69d26c679103","userId":"67fc8c23deeb69d26c679107","isDeleted":false,"__v":0,"createdAt":"2025-04-23T00:31:00.104Z","updatedAt":"2025-05-06T06:01:27.560Z"},{"_id":"68195565f80132b867b6cd69","redBusSource":"Pune","redBusDestination":"Chandrapur","abhiBusSource":"Pune","abhiBusDestination":"Chandrapur","paytmBusSource":"Pune","paytmBusDestination":"Chandrapur","orgId":"67fc8c23deeb69d26c679105","subscriberId":"67fc8c23deeb69d26c679103","userId":"67fc8c23deeb69d26c679107","isDeleted":false,"__v":0,"createdAt":"2025-05-06T00:18:45.807Z","updatedAt":"2025-05-06T00:18:45.807Z"}]},"orgId":"67fc8c23deeb69d26c679105","subscriberId":"67fc8c23deeb69d26c679103","userId":"67fc8c23deeb69d26c679107"}'
// }



const axios = require('axios');

let input = {
  url: "https://automation.aiqod.com:3333/scrapper/playwright",
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: {
    input: {
      route: [
        {
          _id: "680834c429f6e10eff4ada7f",
          redBusSource: "Pune",
          redBusDestination: "nagpur",
          abhiBusSource: "Pune",
          abhiBusDestination: "nagpur",
          paytmBusSource: "Pune",
          paytmBusDestination: "nagpur",
          orgId: "67fc8c23deeb69d26c679105",
          subscriberId: "67fc8c23deeb69d26c679103",
          userId: "67fc8c23deeb69d26c679107",
          isDeleted: false,
          __v: 0,
          createdAt: "2025-04-23T00:31:00.104Z",
          updatedAt: "2025-05-06T06:01:27.560Z"
        },
        {
          _id: "68195565f80132b867b6cd69",
          redBusSource: "Pune",
          redBusDestination: "Chandrapur",
          abhiBusSource: "Pune",
          abhiBusDestination: "Chandrapur",
          paytmBusSource: "Pune",
          paytmBusDestination: "Chandrapur",
          orgId: "67fc8c23deeb69d26c679105",
          subscriberId: "67fc8c23deeb69d26c679103",
          userId: "67fc8c23deeb69d26c679107",
          isDeleted: false,
          __v: 0,
          createdAt: "2025-05-06T00:18:45.807Z",
          updatedAt: "2025-05-06T00:18:45.807Z"
        }
      ]
    },
    orgId: "67fc8c23deeb69d26c679105",
    subscriberId: "67fc8c23deeb69d26c679103",
    userId: "67fc8c23deeb69d26c679107"
  }
};


(async () => {
    try {
        let res = await axios.post(input.url, input.body);
        console.log(res.data); // Better to log `res.data` instead of full response
    } catch (e) {
        console.error('Request failed:', e.message);
    }
})();




// (async () => {
//   try {
//     let res = await axios.post(input.url, input.body, { headers: input.headers });
//     console.log(res.data);
//   } catch (e) {
//     console.error('Request failed:', e.message);
//   }
// })();

