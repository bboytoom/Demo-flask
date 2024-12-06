class CustomAsserts:

    def assert_json_response(self,
                             response,
                             expected_result_status: str,
                             expected_status_code: int,
                             expected_exceptions: dict | None):

        response_data = response.get_json()

        self.assertEqual(response.status_code, expected_status_code)

        if response_data and expected_status_code != 204:
            self.assertIsInstance(response_data, dict)
            self.assertIn(expected_result_status,
                          response_data.get('error', response_data.get('message')))

            if expected_exceptions:
                for field, _ in expected_exceptions.items():
                    with self.subTest(field=field):
                        if response_data.get('exception', None):
                            self.assertEqual(expected_exceptions[field],
                                             response_data['exception'][field])
                            self.assertIn(field, response_data['exception'])
                        elif response_data.get('data', None):
                            self.assertEqual(
                                expected_exceptions[field], response_data['data'][field])
                        else:
                            self.assertEqual(expected_exceptions[field], response_data[field])
