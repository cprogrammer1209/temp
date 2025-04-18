pdfConverter1(input, output, botId, projectId, iterationId) {
  return tslib_2.__awaiter(this, void 0, void 0, function* () {
      try {
          const util = require('util');
          const fs = require('fs/promises');
          const exec = util.promisify(require('child_process').exec);
          const ExcelJS = require('exceljs123');
          // if (typeof input.filePath === "string") {
          //     input.filePath = JSON.parse(input.filePath);
          // }
          let filePath = input.filePath;
          let extractedFilePath = filePath.substring(0, filePath.lastIndexOf('/'));
          let fileName = filePath.substring(filePath.lastIndexOf('/') + 1, filePath.indexOf('.'));
          let ext = filePath.substring(filePath.lastIndexOf('.') + 1, filePath.length);
          if (!(ext == 'xls' || ext == 'xlsx' || ext == 'docx' || ext == 'doc')) {
              console.info("Input file is not a excel file");
              output['filePathArr'] = input.filePath;
              return { message: "Not a excel or docx File", status: 0, data: output };
          }
          if (ext === 'xls') {
              const command = `libreoffice --headless --convert-to xlsx "${filePath}" --outdir "${extractedFilePath}"`;
              const response = yield exec(command);
              console.log(response);
              yield fs.unlink(filePath);
              filePath = `${extractedFilePath}/${fileName}.xlsx`;
              ext = 'xlsx';
              console.log(filePath);
          }
          yield delay(5000);
          if (ext == 'xlsx') {
              // Configuring the workbook and the worksheet
              const workbook = new ExcelJS.Workbook();
              yield workbook.xlsx.readFile(filePath);
              workbook.eachSheet((worksheet, sheetId) => {
                  const totalRows = worksheet.rowCount;
                  const totalColumns = worksheet.columnCount;
                  // Apply wrapText to the entire range of the worksheet
                  if (totalColumns !== 0 || totalRows !== 0)
                      worksheet.getCell(`A1:${worksheet.getColumn(totalColumns).letter}${totalRows}`).alignment = { wrapText: true };
                  // Set page layout properties
                  worksheet.pageSetup.orientation = 'landscape'; // or 'portrait'  'landscape'
                  worksheet.pageSetup.paperSize = 9; // 9 is for A4; refer to documentation for other sizes
                  worksheet.pageSetup.fitToPage = true; // Enable fit to page
                  worksheet.pageSetup.fitToWidth = 1; // Fit content to 1 page width
                  worksheet.pageSetup.fitToHeight = 0; // Fit content to 1 page height
                  worksheet.pageSetup.pageOrder = 'overThenDown';
              });
              //Save the workbook to a file
              yield workbook.xlsx.writeFile(filePath);
              console.log("++++++++++ configured the excel +++++++++++");
          }
          console.log("in the pdf conversion block");
          const command = `libreoffice --headless --convert-to pdf "${filePath}" --outdir "${extractedFilePath}"`;
          yield exec(command);
          yield fs.unlink(filePath);
          filePath = `${extractedFilePath}/${fileName}.pdf`;
          console.log(`File converted to pdf successfully`, filePath);
          input.filePath = filePath;
          output['filePathArr'] = input.filePath;
          output['newFilePath'] = filePath;
          return { message: "Succesfully converted t1he file.", status: 0, data: output };
      }
      catch (e) {
          this.log.error("Error while converting file ---" + e);
          return { message: e, status: 1, data: e };
      }
  });
}