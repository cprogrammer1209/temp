const Imap = require('imap');
const { simpleParser } = require('mailparser');

class MonitoringManager {
    constructor() {
        this.monitorInstances = new Map(); // Store active monitors
        this.storedAccounts = []; // Placeholder for accounts (use DB in production)
    }

    // Add a new account and start monitoring
    addAccount(username, password) {
        const config = {
            user: username,
            password: password,
            host: 'imap.gmail.com',
            port: 993,
            tls: true,
            tlsOptions: { rejectUnauthorized: false },
        };

        if (this.monitorInstances.has(username)) {
            console.log(`Monitoring already active for ${username}`);
            return;
        }

        const imap = new Imap(config);

        imap.once('ready', () => {
            imap.openBox('INBOX', false, (err) => {
                if (err) throw err;
                console.log(`Monitoring started for ${username}`);

                imap.on('mail', () => {
                    this.fetchUnreadEmails(imap, username);
                });
            });
        });

        imap.once('error', (err) => {
            console.error(`Error for ${username}:`, err);
        });

        imap.once('end', () => {
            console.log(`Monitoring ended for ${username}`);
        });

        imap.connect();
        this.monitorInstances.set(username, imap);
        this.storedAccounts.push({ username, password }); // Save to storage
    }

    // Stop monitoring for a specific account
    removeAccount(username) {
        const imap = this.monitorInstances.get(username);
        if (imap) {
            imap.end();
            this.monitorInstances.delete(username);
            console.log(`Monitoring stopped for ${username}`);
        } else {
            console.log(`No monitoring active for ${username}`);
        }
    }

    // Fetch unread emails
    fetchUnreadEmails(imap, username) {
        const searchCriteria = ['UNSEEN'];
        const fetchOptions = { bodies: '' };

        imap.search(searchCriteria, (err, results) => {
            if (err) throw err;
            if (!results || results.length === 0) {
                console.log(`No unread emails for ${username}`);
                return;
            }

            const fetch = imap.fetch(results, fetchOptions);
            fetch.on('message', (msg) => {
                msg.on('body', (stream) => {
                    simpleParser(stream, (err, parsed) => {
                        if (err) throw err;
                        console.log(`Email for ${username}: ${parsed.subject}`);
                    });
                });
            });

            fetch.once('end', () => {
                console.log(`Finished fetching emails for ${username}`);
            });
        });
    }

    // Reinitialize monitoring after restart
    initialize() {
        this.storedAccounts.forEach(({ username, password }) => {
            this.addAccount(username, password);
        });
    }
}

// Example Usage
const manager = new MonitoringManager();

// Add accounts (normally retrieved from a database)
manager.addAccount('user1@example.com', 'password1');
manager.addAccount('user2@example.com', 'password2');

// Reinitialize on restart
manager.initialize();

// Stop monitoring dynamically
setTimeout(() => manager.removeAccount('user1@example.com'), 60000);
