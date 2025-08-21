const XLSX = require('xlsx');
const fs = require('fs');

// The JSON data (already provided)
const jsonData = {
  "Pune to Nagpur": [
    { "time": "4.00pm", "ratings": { "Redbus": 3.7, "Paytm": 4.1, "AbhiBus": 4.8 } },
    { "time": "5.00pm", "ratings": { "Redbus": 4.2, "Paytm": 3.8, "AbhiBus": 4.8 } },
    { "time": "6.00pm", "ratings": { "Redbus": 4.2, "Paytm": 3.5, "AbhiBus": 4.8 } },
    { "time": "6.30pm", "ratings": { "Redbus": 4.2, "Paytm": 3.5, "AbhiBus": 4.8 } },
    { "time": "7.00pm", "ratings": { "Redbus": 3.9, "Paytm": 3.5, "AbhiBus": 4.8 } },
    { "time": "7.30pm", "ratings": { "Redbus": 3.7, "Paytm": 3.5, "AbhiBus": 4.8 } },
    { "time": "8.00pm", "ratings": { "Redbus": 3.9, "Paytm": 3.5, "AbhiBus": 4.8 } },
    { "time": "9.00pm", "ratings": { "Redbus": 3.8, "Paytm": 3.4, "AbhiBus": 4.8 } },
    { "time": "10.00pm", "ratings": { "Redbus": 3.2, "Paytm": 2.8, "AbhiBus": 4.8 } }
  ],
  "Pune to Chandrapur": [
    { "time": "5.00pm", "ratings": { "Redbus": 4.0, "Paytm": 3.6, "AbhiBus": 4.8 } },
    { "time": "6.00pm", "ratings": { "Redbus": 4.2, "Paytm": 3.4, "AbhiBus": 4.8 } },
    { "time": "7.00pm", "ratings": { "Redbus": 3.9, "Paytm": 3.2, "AbhiBus": 4.8 } }
  ],
  "Pune to Amravati": [
    { "time": "8.00pm", "ratings": { "Redbus": 4.0, "Paytm": 3.4, "AbhiBus": 4.8 } }
  ],
  "Pune to Akola": [
    { "time": "9.00pm", "ratings": { "Redbus": 3.4, "Paytm": 2.7, "AbhiBus": 4.8 } }
  ],
  "Pune to Nanded": [
    { "time": "9.00pm", "ratings": { "Redbus": 3.8, "Paytm": 3.2, "AbhiBus": 4.8 } },
    { "time": "10.00pm", "ratings": { "Redbus": 3.6, "Paytm": 3.2, "AbhiBus": 4.8 } }
  ],
  "Pune to Dhule": [
    { "time": "10.00pm", "ratings": { "Redbus": 3.9, "Paytm": 3.6, "AbhiBus": 4.8 } }
  ],
  "Dhule to Pune": [
    { "time": "9.15pm", "ratings": { "Redbus": 3.9, "Paytm": 3.5, "AbhiBus": 4.8 } }
  ],
  "Pune to Goa": [
    { "time": "10.30pm", "ratings": { "Redbus": 3.9, "Paytm": 3.7, "AbhiBus": 4.8 } }
  ],
  "Pune to Ujjain": [
    { "time": "7.00pm", "ratings": { "Redbus": 3.9, "Paytm": 3.5, "AbhiBus": 4.8 } }
  ],
  "Pune to Indore": [
    { "time": "7.45pm", "ratings": { "Redbus": 3.7, "Paytm": 3.5, "AbhiBus": 4.8 } }
  ]
};

// Prepare sheet data
const sheetData = [];
Object.keys(jsonData).forEach(route => {
  jsonData[route].forEach(item => {
    sheetData.push({
      Route: route,
      Time: item.time,
      Redbus_Rating: item.ratings.Redbus,
      Paytm_Rating: item.ratings.Paytm,
      AbhiBus_Rating: item.ratings.AbhiBus
    });
  });
});

// Convert JSON data to worksheet
const ws = XLSX.utils.json_to_sheet(sheetData);

// Create a new workbook with the worksheet
const wb = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(wb, ws, 'Bus Ratings');

// Write the Excel file to disk
XLSX.writeFile(wb, 'bus_ratings.xlsx');
