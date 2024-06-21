from fabric import task

@task
def deploy(c):
    c.run('git pull origin main')
    c.run('source venv/bin/activate && pip install -r requirements.txt')
    c.run('source venv/bin/activate && flask db upgrade')
    c.run('sudo systemctl restart myapp')
