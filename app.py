from flask import Flask, render_template, request, session, redirect
import os
from database import get_connection
from ai.resume_analyzer import analyze_resume
from ai.ats_score import calculate_ats
from ai.interview_generator import generate_questions
from ai.answer_evaluator import evaluate_answer
from flask import send_file
from reportlab.pdfgen import canvas
from ai.resume_suggestions import get_resume_suggestions
from config import Config
from ai.chat_assistant import get_response
from ai.job_recommender import recommend_jobs
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import inspect
import os
print(os.path.abspath(__file__))
print(os.path.abspath("templates"))
print("Running from:")
print(os.path.abspath(__file__))
print("Templates folder:")
print(os.path.abspath("templates"))
print("Imported from:", inspect.getfile(evaluate_answer))
print("Signature:", inspect.signature(evaluate_answer))
print("Database Name:", Config.DB_NAME)

app = Flask(__name__)

# Secret key for session
app.secret_key = "ai_interview_secret_key"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    try:
        conn = get_connection()
        conn.close()
        return render_template("index.html")
    except Exception as e:
        return f"<h2 style='color:red'>Database Error</h2><br>{e}"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        try:

            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            INSERT INTO users(fullname,email,phone,password)
            VALUES(%s,%s,%s,%s)
            """

            cursor.execute(
                sql,
                (
                    fullname,
                    email,
                    phone,
                    password
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            return """
            <h2 style='color:green'>
            Registration Successful!
            </h2>

            <a href='/login'>Go to Login</a>
            """

        except Exception as e:
            return f"<h2>Database Error</h2><br>{e}"

    return "<h1 style='color:red'>THIS IS THE REGISTER TEMPLATE</h1>"


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # ==========================
            # Check Admin Login
            # ==========================
            cursor.execute("""
                SELECT *
                FROM admin
                WHERE email=%s AND password=%s
            """, (email, password))

            admin = cursor.fetchone()

            if admin:

                session.clear()

                session["admin"] = admin["fullname"]
                session["admin_email"] = admin["email"]

                cursor.close()
                conn.close()

                return redirect("/admin_dashboard")

            # ==========================
            # Check User Login
            # ==========================
            cursor.execute("""
                SELECT *
                FROM users
                WHERE email=%s AND password=%s
            """, (email, password))

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:

                session.clear()

                session["username"] = user["fullname"]
                session["email"] = user["email"]

                return redirect("/dashboard")

            return render_template(
                "login.html",
                error="Invalid Email or Password"
            )

        except Exception as e:

            return f"<h2>Database Error</h2><br>{e}"

    return render_template("login.html")

@app.route("/upload_resume", methods=["GET", "POST"])
def upload_resume():

    if request.method == "POST":

        file = request.files["resume"]

        if file.filename != "":

            filename = file.filename

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            try:

                conn = get_connection()
                cursor = conn.cursor()

                sql = """
                INSERT INTO resumes
                (fullname,email,resume_name,resume_path)
                VALUES(%s,%s,%s,%s)
                """

                values = (
                    session["username"],
                    session["email"],
                    filename,
                    filepath
)

                cursor.execute(sql, values)

                conn.commit()

                cursor.close()
                conn.close()
                

                result = analyze_resume(filepath)

                score = calculate_ats(result)

                # Create new interview
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO interviews
                (fullname, email, resume_name)
                VALUES (%s, %s, %s)
                """,
                (
                    session["username"],
                    session["email"],
                    filename
                ))

                conn.commit()

                # Save interview id in session
                session["interview_id"] = cursor.lastrowid

                cursor.close()
                conn.close()

                questions = generate_questions(result["skills"])
                jobs = recommend_jobs(result["skills"])
                suggestions = get_resume_suggestions(result)
                session["questions"] = questions
                session["current_question"] = 0
                return render_template(
                    "analysis.html",
                     result=result,
                     score=score,
                     questions=questions,
                     jobs=jobs,
                     suggestions=suggestions
                )

            except Exception as e:

                return f"<h2>Database Error</h2><br>{e}"

    return render_template("upload_resume.html")

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )

