# Development of applications with FAST API

### Install the fast api and the dependencied (uvconr) - recommended to install in a virtual environment

```
python3 -m pip install "fastapi[all]"
```

### Create a main.py file and create the first api

```
from fastapi import FastAPI

app = FastAPI()

app.get("/")
async def func_name():
    return {"what_ever"}

```

### Run the server
```
uvicorn main:app --reload
# Make sure run the above commond in the main file directory
```

### Access the api
* Navigate to the localhost url
* type /docs after the port number in the url for swagger documentation

## Create a object with BASE MODEL - boject will have different variables
Basemodel is a datavalidation library from Pydantic (is data validation and settings management)

from pydantic import BaseModel
