"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const routing_controllers_1 = require("routing-controllers");
const botServices_1 = require("./services/botServices");
const scriptHelper_1 = require("./scripts/scriptHelper");
const botCommonFunctions_1 = require("./botCommonFunctions/botCommonFunctions");
const util_1 = require("util");
const request = require("request");
const multer = require("multer");
const storage = multer.memoryStorage();
exports.upload = multer({ storage });
let config = require('../../../resource/config.json');
let { OAuth } = require('oauth');
let BotsController = class BotsController {
    constructor(botsService, scriptHelper, botCommonFunctions) {
        this.botsService = botsService;
        this.scriptHelper = scriptHelper;
        this.botCommonFunctions = botCommonFunctions;
    }
    saveBots(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            const param = req.headerParams;
            let saveResult = yield this.botsService.saveBots(body, param);
            return res.send({ status: saveResult.status, data: saveResult.data, message: saveResult.msg });
        });
    }
    deleteBots(id, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let deleteResult = yield this.botsService.deleteResult(id);
            return res.send({ status: deleteResult.status, data: deleteResult.data, message: deleteResult.msg });
        });
    }
    updateBots(id, req, res, body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let updateBots = yield this.botsService.updateBots(body, id);
            return res.send({ status: updateBots.status, data: updateBots.data, message: updateBots.msg });
        });
    }
    // @Authorized()
    // @Post('/botCommonFunction')
    // public async dynmaicBotCall(@Body() body: any, @Req() req: any, @Res() res: any) {
    //     if (!isNullOrUndefined(body) && !isNullOrUndefined(body['functionName'])) {
    //         const data = await this.botCommonFunctions[body['functionName']](body.input, body.output, body.botId, body.projectId, body.iterationId);
    //         return res.send({
    //             status: data.status,
    //             message: data.message,
    //             data: data.data
    //         })
    //     }
    // }
    getAllBots(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let deleteResult = yield this.botsService.getAllBots(body, req);
            return res.send({ status: deleteResult.status, data: deleteResult.data, message: deleteResult.msg, count: deleteResult.count });
        });
    }
    getAllBotsAdmin(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let deleteResult = yield this.botsService.getAllBotsAdmin(body, req);
            return res.send({ status: deleteResult.status, data: deleteResult.data, message: deleteResult.msg, count: deleteResult.count });
        });
    }
    getBots(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            const deleteResult = yield this.botsService.getBots(body, req);
            return res.send({ status: deleteResult.status, data: deleteResult.data, message: " deleteResult.msg" });
        });
    }
    getAllBotsFunction(req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let Result = yield this.botsService.getAllBotsFunction(req);
            return res.send({ status: Result.status, data: Result.data, message: Result.msg });
        });
    }
    botsiowrite(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let Result = yield this.botsService.insertBotIOInProject(req, body);
            return res.send({ status: Result.status, data: Result.data, message: Result.msg });
        });
    }
    getbotInputOutput(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let Result = yield this.botsService.getbotInputOutput(body);
            return res.send({ status: Result.status, data: Result.data, message: Result.msg });
        });
    }
    getOperationStatus(req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let Result = yield this.botsService.getOperationStatus();
            return res.send({ status: Result.status, data: Result.data, message: Result.msg });
        });
    }
    getBotsequenceNum(req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            const param = req.headerParams;
            let Result = yield this.botsService.getBotsequenceNumber(param);
            return res.send({ status: Result.status, data: Result.data, message: Result.msg });
        });
    }
    // @Post('/evaluateExpression')
    // public async evaluateExpression(@Body() body: any, @Req() req: any, @Res() res: any) {
    //     let Result = await this.botsService.evaluateExpression(body);
    //     return res.send({ status: Result.status, data: Result.data, message: Result.msg });
    // }
    // @Post('/botCommonFunction')
    // public async dynmaicBotCall(@Body() body: any, @Req() req: any, @Res() res: any) {
    //     if (!isNullOrUndefined(body) && !isNullOrUndefined(body['functionName'])) {
    //         const data = await this.botCommonFunctions[body['functionName']](body.input, body.output, body.botId, body.projectId, body.iterationId);
    //         return res.send({
    //             status: data.status,
    //             message: data.message,
    //             data: data.data
    //         })
    //     }
    // }
    fetchImage(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                const param = req.headerParams;
                let referNo = new Date().getTime().toString();
                param['referNo'] = referNo;
                let resSent = false;
                setTimeout(() => {
                    if (!resSent) {
                        res.send({
                            message: "Query is running",
                            status: 0,
                            data: {
                                referNo: referNo ? referNo : '',
                                status: "inProgress"
                            },
                        });
                        resSent = true;
                    }
                }, config.timeExceed ? config.timeExceed : 40000);
                let Result = yield this.botCommonFunctions.fetchImage(body, param);
                if (!resSent) {
                    resSent = true;
                    return res.send({ status: Result.status, data: Result.data, message: Result.message });
                }
                else {
                    return;
                }
            }
            catch (e) {
                console.log("err in controller--------", e);
                return res.send({ status: 1, data: {}, message: "Internal Server Error" });
            }
        });
    }
    checkImage(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                const param = req.headerParams;
                let Result = yield this.botCommonFunctions.checkfetchImage(body, param);
                return res.send({ status: Result.status, data: Result.data, message: Result.message });
            }
            catch (e) {
                console.log("err in controller--------", e);
                return res.send({ status: 1, data: {}, message: "Internal Server Error" });
            }
        });
    }
    emailTicketIsResolved(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let response = yield this.botsService.emailTicketIsResolved(req);
            return res.send(response);
        });
    }
    emailRaiseATicket(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let response = yield this.botsService.emailRaiseATicket(req);
            return res.send(response);
        });
    }
    getSummaryQuery(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let response = yield this.botsService.getSummaryQuery(req, body);
                return res.send(response);
            }
            catch (e) {
                console.log("err in controller--------", e);
                return res.send({ status: 1, data: {}, message: "Internal Server Error" });
            }
        });
    }
    extractionStatus(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let bodyData = req.body;
                let result = yield this.botsService.isExtractionCompleted(bodyData);
                return result;
            }
            catch (e) {
                console.log(e);
                return { error: e, msg: "Error while Uploading", status: 1 };
            }
        });
    }
    royalTechJSONAPI(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let bodyData = req.body;
                let result = yield this.botsService.royalTechJSONAPI(bodyData);
                return result;
            }
            catch (e) {
                console.log(e);
                return { error: e, msg: "Error while Uploading", status: 1 };
            }
        });
    }
    triggerProcess(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                console.log(body); // Logs the form data (non-file fields)
                console.log(req.files); // Logs the uploaded file (if any)
                let response = yield this.botsService.triggerProcess(body, req, res);
                console.log(response);
                return response;
            }
            catch (e) {
                console.log(e);
                return { error: e, msg: "Error while Uploading", status: 1 };
            }
        });
    }
    TwitterCallback(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            const { api_key, api_secret } = req.query;
            const host_name = req.rawHeaders[1];
            const oauth = new OAuth("https://api.twitter.com/oauth/request_token", "https://api.twitter.com/oauth/access_token", api_key, api_secret, "1.0A", `http://${host_name}/gibots-api/bots/auth/twitter/callback`, "HMAC-SHA1");
            const { oauth_verifier, oauth_token } = req.query;
            oauth.getOAuthAccessToken(oauth_token, null, oauth_verifier, (error, oauthAccessToken, oauthAccessTokenSecret, results) => {
                if (error) {
                    console.error('Error obtaining access token:', error);
                    res.status(500).send('Authentication failed');
                }
                else {
                    res.send(`
                <script>
                  window.opener.postMessage({
                    accessToken: '${oauthAccessToken}',
                    accessTokenSecret: '${oauthAccessTokenSecret}'
                  }, '${config.HostOrigin}');
                  window.close();
                </script>
              `);
                }
            });
        });
    }
    ;
    dynmaicBotCall(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            if(!body.input.return) {
            res.send({
                status: 0,
                message: "Acknowledeged",
                data: "Acknowledeged"
            });
            }
            let self = this;
            // await self.botsService.sleep(1000);
            if (!util_1.isNullOrUndefined(body) && !util_1.isNullOrUndefined(body['functionName'])) {
                console.log("<< <<< <<< --- ---- --- --- BEFORE  BOTCOMMONFUNCTIONS ----- ----- ----- >>>> >>>>> >>>> >>>> ");
                return yield new Promise((resolve, reject) => tslib_1.__awaiter(this, void 0, void 0, function* () {
                    body = yield self.botsService.getbotInputOutput(body);
                    let repsonse = yield self.botCommonFunctions[body['functionName']](body.input, body.output, body.botId, body.projectId, body.iterationId);
                    if (body.input.return && !util_1.isNullOrUndefined(repsonse) && !util_1.isNullOrUndefined(repsonse.status)) {
                        res.send({ status: "200", message: repsonse.message, data: repsonse.data });
                    } else if (!util_1.isNullOrUndefined(repsonse) && !util_1.isNullOrUndefined(repsonse.status)) {
                        console.log("<< <<< <<< --- ---- --- --- AFTER  BOTCOMMONFUNCTIONS ----- ----- ----- >>>> >>>>> >>>> >>>> ");
                        console.warn(" ----- ----- Body ------ --- ----- >>> >> ");
                        resolve(yield self.botsService.iowrite(repsonse, body));
                        // resolve(res.send({ status: 0, message: repsonse.message, data: repsonse.data }));
                    }
                }));
            }
            else {
                return yield self.botsService.iowrite({ status: 1, message: "No Function Name Found", data: {} }, body);
                //return res.send({ status: 1, message: "No Function Name Found", data: {} });
            }
        });
    }
    evaluateExpression(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let Result = yield this.botsService.evaluateExpression(body);
            return res.send({ status: Result.status, data: Result.data, message: Result.msg });
        });
    }
    getScanFieldApi(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let output = {};
            //const headerParams = req.headers;
            //console.log(JSON.stringify(headerParams));
            //let body = req.body;
            let Result = yield this.botCommonFunctions.decisionMakingBot(body, output, body.botId, body.projectId, body.iterationId);
            let outputData = { "isException": Result.data, 'statusCode': '200' };
            let taskData = { 'projectId': body['projectId'], 'botId': body['botId'], 'eventId': body['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': body['iterationId'] };
            let head = { 'authorization': body['token'], 'content-type': "application/json", "selectedorgid": body['selectedorgid'] };
            //"https://cuda-testing.gibots.com/gibots-api/orchestrator/botsiowrite"
            console.log(JSON.stringify(head), " ======>>>>>>>----------->>>>>>>> ", JSON.stringify(taskData));
            var options = {
                method: 'POST',
                url: "http://cuda-testing.gibots.com:1443/gibots-api/orchestrator/botsiowrite",
                headers: head,
                body: taskData,
                json: true
            };
            process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
            request(options, function (error, response, body) {
            });
        });
    }
    triggerProcesswithVariables(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let output = {};
            const param = req.headerParams;
            body['subscriberId'] = param['subscriberId'];
            body['userId'] = param['userId'];
            body['orgId'] = body['orgId'] ? body['orgId'] : param['orgId'];
            console.log(param, body);
            let Result = yield this.botCommonFunctions.triggerProcesswithVariables(body, output, null, null, 0);
            console.log(Result);
            return res.send(Result);
        });
    }
};
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "saveBots", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Delete('/:id'),
    tslib_1.__param(0, routing_controllers_1.Param('id')), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [String, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "deleteBots", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Put('/:id'),
    tslib_1.__param(0, routing_controllers_1.Param('id')), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()), tslib_1.__param(3, routing_controllers_1.Body()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [String, Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "updateBots", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/getBots123'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getAllBots", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/getBots1234'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getAllBotsAdmin", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/getBots'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getBots", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Get('/function'),
    tslib_1.__param(0, routing_controllers_1.Req()), tslib_1.__param(1, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getAllBotsFunction", null);
tslib_1.__decorate([
    routing_controllers_1.Post('/botsiowrite'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "botsiowrite", null);
tslib_1.__decorate([
    routing_controllers_1.Post('/get/botInputOutput'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getbotInputOutput", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Get('/operationStatus'),
    tslib_1.__param(0, routing_controllers_1.Req()), tslib_1.__param(1, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getOperationStatus", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Get('/botSequence/sequenceNum'),
    tslib_1.__param(0, routing_controllers_1.Req()), tslib_1.__param(1, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getBotsequenceNum", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/ImageGeneration'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "fetchImage", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/CheckImageGeneration'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "checkImage", null);
tslib_1.__decorate([
    routing_controllers_1.Get('/isResolved:id'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "emailTicketIsResolved", null);
tslib_1.__decorate([
    routing_controllers_1.Get('/raiseATicket:id'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "emailRaiseATicket", null);
tslib_1.__decorate([
    routing_controllers_1.Post('/getSummaryQuery'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getSummaryQuery", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/extractionStatus'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "extractionStatus", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/getJSON'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "royalTechJSONAPI", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/triggerProcess'),
    routing_controllers_1.UseBefore(exports.upload.any()),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "triggerProcess", null);
tslib_1.__decorate([
    routing_controllers_1.Get('/auth/twitter/callback'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "TwitterCallback", null);
tslib_1.__decorate([
    routing_controllers_1.Post('/botCommonFunction'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "dynmaicBotCall", null);
tslib_1.__decorate([
    routing_controllers_1.Post('/evaluateExpression'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "evaluateExpression", null);
tslib_1.__decorate([
    routing_controllers_1.Post('/getscanfield'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "getScanFieldApi", null);
tslib_1.__decorate([
    routing_controllers_1.Authorized(),
    routing_controllers_1.Post('/triggerProcesswithVariables'),
    tslib_1.__param(0, routing_controllers_1.Body()), tslib_1.__param(1, routing_controllers_1.Req()), tslib_1.__param(2, routing_controllers_1.Res()),
    tslib_1.__metadata("design:type", Function),
    tslib_1.__metadata("design:paramtypes", [Object, Object, Object]),
    tslib_1.__metadata("design:returntype", Promise)
], BotsController.prototype, "triggerProcesswithVariables", null);
BotsController = tslib_1.__decorate([
    routing_controllers_1.JsonController('/bots'),
    tslib_1.__metadata("design:paramtypes", [botServices_1.BotsService,
        scriptHelper_1.ScriptHelper,
        botCommonFunctions_1.botCommonFunctions])
], BotsController);
exports.BotsController = BotsController;
//# sourceMappingURL=botsController.js.map