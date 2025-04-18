 pdfConverter(input, output, botId, projectId, iterationId) {
    try {

        const util = require('util');
        const exec = util.promisify(require('child_process').exec);
        const ExcelJS = require('exceljs123');
                
        // let filePath = input.filePath;
        let filePath = input.fileArr[iterationId].filePath
        let extractedFilePath = filePath.substring(0,filePath.lastIndexOf('/'))
        let fileName = filePath.substring(filePath.lastIndexOf('/')+1,filePath.indexOf('.'))
        let ext = filePath.substring(filePath.lastIndexOf('.')+1,filePath.length);

        if(!(ext == 'xls' || ext == 'xlsx')){
            console.info("Input file is not a excel file")
            output['newFileArr'] = input.fileArr;
            return { message: "Not a excel File", status: 0, data: output };    
        }

        console.log(extractedFilePath)
        console.log(ext)
        
        if(ext==='xls'){
            const command = `libreoffice --headless --convert-to xlsx "${filePath}" --outdir "${extractedFilePath}"`;
            await exec(command);
            filePath =`${extractedFilePath}/${fileName}.xlsx` 
            console.log(filePath)
                           
        }
        
        console.log("78"+filePath)

        await delay(5000)

        console.log("This message appears after 5 seconds");

        // Configuring the workbook and the worksheet
        console.log("78123")
        const workbook = new ExcelJS.Workbook();
        await workbook.xlsx.readFile(filePath);
        console.log("fgh")
        workbook.eachSheet((worksheet, sheetId) => {
            const totalRows = worksheet.rowCount;
            const totalColumns = worksheet.columnCount;
            // Apply wrapText to the entire range of the worksheet
            if(totalColumns!==0 || totalRows!==0) 
                worksheet.getCell(
                    `A1:${worksheet.getColumn(totalColumns).letter}${totalRows}`
                ).alignment = { wrapText: true };
            // Set page layout properties
            worksheet.pageSetup.orientation = 'landscape'; // or 'portrait'  'landscape'
            worksheet.pageSetup.paperSize = 9; // 9 is for A4; refer to documentation for other sizes
            worksheet.pageSetup.fitToPage = true; // Enable fit to page
            worksheet.pageSetup.fitToWidth = 1; // Fit content to 1 page width
            worksheet.pageSetup.fitToHeight = 0; // Fit content to 1 page height
            worksheet.pageSetup.pageOrder = 'overThenDown'
            
        });
        console.log("sdfgd")
        //Save the workbook to a file
        await workbook.xlsx.writeFile(filePath)
    
        
        console.log("++++++++++ configured the excel +++++++++++")

        console.log("in the pdf conversion block")
        const command = `libreoffice --headless --convert-to pdf "${filePath}" --outdir "${extractedFilePath}"`;
        await exec(command);
        
        
        filePath = `${extractedFilePath}/${fileName}.pdf`  
   
        console.log(`File converted to pdf successfully`,filePath);
        input.fileArr[iterationId].filePath = filePath
        output['newFileArr'] = input.fileArr
        output['newFilePath'] = filePath
        return { message: "Succesfully converted the file.", status: 0, data: output };
    
    } catch (e) {
        this.log.error("Error while converting file ---" + e);
        return { message: e, status: 1, data: e };
    }
}