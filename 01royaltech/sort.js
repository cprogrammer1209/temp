const { CURSOR_FLAGS } = require("mongodb");

function sortObjectByKeys(obj) {
  return Object.keys(obj)
    .sort() // Default is lexicographical sort
    .reduce((acc, key) => {
      acc[key] = obj[key];
      return acc;
    }, {});
}

let data =


  {
          "InvoiceSlNo": 1,
          "itemSlNo": 1,
          "ItemDesc": "0900815167 O-ring 90x8 EPDM peroxide",
          "Quantity": "1",
          "Rate": "20,00",
          "Amount": "20,00",
          "PartNo": null,
          "PONumber": null,
          "ItemNETWEIGHT": null,
          "ItemHSCODE": "401693",
          "ItemCountry": "JP"
        }

console.log(sortObjectByKeys(data));
