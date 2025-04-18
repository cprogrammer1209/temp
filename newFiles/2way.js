twoWayReConciliationNew(input, output, botId, projectId, iterationId) {
  return tslib_2.__awaiter(this, void 0, void 0, function* () {
      try {
          let docType = input.docType;
          let collectionName = input.collectionName;
          let caseNo = input.caseNo;
          let keys = input.keys ? input.keys.split(',') : [];
let recon = input.recon;
          console.log("Input ---->", input, docType, collectionName, caseNo,recon);
          console.log("Keys ---->", keys);
          function levenshtein(a, b) {
              const m = a.length;
              const n = b.length;
              const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
              for (let i = 0; i <= m; i++) {
                  dp[i][0] = i;
              }
              for (let j = 0; j <= n; j++) {
                  dp[0][j] = j;
              }
              for (let i = 1; i <= m; i++) {
                  for (let j = 1; j <= n; j++) {
                      if (a[i - 1] === b[j - 1]) {
                          dp[i][j] = dp[i - 1][j - 1];
                      }
                      else {
                          dp[i][j] = Math.min(dp[i - 1][j] + 1, // deletion
                          dp[i][j - 1] + 1, // insertion
                          dp[i - 1][j - 1] + 1 // substitution
                          );
                      }
                  }
              }
              return dp[m][n];
          }
          function similarity(a, b) {
              const distance = levenshtein(a, b);
              const maxLen = Math.max(a.length, b.length);
              return ((maxLen - distance) / maxLen) * 100;
          }
          function isNumeric(str) {
              return /^-?\d+(\.\d+)?$/.test(str);
          }
          let data = {};
          if (!util_1.isNullOrUndefined(caseNo) && caseNo !== "" && !util_1.isNullOrUndefined(collectionName) && collectionName !== "") {
              let fromDocs = yield (db.collection(docType)).findOne({ DirName: caseNo }).lean();
              let toDocs = yield (db.collection(collectionName)).findOne({ DirName: caseNo }).lean();
              console.log("fromDocs:--->>>", fromDocs);
              console.log("toDocs:--->>>", toDocs);
              console.log("fromDocs.length " + !util_1.isNullOrUndefined(fromDocs));
              console.log("toDocs.length " + !util_1.isNullOrUndefined(toDocs));
              if (!util_1.isNullOrUndefined(fromDocs) && !util_1.isNullOrUndefined(toDocs)) {
                  keys = lodash_1.toArray(keys);
                  console.log("Keys---" + keys);
                  for (let i = 0; i < keys.length; i++) {
                      console.log("key--" + keys[i]);
                      if (!data[collectionName]) {
                          data[collectionName] = {};
                      }
                      if (!data[docType]) {
                          data[docType] = {};
                      }
                      if (!data['Similarity']) {
                          data['Similarity'] = {};
                      }
                      if (!data['Document Type']) {
                          data['Document Type'] = {};
                      }
                      if (!util_1.isNullOrUndefined(toDocs['Document Type'][keys[i]])) {
                          data['Document Type'][keys[i]] = toDocs['Document Type'][keys[i]];
                      }
                      else {
                          data['Document Type'][keys[i]] = "";
                      }
                      data['documentType'] = docType;
                      data['caseNo'] = caseNo;
                      if (!util_1.isNullOrUndefined(toDocs[keys[i]])) {
                          data[collectionName][keys[i]] = toDocs[keys[i]];
                      }
                      else {
                          data[collectionName][keys[i]] = "";
                      }
                      if (!util_1.isNullOrUndefined(fromDocs[keys[i]])) {
                          data[docType][keys[i]] = fromDocs[keys[i]];
                      }
                      else {
                          data[docType][keys[i]] = "Document not found";
                      }
                      if (!util_1.isNullOrUndefined(fromDocs[keys[i]]) && !util_1.isNullOrUndefined(toDocs[keys[i]])) {
                          if (isNumeric(toDocs[keys[i]])) {
                              const numberWithCommas = fromDocs[keys[i]].toString().match(/[\d,]+/)[0];
                              const number = numberWithCommas.replace(/,/g, '');
                              data['Similarity'][keys[i]] = parseFloat(similarity(number, toDocs[keys[i]].toString().toLowerCase()).toFixed(2));
                          }
                          else {
                              data['Similarity'][keys[i]] = parseFloat(similarity(fromDocs[keys[i]].toString().toLowerCase(), toDocs[keys[i]].toString().toLowerCase()).toFixed(2));
                          }
                      }
                      else {
                          data['Similarity'][keys[i]] = 0;
                      }
                      console.log("Similarity: " + data['Similarity'][keys[i]]);

                  }
                  console.log("Data ---------------");
                  console.log(data);
              }
              yield (db.collection(recon)).create(data);
              output['outputData'] = "Acknowledge";
              return { message: 'Data Found Sucessfull', status: 0, data: output };
          }
          else {
              return { message: 'Please Give Pan Number', status: 1, data: output };
          }
      }
      catch (e) {
          this.log.error("Error in Finding User Data" + e);
          return {
              message: e, status: 1, data: e + '[ eventId - ' + input.eventId + ' projectId - ' +
                  projectId + ' botId - ' + botId + ' iterationId - ' + iterationId + ']'
          };
      }
  });
}