// function replacePlaceholdersRecursive(obj, replacements) {
//     if (typeof obj === 'string') {
//         return obj.replace(/{(\w+)}/g, (_, key) =>
//             replacements[key] !== undefined ? replacements[key] : `{${key}}`
//         );
//     }

//     if (Array.isArray(obj)) {
//         return obj.map(item => replacePlaceholdersRecursive(item, replacements));
//     }

//     if (obj !== null && typeof obj === 'object') {
//         const updated = {};
//         for (const key in obj) {
//             updated[key] = replacePlaceholdersRecursive(obj[key], replacements);
//         }
//         return updated;
//     }

//     // Return primitive values as-is (numbers, booleans, null, etc.)
//     return obj;
// }



// function replacePlaceholdersRecursive(obj, replacements) {
//     if (typeof obj === 'string') {
//         return obj.replace(/{(\w+)}/g, (_, key) => {
//             const val = replacements[key];
//             if (val === undefined) return `{${key}}`;

//             // Serialize objects/arrays into JSON strings
//             if (typeof val === 'object') {
//                 return JSON.stringify(val);
//             }

//             return val;
//         });
//     }

//     if (Array.isArray(obj)) {
//         return obj.map(item => replacePlaceholdersRecursive(item, replacements));
//     }

//     if (obj !== null && typeof obj === 'object') {
//         const updated = {};
//         for (const key in obj) {
//             updated[key] = replacePlaceholdersRecursive(obj[key], replacements);
//         }
//         return updated;
//     }

//     return obj; // Primitive values like number, boolean, null
// }

  function replacePlaceholdersRecursive(obj, replacements) {
    if (typeof obj === 'string') {
        const exactMatch = obj.match(/^({(\w+)})$/);
        if (exactMatch) {
            const key = exactMatch[2];
            return replacements[key] !== undefined ? replacements[key] : obj;
        }

        // Partial replacement for strings like "ticket-{id}"
        return obj.replace(/{(\w+)}/g, (_, key) => {
            const val = replacements[key];
            if (val === undefined) return `{${key}}`;
            return typeof val === 'object' ? JSON.stringify(val) : val;
        });
    }

    if (Array.isArray(obj)) {
        return  obj.map(item => replacePlaceholdersRecursive(item, replacements));
    }

    if (obj !== null && typeof obj === 'object') {
        const updated = {};
        for (const key in obj) {
            updated[key] =   replacePlaceholdersRecursive(obj[key], replacements);
        }
        return updated;
    }

    return obj;
}

let replacements = { 
    username:"Yuvaraj",
    email:{
        email:"yuvara12334j"
    },
    ticketDescription:"c",
    ticketJSON:"b",
    customerJSON:[12,,2,3]
}

