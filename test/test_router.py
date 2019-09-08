import unittest

import app.router


class TestRouter(unittest.TestCase):
    """
    unit test for app.router.Router class
    """

    def get_normal_data(self):
        """
        normal route data to be reused in multiple testsß
        """
        return [
            {
                'from': 'A',
                'to': 'B',
                'time': 2,
            },
            {
                'from': 'B',
                'to': 'C',
                'time': 3,
            },
            {
                'from': 'A',
                'to': 'C',
                'time': 4,
            },
            {
                'from': 'C',
                'to': 'D',
                'time': 1,
            },
            {
                'from': 'X',
                'to': 'Y',
                'time': 5,
            },
            {
                'from': 'Y',
                'to': 'Z',
                'time': 7,
            },
        ]

    def test_immediate_route(self):
        """
        should return route when points are connected directly
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        route = router.get_route('A', 'B')
        self.assertEqual({'time': 2, 'length': 1, 'from': None}, route)

    def test_immediate_route_reversed(self):
        """
        should return no route for B -> A when there is only route for A -> B
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        route = router.get_route('B', 'A')
        self.assertEqual(None, route)

    def test_shortcut_route(self):
        """
        should return the route with min time when there are multiple routes
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        route = router.get_route('A', 'C')
        self.assertEqual({'time': 4, 'length': 1, 'from': None}, route)

    def test_long_route(self):
        """
        should return route when points are connected through multiple stations
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        route = router.get_route('A', 'D')
        self.assertEqual({'time': 5, 'length': 2, 'from': 'C'}, route)

    def test_unconnected_route(self):
        """
        should return no route when points are disconnected
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        route = router.get_route('A', 'X')
        self.assertEqual(None, route)

    def test_invalid_route(self):
        """
        should return None without errors when params types are invalid
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)

        route = router.get_route({}, None)
        self.assertEqual(None, route)

        route = router.get_route(None, None)
        self.assertEqual(None, route)

        route = router.get_route('-', '-')
        self.assertEqual(None, route)

    def test_invalid_point(self):
        """
        should return False when point not found
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        result = router.is_valid_point(None)
        self.assertEqual(False, result)

    def test_invalid_type_point(self):
        """
        should return False when input type is invalid
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        result = router.is_valid_point({})
        self.assertEqual(False, result)

    def test_valid_point(self):
        """
        should return True when the point is valid
        """
        route_data = self.get_normal_data()
        router = app.router.Router()
        router.build_routes(route_data)
        result = router.is_valid_point('A')
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()
