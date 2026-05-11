# ATV-QualidadeTestes

## Aula20 - Projeto final
Este repositorio consolida as atividades de qualidade e testes com Flask.

### Requisitos
- Python 3.11+
- Google Chrome ou Chromium (E2E com Selenium)

### Instalacao
```bash
cd Aula20
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Executar a aplicacao
```bash
cd Aula20
python run.py
```
Acesse `http://127.0.0.1:5000`.

### Qualidade e testes
```bash
cd Aula20
black --check .
flake8 .
pytest
```
Para executar os testes E2E localmente, defina o caminho do navegador:
```bash
export CHROME_BIN=/usr/bin/google-chrome
```
Se o navegador nao estiver disponivel, os testes E2E sao marcados como skipped.

### Tipos de testes
- Unitarios: `tests/unit`
- Integracao: `tests/integration`
- Funcionais: `tests/functional`
- E2E (Selenium): `tests/e2e`

### Evidencia de TDD (RED -> GREEN -> REFACTOR)
Nova funcionalidade: filtro por nome em `GET /users?name=...`.

- RED: testes adicionados em `tests/functional/test_users_functional.py` e
	`tests/integration/test_user_routes_integration.py` falharam inicialmente.
- GREEN: implementacao do filtro em `app/services/user_service.py` e
	`app/routes/user_routes.py`.
- REFACTOR: normalizacao de nome com `normalize_name()` e reutilizacao da
	validacao de duplicidade.

### CI/CD
Pipeline configurada em `.github/workflows/ci.yml` executa:
`pytest`, `flake8 .`, `black --check .`.
No CI, o Chromium e instalado e `CHROME_BIN` e configurado automaticamente.