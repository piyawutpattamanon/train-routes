import argparse

import app.loader
import app.router


class CommandLineUI:
    """
    The command line interface for Train Routes app
    """

    def __init__(self, router, loader,
                 argparse_module=argparse,
                 print_function=print,
                 input_function=input
                 ):
        """
        initialization
        """
        self.loader = loader
        self.router = router

        self.argparse_module = argparse_module
        self.output = print_function
        self.input = input_function

    def start(self):
        """
        start the UI
        """
        self.get_args()
        self.loader.set_file_path(self.args.file)

        try:
            self.router.build_routes(self.loader)
        except FileNotFoundError:
            self.output('File', self.args.file, 'not found.')
            return

        self.ask()

    def ask(self):
        """
        ask for starting and destination points and show routes
        """
        points = self.get_points()
        self.display_route(points['from'], points['to'])

    def get_points(self):
        """
        ask for starting and destination points
        """
        point1 = None
        while point1 is None:
            self.output('What station are you getting on the train?:', end='')
            point = self.input().strip()
            if self.router.is_valid_point(point):
                point1 = point
            else:
                self.output("That's not a valid point.")

        point2 = None
        while point2 is None:
            self.output('What station are you getting off the train?:', end='')
            point = self.input().strip()
            if self.router.is_valid_point(point):
                point2 = point
            else:
                self.output("That's not a valid point.")

        result = {
            'from': point1,
            'to': point2,
        }

        return result

    def display_route(self, point1, point2):
        """
        display the route information
        """
        route = self.router.get_route(point1, point2)
        if route is None:
            self.output('No routes from', point1, 'to', point2)
        else:
            self.output(
                'Your trip from',
                point1,
                'to',
                point2,
                'includes',
                route['length']-1,
                'stops and will take',
                route['time'],
                'minutes.'
            )

    def get_args(self):
        """
        process the command line arguments
        """
        parser = self.argparse_module.ArgumentParser(
            description="THE Train Routes App"
        )
        parser.add_argument(
            '--file',
            default='routes.csv',
            help='The path to CSV file'
        )

        self.args = parser.parse_args()
