from flask import Flask
from config import Config
from routes.student_routes import student_bp
from core.db_singleton import Database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Tạo bảng nếu chưa có
    Database().init_schema()

    # Gắn blueprint
    app.register_blueprint(student_bp)

    @app.route("/")
    def index():
        return """
        <div style="font-family: system-ui; padding:24px;">
            <h2>Student Management Home</h2>
            <p><a href='/students/' style='color:#4f46e5;font-weight:500;text-decoration:none;'>→ Đi tới danh sách sinh viên</a></p>
        </div>
        """

    return app

if __name__ == "__main__":
    app = create_app()
    # debug=True chỉ nên dùng khi dev
    app.run(debug=True)
