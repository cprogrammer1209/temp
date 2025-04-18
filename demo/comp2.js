{
    "schedular" : {
        "startDate" : ISODate("2024-05-02T12:25:00.000+05:30"),
        "startTime" : ISODate("2024-05-03T11:05:00.000+05:30"),
        "endDate" : ISODate("2024-05-02T12:25:00.000+05:30"),
        "endTime" : ISODate("2024-05-03T11:05:00.000+05:30"),
        "andTime" : false,
        "orTime" : false
    },
    "taskDesc" : "convertPdfToImage",
    "inProgressGif" : "./../../../assets/videogif/msmeScreen.gif",
    "botIcon" : "",
    "notify" : false,
    "invisible" : true,
    "scriptFile" : "",
    "category" : "Automatic",
    "isRuleSet" : false,
    "isRuleSetCopy" : true,
    "rulesSet" : [ ],
    "inputParameters" : [
        {
            "tags" : [ ],
            "_id" : "5f574167cd315e7d0307fc93",
            "name" : "filePath",
            "dataType" : "Any",
            "regex" : "",
            "displayName" : "filePath"
        },
        {
            "tags" : [ ],
            "_id" : "60be199ed1deba4d0ae57a9b",
            "name" : "imageBasedPdf",
            "dataType" : "Any",
            "regex" : "",
            "displayName" : "imageBasedPdf"
        },
        {
            "tags" : [ ],
            "_id" : "60ffe402bec54606f53119ad",
            "name" : "docType",
            "dataType" : "Any",
            "regex" : "",
            "displayName" : "docType"
        }
    ],
    "outputParameters" : [
        {
            "tags" : [ ],
            "_id" : "5f574167cd315e7d0307fc94",
            "name" : "imagesPathaaray",
            "dataType" : "Any",
            "regex" : "",
            "displayNameOutput" : "imagesPathaaray"
        }
    ],
    "assignToList" : [ ],
    "attachments" : [ ],
    "isTemplateFixed" : false,
    "order" : 0,
    "additionalInfo" : [ ],
    "isDeleted" : false,
    "leaf" : true,
    "successor" : [ Double("1701192534245") ],
    "andPredecessor" : [ Double("1639418345000") ],
    "orPredecessor" : [ ],
    "condition" : "",
    "botId" : Double("1639418549677"),
    "showManualBot" : true,
    "iterationId" : 0,
    "isRemote" : false,
    "botShape" : "rectangle",
    "isProcess" : true,
    "startDate" : ISODate("2021-12-13T00:24:00.000+05:30"),
    "graphId" : "1639418549677",
    "scheduleBot" : false,
    "statusName" : "convertPdfToImage",
    "isDependent" : false,
    "isStart" : false,
    "isBack" : false,
    "isEnd" : false,
    "conditionalCounter" : 0,
    "loopSuccessor" : [ ],
    "syncLoop" : true,
    "ignoreFailed" : false,
    "onFailed" : 0,
    "waitSubProcess" : false,
    "notificationCriteria" : [ ],
    "selectedAssignToName" : [ ],
    "selectedAssignToEmail" : [ ],
    "selectedAssignToList" : [ ],
    "selectedGroupList" : [ ],
    "selectedRoleList" : [ ],
    "selectedRulesList" : [ ],
    "executeAll" : false,
    "manualSubProcess" : false,
    "isSlaMet" : true,
    "slaId" : null,
    "escalationId" : null,
    "isEscalationMet" : true,
    "isLimit" : false,
    "_id" : ObjectId("5f574167cd315e7d0307fc92"),
    "botMappingList" : [
        {
            "label" : "orgfilePath",
            "value" : "filePath",
            "category" : "task"
        },
        {
            "label" : "empty",
            "value" : "imageBasedPdf",
            "category" : ""
        },
        {
            "label" : "empty",
            "value" : "docType",
            "category" : ""
        }
    ],
    "outputBotMappingList" : [
        {
            "label" : "imagesPathaaray",
            "value" : "imageArr",
            "category" : "task"
        }
    ],
    "taskTitle" : "convertPdfToImage",
    "functionName" : "convertPdftoPng",
    "projectId" : ObjectId("673b14d2c4e11a6e7f8156a4"),
    "masterBotId" : ObjectId("5f574167cd315e7d0307fc92")
},