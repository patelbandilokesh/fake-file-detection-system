from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from werkzeug.utils import secure_filename
from utils import analyze_file
import calendar
from datetime import datetime, timedelta
from utils import analyze_file
from flask import flash
from flask import session
import MySQLdb.cursors

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simulated database (store hashes)
stored_hashes = set()

app.secret_key = "mysecretkey"

# ---------------- MYSQL ----------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Lokesh@123"
app.config["MYSQL_DB"] = "fake_file_system"

mysql = MySQL(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SAVE TO DB ----------------
def save_to_db(filename, filetype, filesize, status, uploaded_by, sha512):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO files 
        (filename, filetype, filesize, status, uploaded_by, sha512, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """,
        (filename, filetype, filesize, status, uploaded_by, sha512),
    )
    mysql.connection.commit()
    cursor.close()


def is_duplicate_hash(file_hash, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id FROM files WHERE sha512 = %s AND uploaded_by=%s",
        (file_hash, user_id),
    )
    data = cursor.fetchone()
    cursor.close()
    return data is not None


# ------------------- REGISTER PAGE -------------------


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email").strip()
        username = request.form.get("username").strip()
        password = request.form.get("password")

        # ================= PASSWORD VALIDATION =================
        pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

        if not re.match(pattern, password):

            flash(
                "Password must contain 8 characters, 1 uppercase, 1 number & 1 special character",
                "error",
            )

            return render_template("register.html")

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ================= CHECK USERNAME =================
        cur.execute(
            "SELECT * FROM register WHERE BINARY username=%s",
            (username,),
        )

        existing_username = cur.fetchone()

        if existing_username:

            flash("Username already exists!", "error")

            return render_template("register.html")

        # ================= CHECK EMAIL =================
        cur.execute(
            "SELECT * FROM register WHERE BINARY email=%s",
            (email,),
        )

        existing_email = cur.fetchone()

        if existing_email:

            flash("Email already exists!", "error")

            return render_template("register.html")

        # ================= HASH PASSWORD =================
        hashed_password = generate_password_hash(password)

        try:

            # ================= INSERT =================
            cur.execute(
                """
                INSERT INTO register (email, username, password)
                VALUES (%s, %s, %s)
                """,
                (email, username, hashed_password),
            )

            mysql.connection.commit()

            flash(
                f"Welcome {username}! Registration successful",
                "success",
            )

            return render_template("register.html", redirect_to_login=True)

        except Exception as e:

            print(e)

            flash("Registration failed!", "error")

            return render_template("register.html")

        finally:
            cur.close()

    return render_template("register.html")


# ------------------- LOGIN PAGE -------------------


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ✅ CASE SENSITIVE USERNAME
        cursor.execute("SELECT * FROM register WHERE BINARY username=%s", (username,))

        user = cursor.fetchone()

        # ❌ INVALID USERNAME
        if not user:

            flash("Invalid username", "error")

            return render_template("login.html")

        # ❌ INVALID PASSWORD
        if not check_password_hash(user["password"], password):

            flash("Invalid password", "error")

            return render_template("login.html")

        # ✅ SUCCESS LOGIN
        session["user_id"] = user["id"]

        # =====================================
        # INSERT LOGIN ACTIVITY
        # =====================================

        uploaded_by = user["id"]

        cursor.execute(
            "INSERT INTO login_activity(uploaded_by) VALUES(%s)", (uploaded_by,)
        )

        mysql.connection.commit()

        flash("Login successful", "success")
        cursor.close()

        # ✅ WAIT + REDIRECT
        return render_template("login.html", redirect_to_dashboard=True)

    return render_template("login.html")


# ================= FORGOT PASSWORD =================


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email").strip()
        username = request.form.get("username").strip()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ===== CHECK USER =====
        cur.execute(
            """
            SELECT * FROM register
            WHERE BINARY email=%s
            AND BINARY username=%s
            """,
            (email, username),
        )

        user = cur.fetchone()

        cur.close()

        # ===== SUCCESS =====
        if user:

            session["reset_user"] = user["id"]

            flash("User verified successfully", "success")

            return render_template("forgot_password.html", redirect_to_change=True)

        # ===== INVALID =====
        else:

            flash("Invalid email or username!", "error")

            return render_template("forgot_password.html")

    return render_template("forgot_password.html")


# ------------------- CHANGE PASSWORD PAGE -------------------


@app.route("/change_password")
def change_password():
    return render_template("change_password.html")


# ------------------- RESET PASSWORD PAGE -------------------


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

    if request.method == "POST":

        new_password = request.form.get("new_password").strip()
        confirm_password = request.form.get("confirm_password").strip()

        # ===== EMPTY CHECK =====

        if not new_password or not confirm_password:

            return render_template(
                "change_password.html", message="Fill all fields!", category="error"
            )

        # ===== MINIMUM 8 CHARACTERS =====

        if len(new_password) < 8:

            return render_template(
                "change_password.html",
                message="Password must contain at least 8 characters!",
                category="error",
            )

        # ===== CAPITAL LETTER CHECK =====

        if not re.search(r"[A-Z]", new_password):

            return render_template(
                "change_password.html",
                message="Add at least one capital letter!",
                category="error",
            )

        # ===== SMALL LETTER CHECK =====

        if not re.search(r"[a-z]", new_password):

            return render_template(
                "change_password.html",
                message="Add at least one small letter!",
                category="error",
            )

        # ===== NUMBER CHECK =====

        if not re.search(r"[0-9]", new_password):

            return render_template(
                "change_password.html",
                message="Add at least one number!",
                category="error",
            )

        # ===== SPECIAL CHARACTER CHECK =====

        if not re.search(r"[@$!%*?&]", new_password):

            return render_template(
                "change_password.html",
                message="Add at least one special character!",
                category="error",
            )

        # ===== PASSWORD MATCH CHECK =====

        if new_password != confirm_password:

            return render_template(
                "change_password.html",
                message="Passwords do not match!",
                category="error",
            )

        # ===== SESSION CHECK =====

        user_id = session.get("reset_user")

        if not user_id:

            return render_template(
                "change_password.html",
                message="Session expired! Try again.",
                category="error",
            )

        # ===== HASH PASSWORD =====

        hashed_password = generate_password_hash(new_password)

        # ===== UPDATE DATABASE =====

        cur = mysql.connection.cursor()

        cur.execute(
            "UPDATE register SET password=%s WHERE id=%s", (hashed_password, user_id)
        )

        mysql.connection.commit()
        cur.close()

        # ===== REMOVE SESSION =====

        session.pop("reset_user", None)

        # ===== SUCCESS =====

        return render_template(
            "change_password.html",
            message="Password changed successfully!",
            category="success",
            redirect_to_login=True,
        )

    return render_template("change_password.html")


# ------------------- USER PAGE -------------------


@app.route("/user")
def user():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("user.html")


# ---------------- DASHBOARD PAGE ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ---------------- GRAPH DATA ----------------


# ---------------- GRAPH DATA ----------------


@app.route("/dashboard_data/<filter>")
def dashboard_data(filter):

    try:

        # ✅ LOGIN CHECK
        if "user_id" not in session:
            return jsonify({"bar": [], "line": []})

        user_id = session["user_id"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ================= FILTER =================

        if filter == "7days":
            condition = "created_at >= CURDATE() - INTERVAL 7 DAY"
            days = 7

        elif filter == "30days":
            condition = "created_at >= CURDATE() - INTERVAL 30 DAY"
            days = 30

        elif filter == "year":
            condition = "created_at >= CURDATE() - INTERVAL 1 YEAR"
            days = 365

        else:
            condition = "created_at >= CURDATE() - INTERVAL 30 DAY"
            days = 30

        # ================= BAR GRAPH =================

        cur.execute(
            f"""
            SELECT 
                IFNULL(filetype,'Unknown') AS label,
                COUNT(*) AS value
            FROM files
            WHERE uploaded_by=%s
            AND {condition}
            GROUP BY filetype
        """,
            (user_id,),
        )

        bar = cur.fetchall()

        print("BAR DATA =", bar)

        # ================= LINE GRAPH =================

        cur.execute(
            f"""
            SELECT 
                DATE(created_at) AS day,
                COUNT(*) AS count
            FROM files
            WHERE uploaded_by=%s
            AND {condition}
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """,
            (user_id,),
        )

        db_data = cur.fetchall()

        print("DB LINE DATA =", db_data)

        result = []

        today = datetime.today()

        # ✅ FULL DATE RANGE
        for i in range(days - 1, -1, -1):

            date_value = (today - timedelta(days=i)).strftime("%Y-%m-%d")

            found = next((x for x in db_data if str(x["day"]) == date_value), None)

            result.append(
                {"label": date_value, "value": found["count"] if found else 0}
            )

        print("FINAL LINE =", result)

        cur.close()

        return jsonify({"bar": bar, "line": result})

    except Exception as e:

        print("DASHBOARD ERROR =", str(e))

        return jsonify({"bar": [], "line": []})


# ---------------- PIE + DONUT ----------------


@app.route("/status_data")
def status_data():

    try:

        if "user_id" not in session:
            return jsonify([])

        user_id = session["user_id"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            """
            SELECT 
                IFNULL(status,'Unknown') AS label,
                COUNT(*) AS value
            FROM files
            WHERE uploaded_by=%s
            GROUP BY status
        """,
            (user_id,),
        )

        data = cursor.fetchall()

        print("STATUS DATA =", data)

        cursor.close()

        return jsonify(data)

    except Exception as e:

        print("STATUS ERROR =", str(e))

        return jsonify([])


# ---------------- UPLOAD PAGE ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]

        filename = file.filename
        filepath = os.path.join("uploads", filename)
        file.save(filepath)

        # 🔥 STEP 1: analyze file
        result = analyze_file(filepath)

        # 🔥 STEP 2: ADD THIS BLOCK HERE 👇

        # 🔥 STEP 2

        user_id = str(session.get("user_id")).zfill(2)

        file_hash = result["hash"]

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT * FROM files 
            WHERE sha512 = %s AND uploaded_by = %s
        """,
            (file_hash, user_id),
        )

        existing = cur.fetchone()

        if existing:
            result["status"] = "Duplicate"

        # 🔥 STEP 3: INSERT INTO DB
        cur.execute(
            """
            INSERT INTO files (filename, filetype, filesize, status, uploaded_by, sha512)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (
                filename,
                result.get("file_type"),
                os.path.getsize(filepath),
                result.get("status"),
                user_id,
                file_hash,
            ),
        )

        mysql.connection.commit()
        cur.close()

        return render_template("result.html", result=result)

    return render_template("upload.html")


# ================= GET HISTORY =================
@app.route("/get_history")
def get_history():
    if "user_id" not in session:
        return jsonify([])

    user_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT id, filename, filesize, filetype, sha512, status
        FROM files
        WHERE uploaded_by = %s
        ORDER BY id DESC
    """,
        (user_id,),
    )

    rows = cur.fetchall()

    # 🔥 convert to JSON format
    data = []
    for r in rows:
        data.append(
            {
                "id": r[0],
                "name": r[1],
                "size": r[2],
                "type": r[3],
                "hash": r[4],
                "status": r[5],
            }
        )
        cur.close()

    return jsonify(data)


# ================= DELETE ONE =================
@app.route("/delete_file/<int:id>", methods=["DELETE"])
def delete_file(id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM files WHERE id=%s AND uploaded_by=%s", (id, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"success": True})


# ================= DELETE SELECTED =================
@app.route("/delete_selected", methods=["POST"])
def delete_selected():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    ids = request.json.get("ids", [])

    if not ids:
        return jsonify({"success": False})

    cur = mysql.connection.cursor()

    format_strings = ",".join(["%s"] * len(ids))
    query = f"DELETE FROM files WHERE id IN ({format_strings}) AND uploaded_by=%s"

    cur.execute(query, (*ids, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"success": True})


# ================= DELETE HARMFUL =================
@app.route("/delete_harmful", methods=["POST"])
def delete_harmful():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute(
        """
        DELETE FROM files
        WHERE status='harmful' AND uploaded_by=%s
    """,
        (user_id,),
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"success": True})


# ================= DELETE ALL =================
@app.route("/delete_all", methods=["POST"])
def delete_all():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM files WHERE uploaded_by=%s", (user_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"success": True})


# ---------------------------------------------------------------


@app.route("/update_account", methods=["POST"])
def update_account():

    if "user_id" not in session:
        return jsonify({"message": "Login required"})

    data = request.get_json()  # 🔥 MAIN CHANGE

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    old_username = data.get("old_username")
    new_username = data.get("new_username")

    old_email = data.get("old_email")
    new_email = data.get("new_email")

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    cur.execute("SELECT * FROM register WHERE id=%s", (user_id,))
    user = cur.fetchone()

    # USERNAME UPDATE
    if old_username and new_username:
        if user[1] == old_username:
            cur.execute(
                "UPDATE register SET username=%s WHERE id=%s",
                (new_username, user_id),
            )
            mysql.connection.commit()
        else:
            return jsonify({"message": "Wrong old username"})

    # EMAIL UPDATE
    if old_email and new_email:
        if user[2] == old_email:
            cur.execute(
                "UPDATE register SET email=%s WHERE id=%s",
                (new_email, user_id),
            )
            mysql.connection.commit()
        else:
            return jsonify({"message": "Wrong old email"})

    # PASSWORD UPDATE
    if old_password and new_password:
        if check_password_hash(user[3], old_password):

            pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
            if not re.match(pattern, new_password):
                return jsonify({"message": "Weak password"})

            hashed_password = generate_password_hash(new_password)

            cur.execute(
                "UPDATE register SET password=%s WHERE id=%s",
                (hashed_password, user_id),
            )
            mysql.connection.commit()
        else:
            return jsonify({"message": "Old password incorrect ❌"})

    cur.close()

    return jsonify({"message": "Updated Successfully ✅"})


# ================= ADMIN LOGIN =================


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # ===== EMPTY CHECK =====

        if not username or not password:

            flash("Fill all fields!", "error")

            return render_template("admin_login.html")

        # ===== FETCH DATA FROM ADMIN TABLE =====

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute(
            """
            SELECT * FROM admin
            WHERE BINARY username=%s
            """,
            (username,),
        )

        admin = cur.fetchone()

        cur.close()

        # ===== INVALID USERNAME =====

        if not admin:

            flash("Invalid admin username!", "error")

            return render_template("admin_login.html")

        # ===== PASSWORD CHECK =====

        if not check_password_hash(admin["password"], password):

            flash("Invalid password!", "error")

            return render_template("admin_login.html")

        # ===== SESSION =====

        session["admin_loggedin"] = True
        session["admin_id"] = admin["id"]
        session["admin_username"] = admin["username"]

        # ===== SUCCESS =====

        flash("Admin login successful!", "success")

        return redirect("/admin_page")

    return render_template("admin_login.html")


# ================= ADMIN UPDATE ACCOUNT =================


@app.route("/admin_update_account", methods=["POST"])
def admin_update_account():

    if "admin_id" not in session:

        return jsonify({"message": "Admin login required ❌"})

    data = request.get_json()

    admin_id = session["admin_id"]

    cur = mysql.connection.cursor()

    # =====================================
    # GET ADMIN
    # =====================================

    cur.execute("SELECT * FROM admin WHERE id=%s", (admin_id,))

    admin = cur.fetchone()

    # =====================================
    # GET VALUES
    # =====================================

    old_username = data.get("old_username", "").strip()
    new_username = data.get("new_username", "").strip()

    old_email = data.get("old_email", "").strip()
    new_email = data.get("new_email", "").strip()

    old_password = data.get("old_password", "").strip()
    new_password = data.get("new_password", "").strip()

    # =====================================
    # USERNAME UPDATE
    # =====================================

    if old_username and new_username:

        if admin[1] == old_username:

            cur.execute(
                "UPDATE admin SET username=%s WHERE id=%s", (new_username, admin_id)
            )

            mysql.connection.commit()

        else:

            cur.close()

            return jsonify({"message": "Wrong old username ❌"})

    # =====================================
    # EMAIL UPDATE
    # =====================================

    if old_email and new_email:

        if admin[2] == old_email:

            cur.execute("UPDATE admin SET email=%s WHERE id=%s", (new_email, admin_id))

            mysql.connection.commit()

        else:

            cur.close()

            return jsonify({"message": "Wrong old email ❌"})

    # =====================================
    # PASSWORD UPDATE
    # =====================================

    if old_password and new_password:

        # ===== CHECK OLD PASSWORD =====

        if not check_password_hash(admin[3], old_password):

            cur.close()

            return jsonify({"message": "Old password incorrect ❌"})

        # ===== NEW PASSWORD RULES =====

        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*?&]).{8,}$"

        if not re.match(pattern, new_password):

            cur.close()

            return jsonify(
                {
                    "message": "New password must contain:\n• 8 characters\n• 1 Capital\n• 1 Small\n• 1 Number\n• 1 Special symbol ❌"
                }
            )

        # ===== HASH PASSWORD =====

        hashed_password = generate_password_hash(new_password)

        # ===== UPDATE PASSWORD =====

        cur.execute(
            "UPDATE admin SET password=%s WHERE id=%s", (hashed_password, admin_id)
        )

        mysql.connection.commit()

    cur.close()

    return jsonify({"message": "Admin updated successfully ✅"})


