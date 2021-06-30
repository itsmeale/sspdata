import os


def check_import_order():
    os.system("isort --check ./sspdata/ --skip __init__.py --gitignore --dont-follow-links --verbose")


def check_code_formatting():
    os.system("black --check ./sspdata/ --exclude __init__.py --verbose")


def sort_import_order():
    os.system("isort ./sspdata/ ./tests/ --skip __init__.py --gitignore --dont-follow-links --verbose")


def do_code_formatting():
    os.system("black ./sspdata/ ./tests/ --exclude __init__.py --exclude .ipynb_checkpoints/ --verbose")


def linter():
    os.system("pylama ./sspdata/ ./tests/")


def run_tests():
    os.system("pytest ./tests/ --verbose --color=yes --code-highlight=yes")
