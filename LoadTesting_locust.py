# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 03:53:40 2024

@author: fatim
"""

from locust import HttpUser, task, between

class DrugInteractionUser(HttpUser):
    wait_time = between(1, 2)  # Random wait time between tasks to mimic real user behavior

    @task
    def query_drug_interactions(self):
        # List of queries and their expected results for validation
        interactions = [
            {"query": "What is the interaction between Bivalirudin and Acemetacin?", "expected": "Risk or severity of bleeding"},
            {"query": "What is the interaction between Goserelin and Ceritinib?", "expected": "QTc-prolonging activities"}
        ]

        for interaction in interactions:
            with self.client.get(f"/query?query_text={interaction['query']}", catch_response=True) as response:
                if response.status_code == 200:
                    # Convert response from JSON format and check the 'completion' field
                    data = response.json()
                    if data.get('completion', '').lower() != interaction['expected'].lower():
                        response.failure(f"Unexpected completion: {data.get('completion')}")
                else:
                    response.failure(f"Failed with status code {response.status_code}")

