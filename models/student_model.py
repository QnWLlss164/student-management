from core.db_singleton import Database

class Student:
    def __init__(self, id, student_id, name, classroom, midterm, final):
        self.id = id
        self.student_id = student_id
        self.name = name
        self.classroom = classroom
        self.midterm = midterm
        self.final = final

    @staticmethod
    def from_row(row):
        return Student(
            id=row["id"],
            student_id=row["student_id"],
            name=row["name"],
            classroom=row["classroom"],
            midterm=row["midterm"],
            final=row["final"]
        )

def get_all_students():
    db = Database().get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM students ORDER BY id DESC;")
    rows = cur.fetchall()
    return [Student.from_row(r) for r in rows]

def get_student_by_id(student_db_id: int):
    db = Database().get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM students WHERE id=?;", (student_db_id,))
    row = cur.fetchone()
    return Student.from_row(row) if row else None

def create_student(student_id, name, classroom, midterm, final):
    db = Database().get_connection()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO students (student_id, name, classroom, midterm, final)
        VALUES (?,?,?,?,?)
    """, (student_id, name, classroom, midterm, final))
    db.commit()

def update_student(student_db_id, student_id, name, classroom, midterm, final):
    db = Database().get_connection()
    cur = db.cursor()
    cur.execute("""
        UPDATE students
        SET student_id=?, name=?, classroom=?, midterm=?, final=?
        WHERE id=?
    """, (student_id, name, classroom, midterm, final, student_db_id))
    db.commit()

def delete_student(student_db_id):
    db = Database().get_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM students WHERE id=?;", (student_db_id,))
    db.commit()
