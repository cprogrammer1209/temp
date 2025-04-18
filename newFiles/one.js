public async EMailRecieverforUtility(inputData, outputParameters, botId, projectId, iterationId) {
  try {
      let Attachfilename;
      let textbody;
      let htmlbody;
      let allorseen;
      let subject;
      let date;
      let from;
      let to;
      let cc = '';
      let bodydata = [];
      let bodyData = {};
      let self = this;
      if (!isNullOrUndefined(inputData["password"]) && inputData["password"] !== "") {
          inputData["password"] = Buffer.from(inputData["password"], 'base64').toString()
      }
      console.log("Input --------->>  ", inputData)
      let config = {
          imap: {
              user: inputData.user,
              password: inputData.password,//Password
              host: inputData.host,
              port: 993,
              tls: true
          }
      };
      if (!isNullOrUndefined(inputData.filePath) && inputData.filePath !== '') {
          let tlsOptions = {
              ca: [fs.readFileSync(inputData.filePath)],
              rejectUnauthorized: false
          }
          config["imap"]['tlsoptions'] = tlsOptions;
          config["imap"]["authTimeout"] = 120000;
          config["imap"]["connTimeout"] = 120000;
      } else {
          config["imap"]["tlsOptions"] = { rejectUnauthorized: false },
              config["imap"]["authTimeout"] = 120000,
              config["imap"]["connTimeout"] = 120000;
      }

      console.log("Main Config======>>>>>", config)
      allorseen = inputData.allorseen;
      date = inputData.date;
      subject = inputData.subject;
      from = inputData.fromMail;
      to = inputData.toMail;
      //let currentdate = new Date().toISOString();
      let updateDate = "";
      if (date.length !== 0) {
          updateDate = new Date(date).toISOString()
          console.log("date given by user", updateDate);
      }
      let searchCriteria = [];
      let fetchOptions = {};
      console.info(" -- -- --- IN SINCE  BEFORE CONNECTION -------- --- ---- ");


      if (from.length > 0 && to.length > 0 && subject.length > 0) {
          console.log("<<< <<<< <<<<< <<<<< ---------  Inside InBOX  ------- >>>> >>>> >>>>> >>>>> >>>> ");
          if (inputData.subjectSearch === "true") {
              searchCriteria = [allorseen, ['SINCE', updateDate], ['FROM', from], ['TO', to]];
          } else {
              searchCriteria = [allorseen, ['SINCE', updateDate], ['FROM', from], ['TO', to], ['SUBJECT', subject]];
          }
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)', 'TEXT', ''], markSeen: true, struct: true };
      }
      else if (from.length > 0 && to.length > 0) {
          console.log("fetch from and to");
          searchCriteria = [allorseen, ['SINCE', updateDate], ['FROM', from], ['TO', to]];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)'], markSeen: true, struct: true };
      }
      else if (from.length > 0 && subject.length > 0) {
          console.log("this is search only from and subjects");
          searchCriteria = [allorseen, ['SINCE', updateDate], ['FROM', from], ['SUBJECT', subject]];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)'], markSeen: true, struct: true };
      }
      else if (subject.length > 0 && to.length > 0) {
          console.log("only fetch sub and to");
          searchCriteria = [allorseen, ['SINCE', updateDate], ['TO', to], ['SUBJECT', subject]];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)', 'TEXT', ''], markSeen: true, struct: true };
      }
      else if (from.length > 0 && to.length === 0 && subject.length === 0) {
          console.log("only access from");
          searchCriteria = [allorseen, ['SINCE', updateDate], ['FROM', from]];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)'], markSeen: true, struct: true };
      }
      else if (subject.length > 0 && from.length === 0 && to.length === 0) {
          console.log("only fetch subjectss");
          searchCriteria = [allorseen, ['SINCE', updateDate], ['SUBJECT', subject]];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)'], markSeen: true, struct: true };
      }
      else if (to.length > 0 && from.length === 0 && subject.length === 0 && updateDate != '') {
          console.log("<< <<< ------------ -------- SESRCH USING TO MAIL WITH DATE-------- --------- -------- >>>> ");

          searchCriteria = [allorseen, ['SINCE', updateDate], ['TO', to]];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)', 'TEXT', ''], markSeen: true, struct: true };
      } else if (to.length == 0 && from.length === 0 && subject.length === 0) {
          console.log("<< <<< ------------ -------- SESRCH USING TO MAIL WITHOUT DATE AND TO MAIL -------- --------- -------- >>>> ");

          searchCriteria = [allorseen];
          fetchOptions = { bodies: ['HEADER.FIELDS (FROM TO SUBJECT DATE)', 'TEXT', ''], markSeen: true, struct: true };
      }
      else {
          console.log("-- --- --- --- ----    IN ELSE FOR    --- ---- ----- ----- ----- ----- ---- ----- ");
      }



      return await new Promise(async (resolve, reject) => {

          let connectionEmail = await imaps.connect(config);

          await connectionEmail.openBox('INBOX');

          let messages = await connectionEmail.search(searchCriteria, fetchOptions);

          if (!isNullOrUndefined(messages) && messages.length > 0) {
              let attachments = [];
              if (inputData.multipleMails && [true, 'true'].includes(inputData.multipleMails)) {
                  from = [];
                  to = [];
                  subject = [];
                  textbody = [];
                  htmlbody = [];
                  for (let i = 0; i < messages.length; i++) {
                      let message = messages[i];
                      var all = _.find(message.parts, { "which": "" });
                      var id = message.attributes.uid;
                      var idHeader = "Imap-Id: " + id + "\r\n";
                      console.log(id)
                      bodyData = await self.messageExtraction(message, all, idHeader, outputParameters, bodydata, from, to, subject, htmlbody, textbody, inputData, Attachfilename, cc);
                      bodydata = bodyData["bodydata"];
                      let lfrom = !isNullOrUndefined(bodyData['from']) && bodyData['from'] !== "" ? bodyData['from'] : "";
                      let lto = !isNullOrUndefined(bodyData['to']) && bodyData['to'] !== "" ? bodyData['to'] : "";
                      let lsubject = !isNullOrUndefined(bodyData['subject']) && bodyData['subject'] !== "" ? bodyData['subject'] : "";
                      let ltextbody = !isNullOrUndefined(bodyData['textbody']) && bodyData['textbody'] !== "" ? bodyData['textbody'] : (all.body ? `${all.body.replace(/"/g, "'")}` : "");
                      let lhtmlbody = !isNullOrUndefined(bodyData['htmlbody']) && bodyData['htmlbody'] !== "" ? bodyData['htmlbody'] : (all.body ? `${all.body.replace(/"/g, "'")}` : "");

                      from.push(lfrom);
                      to.push(lto);
                      subject.push(lsubject);
                      textbody.push(ltextbody);
                      htmlbody.push(lhtmlbody);
                      let parts = await imaps.getParts(message.attributes.struct);
                      const getSub = message.parts.filter(m => m.which === "HEADER.FIELDS (FROM TO SUBJECT DATE)");
                      if (getSub[0].body.subject[0].startsWith(subject)) {
                          for (let k = 0; k < parts.length; k++) {
                              let part = parts[k];
                              if (!isNullOrUndefined(part.disposition) && !isNullOrUndefined(part.disposition.type) && part.disposition.type.toUpperCase() === 'ATTACHMENT') {
                                  attachments.push(await self.fetchFileData(part, connectionEmail, message, getSub, inputData));
                              }
                          }
                      }
                  }
              }
              else {
                  for (let i = 0; i < messages.length; i++) {
                      let message = messages[i];
                      var all = _.find(message.parts, { "which": "" });
                      var id = message.attributes.uid;
                      var idHeader = "Imap-Id: " + id + "\r\n";
                      console.log(id)
                      bodyData = await self.messageExtraction(message, all, idHeader, outputParameters, bodydata, from, to, subject, htmlbody, textbody, inputData, Attachfilename, cc);
                      bodydata = bodyData["bodydata"];
                      from = !isNullOrUndefined(bodyData['from']) && bodyData['from'] !== "" ? bodyData['from'] : "";
                      to = !isNullOrUndefined(bodyData['to']) && bodyData['to'] !== "" ? bodyData['to'] : "";
                      subject = !isNullOrUndefined(bodyData['subject']) && bodyData['subject'] !== "" ? bodyData['subject'] : "";
                      textbody = !isNullOrUndefined(bodyData['textbody']) && bodyData['textbody'] !== "" ? bodyData['textbody'] : (all.body ? `${all.body.replace(/"/g, "'")}` : "");
                      htmlbody = !isNullOrUndefined(bodyData['htmlbody']) && bodyData['htmlbody'] !== "" ? bodyData['htmlbody'] : (all.body ? `${all.body.replace(/"/g, "'")} ` : "");
                      let parts = await imaps.getParts(message.attributes.struct);
                      const getSub = message.parts.filter(m => m.which === "HEADER.FIELDS (FROM TO SUBJECT DATE)");
                      if (getSub[0].body.subject[0].startsWith(subject)) {
                          for (let k = 0; k < parts.length; k++) {
                              let part = parts[k];
                              if (!isNullOrUndefined(part.disposition) && !isNullOrUndefined(part.disposition.type) && part.disposition.type.toUpperCase() === 'ATTACHMENT') {
                                  attachments.push(await self.fetchFileData(part, connectionEmail, message, getSub, inputData));
                              }
                          }
                      }
                  }
              }
              if (!isNullOrUndefined(attachments) && attachments.length > 0) {
                  console.log("<<< <<<< <<<< <<<< --------- ---- EMAIL HAS ATTACHMENTS ----- ----- ----- ----- >>> >>>> ", attachments.length);

                  let count = 0;
                  outputParameters['AttachmentCount'] = attachments.length;
                  let filepath;
                  if (!isNullOrUndefined(inputData.path) && (inputData.path !== "")) {
                      filepath = inputData.path
                  } else {
                      filepath = process.cwd();
                  }

                  let outputDirectory;
                  if ([true, "true"].includes(inputData.dynamicDir)) {
                      outputDirectory = `${filepath}/Case_${Date.now()}`;
                      console.log("Creating new Directory....", `${filepath}/Case_${Date.now()}`);
                  }
                  else {
                      outputDirectory = filepath;
                  }
                  if (!fs.existsSync(outputDirectory)) {
                      await fs.mkdirSync(outputDirectory);
                  }

                  inputData['outputParameters'] = { statusCode: "200", successMessage: 'File read successfull', fromMail: from, tomail: to, subject: subject, attachment_path: [], textbody: textbody, body: textbody, htmlbody: htmlbody, AttachFolder: outputDirectory };
                  //For loop For Attachments
                  console.log("BEFORE ATTACHMENT FOR LOOP")

                  inputData["outputParameters"]["folder_path"] = [];
                  inputData["outputParameters"]["folder_count"] = 0;

                  if (inputData.isSubjectWise === "yes") {

                      for (let element of attachments) {
                          console.log("INSIDE EMAIL ATTACHEMENT FOR FORLOOP ONEE 1");
                          let directory = path.dirname(element.filename)
                          let file = path.basename(element.filename)
                          directory = directory.replace(/[(#,&*)]/g, "")
                          let newDirectory = outputDirectory + "/" + directory
                          if (!fs.existsSync(newDirectory)) {
                              console.log("  <<<< <<< << -------- ------ FOLDER PATH ---- ---  -- >> >>  ", outputDirectory + directory);
                              inputData["outputParameters"]["folder_path"].push(newDirectory);
                              await fs.mkdirSync(newDirectory);
                              count = count + 1;
                          } else if (inputData["outputParameters"]["folder_path"].indexOf(newDirectory) == -1) {
                              console.log("  <<<< <<< << -------- ------ FOLDER PATH ALREADY EXISTS ---- ---  -- >> >>  ", outputDirectory + directory);
                              inputData["outputParameters"]["folder_path"].push(newDirectory);
                              count = count + 1;
                          }
                          console.log("fileNamee isss-----", element.filename);
                          Attachfilename = newDirectory + '/' + file
                          await fs.writeFileSync(Attachfilename, element.data);
                          inputData['outputParameters']['attachment_path'].push(Attachfilename);

                      }
                      inputData["outputParameters"]["folder_count"] = count;
                  } else {
                      for (let element of attachments) {
                          console.log("INSIDE EMAIL ATTACHEMENT FOR FORLOOP TWO 2");
                          console.log("fileNamee isss-----", element.filename);
                          Attachfilename = outputDirectory + '/' + element.filename
                          await fs.writeFileSync(Attachfilename, element.data);
                          inputData['outputParameters']['attachment_path'].push(Attachfilename);

                      }
                  }
                  console.log("AFTER EMAIL ATTACHEMENT FOR FORLOOP")

                  outputParameters['subject'] = inputData['outputParameters']['subject'];
                  outputParameters['fromMail'] = inputData['outputParameters']['from'];
                  outputParameters['tomail'] = inputData['outputParameters']['to'];
                  outputParameters['textbody'] = inputData['outputParameters']['textbody'];
                  outputParameters['htmlbody'] = inputData['outputParameters']['htmlbody'];
                  outputParameters['attachment_path'] = inputData['outputParameters']['attachment_path'];
                  outputParameters['body'] = inputData['outputParameters']['body'];
                  outputParameters['AttachFolder'] = inputData['outputParameters']['AttachFolder'];
                  outputParameters['emailContent'] = bodydata;
                  outputParameters['folder_path'] = inputData["outputParameters"]["folder_path"];
                  outputParameters['folder_count'] = inputData["outputParameters"]["folder_count"];
                  outputParameters['MessageCount'] = Array.isArray(textbody) ? textbody.length : 1;
                  outputParameters['refNo'] = !isNullOrUndefined(inputData['outputParameters']['refNo']) ? inputData['outputParameters']['refNo'] : null;
                  // console.log("attchfolder --->", inputData['outputParameters']['AttachFolder']);
                  // console.log("attachpath -->", inputData['outputParameters']['attachment_path']);
                  console.log("< < < < < --- ---- ATTACH FOLDERS PATH --- ----- --- > > > > > >  LENGTH   ", outputParameters['folder_count'], "   << < << << <<< < ------ ---------- ATTACH FOLDER PATH ------- --------- > >> >> >> >>    ", outputParameters['folder_path']);
                  console.log("DATA RECIEVED SUCCESSFULLY");

                  console.info(outputParameters);
                  connectionEmail.end();
                  // connectionEmail.destroy();
                  resolve({ message: "Data recieve SuccessFully", status: 0, data: outputParameters });

              } else {
                  connectionEmail.end();
                  console.log("attachments not found");
                  outputParameters['subject'] = subject;
                  outputParameters['fromMail'] = from;
                  outputParameters['tomail'] = to;
                  outputParameters['textbody'] = textbody;
                  outputParameters['htmlbody'] = htmlbody;
                  outputParameters['emailContent'] = bodydata;
                  outputParameters['AttachmentCount'] = 0;
                  outputParameters['MessageCount'] = Array.isArray(textbody) ? textbody.length : 1;
                  // connectionEmail.destroy();
                  resolve({ message: "NO ATTACHEMENT MAIL TO READ AVAIALBLE", status: 0, data: outputParameters });
              }
          } else {
              connectionEmail.end();
              // connectionEmail.destroy();
              resolve({ message: "NO MAIL TO READ AVAIALBLE", status: 0, data: {} })
          }
      });
  }
  catch (e) {
      console.log('Error in fetching details from bank', e);
      return { message: '', status: 1, data: e };
  }
}