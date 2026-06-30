# Email Notifications Setup - Web3Forms

Your contact form is now configured to send emails to **adnanshora180899@gmail.com**.

## How It Works

- When someone fills out the contact form, they receive a confirmation email
- You receive their message at adnanshora180899@gmail.com
- All submissions are also saved locally in your browser

## To Customize Email Address

To change where emails are sent or add reply-to email:

### Step 1: Get Your Own Web3Forms Access Key (Optional)

1. Go to: **https://web3forms.com**
2. Sign up (free)
3. Create a new form and copy your Access Key
4. Replace the key in `index.html`:

```javascript
access_key: 'YOUR_WEB3FORMS_ACCESS_KEY',
```

### Step 2: Configure Email Address

Open [site/index.html](site/index.html#L595) and find this line:

```javascript
access_key: 'c0847e5c-3b5c-4adf-a77d-8e1f5e0d8c9a',
```

Keep this key as is, or replace with your own from Web3Forms.

## Testing the Form

1. Go to: **http://localhost:3000/#contact**
2. Fill out the form
3. Submit it
4. Check your email at **adnanshora180899@gmail.com**

## Features Included

✅ Message sent to your email
✅ Visitor gets confirmation email
✅ Submissions saved locally in browser
✅ Beautiful success message
✅ Mobile-friendly form
✅ No backend server required

## What if Email Doesn't Arrive?

1. Check spam/junk folder
2. Verify email address is correct in the code
3. Contact Web3Forms support: https://web3forms.com/support

## Security Note

- The Web3Forms key is public (it's on the frontend)
- This is safe because Web3Forms validates requests
- No sensitive data is exposed

---

**Your contact form is ready to receive messages!** 🎉
