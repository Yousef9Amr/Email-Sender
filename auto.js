const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');

const app = express();

// Serve static files (HTML, CSS)
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

// Email sending route
app.post('/send-email', async (req, res) => {
    const { emails, names, subject, body } = req.body;

    // Split emails and names into arrays
    const recipientList = emails.split(',').map(email => email.trim());
    const firstNames = names.split(',').map(name => name.trim());
    


    if (recipientList.length !== firstNames.length) {
        return res.status(400).send("Emails and names count do not match!");
    }

    // Nodemailer setup
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'yousef9amr@gmail.com',  // Replace with your email
            pass: 'vqgs jgpn aels krgj'  // Replace with your app-specific password
        }
    });

    try {
        for (let i = 0; i < recipientList.length; i++) {
            const recipientEmail = recipientList[i];
            const firstName = firstNames[i];

            const personalizedBody = `Dear Doctor ${firstName},\n\n${body}`;

            let mailOptions = {
                from: 'yousef9amr@gmail.com',  // Replace with your email
                to: recipientEmail,
                subject: subject,
                text: personalizedBody
            };

            await transporter.sendMail(mailOptions);
            console.log(`Email sent to ${recipientEmail} with greeting: 'Dear Doctor ${firstName}'`);
        }

        res.send("Emails sent successfully!");

    } catch (error) {
        console.error('Error sending emails:', error);
        res.status(500).send("Failed to send emails.");
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