# ================= ADMIN REGISTER ================


@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():

    if request.method == "POST":

        # ===== GET FORM DATA =====

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # ===== EMPTY CHECK =====

        if not username or not email or not password:

            flash("Fill all fields!", "error")

            return render_template("admin_register.html")

        # ===== USERNAME LENGTH =====

        if len(username) < 3:

            flash("Username must contain minimum 3 letters!", "error")

            return render_template("admin_register.html")

        # ===== PASSWORD LENGTH =====

        if len(password) < 8:

            flash("Password must contain 8 characters!", "error")

            return render_template("admin_register.html")

        # ===== CAPITAL LETTER =====

        if not re.search(r"[A-Z]", password):

            flash("Add at least one capital letter!", "error")

            return render_template("admin_register.html")

        # ===== SMALL LETTER =====

        if not re.search(r"[a-z]", password):

            flash("Add at least one small letter!", "error")

            return render_template("admin_register.html")

        # ===== NUMBER =====

        if not re.search(r"[0-9]", password):

            flash("Add at least one number!", "error")

            return render_template("admin_register.html")

        # ===== SPECIAL CHARACTER =====

        if not re.search(r"[@$!%*?&]", password):

            flash("Add at least one special character!", "error")

            return render_template("admin_register.html")

        # ===== DATABASE =====

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ===== CHECK EMAIL =====

        cur.execute(
            "SELECT * FROM admin WHERE BINARY email=%s",
            (email,),
        )

        email_data = cur.fetchone()

        if email_data:

            cur.close()

            flash("Email already exists!", "error")

            return render_template("admin_register.html")

        # ===== CHECK USERNAME =====

        cur.execute(
            "SELECT * FROM admin WHERE BINARY username=%s",
            (username,),
        )

        user_data = cur.fetchone()

        if user_data:

            cur.close()

            flash("Username already exists!", "error")

            return render_template("admin_register.html")

        # ===== HASH PASSWORD =====

        hashed_password = generate_password_hash(password)

        # ===== INSERT INTO ADMIN TABLE =====

        cur.execute(
            """
            INSERT INTO admin(username,email,password)
            VALUES(%s,%s,%s)
            """,
            (username, email, hashed_password),
        )

        mysql.connection.commit()

        cur.close()

        # ===== SUCCESS =====

        flash("Admin Registered Successfully!", "success")

        return render_template("admin_register.html", redirect_to_login=True)

    return render_template("admin_register.html")


