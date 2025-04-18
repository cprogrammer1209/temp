const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const puppeteer = require("puppeteer");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json({ limit: "10mb" })); // Allows sending large HTML content
app.use(cors()); // Enable CORS for external requests

/**
 * Function to generate a PDF from HTML content.
 * @param {string} htmlContent - The HTML content as a string.
 * @param {string} outputFilePath - The path where the PDF will be saved.
 */
async function generatePDF(htmlContent, outputFilePath) {
    try {
        // const browser = await puppeteer.launch({
        //     args: ["--no-sandbox", "--disable-setuid-sandbox"],
        //     headless: "new",
        //     executablePath: "/usr/bin/google-chrome"  // Ensures it uses the installed Chrome
        // });
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();
        await page.setContent(htmlContent, { waitUntil: "networkidle0" });

        await page.pdf({
            path: outputFilePath,
            format: "A4",
            printBackground: true,
            displayHeaderFooter: false,
            preferCSSPageSize: true,
        });

        await browser.close();
        console.log(`✅ PDF successfully generated: ${outputFilePath}`);
    } catch (error) {
        console.error("❌ Error generating PDF:", error);
        throw error;
    }
}

// POST API to Generate PDF
app.post("/generate-pdf", async (req, res) => {
    try {
        const { htmlContent } = req.body;
        console.log(`Running Node.js version: ${process.version}`);
        if (!htmlContent) {
            return res.status(400).json({ error: "Missing htmlContent in request body" });
        }

        const outputFilePath = path.join(__dirname, "output.pdf");
        let temp = await fs.readFileSync(htmlContent, 'utf8');
        await generatePDF(temp, outputFilePath);

        // Send the PDF as a response
        res.download(outputFilePath, "generated.pdf", (err) => {
            if (err) {
                console.error("❌ Error sending file:", err);
                res.status(500).json({ error: "Failed to send PDF file" });
            } else {
                console.log("📩 PDF sent successfully");
                fs.unlinkSync(outputFilePath); // Delete the file after sending
            }
        });

    } catch (error) {
        res.status(500).json({ error: "Error generating PDF", details: error.message });
    }
});

// Start the Server
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});



