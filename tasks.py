from invoke import task

@task
def test(c):
    """Run unit tests"""
    c.run("python -m unittest discover -s tests -v")

@task
def coverage(c):
    """Run test coverage"""
    c.run("coverage run -m unittest discover -s tests")
    c.run("coverage report")
    c.run("coverage html")

@task
def build(c):
    """Build the project"""
    c.run("pip install -r requirements.txt")
    c.run("pyinstaller --onefile --name fsa analyzer/main.py")

@task(pre=[test, coverage, build])
def all(c):
    """Run all tasks"""
    print("All tasks completed!")