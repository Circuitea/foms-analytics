from functools import cache
from flask import Blueprint, request, current_app, abort
from pickle import load
import math
import numpy as np
import pandas as pd
import os

bp = Blueprint('recommendations', __name__, url_prefix='/recommendations')

@cache
def Model(model_ident):
  model_path = os.path.join(current_app.instance_path, 'models', f"{model_ident}.pkl")

  if not os.path.isfile(model_path):
    raise FileNotFoundError(f"'{model_ident}' is an invalid model identifier.")
  
  with open(model_path, 'rb') as f:
    model = load(f)

  return model

@cache
def Scaler(model_ident):
  scaler_path = os.path.join(current_app.instance_path, 'scalers', f"{model_ident}.scaler.pkl")

  if not os.path.isfile(scaler_path):
    raise FileNotFoundError(f"'{model_ident}' is an invalid scaler identifer.")
  
  with open(scaler_path, "rb") as f:
    scaler = load(f)

  return scaler


@bp.post('/<model_ident>/make')
def make(model_ident):
  output = []
  predictions = {}
  data = {
    'year': request.json['year'],
    'month': request.json['month'],
    'quarter': request.json['quarter'],
    'quantity': request.json['quantities'], # array of 6
  }

  X = pd.DataFrame([{
    'Time_Index': 0,
    'Month': data['month'],
    'Quarter': data['quarter'],
    'Year': data['year'],

    'Month_Sin': math.sin(2 * np.pi * data['month'] / 12),
    'Month_Cos': math.cos(2 * np.pi * data['month'] / 12),
    'Quarter_Sin': math.sin(2 * np.pi * data['quarter'] / 4),
    'Quarter_Cos': math.cos(2 * np.pi * data['quarter'] / 4),

    'Lag_1': data['quantity'][1],
    'Lag_2': data['quantity'][2],
    'Lag_3': data['quantity'][3],

    'Rolling_Mean_3': np.mean(data['quantity'][:3]),
    'Rolling_Mean_6': np.mean(data['quantity'][:6]),
    'Rolling_Std_3': np.std(data['quantity'][:3]),
  }])

  try:
    scaler = Scaler(model_ident)
    model = Model(model_ident)

    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)

  except FileNotFoundError:
    abort(404)

  return {
    'model_ident': model_ident,
    'X': X.to_dict(),
    'X_scaled': X_scaled.tolist(),
    'predictions': predictions.tolist(),
  }
