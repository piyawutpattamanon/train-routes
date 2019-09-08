import unittest
import unittest.mock

import app.loader


class TestLoader(unittest.TestCase):
    """
    unit test for app.loader.CSVLoader
    """

    def setUp(self):
        self.file_open_function = unittest.mock.MagicMock()

        self.loader = app.loader.CSVLoader()
        self.loader.set_file_path('somepath')
        self.loader.set_file_open(self.file_open_function)

    def test_file_not_found(self):
        """
        should raise FileNotFoundError when csv file not found
        """
        self.file_open_function.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            for _ in self.loader:
                pass

    def test_normal(self):
        """
        should return correct result when input is correct
        """

        def csv_reader(self): return iter(
            [
                ['10', '20', '30'],
                ['12', '22', '40'],
                ['14', '24', '5'],
            ]
        )

        self.loader.set_csv_reader(csv_reader)

        result = []
        for item in self.loader:
            result.append(item)

        expected = [
            {'from': '10', 'to': '20', 'time': 30},
            {'from': '12', 'to': '22', 'time': 40},
            {'from': '14', 'to': '24', 'time': 5},
        ]

        self.assertEqual(expected, result)

    def test_invalid_number(self):
        """
        should skip gracefully when some rows are invalid
        """

        def csv_reader(self): return iter(
            [
                ['10', '20', '30'],
                ['11', '21', None],
                ['12', '22', '40'],
                ['13', '23', 'xx'],
                ['14', '24', '5'],
            ]
        )

        self.loader.set_csv_reader(csv_reader)

        result = []
        for item in self.loader:
            result.append(item)

        expected = [
            {'from': '10', 'to': '20', 'time': 30},
            None,
            {'from': '12', 'to': '22', 'time': 40},
            None,
            {'from': '14', 'to': '24', 'time': 5},
        ]

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
