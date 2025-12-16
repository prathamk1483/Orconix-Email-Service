echo "Deployment started"

python3.12 -m venv env

source env/bin/activate

echo "Environment created"

pip install --upgrade pip
pip install Django==5.1.6 sqlparse==0.5.3 tzdata==2025.1

echo "Installing PsycoPG"

python manage.py collectstatic --noinput

echo "Deployment completed"