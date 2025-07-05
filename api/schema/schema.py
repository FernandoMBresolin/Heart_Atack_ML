from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Range, OneOf

class PatientSchema:
    @staticmethod
    def validate_patient_data(data, partial=False):
        schema = PatientSchemaImpl(partial=partial)
        try:
            validated_data = schema.load(data)
            return {}, validated_data
        except ValidationError as err:
            return err.messages, {}

class PatientSchemaImpl(Schema):
    idade = fields.Integer(required=True, validate=Range(min=1, max=120, error="Idade deve estar entre 1 e 120 anos."))
    sexo = fields.String(required=True, validate=OneOf(['M', 'F'], error="Sexo deve ser 'M' ou 'F'."))
    chest_pain_type = fields.String(required=True, validate=OneOf(['ATA', 'NAP', 'ASY', 'TA'], error="Tipo de dor torácica deve ser 'ATA', 'NAP', 'ASY' ou 'TA'."))
    resting_bp = fields.Integer(required=True, validate=Range(min=50, max=250, error="Pressão arterial deve estar entre 50 e 250 mmHg."))
    cholesterol = fields.Integer(required=True, validate=Range(min=30, max=600, error="Colesterol deve estar entre 30 e 600 mg/dl."))
    fasting_bs = fields.Integer(required=True, validate=OneOf([0, 1], error="Glicemia em jejum deve ser 0 ou 1."))
    resting_ecg = fields.String(required=True, validate=OneOf(['Normal', 'ST', 'LVH'], error="ECG em repouso deve ser 'Normal', 'ST' ou 'LVH'."))
    max_hr = fields.Integer(required=True, validate=Range(min=40, max=220, error="Frequência cardíaca máxima deve estar entre 40 e 220."))
    exercise_angina = fields.String(required=True, validate=OneOf(['Y', 'N'], error="Angina induzida por exercício deve ser 'Y' ou 'N'."))
    oldpeak = fields.Float(required=True, validate=Range(min=-5.0, max=10.0, error="Oldpeak deve estar entre -5.0 e 10.0."))
    st_slope = fields.String(required=True, validate=OneOf(['Up', 'Flat', 'Down'], error="Inclinação ST deve ser 'Up', 'Flat' ou 'Down'."))

    def __init__(self, partial=False, **kwargs):
        super().__init__(**kwargs)
        if partial:
            for field in self.fields.values():
                field.required = False

    @validates('resting_bp')
    def validate_resting_bp(self, value, **kwargs):
        if value == 0:
            raise ValidationError('Pressão arterial não pode ser 0.')

    @validates('cholesterol')
    def validate_cholesterol(self, value, **kwargs):
        if value == 0:
            raise ValidationError('Colesterol não pode ser 0.')