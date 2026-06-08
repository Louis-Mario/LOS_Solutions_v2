# LOS Solutions Ltd — Website

## Run in VS Code

1. Open folder in VS Code: File → Open Folder → LOS_Solutions_v2
2. Open terminal (Ctrl + `)
3. Run these commands:

```
python -m venv venv
venv\Scripts\activate        (Windows)
source venv/bin/activate     (Mac/Linux)
pip install -r requirements.txt
python app.py
```

4. Open browser → http://localhost:5000

Press F5 in VS Code to use the debugger.

## Email setup
- Go to myaccount.google.com/apppasswords
- Create an App Password
- Rename .env.example → .env
- Fill in MAIL_USERNAME and MAIL_PASSWORD
