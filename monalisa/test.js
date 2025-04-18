const axios = require("axios");
const fs = require("fs");

async function fetchData(html) {
  try {
    const response = await axios.post(
      "http://172.168.1.199:3000/generate-pdf",
      { htmlContent: html},
      {
        responseType: "stream", // Ensures the server knows we expect a PDF
      }
    );
    const filePath = "downloaded.pdf"; // Path where the PDF will be saved
    const writer = fs.createWriteStream(filePath);

    response.data.pipe(writer);

    writer.on("finish", () => {
      console.log("✅ PDF downloaded successfully:", filePath);
    });

    writer.on("error", (err) => {
      console.error("❌ Error writing PDF file:", err);
    });

    console.log("📄 PDF downloaded successfully!");
  } catch (error) {
    console.error("Error fetching data:", error.message);
  }
}
html=`
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vehicle Valuation Report</title>
  </head>
  <body
    style="
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f9f9f9;
      color: #333;
    "
  >
    <div
      style="
        max-width: 1000px;
        margin: 20px auto;
        background-color: white;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        overflow: hidden;
      "
    >
      <!-- Header Section -->
      <div
        style="
          background: linear-gradient(135deg, #0066ff 0%, #3b5998 100%);
          padding: 25px;
          color: white;
          display: flex;
          justify-content: space-between;
          align-items: center;
        "
      >
        <div style="display: flex; align-items: center">
          <div style="font-size: 24px; font-weight: bold">
            AUTO<span style="color: #ffa500">ASSIST</span>(<span
              style="color: #ff80ff"
              >Ki</span
            >
            Mobility)
          </div>
        </div>
        <div
          style="
            font-size: 28px;
            font-weight: 800;
            text-align: right;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
          "
        >
          VEHICLE VALUATION REPORT<br />
          <span style="font-size: 20px">FOR PRIVATE VEHICLE</span>
        </div>
      </div>

      <!-- Vehicle Info Banner -->
      <div
        style="
          background-color: #f0f4f8;
          padding: 20px;
          border-bottom: 3px solid #e0e0e0;
          display: flex;
          justify-content: space-between;
          align-items: center;
        "
      >
        <div style="flex: 2">
          <div
            style="
              font-size: 24px;
              font-weight: bold;
              color: #2c3e50;
              margin-bottom: 5px;
            "
          >
            EICHER 10.75 H CWC BUS
          </div>
          <div
            style="
              font-size: 20px;
              font-weight: bold;
              color: #3b5998;
              margin-bottom: 5px;
            "
          >
            Registration: MH12QG3163
          </div>
          <div
            style="
              font-size: 16px;
              color: #666;
              display: flex;
              align-items: center;
            "
          >
            <span
              style="
                background-color: #ffffcc;
                color: #333;
                padding: 2px 8px;
                border-radius: 3px;
                margin-right: 10px;
              "
              >YELLOW</span
            >
            <span
              style="
                background-color: #e6e6e6;
                color: #333;
                padding: 2px 8px;
                border-radius: 3px;
                margin-right: 10px;
              "
              >DIESEL</span
            >
            <span
              style="
                background-color: #e6e6e6;
                color: #333;
                padding: 2px 8px;
                border-radius: 3px;
                margin-right: 10px;
              "
              >2018</span
            >
          </div>
        </div>
        <div style="flex: 1; text-align: right">
          <div
            style="
              background: linear-gradient(135deg, #ffb74d 0%, #ffa000 100%);
              padding: 15px;
              border-radius: 8px;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            "
          >
            <div style="font-size: 18px; color: #333; margin-bottom: 5px">
              Valuation Price:
            </div>
            <div style="font-size: 28px; font-weight: bold; color: #333">
              ₹1,200,000
            </div>
          </div>
        </div>
      </div>

      <!-- Vehicle Details Grid -->
      <div style="padding: 25px">
        <div
          style="text-align: center; position: relative; margin-bottom: 25px"
        >
          <h2
            style="
              font-size: 22px;
              font-weight: bold;
              color: #3b5998;
              margin: 0;
              display: inline-block;
              background-color: white;
              padding: 0 20px;
              position: relative;
              z-index: 1;
            "
          >
            Vehicle Details
          </h2>
          <div
            style="
              height: 2px;
              background-color: #e0e0e0;
              width: 100%;
              position: absolute;
              top: 50%;
              left: 0;
              z-index: 0;
            "
          ></div>
        </div>

        <div
          style="
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
          "
        >
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Color
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              YELLOW
            </div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Fuel Type
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              DIESEL
            </div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Year
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              2018
            </div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Owners
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">1</div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Odometer
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              21,421 mi
            </div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Transmission
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              Automatic
            </div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Vehicle Type
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              Bus (LPV)
            </div>
          </div>
          <div
            style="
              padding: 15px;
              text-align: center;
              background: white;
              border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              border: 1px solid #e0e0e0;
            "
          >
            <div style="color: #777; font-size: 14px; margin-bottom: 5px">
              Insurance
            </div>
            <div style="color: #333; font-weight: bold; font-size: 16px">
              Kotak Mahindra General Insurance
            </div>
          </div>
        </div>

        <!-- VAHAN Details Section -->
        <div style="margin-top: 30px">
          <div
            style="text-align: center; position: relative; margin-bottom: 25px"
          >
            <h2
              style="
                font-size: 22px;
                font-weight: bold;
                color: #3b5998;
                margin: 0;
                display: inline-block;
                background-color: white;
                padding: 0 20px;
                position: relative;
                z-index: 1;
              "
            >
              VAHAN DETAILS
            </h2>
            <div
              style="
                height: 2px;
                background-color: #e0e0e0;
                width: 100%;
                position: absolute;
                top: 50%;
                left: 0;
                z-index: 0;
              "
            ></div>
          </div>

          <table
            style="
              width: 100%;
              border-collapse: collapse;
              margin-bottom: 30px;
              box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
            "
          >
            <tr>
              <th
                style="
                  background-color: #3b5998;
                  color: white;
                  padding: 12px 15px;
                  text-align: left;
                  border: 1px solid #2d4373;
                "
              >
                Variable Name
              </th>
              <th
                style="
                  background-color: #3b5998;
                  color: white;
                  padding: 12px 15px;
                  text-align: left;
                  border: 1px solid #2d4373;
                "
              >
                Value
              </th>
              <th
                style="
                  background-color: #3b5998;
                  color: white;
                  padding: 12px 15px;
                  text-align: left;
                  border: 1px solid #2d4373;
                "
              >
                Variable Name
              </th>
              <th
                style="
                  background-color: #3b5998;
                  color: white;
                  padding: 12px 15px;
                  text-align: left;
                  border: 1px solid #2d4373;
                "
              >
                Value
              </th>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Customer State
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                MH, MAHARASHTRA
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Customer City
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                Pune
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Vehicle Model
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                EICHER 10.75 H CWC BUS
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Vehicle Type
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                Bus (LPV)
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Manufacturing Year
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                2018
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Registration Year
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                2018
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Registration Month
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">02</td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Number of Owner
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">1</td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Fuel Type
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                DIESEL
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                RC Status
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                As per Fitness
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Hypothecation
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0"></td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Chassis
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                MC2A5HRTOJB397556
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Registration Number
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                MH12QG3163
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Color
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                YELLOW
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Owner Name
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                SUDEEP LOGISTICS PVT LTD, M/S. SUDEEP LOGISTICS PVT LTD
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Permanent Address
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                H.NO 4,314, PROGRESSIVE MODEL COLONY, VAIDUWADI, HADAPSA, Pune,
                MH, 411013, SAFALYA BUNGALOW NO - 04 PROGRESSIVE MODEL CO OP
                SOCIETY WAIDWADI HADAPS, Pune 411013, H.NO 4,314, PROGRESSIVE
                MODEL COLONY, VAIDUWADI, HADAPSA, Pune, MH, 411013
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Vehicle Maker
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                VE COMMERCIAL VEHICLES LTD
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Body Type
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                SCHOOL BUS
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Manufacturing Date
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                02-2018
              </td>
              <td
                style="
                  padding: 12px 15px;
                  border: 1px solid #e0e0e0;
                  background-color: #f8f9fa;
                  font-weight: 500;
                  color: #2c3e50;
                "
              >
                Cubic Capacity
              </td>
              <td style="padding: 12px 15px; border: 1px solid #e0e0e0">
                3298.00
              </td>
            </tr>
          </table>
        </div>

        <!-- Vehicle Photos Section -->
        <div style="margin-top: 30px; margin-bottom: 40px">
          <div
            style="text-align: center; position: relative; margin-bottom: 25px"
          >
            <h2
              style="
                font-size: 22px;
                font-weight: bold;
                color: #3b5998;
                margin: 0;
                display: inline-block;
                background-color: white;
                padding: 0 20px;
                position: relative;
                z-index: 1;
              "
            >
              Vehicle Images
            </h2>
            <div
              style="
                height: 2px;
                background-color: #e0e0e0;
                width: 100%;
                position: absolute;
                top: 50%;
                left: 0;
                z-index: 0;
              "
            ></div>
          </div>

          <div
            style="
              display: flex;
              flex-wrap: nowrap;
              justify-content: space-between;
              gap: 15px;
              overflow-x: auto;
              padding: 10px;
            "
          >
            <div style="flex: 1; min-width: 180px; text-align: center">
              <div
                style="
                  border-radius: 8px;
                  overflow: hidden;
                  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                  margin-bottom: 8px;
                  border: 1px solid #e0e0e0;
                "
              >
                <img
                  src="https://liberty-fs.gibots.com:843/staging-pub/Filee72d9b9e8fcff9f315df47ec1580250b_odometer.jpg"
                  alt="Odometer"
                  style="width: 100%; height: auto; display: block"
                />
              </div>
              <span
                style="
                  display: inline-block;
                  background-color: #3b5998;
                  color: white;
                  padding: 8px 15px;
                  border-radius: 4px;
                  font-weight: bold;
                  font-size: 14px;
                  margin-top: 5px;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                "
                >ODOMETER</span
              >
            </div>

            <div style="flex: 1; min-width: 180px; text-align: center">
              <div
                style="
                  border-radius: 8px;
                  overflow: hidden;
                  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                  margin-bottom: 8px;
                  border: 1px solid #e0e0e0;
                "
              >
                <img
                  src="https://liberty-fs.gibots.com:843/staging-pub/Filebe68bef10499d98f746abf67a6294d8d_frontside.jpg"
                  alt="Dashboard"
                  style="width: 100%; height: auto; display: block"
                />
              </div>
              <span
                style="
                  display: inline-block;
                  background-color: #3b5998;
                  color: white;
                  padding: 8px 15px;
                  border-radius: 4px;
                  font-weight: bold;
                  font-size: 14px;
                  margin-top: 5px;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                "
                >SELFIE WITH VEHICLE</span
              >
            </div>

            <div style="flex: 1; min-width: 180px; text-align: center">
              <div
                style="
                  border-radius: 8px;
                  overflow: hidden;
                  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                  margin-bottom: 8px;
                  border: 1px solid #e0e0e0;
                "
              >
                <img
                  src="https://liberty-fs.gibots.com:843/staging-pub/Fileba8aff79739434a196f0260563799ffe_backside.jpg"
                  alt="Seat"
                  style="width: 100%; height: auto; display: block"
                />
              </div>
              <span
                style="
                  display: inline-block;
                  background-color: #3b5998;
                  color: white;
                  padding: 8px 15px;
                  border-radius: 4px;
                  font-weight: bold;
                  font-size: 14px;
                  margin-top: 5px;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                "
                >FRONTSIDE</span
              >
            </div>

            <div style="flex: 1; min-width: 180px; text-align: center">
              <div
                style="
                  border-radius: 8px;
                  overflow: hidden;
                  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                  margin-bottom: 8px;
                  border: 1px solid #e0e0e0;
                "
              >
                <img
                  src="https://liberty-fs.gibots.com:843/staging-pub/File686de4ebaac76444ce3b80dab7d9d83c_backside.jpg"
                  alt="Gear and Pedal"
                  style="width: 100%; height: auto; display: block"
                />
              </div>
              <span
                style="
                  display: inline-block;
                  background-color: #3b5998;
                  color: white;
                  padding: 8px 15px;
                  border-radius: 4px;
                  font-weight: bold;
                  font-size: 14px;
                  margin-top: 5px;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                "
                >BACKSIDE</span
              >
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div
          style="
            text-align: center;
            padding: 20px;
            background-color: #f0f4f8;
            border-top: 1px solid #e0e0e0;
            margin-top: 40px;
          "
        >
          <div style="font-size: 14px; color: #666">
            Vehicle Valuation Report generated by
          </div>
          <div
            style="
              font-size: 18px;
              font-weight: bold;
              color: #3b5998;
              margin-top: 5px;
            "
          >
            AUTO<span style="color: #ffa500">ASSIST</span>(<span
              style="color: #ff80ff"
              >Ki</span
            >
            Mobility)
          </div>
        </div>
      </div>
    </div>
  </body>
</html>

`
console.log(JSON.stringify(html));
// fetchData(html);
