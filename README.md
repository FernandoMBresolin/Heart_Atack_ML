# Gerenciador de Exames Médicos

## Bem-vindo ao Gerenciador de Exames Médicos, um projeto que combina uma API RESTful e uma interface web para gerenciar registros de pacientes e prever riscos cardíacos usando um modelo de machine learning treinado com o dataset UCI Heart Disease. A API, construída com Flask e SQLite, permite criar, listar, atualizar, deletar pacientes e realizar predições de risco cardíaco. O frontend, desenvolvido com HTML, CSS e JavaScript, oferece uma interface amigável para interagir com a API.

## O projeto é dividido em três módulos principais:

- API: Gerencia dados de pacientes e predições, com documentação interativa via Swagger UI.
- Frontend: Interface web para visualizar, adicionar, editar, deletar pacientes e calcular riscos cardíacos.
- Machine Learning: O modelo é treinado com cinco algoritmos (Regressão Logística, KNN, Árvore de Decisão, Naive Bayes, SVM), otimizado com GridSearchCV, e salvo para uso na API.