@app.route("/interview", methods=["GET", "POST"])
def interview():

    if "questions" not in session:
        return redirect("/upload_resume")

    questions = session["questions"]
    current = session.get("current_question", 0)

    # Interview completed
    if current >= len(questions):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(score) AS total_score
            FROM interview_answers
            WHERE interview_id=%s
        """, (session["interview_id"],))

        data = cursor.fetchone()

        total = data["total"] or 0
        total_score = data["total_score"] or 0

        percentage = 0
        if total > 0:
            percentage = round((total_score / (total * 10)) * 100, 2)

        cursor.execute("""
            UPDATE interviews
            SET total_questions=%s,
                total_score=%s,
                percentage=%s
            WHERE interview_id=%s
        """,
        (
            total,
            total_score,
            percentage,
            session["interview_id"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/performance")

    # ✅ VERY IMPORTANT
    question = questions[current]

    if request.method == "POST":

        answer = request.form["answer"]

        result = evaluate_answer(question, answer)

        score = result["score"]
        feedback = "\n".join(result["feedback"])

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO interview_answers
            (interview_id, fullname, question, answer, score, feedback)
            VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            session["interview_id"],
            session["username"],
            question,
            answer,
            score,
            feedback
        ))

        conn.commit()

        cursor.close()
        conn.close()

        session["current_question"] += 1

        return redirect("/interview")

    return render_template(
        "interview.html",
        question=question,
        number=current + 1,
        total=len(questions)
    )
@app.route("/hr_interview")
def hr_interview():

    questions = [

        "Tell me about yourself.",

        "Why should we hire you?",

        "What are your strengths?",

        "What are your weaknesses?",

        "Where do you see yourself in 5 years?"

    ]

    return render_template(
        "hr_interview.html",
        questions=questions
    )
@app.route("/python_interview")
def python_interview():

    questions = [

        "What is Python?",

        "Difference between List and Tuple?",

        "Explain OOP.",

        "What is Flask?",

        "What are decorators?"

    ]

    return render_template(
        "python_interview.html",
        questions=questions
    )
@app.route("/sql_interview")
def sql_interview():

    questions = [

        "What is SQL?",

        "Explain JOIN.",

        "Difference between DELETE and TRUNCATE?",

        "What is GROUP BY?",

        "What is Primary Key?"

    ]

    return render_template(
        "sql_interview.html",
        questions=questions
    )
@app.route("/profile")
def profile():

    return render_template(
        "profile.html",
        username=session["username"],
        email=session["email"]
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
    
@app.route("/performance")
def performance():

    if "username" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    # Latest Interview
    cursor.execute("""
        SELECT interview_id
        FROM interviews
        WHERE email=%s
        ORDER BY interview_id DESC
        LIMIT 1
    """, (session["email"],))

    latest = cursor.fetchone()

    if not latest:

        cursor.close()
        conn.close()

        return "<h2>No interview completed yet.</h2>"

    interview_id = latest["interview_id"]

    # Questions and Answers
    cursor.execute("""
        SELECT
            question,
            answer,
            score,
            feedback
        FROM interview_answers
        WHERE interview_id=%s
        ORDER BY answer_id
    """, (interview_id,))

    reports = cursor.fetchall()

    # Summary
    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(score) AS total_score,
            AVG(score) AS average_score
        FROM interview_answers
        WHERE interview_id=%s
    """, (interview_id,))

    summary = cursor.fetchone()

    cursor.close()
    conn.close()

    percentage = 0

    if summary["total"] > 0:
        percentage = round(
            (summary["total_score"] /
            (summary["total"] * 10)) * 100,
            2
        )

    return render_template(
        "performance.html",
        reports=reports,
        summary=summary,
        percentage=percentage,
        username=session["username"]
    )
@app.route("/history/<int:interview_id>")
def interview_details(interview_id):

    if "username" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            question,
            answer,
            score,
            feedback
        FROM interview_answers
        WHERE interview_id=%s
    """, (interview_id,))

    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history_details.html",
        reports=reports,
        interview_id=interview_id
    ) 
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM admin
            WHERE email=%s
        """, (email,))

        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin is None:
            return render_template(
                "admin_login.html",
                error="Admin Email Not Found"
            )

        if admin["password"] != password:
            return render_template(
                "admin_login.html",
                error="Wrong Password"
            )

        session["admin"] = admin["fullname"]
        session["admin_email"] = admin["email"]

        return redirect("/admin_dashboard")

    return render_template("admin_login.html")