# -------------------------ADMIN FORGOT PASSWORD ------------------------------------------


@app.route("/admin_forgot_password", methods=["GET", "POST"])
def admin_forgot_password():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()

        # ===== EMPTY CHECK =====

        if not email or not username:

            flash("Fill all fields!", "error")

            return render_template("admin_forgot_password.html")

        # ===== DATABASE =====

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ===== CHECK ADMIN =====

        cur.execute(
            """
            SELECT * FROM admin
            WHERE BINARY email=%s
            AND BINARY username=%s
            """,
            (email, username),
        )

        admin = cur.fetchone()

        cur.close()

        # ===== SUCCESS =====

        if admin:

            session["reset_admin"] = admin["id"]

            flash("Admin verified successfully", "success")

            return render_template(
                "admin_forgot_password.html", redirect_to_change=True
            )

        # ===== INVALID =====

        else:

            flash("Invalid email or username!", "error")

            return render_template("admin_forgot_password.html")

    return render_template("admin_forgot_password.html")


@app.route("/admin_change_password")
def admin_change_password():
    return render_template("admin_change_password.html")


# ------------------- ADMIN RESET PASSWORD PAGE -------------------


@app.route("/admin_reset_password", methods=["GET", "POST"])
def admin_reset_password():

    if request.method == "POST":
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        # ===== EMPTY CHECK =====

        if not new_password or not confirm_password:

            return render_template(
                "admin_change_password.html",
                message="Fill all fields!",
                category="error",
            )

        # ===== MINIMUM 8 CHARACTERS =====

        if len(new_password) < 8:

            return render_template(
                "admin_change_password.html",
                message="Password must contain at least 8 characters!",
                category="error",
            )

        # ===== CAPITAL LETTER CHECK =====

        if not re.search(r"[A-Z]", new_password):

            return render_template(
                "admin_change_password.html",
                message="Add at least one capital letter!",
                category="error",
            )

        # ===== SMALL LETTER CHECK =====

        if not re.search(r"[a-z]", new_password):

            return render_template(
                "admin_change_password.html",
                message="Add at least one small letter!",
                category="error",
            )

        # ===== NUMBER CHECK =====

        if not re.search(r"[0-9]", new_password):

            return render_template(
                "admin_change_password.html",
                message="Add at least one number!",
                category="error",
            )

        # ===== SPECIAL CHARACTER CHECK =====

        if not re.search(r"[@$!%*?&]", new_password):

            return render_template(
                "admin_change_password.html",
                message="Add at least one special character!",
                category="error",
            )

        # ===== PASSWORD MATCH CHECK =====

        if new_password != confirm_password:

            return render_template(
                "admin_change_password.html",
                message="Passwords do not match!",
                category="error",
            )

        # ===== SESSION CHECK =====

        admin_id = session.get("reset_admin")

        if not admin_id:

            return render_template(
                "admin_change_password.html",
                message="Session expired! Try again.",
                category="error",
            )

        # ===== HASH PASSWORD =====

        hashed_password = generate_password_hash(new_password)

        # ===== UPDATE DATABASE =====

        cur = mysql.connection.cursor()

        cur.execute(
            "UPDATE admin SET password=%s WHERE id=%s", (hashed_password, admin_id)
        )

        mysql.connection.commit()
        cur.close()

        # ===== REMOVE SESSION =====

        session.pop("reset_admin", None)

        # ===== SUCCESS =====

        return render_template(
            "admin_change_password.html",
            message="Password changed successfully!",
            category="success",
            redirect_to_login=True,
        )

    return render_template("admin_change_password.html")


