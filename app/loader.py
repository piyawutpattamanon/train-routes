import csv


class CSVLoader:
    """
    load route from CSV
    """

    def __init__(self):
        """
        initialization
        """
        self.file_path = None
        self.set_file_open(open)
        self.set_csv_reader(csv.reader)

    def set_file_path(self, file_path):
        """
        set the file path
        """
        self.file_path = file_path

    def set_csv_reader(self, csv_reader):
        """
        dependency injection for `csv.reader`
        """
        self.csv_reader = csv_reader

    def set_file_open(self, file_open):
        """
        dependency injectino for `open` function
        """
        self.file_open = file_open

    def __iter__(self):
        """
        acts as iterator by opening csv file and iterate row by row
        """
        self.file = self.file_open(self.file_path)
        self.reader = self.csv_reader(self.file)

        return self

    def __next__(self):
        """
        iterate each row in the csv file
        """
        try:
            row = next(self.reader)
        except StopIteration:
            self.file.close()
            self.file = None
            self.reader = None

            raise StopIteration

        if len(row) < 3:
            return None

        if not isinstance(row[0], str) or not isinstance(row[1], str):
            return None

        time_cost = None
        try:
            time_cost = int(row[2])
        except (TypeError, ValueError):
            return None

        item = {
            'from': str(row[0]).strip(),
            'to': str(row[1]).strip(),
            'time': time_cost,
        }

        return item
