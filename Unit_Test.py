#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 16:43:55 2024

@author: mehta
"""

        
from fastapi.testclient import TestClient
from DDI_API_copy import app, DocumentID, Metadata  # Adjust the import to match your actual file structure and name
import pytest

client = TestClient(app)

def test_drug_interaction(mocker):
    # Arrange
    interaction_query = {"id": "0", "query_text": "What is the interaction between Goserelin and Ceritinib?"}
    mock_response = {"id": "0", "completion": "QTc-prolonging activities"}
    mocker.patch("DDI_API_copy.fetch_document_details", return_value=mock_response)  # Adjust the path

    # Act
    response = client.post("/document/details", json=interaction_query)

    # Assert
    assert response.status_code == 200
    assert response.json() == mock_response