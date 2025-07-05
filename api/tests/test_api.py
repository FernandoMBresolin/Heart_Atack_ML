import pytest
import sys
import os
import pickle
from io import BytesIO

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from model.model import Patient
from schema.schema import PatientSchema
import json

# Configuração do ambiente de teste
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()

# Dados válidos para testes
valid_patient_data = {
    'idade': 45,
    'sexo': 'M',
    'chest_pain_type': 'ATA',
    'resting_bp': 120,
    'cholesterol': 200,
    'fasting_bs': 0,
    'resting_ecg': 'Normal',
    'max_hr': 150,
    'exercise_angina': 'N',
    'oldpeak': 1.5,
    'st_slope': 'Up'
}

# Dados adicionais para teste
different_patient_data = {
    'idade': 70,
    'sexo': 'F',
    'chest_pain_type': 'ASY',
    'resting_bp': 130,
    'cholesterol': 300,
    'fasting_bs': 1,
    'resting_ecg': 'ST',
    'max_hr': 110,
    'exercise_angina': 'Y',
    'oldpeak': 2.0,
    'st_slope': 'Flat'
}

# Testes para GET /api/patients
def test_get_all_patients_empty(client):
    response = client.get('/api/patients')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 0
    assert data['patients'] == []

def test_get_all_patients_with_data(client):
    client.post('/api/patients', json=valid_patient_data)
    response = client.get('/api/patients')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 1
    assert len(data['patients']) == 1
    assert data['patients'][0]['idade'] == 45
    assert data['patients'][0]['sexo'] == 'M'

# Testes para POST /api/patients
def test_create_patient_success(client):
    response = client.post('/api/patients', json=valid_patient_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Paciente criado com sucesso'
    assert 'patient' in data
    assert data['patient']['id'] == 1
    assert data['patient']['idade'] == 45
    assert data['patient']['heart_disease'] is None

def test_create_patient_invalid_data(client):
    invalid_data = valid_patient_data.copy()
    invalid_data['idade'] = 150  # Fora do intervalo
    response = client.post('/api/patients', json=invalid_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data
    assert 'idade' in data['errors']
    assert data['errors']['idade'][0] == 'Idade deve estar entre 1 e 120 anos.'

def test_create_patient_missing_field(client):
    invalid_data = valid_patient_data.copy()
    del invalid_data['sexo']
    response = client.post('/api/patients', json=invalid_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data
    assert 'sexo' in data['errors']

# Testes para GET /api/patients/{patient_id}
def test_get_patient_by_id_success(client):
    client.post('/api/patients', json=valid_patient_data)
    response = client.get('/api/patients/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['idade'] == 45
    assert data['sexo'] == 'M'

def test_get_patient_by_id_not_found(client):
    response = client.get('/api/patients/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

# Testes para PUT /api/patients/{patient_id}
def test_update_patient_success(client):
    client.post('/api/patients', json=valid_patient_data)
    update_data = {'idade': 50, 'sexo': 'F'}
    response = client.put('/api/patients/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Paciente atualizado com sucesso! Risco cardíaco redefinido para "Não calculado".'
    assert 'patient' in data
    assert data['patient']['idade'] == 50
    assert data['patient']['sexo'] == 'F'
    assert data['patient']['heart_disease'] is None

def test_update_patient_invalid_data(client):
    client.post('/api/patients', json=valid_patient_data)
    update_data = {'idade': 150}
    response = client.put('/api/patients/1', json=update_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data
    assert 'idade' in data['errors']
    assert data['errors']['idade'][0] == 'Idade deve estar entre 1 e 120 anos.'

def test_update_patient_not_found(client):
    response = client.put('/api/patients/999', json=valid_patient_data)
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

# Testes para DELETE /api/patients/{patient_id}
def test_delete_patient_success(client):
    client.post('/api/patients', json=valid_patient_data)
    response = client.delete('/api/patients/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Paciente deletado com sucesso'
    response = client.get('/api/patients/1')
    assert response.status_code == 404

def test_delete_patient_not_found(client):
    response = client.delete('/api/patients/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

# Testes para POST /api/patients/{patient_id}/predict
def test_predict_patient_success(client):
    # Criar um paciente
    client.post('/api/patients', json=valid_patient_data)
    response = client.post('/api/patients/1/predict')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Previsão de risco cardíaco realizada com sucesso'
    assert data['heart_disease'] in [0, 1]
    assert data['patient']['heart_disease'] == data['heart_disease']

def test_predict_patient_different_data(client):
    # Criar um paciente com dados diferentes
    client.post('/api/patients', json=different_patient_data)
    response = client.post('/api/patients/1/predict')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Previsão de risco cardíaco realizada com sucesso'
    assert data['heart_disease'] in [0, 1]
    assert data['patient']['heart_disease'] == data['heart_disease']

def test_predict_patient_not_found(client):
    response = client.post('/api/patients/999/predict')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_predict_patient_model_not_found(client, monkeypatch):
    # Simular FileNotFoundError
    def mock_open(*args, **kwargs):
        raise FileNotFoundError
    monkeypatch.setattr('builtins.open', mock_open)
    client.post('/api/patients', json=valid_patient_data)
    response = client.post('/api/patients/1/predict')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert data['error'].startswith('Modelo BEST_model.pkl não encontrado')