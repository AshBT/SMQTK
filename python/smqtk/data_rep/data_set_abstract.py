__author__ = 'purg'

import abc
import logging


class DataSet (object):
    """
    Base abstract class for data sets.
    """
    __metaclass__ = abc.ABCMeta

    @property
    def _log(self):
        return logging.getLogger('.'.join([self.__module__,
                                           self.__class__.__name__]))

    @abc.abstractmethod
    def count(self):
        """
        :return: The number of data elements in this set.
        :rtype: int
        """
        return

    @abc.abstractmethod
    def uuids(self):
        """
        :return: a set of uuids represented in this data set.
        :rtype: set
        """
        return

    @abc.abstractmethod
    def has_uuid(self, uuid):
        """
        Test if the given uuid refers to an element in this data set.

        :param uuid: Unique ID to test for inclusion. This should match the
            type that the set implementation expects or cares about.

        :return: True if the given uuid matches an element in this set, or
            False if it does not.
        :rtype: bool

        """
        return

    @abc.abstractmethod
    def add_data(self, elem):
        """
        Add the given data element instance to this data set.

        :param elem: Data element to add
        :type elem: smqtk.data_rep.DataElement

        """
        return

    @abc.abstractmethod
    def get_data(self, uuid):
        """
        Get the data element the given uuid references, or raise an
        exception if the uuid does not reference any element in this set.

        :raises KeyError: If the given uuid does not refer to an element in
            this data set.

        :param uuid: The uuid of the element to retrieve.

        :return: The data element instance for the given uuid.
        :rtype: smqtk.data_rep.DataElement

        """
        return
