from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flasgger import Swagger
from model.model import db, Patient
from schema.schema import PatientSchema, ValidationError
import pandas as pd
import pickle
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.config['SWAGGER'] = {
    'title': 'API de Exames Médicos',
    'uiversion': 3,
    'openapi': '3.0.3'
}
swagger = Swagger(app, template_file='swagger.json')

def serialize_patient(patient):
    """Serializa um objeto Patient em um dicionário."""
    return {
        'id': patient.id,
        'idade': patient.idade,
        'sexo': patient.sexo,
        'chest_pain_type': patient.chest_pain_type,
        'resting_bp': patient.resting_bp,
        'cholesterol': patient.cholesterol,
        'fasting_bs': patient.fasting_bs,
        'resting_ecg': patient.resting_ecg,
        'max_hr': patient.max_hr,
        'exercise_angina': patient.exercise_angina,
        'oldpeak': patient.oldpeak,
        'st_slope': patient.st_slope,
        'heart_disease': patient.heart_disease
    }

class PatientResource(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = db.session.get(Patient, patient_id)
            if not patient:
                return {'error': 'Paciente não encontrado'}, 404
            return serialize_patient(patient), 200
        patients = Patient.query.all()
        return {
            'patients': [serialize_patient(p) for p in patients],
            'total': len(patients)
        }, 200

    def post(self):
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        try:
            errors, validated_data = PatientSchema.validate_patient_data(data)
            if errors:
                return {'errors': errors}, 400
            patient = Patient(**validated_data)
            db.session.add(patient)
            db.session.commit()
            return {
                'message': 'Paciente criado com sucesso',
                'patient': serialize_patient(patient)
            }, 201
        except ValidationError as err:
            return {'errors': err.messages}, 400
        except Exception as e:
            logger.error(f"Erro ao criar paciente: {str(e)}")
            return {'errors': {'geral': f'Erro interno ao criar paciente: {str(e)}'}}, 500

    def put(self, patient_id):
        patient = db.session.get(Patient, patient_id)
        if not patient:
            return {'error': 'Paciente não encontrado'}, 404
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        try:
            errors, validated_data = PatientSchema.validate_patient_data(data, partial=True)
            if errors:
                return {'errors': errors}, 400
            patient.heart_disease = None
            for key, value in validated_data.items():
                setattr(patient, key, value)
            db.session.commit()
            logger.info(f"Paciente ID {patient_id} atualizado, heart_disease redefinido para null")
            return {
                'message': 'Paciente atualizado com sucesso! Risco cardíaco redefinido para "Não calculado".',
                'patient': serialize_patient(patient)
            }, 200
        except ValidationError as err:
            return {'errors': err.messages}, 400
        except Exception as e:
            logger.error(f"Erro ao atualizar paciente: {str(e)}")
            return {'errors': {'geral': f'Erro interno ao atualizar paciente: {str(e)}'}}, 500

    def delete(self, patient_id):
        patient = db.session.get(Patient, patient_id)
        if not patient:
            return {'error': 'Paciente não encontrado'}, 404
        try:
            db.session.delete(patient)
            db.session.commit()
            return {'message': 'Paciente deletado com sucesso'}, 200
        except Exception as e:
            logger.error(f"Erro ao deletar paciente: {str(e)}")
            return {'errors': {'geral': f'Erro interno ao deletar paciente: {str(e)}'}}, 500

class PatientPredictResource(Resource):
    def post(self, patient_id):
        patient = db.session.get(Patient, patient_id)
        if not patient:
            return {'error': 'Paciente não encontrado'}, 404
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'BEST_model.pkl')
            logger.debug(f"Tentando carregar modelo de: {model_path}")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            logger.debug(f"Preparando dados para previsão: {patient.__dict__}")
            data = {
                'Age': patient.idade,
                'Sex': patient.sexo,
                'ChestPainType': patient.chest_pain_type,
                'RestingBP': patient.resting_bp,
                'Cholesterol': patient.cholesterol,
                'FastingBS': patient.fasting_bs,
                'RestingECG': patient.resting_ecg,
                'MaxHR': patient.max_hr,
                'ExerciseAngina': patient.exercise_angina,
                'Oldpeak': patient.oldpeak,
                'ST_Slope': patient.st_slope
            }
            df = pd.DataFrame([data])
            prediction = model.predict(df)[0]
            
            patient.heart_disease = int(prediction)
            db.session.commit()
            
            logger.info(f"Previsão realizada: heart_disease={prediction} para paciente ID {patient_id}")
            return {
                'message': 'Previsão de risco cardíaco realizada com sucesso',
                'heart_disease': int(prediction),
                'patient': serialize_patient(patient)
            }, 200
        except FileNotFoundError:
            logger.error(f"Modelo BEST_model.pkl não encontrado em: {model_path}")
            return {'error': f'Modelo BEST_model.pkl não encontrado em: {model_path}'}, 500
        except Exception as e:
            logger.error(f"Erro ao realizar previsão: {str(e)}")
            return {'error': f'Erro ao realizar previsão: {str(e)}'}, 500

api.add_resource(PatientResource, '/api/patients', '/api/patients/<int:patient_id>')
api.add_resource(PatientPredictResource, '/api/patients/<int:patient_id>/predict')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)