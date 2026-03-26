@echo off
cd /d "%~dp0apex-backend_2\apex-backend"

echo [APEX] Installation des dependances...
py -m pip install fastapi "uvicorn[standard]" sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-multipart "pydantic[email]" --quiet

echo [APEX] Demarrage du backend...
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