# ------------------- ADMIN PAGE -------------------


@app.route("/admin_page")
def admin_page():

    # ===== SESSION CHECK =====

    if "admin_id" not in session:

        return redirect("/admin_login")

    return render_template("admin_page.html")


# ================= DASHBOARD PAGE =================


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_page.html")


# ================= LIVE DASHBOARD =================


from datetime import datetime, timedelta


@app.route("/live-dashboard")
def live_dashboard():

    cursor = mysql.connection.cursor()

    # TOTAL USERS

    cursor.execute("SELECT COUNT(*) FROM register")
    total_users = cursor.fetchone()[0]

    # TOTAL FILES

    cursor.execute("SELECT COUNT(*) FROM files")
    total_files = cursor.fetchone()[0]

    # HARMFUL FILES

    cursor.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE status='harmful'
    """)
    harmful_files = cursor.fetchone()[0]

    # GENUINE FILES

    cursor.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE status='genuine'
    """)
    genuine_files = cursor.fetchone()[0]

    # TODAY UPLOADS

    cursor.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE DATE(created_at)=CURDATE()
    """)
    today_uploads = cursor.fetchone()[0]

    # WEEKLY GRAPH

    weekly_data = []

    weekly_labels = []

    for i in range(6, -1, -1):

        day_date = datetime.now() - timedelta(days=i)

        day_name = day_date.strftime("%a")

        weekly_labels.append(day_name)

        cursor.execute(
            """

            SELECT COUNT(*)

            FROM files

            WHERE DATE(created_at)=CURDATE() - INTERVAL %s DAY

        """,
            (i,),
        )

        count = cursor.fetchone()[0]

        weekly_data.append(count)

    cursor.close()

    return jsonify(
        {
            "total_users": total_users,
            "total_files": total_files,
            "harmful_files": harmful_files,
            "genuine_files": genuine_files,
            "today_uploads": today_uploads,
            "weekly_data": weekly_data,
            "weekly_labels": weekly_labels,
        }
    )


# ================= USERS ANALYTICS =================


# =========================================================
# PARTICULAR USER WEEKLY TREND
# =========================================================
@app.route("/particular_user_weekly_trend")
def particular_user_weekly_trend():

    uploaded_by = request.args.get("uploaded_by")

    cursor = mysql.connection.cursor(dictionary=True)

    query = """

        SELECT

            DAYNAME(created_at) AS day_name,

            COUNT(*) AS uploads

        FROM files

        WHERE uploaded_by = %s

        AND YEARWEEK(created_at,1)=YEARWEEK(CURDATE(),1)

        GROUP BY DAYOFWEEK(created_at)

        ORDER BY DAYOFWEEK(created_at)

    """

    cursor.execute(query, (uploaded_by,))

    data = cursor.fetchall()

    cursor.close()

    return jsonify(data)


@app.route("/daily_login_activity")
def daily_login_activity():

    uploaded_by = request.args.get("uploaded_by")

    cursor = mysql.connection.cursor(dictionary=True)

    query = """

        SELECT

            DAYNAME(login_time) AS day_name,

            COUNT(*) AS logins

        FROM login_activity

        WHERE uploaded_by = %s

        AND YEARWEEK(login_time,1)=YEARWEEK(CURDATE(),1)

        GROUP BY DAYOFWEEK(login_time)

        ORDER BY DAYOFWEEK(login_time)

    """

    cursor.execute(query, (uploaded_by,))

    data = cursor.fetchall()

    cursor.close()

    return jsonify(data)


# ================= PARTICULAR USER DETAILS =================


@app.route("/user-details/<search>")
def user_details(search):

    cursor = mysql.connection.cursor()

    user = None

    # =====================================================
    # SEARCH USING USERNAME
    # =====================================================

    cursor.execute(
        """
        SELECT *
        FROM register
        WHERE LOWER(username)=LOWER(%s)
        """,
        (search,),
    )

    user = cursor.fetchone()

    # =====================================================
    # SEARCH USING uploaded_by ID
    # =====================================================

    if not user and search.isdigit():

        cursor.execute(
            """
            SELECT r.*
            FROM register r
            INNER JOIN files f
            ON r.id = f.uploaded_by
            WHERE f.uploaded_by=%s
            LIMIT 1
            """,
            (search,),
        )

        user = cursor.fetchone()

    # =====================================================
    # USER NOT FOUND
    # =====================================================

    if not user:

        cursor.close()

        return jsonify({"success": False})

    # =====================================================
    # REGISTER TABLE DATA
    # =====================================================

    user_id = user[0]
    username = user[1]

    # =====================================================
    # TOTAL FILES
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        WHERE uploaded_by=%s
        """,
        (user_id,),
    )

    total_files = cursor.fetchone()[0]

    # =====================================================
    # HARMFUL FILES
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        WHERE uploaded_by=%s
        AND LOWER(status)='harmful'
        """,
        (user_id,),
    )

    harmful_files = cursor.fetchone()[0]

    # =====================================================
    # FAKE FILES
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        WHERE uploaded_by=%s
        AND LOWER(status)='fake'
        """,
        (user_id,),
    )

    fake_files = cursor.fetchone()[0]

    # =====================================================
    # GENUINE FILES
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        WHERE uploaded_by=%s
        AND LOWER(status)='genuine'
        """,
        (user_id,),
    )

    genuine_files = cursor.fetchone()[0]

    # =====================================================
    # DUPLICATE FILES
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        WHERE uploaded_by=%s
        AND LOWER(status)='duplicate'
        """,
        (user_id,),
    )

    duplicate_files = cursor.fetchone()[0]

    # =====================================================
    # USER STATUS
    # =====================================================

    if total_files > 0:
        status = "Active User"
    else:
        status = "Inactive User"

    # =====================================================
    # WEEKLY GRAPH DATA
    # =====================================================

    weekly_data = [0, 0, 0, 0, 0, 0, 0]

    cursor.execute(
        """
        SELECT DAYOFWEEK(created_at), COUNT(*)
        FROM files
        WHERE uploaded_by=%s AND DATE(created_at)>=DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY)AND DATE(created_at)<=CURDATE()
        GROUP BY DAYOFWEEK(created_at)
        """,
        (user_id,),
    )

    rows = cursor.fetchall()

    for row in rows:

        day = row[0]
        count = row[1]

        index = day - 2

        if index < 0:
            index = 6

        weekly_data[index] = count

    # =====================================================
    # DAILY LOGIN GRAPH
    # =====================================================

    login_data = [0, 0, 0, 0, 0, 0, 0]

    try:

        cursor.execute(
            """
            SELECT DAYOFWEEK(login_time), COUNT(*)
            FROM login_activity
            WHERE uploaded_by=%s AND DATE(login_time)>=DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE())DAY)AND DATE(login_time)<=CURDATE()
            GROUP BY DAYOFWEEK(login_time)
            """,
            (user_id,),
        )

        login_rows = cursor.fetchall()

        for row in login_rows:

            day = row[0]
            count = row[1]

            index = day - 2

            if index < 0:
                index = 6

            login_data[index] = count

    except:

        login_data = [0, 0, 0, 0, 0, 0, 0]
        cur.close()

    # =====================================================
    # RETURN FINAL JSON
    # =====================================================

    return jsonify(
        {
            "success": True,
            "username": username,
            # uploaded_by id ni user id laga chupisthundi
            "user_id": str(user_id).zfill(2),
            "total_files": total_files,
            "harmful_files": harmful_files,
            "fake_files": fake_files,
            "genuine_files": genuine_files,
            "duplicate_files": duplicate_files,
            "status": status,
            "weekly_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "weekly_data": weekly_data,
            "login_data": login_data,
        }
    )