let input = {
  "chatgenie": {
    "contactInfo": {
      "mobileNo": "",
      "email": ""
    },
    "ticketRaise": {
      "enabled": true,
      "apiInfo": {
        "apiUrl": "https://dev.aiqod.com:843/gibots-orch/event/addExecute/task",
        "apiMethod": "POST",
        "headers": {
          "Selectedorgid": "681440a6a0d2e74324199a17",
          "Content-type": "application/json"
        },
        "Authorization": {
          "type": "Bearer Token",
          "value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZXJtaXNzaW9uIjpbImRhc2hib2FyZC5mYXFzIiwic21hcnR0YWIubm9ybWFsY2hhdCIsInNtYXJ0dGFiLnNtYXJ0Y2hhdCIsInNtYXJ0dGFiLmRtcyIsInNtYXJ0Y2hhdC5vbmxpbmUiLCJ0YXNrbWFuYWdlbWVudC5hbGwiLCJkYXNoYm9hcmQudGFzayIsIm15VGFzay5xdWV1ZWRUYXNrcyIsIm15VGFzay5kZWxldGV0YXNrIiwiZGFzaGJvYXJkLmNvdW50ZXJyZXBvcnQiLCJkYXNoYm9hcmQuUmVwb3J0IiwibmF2Lm15VGFzayIsIm5hdi5wYWNrYWdlIiwib3JnYW5pc2F0aW9uLmFsbCIsImRhc2hib2FyZC5zZXR1cFdpemFyZCIsImRhc2hib2FyZC5vcmdhbmlzYXRpb24iLCJvcmdhbmlzYXRpb24uYWRkIiwib3JnYW5pc2F0aW9uLmVkaXQiLCJuYXYuc2V0dXBXaXphcmQiLCJjaGF0UGVybWlzc2lvbi5vcmciLCJjaGF0UGVybWlzc2lvbi51c2VyIiwiY2hhdFBlcm1pc3Npb24uc3ViIiwiZGFzaGJvYXJkLmhhbmRib29rIiwiZGFzaGJvYXJkLmRtc3RyZWUiLCJkbXMuYWxsIiwid2EuYnVzaW5lc3MiLCJzY2FubmluZy51c2VyIiwic21hcnRDaGF0Lm9mZmxpbmUiLCJzbWFydENoYXQub25saW5lIiwiY2hhdC5wbHVnaW4iLCJyZXN0YXJ0X2JvdCIsImJvdC5hbGwiLCJkYXNoYm9hcmQuYm90cyIsInNraXBfYm90IiwiZGFzaGJvYXJkLnF1ZXVlIiwiZGFzaGJvYXJkLnJ1bGUiLCJkYXNoYm9hcmQuYWxsIiwiZGFzaGJvYXJkLmdpcyIsImRhc2hib2FyZC5ydWxlRW5naW5lIiwiZGFzaGJvYXJkLmhlbHAiLCJkYXNoYm9hcmQucGFja2FnZSIsImRhc2hib2FyZC5jaGFuZ2VPcmciLCJkYXNoYm9hcmQubmV3c3NUZW5kZXJzcyIsImRhc2hib2FyZC5vY3JUcmFpbmluZyIsImRhc2hib2FyZC5tYW5hZ2VSb2xlcyIsImRhc2hib2FyZC5zY2FuRG9jIiwiZGFzaGJvYXJkLmZhdm91cml0ZXMiLCJTdHJ1Y3R1cmUiLCJNb2RlbHNfVHJhaW5pbmciLCJNb2RlbHMxIiwiVHJhaW5pbmciLCJkYXNoYm9hcmQuc2NyZWVuIl0sInVzZXJJZCI6IjY4MTQ0MGE2YTBkMmU3NDMyNDE5OWExOSIsInVzZXJUeXBlIjpbImFkbWluLXNtZSJdLCJyZWdUeXBlIjoiRW50ZXJwcmlzZSIsInN1YnNjcmliZXJJZCI6IjY4MTQ0MGE2YTBkMmU3NDMyNDE5OWExNSIsInVzZXJOYW1lIjoiT3JkZXItTWFpbnRlbmFuY2UiLCJyb2xlIjp7Il9pZCI6IiJ9LCJkZXB0SWQiOm51bGwsInR5cGUiOiJ0YXhwYXllciIsImNyZWRpdEJhc2VkIjpmYWxzZSwiYWNjZXNzS2V5SWQiOiJBS0lBSk1SWUJLSEdENFUySU5FUSIsInNlY3JldEFjY2Vzc0tleSI6IkdoNjQwUHhQMnFQYk1sRUFkWEdFb3dHdVlYb2NyUGljeXRJMHc4M3MiLCJlbmRwb2ludCI6InMzLWFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbSIsInNpZ25hdHVyZVZlcnNpb24iOiJ2NCIsInJlZ2lvbiI6ImFwLXNvdXRoLTEiLCJCdWNrZXQiOiJhZGhpZ2FtdGVzdGluZyIsIkFDTCI6InByaXZhdGUiLCJrbGkiOmZhbHNlLCJkZWZhdWx0QWNjZXNzQ29udG9sIjpbXSwiZXhwIjoyMDcxNDU2MzE0fQ.bU3od2hG1hz56Ua3E8y2BWkI5LL6ef-P-MOFu5jl77U"
        },
        "bodyStructure": {
          "accessControlList": [
            {
              "_id": "6810b814ddba5042b11de544",
              "controlId": "5beaabd82ac6767c86dc311e",
              "controlName": "Admin",
              "controlType": "users",
              "permissionsList": {
                "add": true,
                "edit": true,
                "view": true,
                "execute": true
              }
            }
          ],
          "username": "Order-Maintenance",
          "projectName": "Smart Order Enquiry V2",
          "taskDesc": "",
          "projectId": "683038444aed4d09a5f84d27",
          "processId": "683003af4aed4d09a5f84d26",
          "additionalInfo": [
            {
              "id": "0",
              "value": "{username}",
              "label": "Username",
              "required": false,
              "name": "Username",
              "addToTaskList": false
            },
            {
              "id": "1",
              "value": "{email}",
              "label": "Email",
              "required": false,
              "name": "Email",
              "addToTaskList": false
            },
            {
              "id": "2",
              "value": "{ticketDescription}",
              "label": "QuerySummary",
              "required": false,
              "name": "QuerySummary",
              "addToTaskList": false
            },
            {
              "id": "3",
              "value": "{ticketJSON}",
              "label": "enquiry_data",
              "required": false,
              "name": "enquiry_data",
              "addToTaskList": false
            },
            {
              "id": "4",
              "value": "{customerJSON}",
              "label": "customer_details",
              "required": false,
              "name": "customer_details",
              "addToTaskList": false
            },
            {
              "id": "5",
              "value": "OrderM",
              "label": "Flag",
              "required": false,
              "name": "Flag",
              "addToTaskList": false
            }
          ]
        }
      }
    }
  },
  "_id": "68298c7c8f190e162a4efad9"
}

let res = replacePlaceholdersRecursive(input,replacements)
// console.log(typeof res.chatgenie.ticketRaise.apiInfo.bodyStructure.additionalInfo[1].value)
console.log("res : ",JSON.stringify(res,null,2))