import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from google import genai 
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_developer_key'

os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/portfolios', exist_ok=True)

client = genai.Client(api_key="YOUR_API_KEY_HERE") #<-- REPLACE WITH YOUR ACTUAL API KEYSS

def get_users():
    if not os.path.exists('users.txt'): return {}
    users = {}
    with open('users.txt', 'r') as f:
        for line in f:
            if line.strip():
                u, p, pic = line.strip().split('|')
                users[u] = {'password': p, 'pic': pic}
    return users

def save_user(username, password, pic_filename):
    with open('users.txt', 'a') as f:
        f.write(f"{username}|{password}|{pic_filename}\n")

def update_user_pic(username, new_pic):
    users = get_users()
    if username in users:
        users[username]['pic'] = new_pic
        with open('users.txt', 'w') as f:
            for u, data in users.items():
                f.write(f"{u}|{data['password']}|{data['pic']}\n")

@app.route('/', methods=['GET'])
def index():
    portfolio_file = session.get('portfolio_file')
    return render_template('index.html', 
                           username=session.get('username'), 
                           pic=session.get('pic'),
                           portfolio_file=portfolio_file)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        users = get_users()

        if action == 'signup':
            if username in users:
                flash("User already exists!")
            else:
                pic_file = request.files.get('profile_pic')
                pic_name = 'default.png'
                if pic_file and pic_file.filename != '':
                    pic_name = secure_filename(pic_file.filename)
                    pic_file.save(os.path.join('static/uploads', pic_name))
                save_user(username, password, pic_name)
                session['username'] = username
                session['pic'] = pic_name
                return redirect('/')
                
        elif action == 'login':
            if username in users and users[username]['password'] == password:
                session['username'] = username
                session['pic'] = users[username]['pic']
                return redirect('/')
            else:
                flash("Invalid credentials!")
                
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/update_pic', methods=['POST'])
def update_pic():
    if 'username' in session:
        pic_file = request.files.get('new_profile_pic')
        if pic_file and pic_file.filename != '':
            pic_name = secure_filename(pic_file.filename)
            pic_file.save(os.path.join('static/uploads', pic_name))
            update_user_pic(session['username'], pic_name)
            session['pic'] = pic_name
    return redirect('/')

@app.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        flash("You must be logged in to generate a portfolio.")
        return redirect('/')

    # 1. Clean up the incoming instructions
    instructions = request.form.get('instructions', '').strip()
    pdf_file = request.files.get('resume_pdf')
    resume_text = ""

    # 2. Extract text from PDF if it exists
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""
        except:
            flash("Could not read the PDF. Please try a different file.")
            return redirect('/')

    # FIX #1: Stop immediately if both the text box and PDF are empty
    if not instructions and not resume_text:
        session.pop('portfolio_file', None) # Clears the old portfolio from the session memory
        flash("Please upload a resume or tell EDITH about yourself in the text box!")
        return redirect('/')

    # FIX #2 & #3: Add "Guardrails" to your prompt to reject bad data
    prompt = f"""
    You are an expert Web Developer. 
    Resume Data: {resume_text}
    User Instructions: {instructions}

    CRITICAL VALIDATION STEP:
    Before generating any code, analyze the "Resume Data" and "User Instructions". Do they contain actual professional details, personal background, skills, education, or reasonable portfolio design requests?
    If the data is completely unrelated (e.g., a school assignment, random gibberish, unrelated PDF text, or irrelevant questions), you MUST abort. 
    If it is invalid, output EXACTLY the following text and absolutely nothing else:
    INVALID_DATA_ERROR

    CRITICAL RULES FOR GENERATION (If data is valid):
    Create a stunning, interactive, single-page portfolio website using HTML and Tailwind CSS via CDN based on the provided data.
    Output ONLY the raw HTML code. Do NOT wrap it in ```html blocks. Make it modern and responsive.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt,
        )
        
        output = response.text.strip()
        
        # Intercept the AI's rejection message before trying to save it as HTML
        if output == "INVALID_DATA_ERROR":
            session.pop('portfolio_file', None) # Clears the old portfolio here as well
            flash("EDITH detected invalid data. Please provide actual resume details or a valid professional PDF.")
            return redirect('/')

        # If it passes, clean and save the HTML as normal
        clean_html = output.replace('```html', '').replace('```', '').strip()
        
        filename = f"{session['username']}_portfolio.html"
        filepath = os.path.join('static/portfolios', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_html)
            
        session['portfolio_file'] = filename
    except Exception as e:
        print(f"Error: {e}")
        flash("EDITH System Error. Please try again.")
        
    return redirect('/')

@app.route('/revise', methods=['POST'])
def revise():
    if 'username' not in session or 'portfolio_file' not in session:
        return redirect('/')

    revision_request = request.form.get('revision_request')
    filepath = os.path.join('static/portfolios', session['portfolio_file'])
    
    with open(filepath, 'r', encoding='utf-8') as f:
        current_code = f.read()
    
    prompt = f"""
    You are an expert Web Developer. Here is the current HTML: {current_code}
    The user wants these changes: {revision_request}
    Return the fully updated HTML code. ONLY raw HTML. No markdown.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt,
        )
        clean_html = response.text.replace('```html', '').replace('```', '').strip()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_html)
    except:
        flash("EDITH Revision failed.")
        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)