@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    conn = get_connection()
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()["total"]

    # Total Resumes
    cursor.execute("SELECT COUNT(*) AS total FROM resumes")
    total_resumes = cursor.fetchone()["total"]

    # Total Interviews
    cursor.execute("SELECT COUNT(*) AS total FROM interviews")
    total_interviews = cursor.fetchone()["total"]

    # Average Score
    cursor.execute("""
        SELECT ROUND(AVG(percentage),2) AS avg_score
        FROM interviews
    """)
    avg_score = cursor.fetchone()["avg_score"] or 0

    # Top 5 Candidates
    cursor.execute("""
        SELECT fullname, percentage
        FROM interviews
        ORDER BY percentage DESC
        LIMIT 5
    """)
    top_candidates = cursor.fetchall()

    # Recent Interviews
    cursor.execute("""
        SELECT fullname,resume_name,percentage,interview_date
        FROM interviews
        ORDER BY interview_date DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_resumes=total_resumes,
        total_interviews=total_interviews,
        avg_score=avg_score,
        top_candidates=top_candidates,
        recent=recent
    )
@app.route("/certificate")
def certificate():

    if "username" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT percentage
        FROM interviews
        WHERE fullname=%s
        ORDER BY interview_id DESC
        LIMIT 1
    """, (session["username"],))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    percentage = data["percentage"] if data else 0

    filename = f"certificate_{session['username']}.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 770, "AI Interview Preparation System")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 730, "Certificate of Completion")

    c.setFont("Helvetica", 14)
    c.drawCentredString(
        300,
        680,
        f"This certifies that {session['username']}"
    )

    c.drawCentredString(
        300,
        640,
        "has successfully completed the AI Mock Interview."
    )

    c.drawCentredString(
        300,
        600,
        f"Overall Score : {percentage}%"
    )

    c.save()

    return send_file(filename, as_attachment=True)
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        answer = get_response(question)

    return render_template(
        "chatbot.html",
        answer=answer
    )
@app.route("/resume_builder", methods=["GET","POST"])
def resume_builder():

    if request.method == "POST":

        return render_template(

            "generated_resume.html",

            fullname=request.form["fullname"],
            email=request.form["email"],
            phone=request.form["phone"],
            objective=request.form["objective"],
            skills=request.form["skills"],
            education=request.form["education"],
            projects=request.form["projects"],
            experience=request.form["experience"],
            certifications=request.form["certifications"]

        )

    return render_template("resume_builder.html")
@app.route("/download_resume", methods=["POST"])
def download_resume():

    fullname = request.form["fullname"]
    email = request.form["email"]
    phone = request.form["phone"]
    objective = request.form["objective"]
    skills = request.form["skills"]
    education = request.form["education"]
    projects = request.form["projects"]
    experience = request.form["experience"]
    certifications = request.form["certifications"]

    filename = f"{fullname}_Resume.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph(f"<b>{fullname}</b>", styles["Title"]))
    story.append(Paragraph(f"Email: {email}", styles["Normal"]))
    story.append(Paragraph(f"Phone: {phone}", styles["Normal"]))

    story.append(Paragraph("<b>Career Objective</b>", styles["Heading2"]))
    story.append(Paragraph(objective, styles["Normal"]))

    story.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    story.append(Paragraph(skills, styles["Normal"]))

    story.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    story.append(Paragraph(education, styles["Normal"]))

    story.append(Paragraph("<b>Projects</b>", styles["Heading2"]))
    story.append(Paragraph(projects, styles["Normal"]))

    story.append(Paragraph("<b>Experience</b>", styles["Heading2"]))
    story.append(Paragraph(experience, styles["Normal"]))

    story.append(Paragraph("<b>Certifications</b>", styles["Heading2"]))
    story.append(Paragraph(certifications, styles["Normal"]))

    doc.build(story)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)