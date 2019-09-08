class Router:
    """
    Calculate the any-node-to-any-node path.
    Use Floyd-Warshall algorithm.
    Initial time complexity: O(N^3)
    Memory complexity: O(N^2)
    Query time complexity: O(1)
    """

    def __init__(self):
        """
        initialization
        """
        self.routes = {}
        self.points = set()

    def build_routes(self, rows):
        """
        Calculate the any-node-to-any-node path.
        """
        self._build_immediate_routes(rows)
        self._fill_table()
        self._build_continuous_routes()

    def is_valid_point(self, point):
        """
        check if the point is a valid point
        """
        if not isinstance(point, str):
            return False

        return point in self.points

    def get_route(self, point1, point2):
        """
        Return route information from point1 to point2.
        None if such route doesn't exist.
        """
        if not self.is_valid_point(point1) or not self.is_valid_point(point2):
            return None

        if point1 not in self.points or point2 not in self.points:
            return None

        return self.routes[point1][point2]

    def _build_immediate_routes(self, rows):
        """
        fill the information of nodes directly connected
        """
        for row in rows:
            point1 = row['from']
            point2 = row['to']
            cost = row['time']

            if point1 not in self.routes:
                self.routes[point1] = {}
            if point2 not in self.routes[point1]:
                self.routes[point1][point2] = cost

            self.points.add(point1)
            self.points.add(point2)

    def _fill_table(self):
        """
        make the table full for ease of calculations later
        """
        self.routes = {
            point1: {
                point2: (
                    {
                        'time': self.routes[point1][point2],
                        'length': 1,
                        'from': None,
                    }
                    if (point1 in self.routes and
                        point2 in self.routes[point1]
                        )
                    else None
                )
                for point2
                in self.points
            }
            for point1
            in self.points
        }

    def _build_continuous_routes(self):
        """
        Calculate paths of all nodes indirectly connected.
        Use Floyd-Warshall algorithm
        """
        for point1 in self.points:
            for point2 in self.points:
                for point3 in self.points:
                    if (
                        self.routes[point1][point3] is not None and
                        self.routes[point3][point2] is not None
                    ):
                        time_cost = (
                            self.routes[point1][point3]['time'] +
                            self.routes[point3][point2]['time']
                        )

                        length = (
                            self.routes[point1][point3]['length'] +
                            self.routes[point3][point2]['length'])

                        if (
                            self.routes[point1][point2] is None or
                            time_cost < self.routes[point1][point2]['time']
                        ):

                            self.routes[point1][point2] = {
                                'time': time_cost,
                                'length': length,
                                'from': point3
                            }
