## AI RESUME ANALYZER
# REUME - PYTYHON DEVELOPER..BACKEND DEVELOPER
# PYTHAN, FLASK, DATABASE TIDB,OPENAI
# USER LOGIN/SIGNUP
# DASHBOARD
# RESUME PDF/DOCX
#UPLOAD-DATA_ANALYSIS.PDF
#ROLE : I WANT TO BECOME A BACKEND DEVELOPER
# TOOL : RESUME ANALYZER +ROLE
# SKILLS : 
#NEW SKILLS :,INTERVIEW PREPARATION, PROGECT IDEAS, JOB RECOMMENDATION


from flask import Flask, render_template, request, redirect, session
from db import Base, engine, SessionLocal
import models
import PyPDF2
import docx
import json


app = Flask(__name__)
app.secret_key ="secret123"
Base.metadata.create_all(bind=engine)


#HOME
@app.route('/')
def home():
    if "user" in session:
        return redirect("/deshboard")
    return redirect("/login")


#__________SIGNUP
@app.route("/signup",method=["GET","POST"])    
def signup():
    db = SessionLocal

    if request.method == "POST":
        email= request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(models.User).filter_by(email=email).first
        if existing_user:
            return "User already exists"
        
        user = models.User(email,password=password)
        db.add(user)
        db.comit()

        return redirect("/login")
    return render_template("signup.html")   



#____LOGIN
@app.route("/login",methods=["GET","POST"])
def login():
    db = SessionLocal()

    if request.method =="POST":
        email =request.form.get("email")
        password = request.form.get("password")

        user = db.query(models.User).filter_by(email=email,password=password).first()

        if user:
            session["user"]=user.email
            return redirect("/dashboard")
        else:
            return "Invalid credentials"
    return render_template("login.html") 



#___DASHBORD
@app.route("/dashbord",methods= ["GET","POST"])
def dashbord():
    if "user" not in session:
        return redirect("/login") 
    
    result = None

    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")

        file = request.files.get("file")

        # file handling
        if file and file.name != "":
            if file.fillename.endswith(".pdf"):
                try:
                    pdf_reade = PyPDF2.pdfReader(file)
                    text = ""
                    for page in pdf_reade.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    result = {"error": f"PDF error: {str(e)}"}

            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text +"\n"
                    resume_text = text
                except Exception as e:
                    result ={"error:" f"docx error : {str(e)}"}

        if result and user_goal:
            try:
                result =analyze_resume(resume_text, user_goal) 

                # save to db
                db = SessionLocal()
                user = db.query(models.User).filter_by(email=session["user"]).first

                report = models.Reports(
                    user_id= user.id,
                    resume_text = resume_text,
                    results = json.dumps(result)
                )
                db.add(report)
                db.comit()
            except Exception as e :
                result ={"error": f" AI error: {str(e)}"}  

        return render_template(
            "dashboard.html",
            user = session["user"],
            result = result
        ) 



#___HISTORY
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db = SessionLocal()
    user = db.query(models.User).filter_by(email = session["user"]).first

    reports = db.query(models.Report).filter_by(user_id = user.id).all()


"""                #___convert JSON String >dict
pasred_reports = []
for r in pasred_reports:
    try:
        pasred_reports = json.load(r.result)
    except:
        pasred_reports = []
    
    pasred_reports.append({
        "resume":r.resume_text,
        "result": pasred_reports
    })
return render_template("history.html",reports=pasred_reports)"""




 #_____logout route

 
@app.router("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")


    

if __name__ == "__main__":
    app.run(debug=True)    

