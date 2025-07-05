from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    idade = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    chest_pain_type = db.Column(db.String(50), nullable=False)
    resting_bp = db.Column(db.Integer, nullable=False)
    cholesterol = db.Column(db.Integer, nullable=False)
    fasting_bs = db.Column(db.Integer, nullable=False)
    resting_ecg = db.Column(db.String(50), nullable=False)
    max_hr = db.Column(db.Integer, nullable=False)
    exercise_angina = db.Column(db.String(10), nullable=False)
    oldpeak = db.Column(db.Float, nullable=False)
    st_slope = db.Column(db.String(50), nullable=False)
    heart_disease = db.Column(db.Integer, nullable=True)