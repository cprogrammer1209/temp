public async messageExtraction(message, all, idHeader, outputParameters, bodydata, from, to, subject, htmlbody, textbody, inputData, Attachfilename, cc) {
    try {
        return new Promise((res, rej) => {
            try {

                simpleParser(idHeader + all.body, (err, mail) => {
                    if (err) {
                        res({});
                    } else {

                        console.info("MESSAGE FETCH FROM MAIL ")
                        from = mail.from.value[0].address
                        to = mail.to.value[0].address
                        if (!isNullOrUndefined(mail.cc)) {
                            cc = mail.cc.value[0].address
                        }
                        subject = mail.subject
                        htmlbody = mail.html
                        textbody = mail.text
                        let mailDate = mail.date
                        bodydata.push({ 'fromMail': from, 'tomail': to, 'ccmail': cc, 'subject': subject, 'date': mailDate, 'textbody': textbody, 'htmlbody': htmlbody });
                        outputParameters['bodydata'] = bodydata;
                        //console.info(" --- --- BODY DATA ----- -----   ",bodydata);
                        if (mail.attachments.length === 0 && mail.subject.startsWith(subject)) {

                            inputData['outputParameters'] = { statusCode: "200", successMessage: 'File read successfull', fromMail: from, tomail: to, subject: subject, attachment_path: Attachfilename, textbody: textbody, body: textbody, htmlbody: htmlbody };
                            console.warn("INSIDE BODYDATA FOUND");
                            outputParameters['subject'] = inputData['outputParameters']['subject'];
                            outputParameters['fromMail'] = inputData['outputParameters']['from'];
                            outputParameters['tomail'] = inputData['outputParameters']['to'];
                            outputParameters['textbody'] = inputData['outputParameters']['textbody'];
                            outputParameters['htmlbody'] = inputData['outputParameters']['htmlbody'];
                            outputParameters['attachment_path'] = inputData['outputParameters']['attachment_path'];
                            outputParameters['body'] = inputData['outputParameters']['body'];
                            outputParameters['AttachFolder'] = inputData['outputParameters']['AttachFolder'];

                            //this.socket.emit('utility_response', inputData);
                            res(outputParameters);
                        } else {
                            res(outputParameters);
                        }
                    }
                });
            }
            catch (e) {
                res({ bodydata: bodydata ? bodydata : [] });
            }
        });
    } catch (err) {
        console.error(err);
        return err;
    }
}