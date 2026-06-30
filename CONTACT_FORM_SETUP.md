# Frame & Light Portfolio - Contact Form Setup

Your portfolio now has a working contact form! Here's how to set it up:

## Quick Start (No Email Setup)

The form will work immediately and save all submissions to `submissions.json`:

```bash
cd c:\Users\LGS\Downloads\portfolio-site
npm install
npm start
```

Then visit: **http://localhost:3000**

All form submissions are automatically saved to `submissions.json` in the project root.

---

## Enable Email Notifications

To receive email notifications when someone fills the form:

### Step 1: Set up Gmail App Password

1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security** (left sidebar)
3. Enable **2-Step Verification** (if not already enabled)
4. Go to **App passwords** (appears after 2FA is enabled)
5. Select **Mail** and **Windows Computer**
6. Copy the generated 16-character password

### Step 2: Create .env File

1. In the project root (`c:\Users\LGS\Downloads\portfolio-site\`), create a file named `.env`
2. Add the following (replace with your details):

```
EMAIL_USER=adnanshora180899@gmail.com
EMAIL_PASS=your-16-character-app-password
OWNER_EMAIL=adnanshora180899@gmail.com
PORT=3000
```

### Step 3: Restart Server

Kill the current server (Ctrl+C) and run:
```bash
npm start
```

---

## What Happens When Someone Submits

✅ Form submission is saved to `submissions.json`
✅ You get an email notification at your OWNER_EMAIL
✅ Visitor gets a confirmation email
✅ Success message displays on the form

---

## Viewing Submissions

### In Browser
Visit: http://localhost:3000/api/submissions

### In File
Open: `submissions.json` in the project folder

---

## Contact Form Fields

- **Name** (required)
- **Email** (required)
- **Phone** (optional)
- **Project Type** (required): Editorial Shoot, Brand Content, Wedding Coverage, Other
- **Message** (required)

---

## Troubleshooting

### "Gmail App Password not working"
- Make sure 2-Step Verification is enabled on your Google Account
- Use the 16-character password WITHOUT spaces
- Wait a few minutes after creating the password

### "Can't connect to localhost:3000"
- Make sure you've run `npm install` first
- Check that port 3000 isn't being used by another application
- Try a different port by changing PORT in .env

### "Form submits but no email"
- Check that .env file exists and has correct credentials
- Check the terminal for error messages
- Submissions are still saved to submissions.json even if email fails

---

## Security Notes

- Never share your Gmail App Password
- Add `.env` to `.gitignore` before committing to GitHub
- Consider moving to a dedicated email service later (SendGrid, Mailgun, etc.)

---

## Next Steps

1. Test the form: http://localhost:3000/#contact
2. Submit a test message
3. Check `submissions.json` to confirm it was saved
4. Set up email notifications with the steps above

Enjoy your working portfolio! 🎉
