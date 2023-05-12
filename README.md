# Finance API

Final project for ItSchool course, Python - Intro To Programming.

A webserver with a REST API for keeping track of your different financial assets that allows you to see/compare their evolution.

For Windows, steps to deploy:

```
git clone <git_repo_url>
cd itschool3-finance-project
python3 -m venv env/
env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

```


For Linux, steps to deploy:
```
git clone <git_repo_url>
cd itschool3-finance-project
python3 -m venv env/
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

This project uses FastAPI & uvicorn.

FastAPI docs: https://fastapi.tiangolo.com/
    
The data used in this project is provided through yfinance and yahooquery.

yfinance docs: https://pypi.org/project/yfinance/ yahooquery docs: https://yahooquery.dpguthrie.com/