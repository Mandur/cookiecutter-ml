import os
from typing import Dict, List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import numpy as np
import joblib

app = FastAPI()


class Values(BaseModel):
    data: List = [[]]


@app.get('/api/infer',status_code=200)
def check():
    return 


@app.post('/api/infer')
def extract(values: Values):
    j_data = np.array(values.data)
    y_hat = np.array2string(joblib.load('model.pkl').predict(j_data))
    return y_hat

# Remove these two lines below for non-debug/production mode
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)