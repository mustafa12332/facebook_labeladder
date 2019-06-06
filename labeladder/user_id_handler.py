import csv


class UserIdHandler:
    @staticmethod
    def handle_csv(path_to_csv):
        with open(path_to_csv) as csv_file:
            reader = csv.reader(csv_file)
            list_of_user_ids = []
            for row in reader:
                list_of_user_ids.append(row[0])
            return list_of_user_ids

