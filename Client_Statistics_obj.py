import statistics
from Client_obj import Client


class ClientStatistics:

    def __init__(self, clients: list[Client]):
        self.list_of_clients = clients

    def count_matches(self, func):
        return sum(client.matches_predicate(func) for client in self.list_of_clients)

    def ratio_of_matches(self, func, length):
        if length != 0:
            return self.count_matches(func) / length
        else:
            return -1

    def mean_of_vals(self, func):
        val_list = [func(client) for client in self.list_of_clients if func(client) is not None]
        return statistics.mean(val_list) if val_list else 0

    def pstdv_of_vals(self, func):
        val_list = [func(client) for client in self.list_of_clients if func(client) is not None]
        return statistics.pstdev(val_list) if val_list else 0
