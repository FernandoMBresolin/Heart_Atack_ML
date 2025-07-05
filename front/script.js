document.addEventListener('DOMContentLoaded', () => {
    const patientForm = document.getElementById('patientForm');
    const patientList = document.getElementById('patientList');

    // Função para exibir mensagem de carregamento
    const showLoading = () => {
        patientList.innerHTML = '<tr><td colspan="14" style="text-align: center; padding: 20px;">Carregando...</td></tr>';
    };

    // Função para limpar a tabela
    const hideLoading = () => {
        patientList.innerHTML = '';
    };

    // Função para buscar e renderizar todos os pacientes
    const fetchPatients = async () => {
        showLoading();
        try {
            const response = await fetch('http://127.0.0.1:5000/api/patients');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            const data = await response.json();
            hideLoading();

            // Renderizar cada paciente na tabela
            data.patients.forEach(patient => {
                const row = document.createElement('tr');
                const riskClass = patient.heart_disease === 1 ? 'risk-high' : patient.heart_disease === 0 ? 'risk-low' : '';
                row.innerHTML = `
                    <td>${patient.id}</td>
                    <td>${patient.idade}</td>
                    <td>${patient.sexo}</td>
                    <td>${patient.chest_pain_type}</td>
                    <td>${patient.resting_bp}</td>
                    <td>${patient.cholesterol}</td>
                    <td>${patient.fasting_bs}</td>
                    <td>${patient.resting_ecg}</td>
                    <td>${patient.max_hr}</td>
                    <td>${patient.exercise_angina}</td>
                    <td>${patient.oldpeak}</td>
                    <td>${patient.st_slope}</td>
                    <td class="${riskClass}">${patient.heart_disease === null ? 'Não calculado' : patient.heart_disease === 0 ? 'Sem Risco' : 'Com Risco'}</td>
                    <td>
                        <button class="edit" aria-label="Editar paciente ${patient.id}" onclick="editPatient(${patient.id})">Editar</button>
                        <button class="delete" aria-label="Deletar paciente ${patient.id}" onclick="deletePatient(${patient.id})">Deletar</button>
                        <button class="predict" aria-label="Calcular risco cardíaco do paciente ${patient.id}" onclick="predictHeartDisease(${patient.id})">Calcular Risco</button>
                    </td>
                `;
                patientList.appendChild(row);
            });
        } catch (error) {
            hideLoading();
            alert('Erro ao carregar pacientes: ' + error.message);
        }
    };

    // Manipular envio do formulário (criar ou atualizar paciente)
    patientForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const patientId = document.getElementById('patientId').value;
        const patientData = {
            idade: parseInt(document.getElementById('idade').value),
            sexo: document.getElementById('sexo').value,
            chest_pain_type: document.getElementById('chest_pain_type').value,
            resting_bp: parseInt(document.getElementById('resting_bp').value),
            cholesterol: parseInt(document.getElementById('cholesterol').value),
            fasting_bs: parseInt(document.getElementById('fasting_bs').value),
            resting_ecg: document.getElementById('resting_ecg').value,
            max_hr: parseInt(document.getElementById('max_hr').value),
            exercise_angina: document.getElementById('exercise_angina').value,
            oldpeak: parseFloat(document.getElementById('oldpeak').value),
            st_slope: document.getElementById('st_slope').value
        };

        // Validações no frontend
        const errors = [];
        if (isNaN(patientData.idade) || patientData.idade < 1 || patientData.idade > 120) {
            errors.push('Idade deve estar entre 1 e 120 anos.');
        }
        if (!['M', 'F'].includes(patientData.sexo)) {
            errors.push('Sexo deve ser "M" ou "F".');
        }
        if (!['ATA', 'NAP', 'ASY', 'TA'].includes(patientData.chest_pain_type)) {
            errors.push('Tipo de dor torácica deve ser "ATA", "NAP", "ASY" ou "TA".');
        }
        if (isNaN(patientData.resting_bp) || patientData.resting_bp < 50 || patientData.resting_bp > 250) {
            errors.push('Pressão arterial deve estar entre 50 e 250 mmHg.');
        }
        if (patientData.resting_bp === 0) {
            errors.push('Pressão arterial não pode ser 0.');
        }
        if (isNaN(patientData.cholesterol) || patientData.cholesterol < 30 || patientData.cholesterol > 600) {
            errors.push('Colesterol deve estar entre 30 e 600 mg/dl.');
        }
        if (patientData.cholesterol === 0) {
            errors.push('Colesterol não pode ser 0.');
        }
        if (![0, 1].includes(patientData.fasting_bs)) {
            errors.push('Glicemia em jejum deve ser 0 ou 1.');
        }
        if (!['Normal', 'ST', 'LVH'].includes(patientData.resting_ecg)) {
            errors.push('ECG em repouso deve ser "Normal", "ST" ou "LVH".');
        }
        if (isNaN(patientData.max_hr) || patientData.max_hr < 40 || patientData.max_hr > 220) {
            errors.push('Frequência cardíaca máxima deve estar entre 40 e 220.');
        }
        if (!['Y', 'N'].includes(patientData.exercise_angina)) {
            errors.push('Angina induzida por exercício deve ser "Y" ou "N".');
        }
        if (isNaN(patientData.oldpeak) || patientData.oldpeak < -5.0 || patientData.oldpeak > 10.0) {
            errors.push('Oldpeak deve estar entre -5.0 e 10.0.');
        }
        if (!['Up', 'Flat', 'Down'].includes(patientData.st_slope)) {
            errors.push('Inclinação ST deve ser "Up", "Flat" ou "Down".');
        }

        if (errors.length > 0) {
            alert('Erros no formulário:\n' + errors.join('\n'));
            return;
        }

        // Enviar dados para a API
        try {
            const url = patientId ? `http://127.0.0.1:5000/api/patients/${patientId}` : 'http://127.0.0.1:5000/api/patients';
            const method = patientId ? 'PUT' : 'POST';
            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(patientData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                let errorMessage = 'Falha ao salvar paciente.';
                if (errorData.errors) {
                    const translatedErrors = Object.entries(errorData.errors).map(([key, value]) => {
                        switch (key) {
                            case 'idade':
                                return `Idade: ${value}`;
                            case 'sexo':
                                return `Sexo: ${value}`;
                            case 'chest_pain_type':
                                return `Tipo de dor torácica: ${value}`;
                            case 'resting_bp':
                                return `Pressão arterial: ${value}`;
                            case 'cholesterol':
                                return `Colesterol: ${value}`;
                            case 'fasting_bs':
                                return `Glicemia em jejum: ${value}`;
                            case 'resting_ecg':
                                return `ECG em repouso: ${value}`;
                            case 'max_hr':
                                return `Frequência cardíaca máxima: ${value}`;
                            case 'exercise_angina':
                                return `Angina induzida por exercício: ${value}`;
                            case 'oldpeak':
                                return `Oldpeak: ${value}`;
                            case 'st_slope':
                                return `Inclinação ST: ${value}`;
                            default:
                                return `${key}: ${value}`;
                        }
                    });
                    alert('Erros do servidor:\n' + translatedErrors.join('\n'));
                    return;
                }
                alert(errorMessage);
                return;
            }

            alert(method === 'POST' ? 'Paciente criado com sucesso!' : 'Paciente atualizado com sucesso! Risco cardíaco redefinido para "Não calculado".');
            patientForm.reset();
            document.getElementById('patientId').value = '';
            document.getElementById('fasting_bs').value = '0';
            await fetchPatients();
        } catch (error) {
            alert('Erro de conexão com o servidor: ' + error.message);
        }
    });

    // Função para editar um paciente
    window.editPatient = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/patients/${id}`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            const patient = await response.json();
            document.getElementById('patientId').value = patient.id;
            document.getElementById('idade').value = patient.idade;
            document.getElementById('sexo').value = patient.sexo;
            document.getElementById('chest_pain_type').value = patient.chest_pain_type;
            document.getElementById('resting_bp').value = patient.resting_bp;
            document.getElementById('cholesterol').value = patient.cholesterol;
            document.getElementById('fasting_bs').value = patient.fasting_bs.toString();
            document.getElementById('resting_ecg').value = patient.resting_ecg;
            document.getElementById('max_hr').value = patient.max_hr;
            document.getElementById('exercise_angina').value = patient.exercise_angina;
            document.getElementById('oldpeak').value = patient.oldpeak;
            document.getElementById('st_slope').value = patient.st_slope;
        } catch (error) {
            alert('Erro ao carregar paciente: ' + error.message);
        }
    };

    // Função para deletar um paciente
    window.deletePatient = async (id) => {
        if (confirm('Tem certeza que deseja deletar este paciente?')) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/patients/${id}`, { method: 'DELETE' });
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                alert('Paciente deletado com sucesso!');
                await fetchPatients();
            } catch (error) {
                alert('Erro ao deletar paciente: ' + error.message);
            }
        }
    };

    // Função para calcular risco cardíaco
    window.predictHeartDisease = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/patients/${id}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) {
                const errorData = await response.json();
                alert('Erro ao calcular risco: ' + (errorData.error || 'Falha na previsão'));
                return;
            }
            const data = await response.json();
            alert('Risco cardíaco calculado: ' + (data.heart_disease === 0 ? 'Sem Risco' : 'Com Risco'));
            await fetchPatients();
        } catch (error) {
            alert('Erro ao calcular risco: ' + error.message);
        }
    };

    // Carregar pacientes ao iniciar
    fetchPatients();
});