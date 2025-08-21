"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const typedi_1 = require("typedi");
let msg = require('../../../../resource/messages.json');
const util_1 = require("util");
const bots = require("../models/bots");
const botFuctions = require("../models/botsFunction");
const botInputOutput_1 = require("../../botinputoutput/models/botInputOutput");
// import {project} from "../../project/models/project";
// import {process} from "../../process/models/process";
// import {entityStatuses} from "../../status/models/status";
const operation = require("../models/operationStatus");
const autoSequenceService_1 = require("../../auto-sequence/services/autoSequenceService");
const eventStatusService_1 = require("../../event-statuses/services/eventStatusService");
// import * as io from 'socket.io-client';
// import { project } from "../../project/models/project";
// let config = require('../../../../resource/config.json');
const eventService_1 = require("../../event/services/eventService");
const projectService_1 = require("../../project/services/projectService");
const processService_1 = require("../../process/services/processService");
const Logger_1 = require("../../../../decorators/Logger");
const bot_errors_1 = require("../../bot-errors/helpers/bot-errors");
const botCommonFunctions_1 = require("../botCommonFunctions/botCommonFunctions");
const subcriber_1 = require("../../../controllers/subscriber/models/subcriber");
const env_1 = require("../../../../env");
const db = require('../../../../mongooseClient').default;
let fetch = require('node-fetch');
// import * as mongoose from "mongoose";
// import * as mongoose from "mongoose";
let request = require("request");
let ObjectId = require('mongodb').ObjectId;
const fs = require("fs");
var bytes = require('utf8-length');
let BotsService = class BotsService {
    //  private socket;
    constructor(botCommonFunctions) {
        this.botCommonFunctions = botCommonFunctions;
        this.autoSequenceService = typedi_1.Container.get(autoSequenceService_1.AutoSequenceService);
        this.eventStatusService = typedi_1.Container.get(eventStatusService_1.EventStatusService);
        //  this.socket = io.connect(config.urlLink, { secure: true });
        this.eventService = typedi_1.Container.get(eventService_1.EventService);
        this.projectService = typedi_1.Container.get(projectService_1.ProjectService);
        this.processService = typedi_1.Container.get(processService_1.ProcessService);
        this.botErrorsService = typedi_1.Container.get(bot_errors_1.BotErrors);
    }
    saveBots(body, param) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let findDuplicateBots = yield bots.find({ taskTitle: body.taskTitle });
                if (!util_1.isNullOrUndefined(findDuplicateBots) && findDuplicateBots.length > 0) {
                    return ({ status: 1, err: null, data: [], msg: msg.botsMessage.duplicateBot });
                }
                else {
                    let bostSchema = new bots(body);
                    bostSchema.userId = param.userId;
                    bostSchema.subscriberId = param.subscriberId;
                    bostSchema.gstin = param.gstin;
                    let result = yield bostSchema.save();
                    return ({ status: 0, err: null, data: result, msg: msg.botsMessage.botSavedSuccess });
                }
            }
            catch (err) {
                return ({ status: 1, err: err, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    deleteResult(id) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let result = yield bots.findOneAndUpdate({ _id: id }, { $set: { isDeleted: true } }, { new: true });
                return ({ status: 0, err: null, data: result, msg: msg.botsMessage.deleteSuccess });
            }
            catch (err) {
                return ({ status: 1, err: err, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    updateBots(body, id) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let findDuplicateBots = yield bots.find({ _id: { $nin: [ObjectId(id)] }, taskTitle: body.taskTitle });
                if (!util_1.isNullOrUndefined(findDuplicateBots) && findDuplicateBots.length > 0) {
                    return ({ status: 1, err: null, data: [], msg: msg.botsMessage.duplicateBot });
                }
                else {
                    const reportRes = yield bots.findOneAndUpdate({ _id: id }, body, { new: true });
                    return ({ status: 0, err: null, data: reportRes, msg: msg.botsMessage.updateSuccess });
                }
            }
            catch (err) {
                return ({ status: 1, err: err, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    getAllBotsAdmin(body, req) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                if (!util_1.isNullOrUndefined(body.first) && !util_1.isNullOrUndefined(body.rows) && body.first !== "" && body.rows > 0) {
                    let findDuplicateBots = yield bots.aggregate([{ "$match": { isNotification: body.isNotification, isDeleted: false } },
                        {
                            $group: {
                                _id: null,
                                count: { $sum: 1 },
                                taskList: { $push: '$$ROOT' }
                            }
                        },
                        { $unwind: '$taskList' },
                        {
                            $project: {
                                count: "$count",
                                _id: "$taskList._id",
                                userId: "$taskList.userId",
                                subscriberId: "$taskList.subscriberId",
                                orgId: "$taskList.orgId",
                                gstin: "$taskList.gstin",
                                taskTitle: "$taskList.taskTitle",
                                taskDesc: "$taskList.taskDesc",
                                category: "$taskList.category",
                                botCategory: "$taskList.botCategory",
                                parentId: "$taskList.parentId",
                                functionName: "$taskList.functionName",
                                inputParameters: "$taskList.inputParameters",
                                outputParameters: "$taskList.outputParameters",
                                uiComponent: "$taskList.uiComponent",
                                templateId: "$taskList.templateId",
                                isDeleted: "$taskList.isDeleted",
                                isRemote: "$taskList.isRemote",
                                remoteUrl: "$taskList.remoteUrl",
                                isNotification: "$taskList.isNotification",
                                isAddInfo: "$taskList.isAddInfo",
                                isReports: "$taskList.isReports",
                                botShape: "$taskList.botShape",
                                isRecorder: "$taskList.isRecorder",
                            }
                        },
                        { $skip: body.first }, { $limit: body.rows },
                    ]).allowDiskUse(true).exec();
                    if (!util_1.isNullOrUndefined(findDuplicateBots) && findDuplicateBots.length > 0) {
                        this.log.info("bot data found");
                        return ({ status: 0, data: findDuplicateBots, count: findDuplicateBots[0].count, msg: msg.botsMessage.botsFound });
                    }
                    else {
                        this.log.info("bot data not found");
                        return ({ status: 1, data: [], msg: msg.botsMessage.botNotFound });
                    }
                }
                else {
                    return ({ status: 1, data: [], msg: "first and limit is not found" });
                }
            }
            catch (err) {
                this.log.info("internal server error" + err);
                return ({ status: 1, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    getAllBots(body, req) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let headerParams = req.headerParams;
                if (!util_1.isNullOrUndefined(body.first) && !util_1.isNullOrUndefined(body.rows) && body.first !== "" && body.rows > 0) {
                    let searchText = !util_1.isNullOrUndefined(body.text) ? body.text : '';
                    let myQuery = [
                        { "$match": { "_id": ObjectId(headerParams.subscriberId) } },
                        {
                            "$unwind": {
                                "path": "$packages",
                                "includeArrayIndex": "arrayIndex",
                                "preserveNullAndEmptyArrays": false
                            }
                        },
                        {
                            "$lookup": {
                                "from": "products",
                                "localField": "packages",
                                "foreignField": "_id",
                                "as": "pack"
                            }
                        },
                        {
                            "$unwind": {
                                "path": "$pack",
                                "includeArrayIndex": "arrayIndex",
                                "preserveNullAndEmptyArrays": false
                            }
                        },
                        {
                            "$unwind": {
                                "path": "$pack.BotsList",
                                "includeArrayIndex": "arrayIndex",
                                "preserveNullAndEmptyArrays": false
                            }
                        },
                        {
                            "$lookup": {
                                "from": "bots",
                                "localField": "pack.BotsList",
                                "foreignField": "_id",
                                "as": "final"
                            }
                        },
                        {
                            "$unwind": {
                                "path": "$final",
                                "includeArrayIndex": "arrayIndex",
                                "preserveNullAndEmptyArrays": false
                            }
                        },
                        {
                            "$match": {
                                "final.taskTitle": { $regex: searchText, $options: 'i' }
                            }
                        },
                        {
                            "$project": {
                                count: "$final.count",
                                _id: "$final._id",
                                userId: "$final.userId",
                                subscriberId: "$final.subscriberId",
                                orgId: "$final.orgId",
                                gstin: "$final.gstin",
                                taskTitle: "$final.taskTitle",
                                taskDesc: "$final.taskDesc",
                                category: "$final.category",
                                botCategory: "$final.botCategory",
                                parentId: "$final.parentId",
                                functionName: "$final.functionName",
                                inputParameters: "$final.inputParameters",
                                outputParameters: "$final.outputParameters",
                                uiComponent: "$final.uiComponent",
                                templateId: "$final.templateId",
                                isDeleted: "$final.isDeleted",
                                isRemote: "$final.isRemote",
                                remoteUrl: "$final.remoteUrl",
                                isNotification: "$final.isNotification",
                                isAddInfo: "$final.isAddInfo",
                                isReports: "$final.isReports",
                                botShape: "$final.botShape",
                                isRecorder: "$final.isRecorder",
                            }
                        },
                        { "$skip": body.first }, { "$limit": body.rows },
                    ];
                    let Bots = yield subcriber_1.Subscriber.aggregate(myQuery).allowDiskUse(true).exec();
                    if (!util_1.isNullOrUndefined(Bots) && Bots.length > 0) {
                        this.log.info("bot data found");
                        return ({ status: 0, data: Bots, count: Bots[0].count, msg: msg.botsMessage.botsFound });
                    }
                    else {
                        this.log.info("bot data not found");
                        return ({ status: 1, data: [], msg: msg.botsMessage.botNotFound });
                    }
                }
                else {
                    return ({ status: 1, data: [], msg: "first and limit is not found" });
                }
            }
            catch (err) {
                this.log.info("internal server error" + err);
                return ({ status: 1, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    searchParameter(searchText) {
        let text = {};
        try {
            if (!util_1.isNullOrUndefined(searchText) && searchText !== '') {
                text = {
                    $or: [
                        {
                            taskTitle: {
                                $regex: searchText,
                                $options: '$i',
                            }
                        },
                        {
                            taskDesc: {
                                $regex: searchText,
                                $options: '$i',
                            }
                        },
                        {
                            functionName: {
                                $regex: searchText,
                                $options: '$i',
                            }
                        },
                    ]
                };
            }
            return { text: text };
        }
        catch (err) {
            this.log.info("internal server error" + err);
            return ({ status: 1, data: [], msg: msg.botsMessage.internalServerError });
        }
    }
    getBots(body, req) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let searchText = !util_1.isNullOrUndefined(body.text) ? body.text : '';
                const searchFilter = yield this.getSearchParameter(searchText);
                const findDuplicateBots = yield bots.aggregate([{ "$match": { isDeleted: false } },
                    {
                        "$match": searchFilter.text
                    },
                    {
                        $project: {
                            _id: "$_id",
                            userId: "$userId",
                            subscriberId: "$subscriberId",
                            orgId: "$orgId",
                            gstin: "$gstin",
                            taskTitle: "$taskTitle",
                            taskDesc: "$taskDesc",
                            category: "$category",
                            botCategory: "$botCategory",
                            parentId: "$parentId",
                            functionName: "$functionName",
                            inputParameters: "$inputParameters",
                            outputParameters: "$outputParameters",
                            uiComponent: "$uiComponent",
                            templateId: "$templateId",
                            isDeleted: "$isDeleted",
                            isRemote: "$isRemote",
                            remoteUrl: "$remoteUrl",
                            isNotification: "$isNotification",
                            isAddInfo: "$isAddInfo",
                            isReports: "$isReports",
                            botShape: "$botShape",
                            isRecorder: "$isRecorder",
                            createdAt: "$createdAt"
                        }
                    }
                ]).sort({ "createdAt": -1 });
                if (!util_1.isNullOrUndefined(findDuplicateBots) && findDuplicateBots.length > 0) {
                    this.log.info("bot data found");
                    return ({ status: 0, data: findDuplicateBots, msg: msg.botsMessage.botsFunctionFound });
                }
                else {
                    this.log.info("bot data not found");
                    return ({ status: 1, data: [], msg: msg.botsMessage.botsFunctionNotFound });
                }
            }
            catch (err) {
                this.log.error("Internal Server Error" + err);
                return ({ status: 1, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    sendMail(ticketId) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let ticket = yield db.collection("emails").findOne({ tickectId: ticketId });
                ticket = JSON.parse(JSON.stringify(ticket));
                let emailHtml = `<div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #2c3e50; text-align: center;">Thank You for Using Our AI Agent</h2>
                <p style="font-size: 16px; line-height: 1.5; color: #555;">Dear User,</p>
                <p style="font-size: 16px; line-height: 1.5; color: #555;">Thank you for using our AI agent. We're glad to hear that your issue has been resolved! If you need any further assistance, don't hesitate to reach out.</p>
                <p style="font-size: 16px; line-height: 1.5; color: #555;">We strive to provide excellent service, and your feedback is greatly appreciated.</p>
                <p style="font-size: 16px; line-height: 1.5; color: #555;">Best regards,</p>
                <p style="font-size: 16px; color: #555;">The AI Support Team</p>
                <hr style="border: 1px solid #eee;">
                <p style="font-size: 14px; color: #aaa; text-align: center;">If you have any further questions, feel free to reply to this email.</p>
            </div>`;
                let input = {
                    from: "No-Reply@aiqod.com",
                    user: "No-Reply@aiqod.com",
                    to: ticket.from,
                    subject: ticket.subject,
                    text: "",
                    service: "gmail",
                    html: emailHtml,
                    messageId: ticket.messageId,
                    pass: "QUlRb0RAMjAxNg=="
                };
                this.botCommonFunctions.emailNotify(input, {}, "", "", "");
            }
            catch (e) {
                this.log.error("Internal Server Error in send MAil" + e);
            }
        });
    }
    emailTicketIsResolved(req) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let ticketId = req.params.id;
                ticketId = ticketId.substring(1);
                let isClosed = yield db.collection("emails").findOne({ tickectId: ticketId }, { status: 1, _id: 0 });
                isClosed = JSON.parse(JSON.stringify(isClosed));
                if (util_1.isNullOrUndefined(isClosed)) {
                    return { status: 0, data: [], msg: "Not a valid Ticket ID" };
                }
                if (isClosed.status == "Closed") {
                    return { status: 0, data: [], msg: "Ticket is already CLosed" };
                }
                if (isClosed.status == "Esclated") {
                    return { status: 0, data: [], msg: "Ticket is already Esclated" };
                }
                let result = yield db.collection("emails").update({ tickectId: ticketId }, { $set: { 'status': "Closed" } });
                result = JSON.parse(JSON.stringify(result));
                this.sendMail(ticketId);
                console.log(result);
                return { status: 0, data: [], msg: "Ticket is CLosed" };
            }
            catch (e) {
                return { status: 1, data: [], msg: "Ticket is not CLosed" };
            }
        });
    }
    helperRaiseTicket(result) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let userDetails = yield db.collection("users").findOne({ 'personalInfo.email': result.from }, { personalInfo: 1 });
                userDetails = JSON.parse(JSON.stringify(userDetails));
                let options = {
                    "additionalInfo": [
                        {
                            "addToTaskList": false,
                            "name": "User",
                            "required": false,
                            "label": "User",
                            "value": userDetails.personalInfo.name || "",
                            "id": "0"
                        },
                        {
                            "addToTaskList": false,
                            "name": "sender_email",
                            "required": false,
                            "label": "sender_email",
                            "value": result.from || "",
                            "id": "0"
                        },
                        {
                            "addToTaskList": false,
                            "name": "task_description",
                            "required": false,
                            "label": "task_description",
                            "value": result.body,
                            "id": "1"
                        },
                        {
                            "addToTaskList": false,
                            "name": "task_title",
                            "required": false,
                            "label": "task_title",
                            "value": result.subject,
                            "id": "2"
                        },
                        {
                            "addToTaskList": false,
                            "name": "message_Id",
                            "required": false,
                            "label": "message_Id",
                            "value": result.messageId,
                            "id": "3"
                        }
                    ],
                    "customerId": "5b8fd401b3930517f134c569",
                    "processId": "67729c4be8ea3efa77dfa768",
                    "projectId": "67729c4be8ea3efa77dfa76f",
                    "taskDesc": "",
                    "projectName": "Trigger Process",
                    "username": "Admin",
                    "accessControlList": [
                        {
                            "permissionsList": {
                                "execute": true,
                                "view": true,
                                "edit": true,
                                "add": true
                            },
                            "controlType": "users",
                            "controlName": "Admin",
                            "controlId": "5beaabd82ac6767c86dc311e",
                            "_id": "67729c4be8ea3efa77dfa76a"
                        },
                        {
                            "permissionsList": {
                                "execute": true,
                                "view": true,
                                "edit": true,
                                "add": true
                            },
                            "controlType": "users",
                            "controlName": "Deepa",
                            "controlId": "66eac67c4b94159b93983810",
                            "_id": "67729c4be8ea3efa77dfa769"
                        }
                    ]
                };
                let token = yield this.botCommonFunctions.createToken(result.userId, result.subscriberId, result.orgId);
                console.log(options);
                let res_orch = yield fetch(process.env.gibots_orch + "gibots-orch/event/addExecute/task", {
                    method: 'POST',
                    body: JSON.stringify(options),
                    headers: {
                        "selectedorgid": result.orgId,
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                });
                res_orch = yield res_orch.json();
                console.log(res_orch);
                return res_orch;
            }
            catch (error) {
                this.log.error("Internal Server Error in Helper Raise Ticket" + error);
                return { status: 1, data: [], msg: "Internal Server Error in Helper Raise Ticket" };
            }
        });
    }
    triggerProcess(body, req, res) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            let fetch = require('node-fetch');
            let FormData = require('form-data');
            // const https = require('https');
            // const agent = new https.Agent({ rejectUnauthorized: false });
            // const util = require('util');
            try {
                const token = req.headers.authorization ? req.headers.authorization.split(' ')[1] : null;
                if (!token) {
                    return res.status(400).send({ error: 'Authorization token is missing' });
                }
                const formData = new FormData();
                const filesGroupedByFieldname = {};
                for (const file of req.files) {
                    if (!filesGroupedByFieldname[file.fieldname]) {
                        filesGroupedByFieldname[file.fieldname] = [];
                    }
                    filesGroupedByFieldname[file.fieldname].push(file);
                }
                for (const fieldname in filesGroupedByFieldname) {
                    const files = filesGroupedByFieldname[fieldname];
                    for (const file of files) {
                        if (file.buffer) {
                            formData.append(fieldname, file.buffer, { filename: file.originalname });
                        }
                        else {
                            throw new Error(`File buffer is undefined for file: ${file.originalname}`);
                        }
                    }
                }
                for (const key in req.body) {
                    formData.append(key, req.body[key]);
                }
                const response = yield fetch(`${process.env.adhigam_api}adhigam-api/mapper/scan/multi`, {
                    method: 'POST',
                    body: formData,
                    headers: Object.assign({}, formData.getHeaders(), req.headerParams, { Authorization: `Bearer ${token}` }),
                });
                const responseData = yield response.json();
                const { JobType, PdfClientName } = body;
                if (util_1.isNullOrUndefined(PdfClientName)) {
                    return { error: "The PdfClientName is not expected But Provided", msg: "Error while Uploading" };
                }
                let processDetails;
                if (JobType == "IMP") {
                    processDetails = {
                        "projectId": "6835aaad4e46967727f5e246",
                        "processId": "6835aaad4e46967727f5e23b",
                        "projectName": "Import  API",
                    };
                }
                else if (JobType == "EXP") {
                    processDetails = {
                        "projectName": "Export  API",
                        "projectId": "6835ab034e46967727f5e294",
                        "processId": "6835ab034e46967727f5e289",
                    };
                }
                else {
                    return { error: "The Job Type is not expected", msg: "Error while Uploading" };
                }
                let resArr = [];
                responseData.data.forEach((data) => tslib_1.__awaiter(this, void 0, void 0, function* () {
                    let task = {
                        "additionalInfo": [
                            {
                                "id": "0",
                                "value": data.fileRefNum,
                                "label": "ref_no",
                                "required": false,
                                "name": "ref_no",
                                "addToTaskList": false
                            },
                            {
                                "id": "0",
                                "value": data.filePath,
                                "label": "orgfilePath",
                                "required": false,
                                "name": "orgfilePath",
                                "addToTaskList": false
                            },
                            {
                                "id": "0",
                                "value": PdfClientName,
                                "label": "Document",
                                "required": false,
                                "name": "Document",
                                "addToTaskList": false
                            }
                        ],
                        "customerId": "5b8fd401b3930517f134c569",
                        "processId": processDetails.processId,
                        "projectId": processDetails.projectId,
                        "taskDesc": "",
                        "projectName": processDetails.projectName,
                        "username": "Royal Tech Manager",
                        "accessControlList": [
                            {
                                "_id": "67107e6b850795c52d77411f",
                                "controlId": "5beaabd82ac6767c86dc311e",
                                "controlName": "Admin",
                                "controlType": "users",
                                "permissionsList": {
                                    "add": true,
                                    "edit": true,
                                    "view": true,
                                    "execute": true
                                }
                            },
                            {
                                "_id": "67ed12a55101ea3ca4446f69",
                                "controlId": "67ed114950023d3c8c0ef91d",
                                "controlName": "Royal Tech Manager",
                                "controlType": "users",
                                "permissionsList": {
                                    "add": true,
                                    "edit": true,
                                    "view": true,
                                    "execute": true
                                }
                            }
                        ],
                    };
                    let res_orch = yield fetch(process.env.gibots_orch + "gibots-orch/event/addExecute/task", {
                        method: 'POST',
                        body: JSON.stringify(task),
                        headers: {
                            "selectedorgid": "662b515be421fedde2247c47",
                            Authorization: `Bearer ${token}`,
                            "Content-Type": "application/json"
                        }
                    });
                    res_orch = yield res_orch.json();
                    resArr.push(res_orch);
                    console.log(res_orch);
                }));
                console.log(resArr);
                return { status: 0, data: responseData, msg: "Uploaded Successfully" };
            }
            catch (e) {
                console.error(e);
                return { status: 1, error: e, msg: "Error while Uploading" };
            }
        });
    }
    isExtractionCompleted(bodyData) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let referenceNo = bodyData.referenceNo;
                let result = yield db.collection('filequeues').findOne({ "fileRefNum": referenceNo }, { fileRefNum: 1, fileName: 1, status: 1, _id: 0 });
                result = JSON.parse(JSON.stringify(result));
                console.log("result from the adiswan extraction  ", result);
                if (!util_1.isNullOrUndefined(result)) {
                    return { info: 'Data fetched successfully', status: 0, data: result };
                }
                else {
                    return { info: 'Data not found', status: 1, data: result };
                }
            }
            catch (err) {
                return { info: 'Data not found', status: 1, data: [] };
            }
        });
    }
    royalTechJSONAPI(bodyData) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let referenceNo = bodyData.referenceNo;
                let result = yield db.collection('documents').findOne({ "fileRefNum": referenceNo }, { name: 1, _id: 0 });
                result = JSON.parse(JSON.stringify(result));
                console.log("result from the adiswan extraction  ", result);
		console.log("Boolean !util_1.isNullOrUndefined(result) ",!util_1.isNullOrUndefined(result))
                if (!util_1.isNullOrUndefined(result)) {
                    let fileURL = process.env.fileURL + result.name;
                    let res_orch = yield fetch(fileURL, {
                        method: 'GET',
                        headers: {
                            "Content-Type": "application/json"
                        }
                    });
                    res_orch = yield res_orch.json();
                    return { info: 'Data fetched successfully', status: 0, url: fileURL, json: res_orch };
                }
                else {
                    return { info: 'Data not found', status: 1, data: [] };
                }
            }
            catch (err) {
                return { info: 'Data not found', status: 1, data: [] };
            }
        });
    }
    getSummaryQuery(req, body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let description = body.description;
                let orgId = body.orgid;
                let subscriberId = body.subscriberId;
                let query = `Summarize the following user query in English. If the description is in Odia, translate it to English first. Provide a 2-3 line summary in English in the following JSON format: {'output':{\"summary\": \"\"}}. Description: ${description}`;
                let response = yield this.botCommonFunctions.callopenAI(query, orgId, subscriberId, 'Chat Genie');
                console.log(response);
                return { status: 0, data: response, msg: "Query Fethched" };
            }
            catch (e) {
                return { status: 1, data: [], msg: "Internal Server Error in getSummaryQuery" };
            }
        });
    }
    emailRaiseATicket(req) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let ticketId = req.params.id;
                ticketId = ticketId.substring(1);
                let isClosed = yield db.collection("emails").findOne({ tickectId: ticketId });
                isClosed = JSON.parse(JSON.stringify(isClosed));
                if (util_1.isNullOrUndefined(isClosed)) {
                    return { status: 0, data: [], msg: "Not a valid Ticket ID" };
                }
                if (isClosed.status == "Esclated") {
                    return { status: 0, data: [], msg: "Ticket is already Esclated" };
                }
                if (isClosed.status == "Closed") {
                    return { status: 0, data: [], msg: "Ticket is already CLosed" };
                }
                let res = yield this.helperRaiseTicket(isClosed);
                if (res.status == 0) {
                    let result = yield db.collection("emails").findOneAndUpdate({ tickectId: ticketId }, { $set: { 'status': "Esclated" } });
                    result = JSON.parse(JSON.stringify(result));
                    return { status: 0, data: [], msg: "ticket is raised" };
                }
                else {
                    return { status: 1, data: [], msg: "Ticket Is not raised" };
                }
            }
            catch (e) {
                return { status: 1, data: [], msg: "Ticket is not Raised, Internal Server Error" };
            }
        });
    }
    getSearchParameter(searchText) {
        let text = {};
        try {
            if (!util_1.isNullOrUndefined(searchText) && searchText !== '') {
                text = {
                    $or: [
                        {
                            taskTitle: {
                                $regex: searchText,
                                $options: '$i',
                            }
                        },
                        {
                            taskDesc: {
                                $regex: searchText,
                                $options: '$i',
                            }
                        },
                        {
                            functionName: {
                                $regex: searchText,
                                $options: '$i',
                            }
                        },
                    ]
                };
            }
            return { text: text };
        }
        catch (err) {
            this.log.info("internal server error" + err);
            return ({ status: 1, data: [], msg: msg.botsMessage.internalServerError });
        }
    }
    getAllBotsFunction(req) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let result = yield botFuctions.find({});
                if (!util_1.isNullOrUndefined(result) && result.length > 0) {
                    return ({ status: 0, err: null, data: result, msg: msg.botsMessage.botsFunctionFound });
                }
                else {
                    return ({ status: 1, err: null, data: [], msg: msg.botsMessage.botsFunctionNotFound });
                }
            }
            catch (err) {
                return ({ status: 1, err: err, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    insertBotIOInProject(req, body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let self = this;
                let headerParams = req.headerParams;
                let parseOnFailedTaskdata;
                console.info("Body ======>>>>>>>>>", JSON.stringify(body));
                if (!util_1.isNullOrUndefined(body.projectId)) {
                    let OutPut = yield botInputOutput_1.botInputOutput.findOne({ $or: [{ eventId: body.eventId }, { parentEventId: body.eventId }], projectId: body.projectId, botId: body.botId, isDeleted: false, iterationId: body.iterationId }, { _id: 0 }).lean();
                    let botOutPut = JSON.parse(JSON.stringify(OutPut));
                    if (!util_1.isNullOrUndefined(botOutPut)) {
                        if (!util_1.isNullOrUndefined(botOutPut.outputParameters) && botOutPut.outputParameters.length > 0) {
                            // if (!isNullOrUndefined(botOutPut.outputParameters)) {
                            //     if (botOutPut.outputParameters.length > 0) {
                            //         botOutPut.outputParameters.forEach(function (op) {
                            //             body.outputParameters.forEach(function (bodyOutPut) {
                            //                 if (!isNullOrUndefined(op.name) && !isNullOrUndefined(bodyOutPut.name) && bodyOutPut.name.toLowerCase() == op.name.toLowerCase()) {
                            //                     op['value'] = !isNullOrUndefined(bodyOutPut) && !isNullOrUndefined(bodyOutPut.value) ? bodyOutPut.value : "";
                            //                 }
                            //             });
                            //         });
                            //     }
                            // }
                            let parsedTaskData;
                            let task = yield self.eventStatusService.getEventStatusInfo(body.projectId, body.eventId, body.botId);
                            parsedTaskData = JSON.parse(JSON.stringify(task.data));
                            let projectVariableList = [], processVariableList = [], taskVariableList = [], parentProjectVariableList = [], parentProcessVariableList = [], parentTaskVariableList = [];
                            if (!util_1.isNullOrUndefined(parsedTaskData.outputBotMappingList) && parsedTaskData.outputBotMappingList.length > 0) {
                                const projectData = yield this.projectService.getProjectDetails(headerParams, body.projectId);
                                const processInfo = yield this.processService.getProcessById(parsedTaskData.processId, headerParams);
                                const eventInfo = yield this.eventService.getEventDetailsById(body.eventId, headerParams);
                                let eventInfoParse = JSON.parse(JSON.stringify(eventInfo.data));
                                projectVariableList = projectData.data.variableList;
                                processVariableList = processInfo.data.variableList;
                                taskVariableList = eventInfoParse.variableList;
                                if (parsedTaskData.hasOwnProperty('parentProjectId')) {
                                    if (util_1.isNullOrUndefined(parsedTaskData.parentEventId) && parsedTaskData.isDependent) {
                                        parsedTaskData['parentEventId'] = body.parentEventId;
                                    }
                                    const parentProjectData = yield this.projectService.getProjectDetails(headerParams, parsedTaskData.parentProjectId);
                                    const parentProcessInfo = yield this.processService.getProcessById(parsedTaskData.parentProcessId, headerParams);
                                    const parentEventInfo = yield this.eventService.getEventDetailsById(parsedTaskData.parentEventId, headerParams);
                                    let parentEventInfoParse = JSON.parse(JSON.stringify(parentEventInfo.data));
                                    if (!util_1.isNullOrUndefined(parentProjectData.data)) {
                                        parentProjectVariableList = parentProjectData.data.variableList;
                                    }
                                    if (!util_1.isNullOrUndefined(parentProcessInfo.data)) {
                                        parentProcessVariableList = parentProcessInfo.data.variableList;
                                    }
                                    if (!util_1.isNullOrUndefined(parentEventInfoParse)) {
                                        parentTaskVariableList = parentEventInfoParse.variableList;
                                    }
                                }
                            }
                            if (!util_1.isNullOrUndefined(botOutPut.outputParameters)) {
                                if (botOutPut.outputParameters.length > 0) {
                                    for (const op of botOutPut.outputParameters) {
                                        if (body.outputParameters.hasOwnProperty(op.name) || body.outputParameters['statusCode'] !== '200') {
                                            op['value'] = body.outputParameters[op.name];
                                            op['statusCode'] = body.outputParameters['statusCode'];
                                            op['errorMessage'] = body.outputParameters['errorMessage'];
                                            op['exception'] = body.outputParameters['exception'];
                                        }
                                        if (!util_1.isNullOrUndefined(parsedTaskData.outputBotMappingList) && parsedTaskData.outputBotMappingList.length > 0) {
                                            for (const opInner of parsedTaskData.outputBotMappingList) {
                                                if (opInner.category === 'project') {
                                                    if (op.name === opInner.label) {
                                                        if (!util_1.isNullOrUndefined(parsedTaskData) && parsedTaskData.hasOwnProperty('parentProjectId') && !parsedTaskData.isDependent) {
                                                            if (!util_1.isNullOrUndefined(parentProjectVariableList) && parentProjectVariableList.length > 0) {
                                                                for (const opInnerInner of parentProjectVariableList) {
                                                                    if (opInnerInner.name === opInner.value) {
                                                                        if (opInnerInner.dataType == 'Array') {
                                                                            if (op['value'] == "" || !Array.isArray(op['value'])) {
                                                                                op['value'] = [];
                                                                            }
                                                                            op['value'].push(body.outputParameters[op.name]);
                                                                        }
                                                                        else {
                                                                            op['value'] = body.outputParameters[op.name];
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        if (!util_1.isNullOrUndefined(projectVariableList) && projectVariableList.length > 0) {
                                                            for (const opInnerInner of projectVariableList) {
                                                                if (opInnerInner.name === opInner.value) {
                                                                    if (opInnerInner.dataType == 'Array') {
                                                                        if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                            opInnerInner['value'] = [];
                                                                        }
                                                                        opInnerInner['value'].push(body.outputParameters[op.name]);
                                                                    }
                                                                    else {
                                                                        opInnerInner['value'] = body.outputParameters[op.name];
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                                else if (opInner.category === 'process') {
                                                    if (op.name === opInner.label) {
                                                        if (!util_1.isNullOrUndefined(parsedTaskData) && parsedTaskData.hasOwnProperty('parentProjectId') && !parsedTaskData.isDependent) {
                                                            if (!util_1.isNullOrUndefined(parentProcessVariableList) && parentProcessVariableList.length > 0) {
                                                                for (const opInnerInner of parentProcessVariableList) {
                                                                    if (opInnerInner.name === opInner.value) {
                                                                        if (opInnerInner.dataType == 'Array') {
                                                                            if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                                opInnerInner['value'] = [];
                                                                            }
                                                                            opInnerInner['value'].push(body.outputParameters[op.name]);
                                                                        }
                                                                        else {
                                                                            opInnerInner['value'] = body.outputParameters[op.name];
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        if (!util_1.isNullOrUndefined(processVariableList) && processVariableList.length > 0) {
                                                            for (const opInnerInner of processVariableList) {
                                                                if (opInnerInner.name === opInner.value) {
                                                                    if (opInnerInner.dataType == 'Array') {
                                                                        if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                            opInnerInner['value'] = [];
                                                                        }
                                                                        opInnerInner['value'].push(body.outputParameters[op.name]);
                                                                    }
                                                                    else {
                                                                        opInnerInner['value'] = body.outputParameters[op.name];
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                                else if (opInner.category === 'task') {
                                                    if (op.name === opInner.label || op.name === opInner.displayName) {
                                                        if (!util_1.isNullOrUndefined(parsedTaskData) && parsedTaskData.hasOwnProperty('parentProjectId') && parsedTaskData.isDependent) {
                                                            if (!util_1.isNullOrUndefined(parentTaskVariableList) && parentTaskVariableList.length > 0) {
                                                                for (const opInnerInner of parentTaskVariableList) {
                                                                    if (opInnerInner.name === opInner.value) {
                                                                        if (self.parseDate(body.outputParameters[op.name]) && op.dataType == 'date') {
                                                                            if (opInnerInner.dataType == "Array") {
                                                                                if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                                    opInnerInner['value'] = [];
                                                                                }
                                                                                opInnerInner['value'].push(new Date(body.outputParameters[op.name]));
                                                                            }
                                                                            else {
                                                                                opInnerInner['value'] = new Date(body.outputParameters[op.name]);
                                                                            }
                                                                            opInnerInner['value'] = new Date(body.outputParameters[op.name]);
                                                                        }
                                                                        else {
                                                                            if (opInnerInner.dataType == "Array") {
                                                                                if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                                    opInnerInner['value'] = [];
                                                                                }
                                                                                opInnerInner['value'].push(body.outputParameters[op.name]);
                                                                            }
                                                                            else {
                                                                                opInnerInner['value'] = body.outputParameters[op.name];
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        if (!util_1.isNullOrUndefined(taskVariableList) && taskVariableList.length > 0) {
                                                            for (const opInnerInner of taskVariableList) {
                                                                if (opInnerInner.name === opInner.value) {
                                                                    if (self.parseDate(body.outputParameters[op.name]) && op.dataType == 'date') {
                                                                        if (opInnerInner.dataType == 'Array') {
                                                                            if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                                opInnerInner['value'] = [];
                                                                            }
                                                                            opInnerInner['value'].push(new Date(body.outputParameters[op.name]));
                                                                        }
                                                                        else {
                                                                            opInnerInner['value'] = new Date(body.outputParameters[op.name]);
                                                                        }
                                                                        opInnerInner['value'] = new Date(body.outputParameters[op.name]);
                                                                    }
                                                                    else {
                                                                        if (opInnerInner.dataType == "Array") {
                                                                            if (opInnerInner['value'] == "" || !Array.isArray(opInnerInner['value'])) {
                                                                                opInnerInner['value'] = [];
                                                                            }
                                                                            opInnerInner['value'].push(body.outputParameters[op.name]);
                                                                        }
                                                                        else {
                                                                            opInnerInner['value'] = body.outputParameters[op.name];
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            if (!util_1.isNullOrUndefined(body.status) && body.status != '') {
                                botOutPut['status'] = body.status;
                            }
                            if (!util_1.isNullOrUndefined(body.result) && body.result != '') {
                                botOutPut['result'] = body.result;
                            }
                            let obj = {
                                projectVariableList: projectVariableList,
                                processVariableList: processVariableList,
                                taskVariableList: taskVariableList,
                                parentProjectVariableList: parentProjectVariableList,
                                parentProcessVariableList: parentProcessVariableList,
                                parentTaskVariableList: parentTaskVariableList
                            };
                            yield self.updateVariableList(parsedTaskData, obj);
                        }
                        else if (!util_1.isNullOrUndefined(botOutPut)) {
                            if (!util_1.isNullOrUndefined(body.result) && body.result != '') {
                                botOutPut['result'] = body.result;
                            }
                            if (!util_1.isNullOrUndefined(body.status) && body.status != '') {
                                botOutPut['status'] = body.status;
                            }
                        }
                        if (body.outputParameters['statusCode'] === '200') {
                            botOutPut['status'] = 'Complete';
                        }
                        else if (body.outputParameters['statusCode'] === '202') {
                            botOutPut['status'] = 'IgnoreFailed';
                        }
                        else {
                            botOutPut['status'] = 'Failed';
                            let whereCond = { _id: ObjectId(body.eventId) };
                            let updateCond = { $set: { eventStatus: "Failed" } };
                            let updatedData = yield self.eventService.updateEventStatus(whereCond, updateCond, false);
                            let task = yield self.eventStatusService.getEventStatusInfo(body.projectId, body.eventId, body.botId);
                            let parseTaskData = JSON.parse(JSON.stringify(task.data));
                            let onFailedTaskdata = yield self.eventStatusService.getEventStatusInfo(body.projectId, body.eventId, parseTaskData.onFailed);
                            if (!util_1.isNullOrUndefined(onFailedTaskdata.data)) {
                                parseOnFailedTaskdata = JSON.parse(JSON.stringify(onFailedTaskdata.data));
                            }
                            if (!util_1.isNullOrUndefined(parseTaskData) && !util_1.isNullOrUndefined(parseTaskData['ignoreFailed']) && parseTaskData['ignoreFailed']) {
                                botOutPut['status'] = 'IgnoreFailed';
                            }
                            let processInfo = yield this.processService.getProcessById(parseTaskData.processId, headerParams);
                            let botErrorData = {
                                taskTitle: !util_1.isNullOrUndefined(updatedData.data) ? updatedData.data['taskTitle'] : '',
                                userName: headerParams['userName'],
                                processName: !util_1.isNullOrUndefined(processInfo.data) ? processInfo.data['processName'] : '',
                                botName: !util_1.isNullOrUndefined(parseTaskData) ? parseTaskData['statusName'] : '',
                                exception: !util_1.isNullOrUndefined(body.exception) ? body.exception : '',
                                inputParameters: botOutPut.inputParameters,
                                outputParameters: botOutPut.outputParameters,
                                userId: headerParams['userId'],
                                subscriberId: headerParams['subscriberId'],
                                orgId: headerParams['orgId'],
                                gstin: headerParams['gstin'],
                                iterationId: body.iterationId,
                            };
                            yield self.botErrorsService.saveBotErrors(botErrorData);
                        }
                        botOutPut['exception'] = !util_1.isNullOrUndefined(body.exception) ? body.exception : '';
                        // await self.eventStatusService.updateEventAssignToListStatus([body.botId], body.eventId, botOutPut['status'],req);
                        let query = { projectId: body.projectId, botId: body.botId, $or: [{ eventId: body.eventId }, { parentEventId: body.eventId }], isDeleted: false, iterationId: body.iterationId };
                        let inputData = yield botInputOutput_1.botInputOutput.findOneAndUpdate(query, botOutPut, {
                            new: true,
                            upsert: false,
                            setDefaultsOnInsert: true
                        });
                        if (!util_1.isNullOrUndefined(inputData) && body.category !== 'conditional-loop' && body.category !== 'conditional') {
                            let eventData = yield this.eventStatusService.updateCurrentTaskStatus(body, botOutPut['status'], req, headerParams, []); // If Task Is Completed , Updating Its Status To Complete
                            //socket call
                            // let proData = await project.findOne({ _id: body.projectId });
                            // proData = JSON.parse(JSON.stringify(proData));
                            // const taskListData = await this.eventStatusService.getProjectTask(body.projectId, { subscriberId: proData['subscriberId'], orgId: proData['orgId'] }, proData, body.eventId);
                            // let tempData = { messages: taskListData.info, status: taskListData.status, data: taskListData.data, from: 'bot_data', for: 'event_status', eventId: body.eventId };
                            // this.socket.emit('trigger-event2', JSON.stringify(tempData));
                            if (botOutPut['status'] == 'IgnoreFailed') {
                                return { status: 2, data: parseOnFailedTaskdata, msg: "" };
                            }
                            return { status: 0, data: eventData.data, msg: "" };
                        }
                        else {
                            return { status: 1, data: [], msg: "" };
                        }
                    }
                    else {
                        return { status: 1, data: [], msg: "" };
                    }
                }
                else {
                    return { status: 1, data: [], msg: msg.botsMessage.mandatoryField };
                }
            }
            catch (err) {
                console.log("err", err);
                return ({ status: 1, err: err, data: [], msg: msg.botsMessage.internalServerError });
            }
        });
    }
    parseDate(dateStr) {
        try {
            if (isNaN(dateStr)) {
                var dt = new Date(dateStr);
                if (isNaN(dt.getTime())) {
                    return false;
                }
                else {
                    return true;
                }
            }
            else {
                return false;
            }
        }
        catch (e) {
            return false;
        }
    }
    getbotInputOutputOld(body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let OutPut = yield botInputOutput_1.botInputOutput.findOne({ $or: [{ eventId: body.eventId }, { parentEventId: body.eventId }], botId: body.botId, iterationId: body.iterationId }).lean();
                let OutPutParse = JSON.parse(JSON.stringify(OutPut));
                let ObjInput = {};
                for (const parameter of OutPutParse.inputParameters) {
                    ObjInput[parameter.name] = parameter.value;
                }
                OutPutParse.inputParameters = ObjInput;
                // let ObjOutPut = {};
                // for(const parameter of OutPutParse.outputParameters){
                //     ObjOutPut[parameter.name] = "";
                // }
                //
                // OutPutParse.outputParameters = ObjOutPut
                return { status: 0, err: null, data: OutPutParse, msg: 'Bot Details Found' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    getpredecessorOutput(nextTask) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                // let OutPut = await botInputOutput.find({projectId:nextTask.projectId,$or:[{botId:{$in:nextTask.andPredecessor}},{botId:{$in:nextTask.orPredecessor}}],isDeleted:false,
                // status:'Complete'});
                //
                // let OutPutParse = JSON.parse(JSON.stringify(OutPut))
                let iterationId;
                if (!util_1.isNullOrUndefined(nextTask.parentEventId) && !util_1.isNullOrUndefined(nextTask.parentProcessId) && !util_1.isNullOrUndefined(nextTask.parentProjectId) && nextTask.parentEventId !== "" && nextTask.parentProjectId !== "" && nextTask.parentProcessId !== "") {
                    iterationId = { $match: { iterationId: nextTask.iterationId } };
                }
                else {
                    iterationId = { $match: {} };
                }
                let OutPut = yield botInputOutput_1.botInputOutput.aggregate([
                    {
                        $match: {
                            projectId: ObjectId(nextTask.projectId),
                            isDeleted: false,
                            $and: [{ $or: [{ botId: { $in: nextTask.andPredecessor } }, { botId: { $in: nextTask.orPredecessor } }] }, { $or: [{ eventId: ObjectId(nextTask.eventId) }, { parentEventId: ObjectId(nextTask.eventId) }, { eventId: ObjectId(nextTask.parentEventId) }] }]
                        }
                    },
                    {
                        $sort: {
                            iterationId: -1
                        }
                    },
                    iterationId,
                    {
                        $group: {
                            _id: '$botId',
                            outputInfo: { $push: '$$ROOT' },
                        }
                    },
                ]);
                let OutPutParse = JSON.parse(JSON.stringify(OutPut));
                return { status: 0, err: null, data: OutPutParse, msg: 'Bot Details Found' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    writeBotInput(req, body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let self = this;
                let outputParameters = [];
                if (!util_1.isNullOrUndefined(body.previousBotOutPut)) {
                    outputParameters = body.previousBotOutPut.outputParameters;
                }
                if (!util_1.isNullOrUndefined(body.task.botMappingList)) {
                    if (body.task.botMappingList.length > 0) {
                        if (body.task.category !== "conditional") {
                            outputParameters = [];
                        }
                        if (!util_1.isNullOrUndefined(body.task.inputParameters)) {
                            for (const op of body.task.botMappingList) {
                                if (!util_1.isNullOrUndefined(body.previousBotOutPut)) {
                                    body.previousBotOutPut.outputParameters.forEach(function (bodyOutPut) {
                                        // let arr = []
                                        // if(!isNullOrUndefined(op.label) && op.label !== ""){
                                        //  arr = op.label.split(/[ ,.]+/)
                                        // }
                                        //  if(arr.length >1){
                                        // let data =  op.label.split(".")
                                        //  console.log('-----------------',bodyOutPut);
                                        //  let val = bodyOutPut.value[data[data.length - 1]];
                                        //  console.log('-----------------',bodyOutPut);
                                        //
                                        //      if(!isNullOrUndefined(val) && val !== ""){
                                        //   let obj = {
                                        //      "name": op.value,
                                        //      "dataType": "",
                                        //      "value": val
                                        //  }
                                        //  outputParameters.push(obj)
                                        //  }
                                        //  }
                                        if (bodyOutPut.name === op.label && op.category.toLowerCase() !== 'project' && op.category.toLowerCase() !== 'process' && op.category.toLowerCase() !== 'task') {
                                            let obj = {
                                                "name": op.value,
                                                "dataType": bodyOutPut.dataType,
                                                "value": bodyOutPut.value
                                            };
                                            outputParameters.push(obj);
                                        }
                                    });
                                }
                                if (body.task.isProcess) {
                                    if (op.category === 'project' && !util_1.isNullOrUndefined(body.projectParse)) {
                                        if (body.info.hasOwnProperty('parentProjectInfo') && !util_1.isNullOrUndefined(body.info.parentProjectInfo) && !body.task.isDependent) {
                                            let parentProjectVariableList = body.info.parentProjectInfo.variableList;
                                            if (!util_1.isNullOrUndefined(parentProjectVariableList) && parentProjectVariableList.length > 0) {
                                                parentProjectVariableList.forEach(function (variable) {
                                                    if (op.label === variable.name) {
                                                        let obj = {
                                                            "name": op.value,
                                                            "dataType": variable.dataType,
                                                            "value": variable.value
                                                        };
                                                        outputParameters.push(obj);
                                                    }
                                                });
                                            }
                                        }
                                        let projectVariableList = body.projectParse.variableList;
                                        if (!util_1.isNullOrUndefined(projectVariableList) && projectVariableList.length > 0) {
                                            projectVariableList.forEach(function (variable) {
                                                if (op.label === variable.name) {
                                                    let obj = {
                                                        "name": op.value,
                                                        "dataType": variable.dataType,
                                                        "value": variable.value
                                                    };
                                                    outputParameters.push(obj);
                                                }
                                            });
                                        }
                                    }
                                    else if (op.category === 'process' && !util_1.isNullOrUndefined(body.info.processInfo)) {
                                        if (body.info.hasOwnProperty('parentProcessInfo') && !util_1.isNullOrUndefined(body.info.parentProcessInfo) && !body.task.isDependent) {
                                            let parentProcessVariableList = body.info.parentProcessInfo.variableList;
                                            if (!util_1.isNullOrUndefined(parentProcessVariableList) && parentProcessVariableList.length > 0) {
                                                parentProcessVariableList.forEach(function (variable) {
                                                    if (op.label === variable.name) {
                                                        let obj = {
                                                            "name": op.value,
                                                            "dataType": variable.dataType,
                                                            "value": variable.value
                                                        };
                                                        outputParameters.push(obj);
                                                    }
                                                });
                                            }
                                        }
                                        let processVariableList = body.info.processInfo.variableList;
                                        if (!util_1.isNullOrUndefined(processVariableList) && processVariableList.length > 0) {
                                            processVariableList.forEach(function (variable) {
                                                if (op.label === variable.name) {
                                                    let obj = {
                                                        "name": op.value,
                                                        "dataType": variable.dataType,
                                                        "value": variable.value
                                                    };
                                                    outputParameters.push(obj);
                                                }
                                            });
                                        }
                                    }
                                    else if (op.category === 'task' && !util_1.isNullOrUndefined(body.info.eventInfo)) {
                                        if (body.info.hasOwnProperty('parentEventInfo') && !util_1.isNullOrUndefined(body.info.parentEventInfo) && !body.task.isDependent) {
                                            let parentEventVariableList = body.info.parentEventInfo.variableList;
                                            if (!util_1.isNullOrUndefined(parentEventVariableList) && parentEventVariableList.length > 0) {
                                                parentEventVariableList.forEach(function (variable) {
                                                    if (op.label === variable.name) {
                                                        let obj = {
                                                            "name": op.value,
                                                            "dataType": variable.dataType,
                                                            "value": variable.value
                                                        };
                                                        outputParameters.push(obj);
                                                    }
                                                });
                                            }
                                        }
                                        let taskVariableList = body.info.eventInfo.variableList;
                                        if (!util_1.isNullOrUndefined(taskVariableList) && taskVariableList.length > 0) {
                                            taskVariableList.forEach(function (variable) {
                                                if (op.label === variable.name) {
                                                    let obj = {
                                                        "name": op.value,
                                                        "dataType": variable.dataType,
                                                        "value": variable.value
                                                    };
                                                    outputParameters.push(obj);
                                                }
                                            });
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if (!util_1.isNullOrUndefined(body.task.inputParameters)) {
                    if (body.task.inputParameters.length > 0) {
                        body.task.inputParameters.forEach(function (op) {
                            if (!util_1.isNullOrUndefined(outputParameters)) {
                                outputParameters.forEach(function (bodyOutPut) {
                                    if (!util_1.isNullOrUndefined(op.name) && !util_1.isNullOrUndefined(bodyOutPut.name) && bodyOutPut.name.toLowerCase() == op.name.toLowerCase()) {
                                        op['value'] = !util_1.isNullOrUndefined(bodyOutPut) && !util_1.isNullOrUndefined(bodyOutPut.value) ? bodyOutPut.value : "";
                                    }
                                });
                            }
                        });
                    }
                }
                let updateClause;
                // if (body.task.isStart) { // for start of sub eprocess
                //     updateClause = {$set: {inputParameters: body.task.inputParameters, outputParameters: body.task.inputParameters}};
                // } else {
                //     updateClause = { $set: { inputParameters: body.task.inputParameters} };
                // }
                let OutPut = yield botInputOutput_1.botInputOutput.findOne({ $or: [{ eventId: body.task.eventId }, { parentEventId: body.task.eventId }], projectId: body.task.projectId, botId: body.task.botId, isDeleted: false, iterationId: body.task.iterationId }, { _id: 0 }).lean();
                let botOutPut = JSON.parse(JSON.stringify(OutPut));
                botOutPut.inputParameters.forEach(function (opOut) {
                    body.task.inputParameters.forEach(function (opIn) {
                        if (opOut.name.toLowerCase() == opIn.name.toLowerCase()) {
                            opOut['value'] = opIn['value'];
                        }
                    });
                });
                updateClause = { $set: { inputParameters: botOutPut.inputParameters } };
                if (body.task.isDependent) {
                    updateClause = { $set: { inputParameters: botOutPut.inputParameters, outputParameters: botOutPut.inputParameters, status: 'Complete' } };
                }
                let query = { projectId: body.task.projectId, botId: body.task.botId, $or: [{ eventId: body.task.eventId }, { parentEventId: body.task.eventId }], isDeleted: false, iterationId: body.task.iterationId };
                let dataR = yield botInputOutput_1.botInputOutput.findOneAndUpdate(query, updateClause, {
                    new: true,
                    upsert: false,
                    setDefaultsOnInsert: true
                });
                if (body.task.isDependent) {
                    let ObjInput = {};
                    for (const parameter of botOutPut.inputParameters) {
                        ObjInput[parameter.name] = parameter.value;
                    }
                    ObjInput['statusCode'] = '200';
                    let obj = {
                        projectId: body.task.projectId,
                        botId: body.task.botId,
                        outputParameters: ObjInput,
                        iterationId: body.task.iterationId,
                        category: body.task.category,
                        projectParse: {},
                        eventId: body.task.eventId,
                        parentEventId: body.task.parentEventId
                    };
                    let req = {
                        headerParams: body.headerParams
                    };
                    yield self.insertBotIOInProject(req, obj);
                }
                return { status: 0, err: null, data: dataR, msg: 'Bot Input Written' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    getOperationStatus() {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                console.log('inside operation status');
                let status = yield operation.find({ isDeleted: false }).lean();
                return { status: 0, err: null, data: status, msg: 'Operations Status Details Found' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    isEmpty(obj) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            for (var prop in obj) {
                if (obj.hasOwnProperty(prop))
                    return false;
            }
            return JSON.stringify(obj) === JSON.stringify({});
        });
    }
    getBotsequenceNumber(headerParam) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                console.log('inside get Bot sequenceNum ');
                const sequenceInfo = yield this.autoSequenceService.getValueForNextSequence('bot', headerParam);
                if (sequenceInfo.status === 1)
                    throw sequenceInfo.info;
                return { status: 0, err: null, data: sequenceInfo.sequence, msg: 'SequenceNum Generated' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    evaluateExpression(headerParam) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                const result = yield this.botCommonFunctions.evaluateExpression(headerParam);
                return { status: 0, data: result, msg: 'Expression Evaluated' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, data: err, msg: 'Fail to Evaluate Expression' };
            }
        });
    }
    writeEndBotoutput(task, projectParse, headerParam) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let updateClause = { $set: { outputParameters: task.outputParameters, inputParameters: task.outputParameters, status: 'Complete' } };
                let query = { iterationId: task.iterationId, projectId: projectParse._id, botId: task.botId, isDeleted: false, $or: [{ eventId: task.eventId }, { parentEventId: task.eventId }, { eventId: task.parentEventId }] };
                let dataR = yield botInputOutput_1.botInputOutput.findOneAndUpdate(query, updateClause, {
                    new: true,
                    upsert: false,
                    setDefaultsOnInsert: true
                });
                yield this.eventStatusService.updateCurrentTaskStatus(task, 'Complete', {}, headerParam, []); // If Task Is Completed , Updating Its Status To Complete
                return { status: 0, err: null, data: dataR, msg: 'Bot Input Written' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    updateVariableList(task, obj) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                let self = this;
                if (!util_1.isNullOrUndefined(obj.projectVariableList) && obj.projectVariableList.length > 0) {
                    yield self.projectService.updateProjectVariableList(task.projectId, obj.projectVariableList, [], null);
                }
                if (!util_1.isNullOrUndefined(obj.processVariableList) && obj.processVariableList.length > 0) {
                    yield self.processService.updateProcessVariableList(task.processId, obj.processVariableList);
                }
                if (!util_1.isNullOrUndefined(obj.taskVariableList) && obj.taskVariableList.length > 0) {
                    yield self.eventService.updateEventVariableList(task.eventId, obj.taskVariableList);
                }
                if (!util_1.isNullOrUndefined(obj.parentProjectVariableList) && obj.parentProjectVariableList.length > 0) {
                    yield self.projectService.updateProjectVariableList(task.parentProjectId, obj.parentProjectVariableList, [], null);
                }
                if (!util_1.isNullOrUndefined(obj.parentProcessVariableList) && obj.parentProcessVariableList.length > 0) {
                    yield self.processService.updateProcessVariableList(task.parentProcessId, obj.parentProcessVariableList);
                }
                if (!util_1.isNullOrUndefined(obj.parentTaskVariableList) && obj.parentTaskVariableList.length > 0) {
                    yield self.eventService.updateEventVariableList(task.parentEventId, obj.parentTaskVariableList);
                }
                return { status: 0, err: null, data: [], msg: 'Updated Variables List' };
            }
            catch (err) {
                console.log(err);
                return { status: 1, err: err, msg: msg.botsMessage.internalServerError };
            }
        });
    }
    iowrite(data, body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            if (!util_1.isNullOrUndefined(data.data) && util_1.isNullOrUndefined(data.data.from)) {
                let outputData = data.data;
                //   let outputData = { "mergearray":mergearray,"uplodeStatus": true, 'statusCode': '200' };
                if (data.data.waitForExecution && data.data.waitForExecution == true) {
                    return 0;
                }
                if (data.status == 0) {
                    outputData['statusCode'] = '200';
                }
                else {
                    if (typeof data.data == "string") {
                        outputData = {};
                    }
                    outputData['statusCode'] = '203';
                }
                outputData = yield this.writeBotOutPut(outputData, body.projectId, body.botId, body.iterationId, body.eventId);
                let taskData = { 'projectId': body.projectId, 'botId': body.botId, 'eventId': body.eventId, 'iterationId': body.iterationId, 'status': 'Complete', 'outputParameters': outputData };
                let headers = { 'authorization': body.token, 'content-type': "application/json", "orgId": body.orgId, "selectedorgid": body.orgId };
                if (data.status != 0) {
                    let err = '';
                    if (data.data) {
                        err = data.data.toString();
                    }
                    taskData['exception'] = err;
                }
                var options = {
                    method: 'POST',
                    url: env_1.env.routes.gibots_orch + "gibots-orch/orchestrator/botsiowrite",
                    headers: headers,
                    body: taskData,
                    json: true
                };
                process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
                // request(options, function (error, response, body) {
                //     // console.log("--------------err in res",error);
                //     //console.log("body---responce",body);
                //     //console.log("---res",response);
                // });
                ///////////////////////////////////////////////////////
                let count = 2;
                let self = this;
                let response = yield self.remoteApiCall(options);
                if (response['status'] == 1) {
                    console.log("----------" + response['data']);
                    for (let index = 0; index < count; index++) {
                        yield self.sleep(10000);
                        response = yield self.remoteApiCall(options);
                        if (response['status'] != 1) {
                            break;
                        }
                    }
                    if (response['status'] == 1) {
                        // let outPut = {};
                        // for (const stat of operationStatusesParse.data) {
                        //     if (!stat.isSuccess) {
                        //         outPut['statusCode'] = stat.statusCode;
                        //         if (response['status'] == 1) {
                        //             outPut['exception'] = response['data'];
                        //             outPut['errorMessage'] = response['data'];
                        //         }
                        //         else {
                        //             outPut['exception'] = response['data'];
                        //             outPut['errorMessage'] = response['data'];
                        //         }
                        //     }
                        // }
                    }
                }
                ///////////////////////////////////////////////////////
                return 0;
            }
            else {
                return 0;
            }
        });
    }
    sleep(ms) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve) => {
                setTimeout(resolve, ms);
            });
        });
    }
    remoteApiCall(options) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            // let self=this;
            return new Promise((resolve, reject) => tslib_1.__awaiter(this, void 0, void 0, function* () {
                request(options, function (error, response, body) {
                    // console.log(error, response, body)
                    if (error || (!util_1.isNullOrUndefined(body) && body.status != 0)) {
                        // if (error) {
                        //     resolve({ message: "Api Response", status: 1, data: error });
                        // } else if (!isNullOrUndefined(body) && body.status != 0) {
                        //     resolve({ message: "Api Response", status: 2, data: body.err });
                        // }
                        if (error) {
                            resolve({ message: "Api Response", status: 1, data: error });
                        }
                        else if (!util_1.isNullOrUndefined(body) && !util_1.isNullOrUndefined(body.err)) {
                            resolve({ message: "Api Response", status: 2, data: body.err });
                        }
                        else if (!util_1.isNullOrUndefined(body) && body.status != 0 && body.status != 1 && body.status != 2) {
                            resolve({ message: "Api Response", status: 1, data: body });
                        }
                    }
                    else {
                        resolve({ message: "Api Response", status: 0, data: "" });
                    }
                });
            }));
        });
    }
    formatBytes(bytes, decimals = 2) {
        if (bytes === 0)
            return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        const size = parseFloat((bytes / Math.pow(k, i)).toFixed(dm));
        console.log("fileSize ----  >>> ---- >> ", size + " " + sizes[i]);
        if ((i < 2) || (i == 2 && size < 3)) {
            return true;
        }
        else {
            return false;
        }
    }
    writeBotOutPut(outputData, projectId, botId, iterationId, eventId) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                console.log("Inside writeOutput----");
                let self = this;
                let outPut = JSON.parse(JSON.stringify(outputData));
                if (!util_1.isNullOrUndefined(outPut)) {
                    let outputKeys = Object.keys(outPut);
                    for (let i = 0; i < outputKeys.length; i++) {
                        if (!util_1.isNullOrUndefined(outPut[outputKeys[i]]) && typeof outPut[outputKeys[i]] !== "string" && isNaN(Number(outPut[outputKeys[i]]))) {
                            let byte = bytes(JSON.stringify(outPut[outputKeys[i]]));
                            if (!self.formatBytes(byte) || (typeof outPut[outputKeys[i]] !== "object" && !util_1.isNullOrUndefined(outPut[outputKeys[i]].length) || outPut[outputKeys[i]].length > 100)) {
                                let data = JSON.stringify(outPut[outputKeys[i]]);
                                let filePath = env_1.env.fileConfig.filePath;
                                console.log("filePathb to write large json---------------------------->", filePath);
                                if (!fs.existsSync(filePath)) {
                                    fs.mkdirSync(filePath);
                                }
                                filePath = filePath + projectId + '-' + eventId;
                                if (!fs.existsSync(filePath)) {
                                    fs.mkdirSync(filePath);
                                }
                                filePath = filePath + "/" + botId + "_" + iterationId + "_" + outputKeys[i] + Math.random() + ".json";
                                yield fs.writeFileSync(filePath, data, 'utf-8');
                                console.log(filePath);
                                outPut[outputKeys[i]] = filePath + "/isLocal";
                            }
                        }
                    }
                }
                return outPut;
            }
            catch (e) {
                console.log("Excewption in output bot" + JSON.stringify(e));
                return outputData;
            }
        });
    }
    getbotInputOutput(body) {
        return tslib_1.__awaiter(this, void 0, void 0, function* () {
            try {
                console.log("In getBotInput----");
                let OutPutParse = JSON.parse(JSON.stringify(body.input));
                let ObjInput = {};
                for (let parameter in OutPutParse) {
                    if (!util_1.isNullOrUndefined(OutPutParse[parameter]) && typeof OutPutParse[parameter] == "string" && !util_1.isNullOrUndefined(OutPutParse[parameter].split("/"))) {
                        let splitChar = OutPutParse[parameter].split("/");
                        if (splitChar[splitChar.length - 1] == "isLocal") {
                            OutPutParse[parameter] = OutPutParse[parameter].replace("/isLocal", "");
                            console.log("Reading bot input from json file ----------------------->" + OutPutParse[parameter]);
                            OutPutParse[parameter] = fs.readFileSync(OutPutParse[parameter]);
                            ObjInput[parameter] = JSON.parse(OutPutParse[parameter]);
                        }
                        else {
                            ObjInput[parameter] = OutPutParse[parameter];
                        }
                    }
                    else {
                        ObjInput[parameter] = OutPutParse[parameter];
                    }
                }
                body.input = ObjInput;
                // let ObjOutPut = {};
                // for(const parameter of OutPutParse.outputParameters){
                //     ObjOutPut[parameter.name] = "";
                // }
                //
                // OutPutParse.outputParameters = ObjOutPut
                return body;
            }
            catch (err) {
                console.log("Error in read bot ", err);
                return body;
            }
        });
    }
};
tslib_1.__decorate([
    Logger_1.Logger(__filename),
    tslib_1.__metadata("design:type", Object)
], BotsService.prototype, "log", void 0);
BotsService = tslib_1.__decorate([
    typedi_1.Service(),
    tslib_1.__metadata("design:paramtypes", [botCommonFunctions_1.botCommonFunctions])
], BotsService);
exports.BotsService = BotsService;
//# sourceMappingURL=botServices.js.map