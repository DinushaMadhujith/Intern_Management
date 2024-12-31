from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'os.urandom(24)'

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": "intern_management",
    "user": "intern_management_user",
    "password": "XChpmRsUyOVX3CZ6apsTM2vIl35gGlQE",
    "host": "dpg-ctk6o3i3esus73e6a18g-a.oregon-postgres.render.com"
}

# Database Connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Home Page: Display All Interns
@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, mobile, nic, email, training_start_date, training_end_date, 
                   field_of_specialization, supervisor, target_date 
            FROM interns;
        """)
        interns = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("view.html", interns=interns)
    except Exception as e:
        return f"Error: {str(e)}"

# Add Intern: Form and Submission
@app.route("/add_intern", methods=["GET", "POST"])
def add_intern():
    if request.method == "POST":
        try:
            # Retrieve form data
            name = request.form["name"]
            mobile = request.form["mobile"]
            nic = request.form["nic"]
            email = request.form["email"]
            address = request.form["address"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            institute = request.form["institute"]
            languages = request.form["languages"]
            field = request.form["field"]
            supervisor = request.form["supervisor"]
            assigned_work = request.form["assigned_work"]
            target_date = request.form["target_date"]

            # Insert data into PostgreSQL
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO interns (name, mobile, nic, email, address, training_start_date, training_end_date, institute, 
                                     languages_known, field_of_specialization, supervisor, assigned_work, target_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (name, mobile, nic, email, address, start_date, end_date, institute, languages, field, supervisor, assigned_work, target_date)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Intern added successfully!", "success")
            return redirect(url_for("home"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
    return render_template("form.html", intern=None)

# Update Intern
@app.route("/update_intern/<int:id>", methods=["GET", "POST"])
def update_intern(id):
    if request.method == "POST":
        try:
            # Retrieve form data
            name = request.form["name"]
            mobile = request.form["mobile"]
            email = request.form["email"]
            address = request.form["address"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            institute = request.form["institute"]
            languages = request.form["languages"]
            field = request.form["field"]
            supervisor = request.form["supervisor"]
            assigned_work = request.form["assigned_work"]
            target_date = request.form["target_date"]

            # Update data in PostgreSQL
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE interns
                SET name=%s, mobile=%s, email=%s, address=%s, training_start_date=%s, training_end_date=%s, 
                    institute=%s, languages_known=%s, field_of_specialization=%s, supervisor=%s, 
                    assigned_work=%s, target_date=%s
                WHERE id=%s;
                """,
                (name, mobile, email, address, start_date, end_date, institute, languages, field, supervisor, assigned_work, target_date, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Intern updated successfully!", "success")
            return redirect(url_for("home"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
    else:
        # Retrieve intern details for pre-filling
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM interns WHERE id = %s;", (id,))
        intern = cur.fetchone()
        cur.close()
        conn.close()
        return render_template("form.html", intern=intern)

# Delete Intern
@app.route("/delete_intern/<int:id>", methods=["GET", "POST"])
def delete_intern(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM interns WHERE id = %s;", (id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Intern deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for("home"))

@app.route("/search", methods=["GET", "POST"])
def search_intern():
    search_nic = request.form.get("search_nic", "").strip()  # NIC value from form
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, mobile, nic, email, training_start_date, training_end_date,
                   field_of_specialization, supervisor, target_date
            FROM interns
            WHERE nic = %s;
        """, (search_nic,))
        intern = cur.fetchone()  # Fetch the record
        cur.close()
        conn.close()
        if intern:
            return render_template("search_results.html", intern=intern)
        else:
            flash("No intern found with the given NIC.", "error")
            return redirect(url_for("home"))
    except Exception as e:
        return f"Error: {str(e)}"



# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)

