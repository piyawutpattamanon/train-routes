import unittest

import app.ui


class TestUI(unittest.TestCase):
    """
    unit test for app.ui.UI class
    """

    def setUp(self):
        """
        setup all dependencies
        """
        self.router = unittest.mock.MagicMock()
        self.loader = unittest.mock.MagicMock()
        self.argparse_module = unittest.mock.MagicMock()
        self.print_function = unittest.mock.MagicMock()
        self.input_function = unittest.mock.MagicMock()

        self.ui = app.ui.CommandLineUI(
            router=self.router,
            loader=self.loader,
            argparse_module=self.argparse_module,
            print_function=self.print_function,
            input_function=self.input_function
        )

    def test_file_not_found(self):
        """
        should stop without errors when CSV file is not found
        """
        self.router.build_routes.side_effect = FileNotFoundError
        self.ui.ask = unittest.mock.MagicMock()

        self.ui.start()

        self.ui.ask.assert_not_called()

    def test_file_found(self):
        """
        should proceed to screen input when CSV file is found
        """
        self.ui.ask = unittest.mock.MagicMock()

        self.ui.start()

        self.ui.ask.assert_called_once()

    def test_incorrect_points(self):
        """
        should ask repeatedly until 2 valid points when some wrong input
        """
        self.router.is_valid_point.side_effect = [
            False, False, True, False, False, False, True, True
        ]
        self.input_function.side_effect = [
            'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8'
        ]
        self.ui.display_route = unittest.mock.MagicMock()

        self.ui.start()

        self.assertEqual(7, self.input_function.call_count)
        self.assertEqual(7, self.router.is_valid_point.call_count)
        self.ui.display_route.assert_called_once_with('p3', 'p7')

    def test_no_route(self):
        """
        should not break when there is no route
        """
        self.router.is_valid_point.side_effect = [True, True]
        self.input_function.side_effect = ['A', 'B']
        self.router.get_route.side_effect = [None]

        self.ui.start()

        self.assertEqual(2, self.router.is_valid_point.call_count)
        self.router.get_route.assert_called_once()

    def test_ok(self):
        """
        should be ok when there is route
        """
        self.router.is_valid_point.side_effect = [True, True]
        self.input_function.side_effect = ['A', 'B']
        self.router.get_route.return_value = {
            'length': 3, 'time': 10, 'from': 'G'}

        self.ui.start()

        self.assertEqual(2, self.router.is_valid_point.call_count)
        self.router.get_route.assert_called_once()


if __name__ == '__main__':
    unittest.main()
