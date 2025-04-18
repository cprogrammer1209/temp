let monitorInstances = new Map();
function monitoringEmail(input){
    try {

        
        console.info("inside the monitoring email function");
        let temp = input.username+"_"+input.projectId
        const Imap = require('imap');

        if (monitorInstances.has(temp) {
            console.log(`Monitoring already active for ${temp}`);
            const imap1 = monitorInstances.get(temp);
            if (imap1) {
                imap1.end();
                monitorInstances.delete(input.username);
                console.log(`Monitoring stopped for ${temp}`);
                console.log(`previous IMAP is ended. Now starting a new IMAP Monitoring ${temp}`)
            } else {
                console.log(`No monitoring active for ${temp}`);
            }
            
        }
        console.log("first")
        console.log("second")
        
        const imapConfig = {
            user: input.username, //** */
            password: input.paswword, //** */
            host: 'imap.gmail.com',
            port: 993,
            tls: true,
            authTimeout: 40000 ,
            tlsOptions: {
              rejectUnauthorized: false,
          },
        };

        const imap = new Imap(imapConfig);

        imap.connect();
        monitorInstances.set(temp, imap);
        console.log("third")

        imap.once('ready', () => {
            imap.openBox('INBOX', false, (err, box) => {
                if (err) throw err;
    
                console.log('Monitoring for new emails...');
    
                imap.on('mail', () => {
                    const searchCriteria = ['UNSEEN',['SINCE',input.date/* */],['SUBJECT',input.subject]];
                    
                    console.log("outside")
                    imap.search(searchCriteria, (err, results) => {
                        if (err) throw err;
                        if (!results || results.length === 0) return;
                            console.log("create Task")
                            //this.createTask(input,{},botId,projectId,iterationId)
                            console.log("It is working fine")
                        
                    });
                });
            });
        });

        imap.once('error', (err) => {
            console.error(err);
        });
    
        imap.once('end', () => {
            console.log('Connection ended.');
        });

        setTimeout(()=>{
            imap.end();
            monitorInstances.delete(temp);
        },input.time);

    } catch (error) {
        
    }
}

const yuv = {
    "username":"yuvaraj.s@aiqod.com",
    "paswword" : "Yuvaraj@2003",
    date:"2024-08-08T00:00:00Z",
    subject:"hello",
    time:30000
}
const np =  {
    "username":"yuvaraj.s@aiqod.com",
    "paswword" : "Yuvaraj@2003",
    date:"2024-08-08T00:00:00Z",
    subject:"hello",
    time:30000
}
monitoringEmail(yuv)

setTimeout(() => {
    monitoringEmail(np)
}, 10000);

setTimeout(() => {
    monitoringEmail(np)
}, 60000);