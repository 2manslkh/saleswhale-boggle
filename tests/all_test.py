import unittest
import requests
import json
from jsonschema import ValidationError, validate
from pprint import pprint

from flask import jsonify

BASE_URL = "http://localhost:5000/"

class BasicTests(unittest.TestCase):
    
    def test_1_start_game_random(self):
        payload = {
            'duration':1000,
            'random':True,
        }
        response = requests.post(BASE_URL + "games",json=payload)
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code, 201)

    def test_2_start_game_default(self):
        payload = {
            'duration':1000,
            'random':False,
        }
        response = requests.post(BASE_URL + "games",json=payload)
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['board'], "T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D")

    def test_3_start_game_invalid_duration(self):
        payload = {
            'duration':-1,
            'random':True,
        }
        response = requests.post(BASE_URL + "games",json=payload)
        print(response.status_code)
        print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_4_start_game_invalid_board_length(self):
        payload = {
            'duration':1000,
            'random':False,
            'board':"ABC"
        }
        response = requests.post(BASE_URL + "games",json=payload)
        print(response.status_code)
        print(response.text)
        self.assertEqual(response.status_code, 400)

        payload = {
            'duration':1000,
            'random':False,
            'board':"161616161616"
        }
        response = requests.post(BASE_URL + "games",json=payload)
        print(response.status_code)
        print(response.text)
        self.assertEqual(response.status_code, 400)

        payload = {
            'duration':1000,
            'random':False,
            'board':r"\r\b\s"
        }
        response = requests.post(BASE_URL + "games",json=payload)
        print(response.status_code)
        print(response.text)
        self.assertEqual(response.status_code, 400)