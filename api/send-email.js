const nodemailer = require('nodemailer');

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { emails, names, subject, body } = req.body;

        // Split emails and names into arrays
        const recipientList = emails.split(',').map(email => email.trim());
        const firstNames = names.split(',').map(name => name.trim());

        if (recipientList.length !== firstNames.length) {
            return res.status(400).json({ error: "Emails and names count do not match!" });
        }

        // Nodemailer setup
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL,  // Use environment variables for security
                pass: process.env.EMAIL_PASSWORD,
            },
        });

        try {
            for (let i = 0; i < recipientList.length; i++) {
                const recipientEmail = recipientList[i];
                const firstName = firstNames[i];
                const personalizedBody = `Dear Doctor ${firstName},\n\n${body}`;

                await transporter.sendMail({
                    from: process.env.EMAIL,
                    to: recipientEmail,
                    subject: subject,
                    text: personalizedBody,
                });

                console.log(`Email sent to ${recipientEmail}`);
            }

            return res.status(200).json({ message: "Emails sent successfully!" });

        } catch (error) {
            console.error('Error sending emails:', error);
            return res.status(500).json({ error: "Failed to send emails." });
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
