const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const os = require("os");

/**
 * Generates a PDF by injecting data into an HTML template.
 * 
 * @param {string} htmlTemplate - The HTML template with placeholders.
 * @param {Object} data - The dynamic data to replace placeholders.
 * @param {string} outputFilePath - The path where the PDF will be saved.
 */
async function generatePDF(htmlTemplate, data, outputFilePath = "output.pdf") {
    try {
        // Replace placeholders in the HTML template with actual data
        let htmlContent = htmlTemplate;
        for (const key in data) {
            const regex = new RegExp(`{{${key}}}`, "g");
            htmlContent = htmlContent.replace(regex, data[key]);
        }

        // Create a temporary HTML file
        const tempFilePath = path.join(os.tmpdir(), "temp.html");
        fs.writeFileSync(tempFilePath, htmlContent, "utf8");

        // Convert file path to a file:// URL
        const fileUrl = `file://${tempFilePath}`;

        // Launch Puppeteer
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();

        // Navigate to the temp file instead of using setContent
        await page.goto(fileUrl, { waitUntil: "networkidle0", timeout: 60000 });

        // Ensure JavaScript execution is complete
        await page.waitForFunction(() => window.isJSExecuted === true, { timeout: 5000 }).catch(() => {});

        // Generate the PDF with hyperlinks
        await page.pdf({
            path: outputFilePath,
            format: "A4",
            printBackground: true,
            displayHeaderFooter: false,
            preferCSSPageSize: true,
        });

        await browser.close();

        // Cleanup: Delete the temp file
        fs.unlinkSync(tempFilePath);

        console.log(`PDF successfully generated: ${outputFilePath}`);
    } catch (error) {
        console.error("Error generating PDF:", error);
    }
}

// Example HTML Template with Placeholders
const htmlTemplate = `

`;

// Example Data Object
const data = {
    TVS_logo: "logo link",
    Bank_logo: "bank logo link",
    Ticket_no: "123456789",
    Vehicle_Brand: "Audi",
    Vehicle_Model: "M6",
    REGISTRATION_NO: "12345",
    Loan_Account_No: "12345",
    Vehicle_Img: "link for vehicle image",
    rating: "Good or Bad",
    valuation_price: "123456",
    Ex_showroom_price: "123456",
    Resell_value: "12",
    Report_Date: "Date",
    V_DE_DUPE: "V-DE-DUPE +/-",
    val: "score value",
    QR_code_link: "Qr code link",
    Major_Issues: "Issues",
    Remarks: "Additional Remarks",
    color: "vehicle color",
    Fuel_type: "Petrol or deisel",
    Month_Year: "Month and year of purchase",
    no_of_owners: "no of owners",
    Reading: "odometer reading",
    transmission: "manual or automatic",
    vehicle_type: "private",
    insurance: "active or not",
    Owner_Name: "Name of the owner",
    Permanent_Address: "address",
    Financier: "financier",
    Insurer: "Insurer",
    Registration_Number: "Registration Number",
    RTO_Office: "address",
    Serial_No: "Owner Serial No",
    Vehicle_Maker: "maker",
    Couor_of_vehicle: "color",
    Chassis_number: "Chassis Number",
    Engine_Number: "Engine Number",
    Vehicle_Category: "Vehicle Category",
    Vehicle_Class_Description: "Vehicle Class Description",
    Body_Type: "Body Type",
    Mobile_No: "Mobile No",
    Fitness_validity: "date",
    Tax_validity: "RC Tax Validity",
    Policy_No: "Polocy no",
    Insu_Validity: "date",
    Registration_Date: "Registration Date",
    RC_Status: "RC Status",
    Manufacturing_Date: "Manufacturing Date",
    Vehicle_Model: "Vehicle Model",
    Fuel_Type: "Petrol or deisel",
    Fuel_Norms: "norms",
    Cubic_Capacity: "capacity",
    status: "NCRB Status",
    Blacklist_Status: "Blacklist Status",
    NOC_Details: "NOC Details",
    Permit_No: "Permit No",
    Permit_Issue_Date: "Permit Issue Date",
    Permit_valid_from: "date",
    Permit_valid_to: "date",
    Permit_Type: "Permit Type",
    RC_Status_till: "status",
    policy_Number:"numbe",
    Policy_company: "company",
    policy_Period: "period",
    VIDEO_URL: "link",
    Chasis_num_img: "img link",
    Chasis_print_img: "print img",
    selfie_with_vehicle: "img link",
    rc_front: "img link",
    front_side: "img link",
    right_side: "right side",
    back_side: "back_side link",
    left_side: "left_side link",
    engine: "engine img",
    engine_plate: "engine_plate",
    chassis_plate: "chassis_plate",
    odometer_img: "odometer_img link",
    dashboard: "dashboard link",
    seat: "seat img",
    gear_pedal: "gear_pedal img",
    wind_shield: "wind_shield",
    all_boot: "all_boot",
    tyre1: "tyre1 img",
    tyre2: "tyre2 img",
    tyre3: "tyre3 img",
    tyre4: "tyre4 img"
};

// Generate PDF with dynamic data
generatePDF(htmlTemplate, data, "dynamic_output_final.pdf");