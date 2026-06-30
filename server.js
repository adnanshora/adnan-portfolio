const express = require('express');
const cors = require('cors');
const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'site')));

// Store submissions in a JSON file
const submissionsFile = path.join(__dirname, 'submissions.json');

// Initialize submissions file
if (!fs.existsSync(submissionsFile)) {
  fs.writeFileSync(submissionsFile, JSON.stringify([], null, 2));
}

// Configure email (update with your email details)
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER || 'your-email@gmail.com',
    pass: process.env.EMAIL_PASS || 'your-app-password'
  }
});

// Contact form endpoint
app.post('/api/contact', async (req, res) => {
  try {
    const { name, email, phone, projectType, message, timestamp } = req.body;

    // Validate required fields
    if (!name || !email || !projectType || !message) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Save submission to file
    const submissions = JSON.parse(fs.readFileSync(submissionsFile, 'utf-8'));
    submissions.push({
      id: Date.now(),
      name,
      email,
      phone,
      projectType,
      message,
      timestamp,
      receivedAt: new Date().toISOString()
    });
    fs.writeFileSync(submissionsFile, JSON.stringify(submissions, null, 2));

    // Send email to you
    const ownerEmailText = `
New Portfolio Inquiry

Name: ${name}
Email: ${email}
Phone: ${phone || 'Not provided'}
Project Type: ${projectType}

Message:
${message}

Received: ${new Date().toISOString()}
    `;

    const ownerEmailHtml = `
      <h2>New Portfolio Inquiry</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> <a href="mailto:${email}">${email}</a></p>
      <p><strong>Phone:</strong> ${phone || 'Not provided'}</p>
      <p><strong>Project Type:</strong> ${projectType}</p>
      <h3>Message:</h3>
      <p>${message.replace(/\n/g, '<br>')}</p>
      <hr>
      <p><em>Received: ${new Date().toISOString()}</em></p>
    `;

    try {
      await transporter.sendMail({
        from: process.env.EMAIL_USER || 'your-email@gmail.com',
        to: process.env.OWNER_EMAIL || 'adnanshora180899@gmail.com',
        subject: `New Inquiry: ${projectType} - From ${name}`,
        text: ownerEmailText,
        html: ownerEmailHtml
      });
    } catch (emailError) {
      console.log('Email not sent (server not configured):', emailError.message);
    }

    // Send confirmation email to visitor
    const visitorEmailText = `
Thank you for reaching out, ${name}!

I've received your inquiry about ${projectType}. I'll review your message and get back to you as soon as possible.

Looking forward to working with you!

Best regards,
Frame & Light
    `;

    const visitorEmailHtml = `
      <p>Thank you for reaching out, <strong>${name}</strong>!</p>
      <p>I've received your inquiry about <strong>${projectType}</strong>. I'll review your message and get back to you as soon as possible.</p>
      <p>Looking forward to working with you!</p>
      <p>Best regards,<br><strong>Frame & Light</strong></p>
    `;

    try {
      await transporter.sendMail({
        from: process.env.EMAIL_USER || 'your-email@gmail.com',
        to: email,
        subject: 'Thank you for your inquiry - Frame & Light',
        text: visitorEmailText,
        html: visitorEmailHtml
      });
    } catch (emailError) {
      console.log('Confirmation email not sent (server not configured):', emailError.message);
    }

    res.json({ success: true, message: 'Message received successfully' });
  } catch (error) {
    console.error('Contact form error:', error);
    res.status(500).json({ error: 'Failed to process form' });
  }
});

// Get all submissions (admin endpoint - consider adding authentication)
app.get('/api/submissions', (req, res) => {
  try {
    const submissions = JSON.parse(fs.readFileSync(submissionsFile, 'utf-8'));
    res.json(submissions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve submissions' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   Frame & Light Portfolio Server       ║
║   Running on http://localhost:${PORT}   ║
╚════════════════════════════════════════╝

📸 Site: http://localhost:${PORT}
📧 Contact form submissions saved to: submissions.json

📝 To enable email notifications:
   1. Create a .env file with:
      EMAIL_USER=your-email@gmail.com
      EMAIL_PASS=your-app-password
      OWNER_EMAIL=your-email@gmail.com
   
   2. Use Gmail App Password (not your regular password)
   3. Restart the server

📂 All submissions are stored in submissions.json
  `);
});
