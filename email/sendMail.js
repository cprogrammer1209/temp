const nodemailer = require('nodemailer');

// SMTP configuration
const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com', // Replace with your SMTP server (e.g., 'smtp.gmail.com' for Gmail)
    port: 587, // Use 465 for SSL, 587 for TLS
    secure: false, // Use true for 465, false for other ports
    auth: {
        user: 'yuvaraj.s@aiqod.com', // Your email address
        pass: 'Yuvaraj@2003',   // Your email password or app password
    },
});
let ticketId = 43

// Email options
const mailOptions = {
    from: '"Yuvaraj" <yuvaraj.s@aiqod.com>', // Sender address
    to: 'yuvaraj.s@aiqod.com',                 // List of recipients
    subject: 'Re : Test Email',                       // Subject line
    text: 'Hello, this is a test email!',        // Plain text body
    headers: {
        'In-Reply-To': "<b83596f6-9612-cea9-228e-5953b19c47b8@aiqod.com>",
        References: "<b83596f6-9612-cea9-228e-5953b19c47b8@aiqod.com>",
        
      },
    html: `<!doctype html>
<html ⚡4email>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp4email-boilerplate>body{visibility:hidden}</style>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <script async custom-element="amp-bind" src="https://cdn.ampproject.org/v0/amp-bind-0.1.js"></script>
</head>
<body>
  <!-- Define the initial state -->
  <amp-state id="buttonState">
    <script type="application/json">
      {
        "clicked": false,
        "text": "Click Me"
      }
    </script>
  </amp-state>

  <!-- Message -->
  <p [text]="buttonState.clicked ? 'Thank you! The button has been clicked.' : 'Please click the button.'">
    Please click the button.
  </p>

  <!-- Interactive Button -->
  <button 
    on="tap:AMP.setState({buttonState: {clicked: true, text: 'Already Clicked'}})"
    [disabled]="buttonState.clicked"
    style="padding: 10px 20px; font-size: 16px; cursor: pointer;"
  >
    <span [text]="buttonState.text">Click Me</span>
  </button>

  <!-- Styles -->
  <style amp-custom>
    button {
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
    }
    button.disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }
  </style>
</body>
</html>
`, // HTML body
};

// Send email
transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
        return console.error('Error sending email:', error);
    }
    console.log('Email sent successfully:', info.response);
});



{/* <p>On Thu, Dec 26, 2024 at 7:29 PM Yuvaraj <yuvaraj.s@aiqod.com> wrote:</p>
    <p>Your ticket is being processed. Please let us know if your issue is resolved:</p>
      <div>
        <a href="http://localhost:3000/api/ticket/${ticketId}/resolved" style="padding: 10px 20px; color: white; background-color: green; text-decoration: none; border-radius: 5px;">Resolved</a>
        <a href="http://localhost:3000/api/ticket/${ticketId}/not-resolved" style="padding: 10px 20px; color: white; background-color: red; text-decoration: none; border-radius: 5px;">Not Resolved</a>
      </div> */}