import statistics
from Client_obj import Client


class ClientStatistics:
    """
    ClientStatistics class for calculating statistics on a list of clients.
    """
    def __init__(self, clients: list[Client]):
        self.list_of_clients = clients

    def count_matches(self, func):
        """
        counts the number of clients in the list that match the given predicate
        :param func : function from client => bool
        :return: the number of clients matching the predicate
        """
        return sum(client.matches_predicate(func) for client in self.list_of_clients)

    def ratio_of_matches(self, func, length):
        """
        counts the number of matches in the client list and divides it by the given length it is != 0
        :param func: function from client => bool
        :param length : int: the number of clients in your probabilistic universe
        :return: the ratio of the number of matches and the length and -1 if length == 0
        """
        if length != 0:
            return self.count_matches(func) / length
        else:
            return -1

    def mean_of_vals(self, func):
        """
        computes the mean of the values returned by the given function on the list of clients
        :param func: function from client => Number
        :return: the mean of the computed values and 0 if function never returned anything
        """
        val_list = [func(client) for client in self.list_of_clients if func(client) is not None]
        return statistics.mean(val_list) if val_list else 0

    def pstdv_of_vals(self, func):
        """
        computes the population standard variance of the values returned by the given function on the list of clients
        :param func: function from client => Number
        :return: the pstdv of the computed values and 0 if function never returned anything
        """
        val_list = [func(client) for client in self.list_of_clients if func(client) is not None]
        return statistics.pstdev(val_list) if val_list else 0
