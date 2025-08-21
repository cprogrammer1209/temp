public async emailNotify(input: any, outputParameters, botId, projectId, iterationId) {
        try {
            this.log.info('Inside email notify -- ' + JSON.stringify(input));
            if (input.tackle && input.tackle == 'true') {
                // The sleep of 8 seconds based on iteationId for tackling the Gmail limit reach issue, in case of the same parentEventId
                let iterationData = await db.collection("events").findOne(
                    { _id: ObjectId(input.eventId) },
                    { iterationId: 1 }
                );
                const jsonRes = JSON.parse(JSON.stringify(iterationData));
                // Ensure iterationId is at least 1
                let iteationId = jsonRes && jsonRes.iterationId ? Number(jsonRes.iterationId) : 1;
                iteationId = iteationId * 8000;
                await delay(iteationId);
            }
            let attachments = [];
            let config;
            let transport;
            let isArray
            if (!input['projectVar']) {
                if (!isNullOrUndefined(input['pass'])) {
                    input['pass'] = Buffer.from(input['pass'], 'base64').toString()
                }
            }
            input.messageId = input.messageId ? input.messageId : '';
            if ((!isNullOrUndefined(input.service) && input.service.toLowerCase().trim() == 'gmail') || (!isNullOrUndefined(input.host) && input.host !== "")) {
                config = {
                    host: isNullOrUndefined(input.host) || input.host == "" ? "smtp.gmail.com" : input.host,//"smtp.gmail.com",
                    port: isNullOrUndefined(input.port) || input.port == "" ? 587 : input.port,//587
                    secure: !isNullOrUndefined(input.secure) && input.secure == "true" ? true : false,
                    ignoreTLS: !isNullOrUndefined(input.ignoreTLS) && input.ignoreTLS == "true" ? true : false,

                };
                if (!isNullOrUndefined(input.user) && input.user !== "") {
                    config["auth"] = { user: input.user }
                };
                if (!isNullOrUndefined(input.service) && input.service !== "") {
                    config["service"] = input.service
                }
                if (!isNullOrUndefined(input.pass) && input.pass !== "") {
                    config["auth"]["pass"] = input.pass
                };
                console.log(JSON.parse(JSON.stringify(config)));
                if (!isNullOrUndefined(input.useAccessToken) && (input.useAccessToken || input.useAccessToken == 'true')) {

                    let userData = await UserModel.findOne({ _id: ObjectId(input.userId) })
                    transport = nodemailer.createTransport({
                        service: input.service,
                        auth: {
                            type: 'OAuth2',
                            user: input.from,
                            clientId: userData['client_id'],
                            clientSecret: userData['client_secret'],
                            refreshToken: userData['refresh_token'],
                            accessToken: userData['access_token'],
                        },
                    });
                } else {
                    transport = nodemailer.createTransport(smtpTransport(config));
                }

            } else {
                process.env.NODE_TLS_REJECT_UNAUTHORIZED = input.REJECT_UNAUTHORIZED;
                config = (input.secureConnection != undefined && (input.secureConnection.toString().toLowerCase().trim() == "true" || input.secureConnection.toString().toLowerCase().trim() == "yes") ? "smtps" : "smtp") + "://" + input.from + ":" + encodeURIComponent(input.pass) + "@" + input.host + ":" + input.port;
                this.log.info("configuartion string==" + config);
                transport = nodemailer.createTransport(config);
            }
            if (!isNullOrUndefined(input.attachments) && input.attachments !== "") {
                let attDoc = input.attachments;
                if (!isNullOrUndefined(attDoc) && attDoc.length > 0) {
                    isArray = Array.isArray(attDoc);       // checked attDoc isArray dataType
                    if (!isArray) {
                        isArray = attDoc[0] == "[" ? true : false;   // checked array in string dataType
                    }
                    if (!isNullOrUndefined(attDoc) && attDoc.length > 0 && isArray) {
                        if (typeof attDoc == 'string') {   // checked attDoc is string or not
                            attDoc = JSON.parse(attDoc);
                        }
                        for (let i = 0; i < attDoc.length; i++) {
                            const fileName = attDoc[i].replace(/^.*[\\\/]/, '');
                            attachments.push({ 'filename': fileName, 'path': attDoc[i] });
                        }
                    } else {
                        attachments.push({ 'filename': input.attachments.replace(/^.*[\\\/]/, ''), 'path': attDoc });
                    }
                }
            }

            if (!isNullOrUndefined(input.track) && input.track == "true") {
                if (!isNullOrUndefined(input.campaignId) && input.campaignId !== "") { }
                else {
                    const unixTimestamp = Math.floor(Date.now() / 1000);
                    const timestampHexString = unixTimestamp.toString(16);
                    input.campaignId = timestampHexString;
                }

                let emailHtml = input.html;
                const callbackUrl = `${process.env.Application_URL}gibots-api/email`;
                // const callbackUrl = "http://localhost:2224/gibots-api/email"; // Local callback URL

                // Find URLs in the HTML content and replace them with tracked URLs
                const urlRegex = /(?:https?:\/\/|www\.)[^\s<>"']+/gi; // Match all URLs
                const urls = emailHtml.match(urlRegex);

                if (urls) {
                    console.log("Found URLs:", urls);

                    // Store replacements in an array to process them later
                    const replacements = [];

                    urls.forEach((url) => {
                        console.log(`Processing URL: ${url}`);

                        // Ensure the URL starts with https:// if it doesn't already
                        const ensureHttps = (url) => (!/^https?:\/\//i.test(url) ? `https://${url}` : url);
                        const nUrl = ensureHttps(url);

                        // Create the tracked URL
                        const trackedUrl = `${callbackUrl}/log-external-click?externalURL=${encodeURIComponent(nUrl)}&emailId=${input.to}&fromEmail=${input.from}&campaignId=${input.campaignId}&orgId=${input.orgId}&subscriberId=${input.subscriberId}&userId=${input.userId}`;

                        // Skip replacement if the URL is in a src attribute
                        const srcRegex = new RegExp(`src=["']${url}["']`, "gi");
                        if (srcRegex.test(emailHtml)) {
                            console.log(`Skipping URL in src: ${url}`);
                            return;
                        }

                        // Collect the replacement (do not replace immediately)
                        const urlRegexGlobal = new RegExp(url, "g"); // Global regex for multiple occurrences
                        let match;
                        while ((match = urlRegexGlobal.exec(emailHtml)) !== null) {
                            replacements.push({
                                index: match.index,
                                length: match[0].length,
                                replacement: `<a href="${trackedUrl}">${url}</a>`,
                            });
                        }
                    });

                    // Sort replacements in reverse order of index to handle overlapping replacements
                    replacements.sort((a, b) => b.index - a.index);

                    // Apply replacements to the emailHtml
                    replacements.forEach(({ index, length, replacement }) => {
                        emailHtml = emailHtml.slice(0, index) + replacement + emailHtml.slice(index + length);
                    });

                    //console.log("Processed emailHtml:", emailHtml);
                } else {
                    console.log("No URLs found.");
                }

                if (!emailHtml.includes('</body>')) {
                    emailHtml = `<html><body>${emailHtml}</body></html>`;
                }
                emailHtml = emailHtml.replace('</body>', `<img src="${callbackUrl}/tracking_pixel?emailId=${input.to}&fromEmail=${input.from}&campaignId=${input.campaignId}&orgId=${input.orgId}&subscriberId=${input.subscriberId}&userId=${input.userId}" width="1" height="1" style="display:none;"></body>`);
                //console.log(emailHtml);
                input.html = emailHtml;
            }

            if (!isNullOrUndefined(input.signature) && input.signature !== "") {
                if (input.html.includes('</body>')) {
                    input.html = input.html.replace('</body>', `${input.signature}</body>`);
                } else {
                    input.html = input.html + `${input.signature}`;
                }
            }

            if (!isNullOrUndefined(input.unsubText) && input.unsubText !== "") {
                const callbackUrl = `${process.env.Application_URL}gibots-api/email`;
                if (input.html.includes('</body>')) {
                    input.html = input.html.replace('</body>', `<p>${input.unsubText} click <a href="${callbackUrl}/unsubscribe?emailId=${input.to}&orgId=${input.orgId}&subscriberId=${input.subscriberId}&userId=${input.userId}" style="color: #ff0000; text-decoration: underline;">here</a> to unsubscribe.</p></body>`);
                } else {
                    input.html = input.html + `<p>${input.unsubText} click <a href="${callbackUrl}/unsubscribe?emailId=${input.to}&orgId=${input.orgId}&subscriberId=${input.subscriberId}&userId=${input.userId}" style="color: #ff0000; text-decoration: underline;">here</a> to unsubscribe.</p>`;
                }
            }

            const regex = /<[^>]*>/;
            if (regex.test(input.html)) {

            } else {
                input.html = `<html>${input.html}</html>`;
            }

            // Prepare the email options
            const emailOptions = {
                from: input.from,
                to: input.to, // Only a single recipient now
                replyTo: input.replyTo || '',
                cc: input.cc || '', // cc can be optional
                bcc: input.bcc || '', // bcc can be optional
                subject: input.subject,
                text: input.text,
                html: input.html,
                attachments: attachments,
                headers: {
                    'In-Reply-To': input.messageId,
                    References: input.messageId,

                },
            };

            if (!isNullOrUndefined(input.appendOld) && input.appendOld == "true") {
                const emailToMatch = emailOptions.to;
                const regex = new RegExp(`<${emailToMatch}>|^${emailToMatch}$`, 'i');

                const sentEmails = await db.collection('emails_sent_logs')
                    .find({
                        subscriberId: ObjectId(input.subscriberId),
                        orgId: ObjectId(input.orgId),
                        receiverEmailId: emailOptions.to,
                    })
                    .lean();

                const receivedEmails = await db.collection('emails_received_logs')
                    .aggregate([
                        {
                            $match: {
                                from: { $regex: regex },
                            },
                        },
                        {
                            $lookup: {
                                from: 'emails_sent_logs', // Related collection
                                localField: 'inReplyTo', // Field in emails_received_logs
                                foreignField: 'messageId', // Field in emails_sent_logs
                                as: 'matchingSentLogs', // Resulting array field
                            },
                        },
                        {
                            $match: {
                                'matchingSentLogs.subscriberId': ObjectId(input.subscriberId),
                                'matchingSentLogs.orgId': ObjectId(input.orgId),
                            },
                        },
                        {
                            $project: {
                                matchingSentLogs: 0,
                            },
                        },
                    ])
                    .exec();

                const allEmails = [
                    ...sentEmails.map((email) => ({
                        ...email,
                        type: 'sent',
                        sortDate: new Date(email.createdAt),
                    })),
                    ...receivedEmails.map((email) => ({
                        ...email,
                        type: 'received',
                        sortDate: new Date(email.date),
                    })),
                ];

                const sortedEmails = allEmails.sort((a, b) => b.sortDate - a.sortDate);

                if (sortedEmails.length > 0) {
                    const topEmail = sortedEmails[0];
                    let subject;

                    if (topEmail.type === 'received') {
                        subject = topEmail.subject;
                        emailOptions['subject'] = subject;
                    } else if (topEmail.type === 'sent') {
                        const campaignData = await db.collection('campaigns')
                            .findOne({ eventId: ObjectId(topEmail.campaignId) }, { Subject: 1 }).lean();

                        if (campaignData) {
                            subject = campaignData.Subject;
                            subject = `Re: ${subject}`;
                            emailOptions['subject'] = subject;
                        } else {
                            console.warn('No campaign found for the given campaignId.');
                        }
                    }

                    emailOptions['inReplyTo'] = `<${topEmail.messageId}>`;
                    emailOptions['references'] = [`<${topEmail.messageId}>`];
                }
            }
            let response;
            const retries = 3;
            // Send the email
            for (let attempt = 1; attempt <= retries; attempt++) {
                try {
                    response = await transport.sendMail(emailOptions);
                    // console.log(`Email sent successfully on attempt ${attempt}`);
                    break; // Exit loop on success, but allow further code to run
                } catch (error) {
                    if (attempt < retries) {
                        console.warn(`Attempt ${attempt} failed: ${error.message}. Retrying in ${delay}ms...`);
                        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait before retrying
                    } else {
                        console.error(`Failed to send email after ${attempt} attempts.`, error);
                        break;
                    }
                }
            }

            if ((!isNullOrUndefined(input.MinGapBetTwoEmails) && input.MinGapBetTwoEmails !== "") ||
                (!isNullOrUndefined(input.MaxGapBetTwoEmails) && input.MaxGapBetTwoEmails !== "")) {

                const minGap = !isNullOrUndefined(input.MinGapBetTwoEmails) && input.MinGapBetTwoEmails !== "" ? parseInt(input.MinGapBetTwoEmails, 10) : null;
                const maxGap = !isNullOrUndefined(input.MaxGapBetTwoEmails) && input.MaxGapBetTwoEmails !== "" ? parseInt(input.MaxGapBetTwoEmails, 10) : null;

                let gap;
                if (minGap !== null && maxGap !== null) {
                    gap = Math.floor(Math.random() * (maxGap - minGap + 1)) + minGap;
                } else if (minGap !== null) {
                    gap = minGap;
                } else if (maxGap !== null) {
                    gap = maxGap;
                }
                await new Promise(resolve => setTimeout(resolve, gap * 1000));
            }

            if (isNullOrUndefined(response)) {
                return { info: 'error occurred', status: 0, data: outputParameters };
            } else {
                outputParameters['messageId'] = response.messageId;
                return { info: 'mail sent successfully', status: 0, data: outputParameters };
            }
        } catch (e) {
            return { message: e, status: 1, data: e + '[ eventId - ' + input.eventId + ' projectId - ' + projectId + ' botId - ' + ' iterationId - ' + iterationId + ']' };
        }
    }