import unittest
from main import app

class TestPredictAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_predict_endpoint(self):
        # Define a sample input data
        sample_data = {
  "N": 96,
  "P": 34,
  "K":32,
  "temperature": 26.774,
  "humidity": 56.413,
  "ph": 6.78,
  "rainfall": 200.7745
}
        

        # Send a POST request to the predict endpoint
        response = self.app.post('/predict', json=sample_data)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON
        response_data = response.get_json()

        # Assert the structure of the response JSON
        self.assertIn('prediction', response_data)
        self.assertIn('compactibility', response_data)

        # Assert the data types of the response values
        self.assertIsInstance(response_data['prediction'], str)
        self.assertIsInstance(response_data['compactibility'], float)

if __name__ == '__main__':
    unittest.main()
