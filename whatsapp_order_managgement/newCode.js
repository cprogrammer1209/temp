try {
            console.log("Incoming webhook message:", JSON.stringify(req.body, null, 2));
            const entry = req.body.entry[0];
            const changes = entry.changes[0].value;

            const metadata = changes.metadata;
            const phoneNumberId = metadata.phone_number_id;
            const displayPhoneNum = metadata.display_phone_number
            
            
            const message = changes.messages[0];
            const from = message.from;
            const text = message.text.body;
            const contact = changes.contacts[0];
            const waId = contact.wa_id;
            const userName = contact.profile.name || "";
            console.log(`Received message from ${from}: ${text}`);
            
            
            //  * Getting the details of the organisation for chatgenie configurations
            let userCred  = await db.collection("whatsappOrderManagement").findOne({phoneNumber:displayPhoneNum}).lean();
            if(isNullOrUndefined(userCred)){
                throw Error("No data to send again whatsapp message")
            }
            
            //  * Getting response from chatgenie and also deciding whether again needs to send and store the whatsapp message or not
            let replyText = await this.getResponseFromChatGenie(text,userCred,userName,waId);
            console.log("replyText : ",replyText)
            //  * sending new whatsapp message on basis of replayText response
            if(replyText.status==0){
                let temp = await this._whatsappService.sendMessage(replyText.data,from,phoneNumberId,userCred.token,'')
                let whatsappRes = temp.data;
                console.log(JSON.stringify(temp, null, 2));
                const replyId = whatsappRes.messages[0].id || "";
                // Insert bot reply
                await db.collection("whatsapp_sent_logs").insertMany([{wa_id: waId,from: "bot",message: replyText, timestamp: new Date(), message_id: replyId, source: "sent", type: "text",phone_number_id: phoneNumberId }]);
            }


            

            
            
            
        } catch (err) {
            console.error("Error:", err);
            res.status(500).json({ error: "Processing failed" });
        }