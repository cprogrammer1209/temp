const Imap = require('imap');
const { simpleParser } = require('mailparser');

const imapConfig = {
    user: 'yuvaraj.s@aiqod.com', //** */
    password: 'Yuvaraj@2003', //** */
    host: 'imap.gmail.com',
    port: 993,
    tls: true,
    tlsOptions: {
      rejectUnauthorized: false,
  },
};

const monitorEmails = () => {
    const imap = new Imap(imapConfig);

    imap.once('ready', () => {
        imap.openBox('INBOX', false, (err, box) => {
            if (err) throw err;

            console.log('Monitoring for new emails...');

            imap.on('mail', () => {
                const searchCriteria = ['UNSEEN',['SINCE',"2024-12-09T00:00:00Z"/* */],['SUBJECT',"Hello"]];
                const fetchOptions = { bodies: '' };
                console.log("outside")
                imap.search(searchCriteria, (err, results) => {
                    if (err) throw err;
                    if (!results || results.length === 0) return;

                    
                    //     msg.on('body', (stream) => {
                    //         simpleParser(stream, (err, parsed) => {
                    //             if (err) throw err;

                    //             const subject = parsed.subject || '';
                    //             if (subject.includes('hello')) {
                    //                 console.log('Hello World123321');
                    //                 // create function should be place here
                    //             }
                    //         });
                    //     });
                    // });
                    console.log("It is working fine")
                    fetch.once('end', () => {
                        console.log('Done fetching emails.');
                    });
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

    console.log("first")

    imap.connect();
    
    setTimeout(()=>{
        imap.end();
    },1800000)
};

monitorEmails();




