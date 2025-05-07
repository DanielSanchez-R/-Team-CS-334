Team contributions :
Daniel Sanchez:
   - Flask Backend Implementation
   - Database Setup with Flask-SQLAlchemy
   - Progressive Web App (PWA) Configuration
   - Order Processing and Email Functionality
   - Public JSON API Endpoint
   - GitHub Repository Management
   - Execution pdf
   - Testing of Web app

Hannah Knight:
   - Testing of Web app
   - met with professor
   - loaded app onto awardspace
   - loaded app onto PythonAnywhere
   - presented application to professor

     
New Mexico Tea Shop - Full Web App (out the box instructions and use)

A complete tea shop web application that supports:

1.)Customer login and registration  
2.)Guest checkout option  
3.)Shopping cart and order placement  
4.)Admin dashboard to manage orders  
5.)Admin Product management (add, edit, delete)  
6.)Email receipts for guests and members



Step 1: Install Python (If You Don’t Have It)

Windows OS:
1. Go to [https://www.python.org/downloads](https://www.python.org/downloads)
2. Click the “Download Python 3.x.x” button
3. Run the installer  
   Make sure you **check the box** that says **“Add Python to PATH”**  
   Then click **Install Now**
4. Open Command Prompt and type: (if both show you are good to go)
   python --version
   pip --version
then:
5. pip install Flask Flask-SQLAlchemy Flask-Mail
and:
6. pip show Flask

Step 2:
Then run the app with: python app.py
Then open browser and go to: http://127.0.0.1:5000  and test out the app.

**Or if you prefer Linux**
Step 1:
Linux (Debian/Ubuntu):
1. from shell run:
   sudo apt update
   sudo apt install python3 python3-pip
   python3 --version
   pip3 --version
2. Install dependencies:
   pip3 install Flask Flask-SQLAlchemy Flask-Mail

Step 2:
Then run the app with: python app.py
Then open browser and go to: http://127.0.0.1:5000

**Feel free to test both guest and member logins, and send yourself a email with your order and total.**
**Also, use admin tools with user:default pass:default to mark orders complete or us CRUD system to edit items.**

This app was built with:
1.**Python + Flask**
2.**HTML + Bootstrap**
3.**JavaScript**
4.**SQLite**
5.**Flask-Mail**



