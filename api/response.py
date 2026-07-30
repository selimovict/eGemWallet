from flask import jsonify
from models.base_service_model import BaseServiceModel


def to_json(data, status=200):
    """
    Serijalizuje Service Modele (ili listu istih) u Flask JSON response.
    HTTP status je 200 uvijek kad SP uspjesno odradi (bez baginja).
    Biznis status (npr. "user already exists", "duplicate transaction")
    citaj iz 'Success' i 'Message' polja u response body-ju.
    HTTP 4xx/5xx se rezervisu za stvarne greske (invalid params, DB down, itd.).
    """
    if data is None:
        payload = None
    elif isinstance(data, BaseServiceModel):
        payload = data.to_dict()
    elif isinstance(data, list):
        payload = [d.to_dict() if isinstance(d, BaseServiceModel) else d for d in data]
    else:
        payload = data

    response = jsonify(payload)
    response.status_code = status
    return response


def error_json(message, status=400):
    response = jsonify({"error": message})
    response.status_code = status
    return response
