# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Home route (shows form)
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Handle form submission
# @app.route('/submit', methods=['POST'])
# def submit():
#     name = request.form['name']
#     email = request.form['email']

#     return f"Hello {name}, your email is {email}"

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request
from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os

app = Flask(__name__)

# Change these if needed
DB_USER = os.getenv("DB_USER", "flaskuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "flaskpass123")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "flaskdb")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)


# Create table if it does not exist
Base.metadata.create_all(engine)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not email:
        return "Name and email are required", 400

    session = SessionLocal()
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        return f"Saved successfully: {name} ({email})"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Database error: {str(e)}", 500
    finally:
        session.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)