# =========================================================
# DASHBOARD TOP CARDS DATA
# =========================================================


@app.route("/dashboard-stats")
def dashboard_stats():

    cursor = mysql.connection.cursor()

    # =====================================================
    # TOTAL USERS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM register
        """)

    total_users = cursor.fetchone()[0]

    # =====================================================
    # ACTIVE USERS
    # users who uploaded at least 1 file
    # =====================================================

    cursor.execute("""
        SELECT COUNT(DISTINCT uploaded_by)
        FROM files
        """)

    active_users = cursor.fetchone()[0]

    # =====================================================
    # INACTIVE USERS
    # =====================================================

    inactive_users = total_users - active_users

    if inactive_users < 0:
        inactive_users = 0

    # =====================================================
    # HARMFUL USERS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(DISTINCT uploaded_by)
        FROM files
        WHERE LOWER(status)='harmful'
        """)

    harmful_users = cursor.fetchone()[0]

    # =====================================================
    # NEW USERS TODAY
    # =====================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM register
            WHERE DATE(created_at)=CURDATE()
            """)

        new_users_today = cursor.fetchone()[0]

    except:

        new_users_today = 0

    cursor.close()

    # =====================================================
    # RETURN JSON
    # =====================================================

    return jsonify(
        {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "harmful_users": harmful_users,
            "new_users_today": new_users_today,
        }
    )


# --------------------------------------------------------------------
@app.route("/get-files")
def get_files():

    search = request.args.get("search", "")

    status = request.args.get("status", "")

    date = request.args.get("date", "")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # =========================
    # MAIN QUERY
    # =========================

    query = """

    SELECT *

    FROM files

    WHERE 1=1

    """

    values = []

    # =========================
    # SEARCH
    # =========================

    if search:

        query += """

        AND (

            LOWER(filename) LIKE LOWER(%s)

            OR LOWER(filetype) LIKE LOWER(%s)

            OR LOWER(status) LIKE LOWER(%s)


            OR LOWER(CAST(uploaded_by AS CHAR)) LIKE %s

        )

        """

        search_value = "%" + search + "%"

        values.extend([search_value, search_value, search_value, search_value])

    # =========================
    # STATUS FILTER
    # =========================

    if status:

        query += " AND status=%s "

        values.append(status)

    # =========================
    # DATE FILTER
    # =========================

    if date:

        query += " AND DATE(created_at)=%s "

        values.append(date)

    # =========================
    # ORDER
    # =========================

    query += " ORDER BY created_at DESC "

    cursor.execute(query, values)

    files = cursor.fetchall()

    # =========================
    # TOTAL FILES
    # =========================

    cursor.execute("""

    SELECT COUNT(*)

    AS total

    FROM files

    """)

    total_files = cursor.fetchone()["total"]

    # =========================
    # GENUINE FILES
    # =========================

    cursor.execute("""

    SELECT COUNT(*)

    AS genuine

    FROM files

    WHERE status='genuine'

    """)

    genuine_files = cursor.fetchone()["genuine"]

    # =========================
    # HARMFUL FILES
    # =========================

    cursor.execute("""

    SELECT COUNT(*)

    AS harmful

    FROM files

    WHERE status='harmful'

    """)

    harmful_files = cursor.fetchone()["harmful"]

    # =========================
    # DUPLICATE FILES
    # =========================

    cursor.execute("""

    SELECT COUNT(*)

    AS duplicate_count

    FROM files

    WHERE status='duplicate'

    """)

    duplicate_files = cursor.fetchone()["duplicate_count"]

    # =========================
    # FAKE FILES
    # =========================

    cursor.execute("""

    SELECT COUNT(*)

    AS fake_count

    FROM files

    WHERE status='fake'

    """)

    fake_files = cursor.fetchone()["fake_count"]

    cursor.close()

    # =========================
    # RETURN JSON
    # =========================

    return jsonify(
        {
            "files": files,
            "total_files": total_files,
            "genuine_files": genuine_files,
            "harmful_files": harmful_files,
            "duplicate_files": duplicate_files,
            "fake_files": fake_files,
        }
    )


# ------------------- LOGOUT PAGE -------------------


@app.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect("/login")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
