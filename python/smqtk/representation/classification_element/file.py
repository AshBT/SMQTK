import cPickle
import os.path as osp

from smqtk.representation.classification_element import (
    ClassificationElement,
    NoClassificationError,
)

from smqtk.utils import file_utils
from smqtk.utils.string_utils import partition_string


__author__ = "paul.tunison@kitware.com"


class FileClassificationElement (ClassificationElement):

    @classmethod
    def is_usable(cls):
        return True

    def __init__(self, type_name, uuid, save_dir, subdir_split=None):
        """
        Initialize a file-base descriptor element.

        :param type_name: Type of classification. This is usually the name of
            the classifier that generated this result.
        :type type_name: str

        :param uuid: uuid for this classification
        :type uuid: collections.Hashable

        :param save_dir: Directory to save this element's contents. If this path
            is relative, we interpret as relative to the current working
            directory.
        :type save_dir: str | unicode

        :param subdir_split: If a positive integer, this will cause us to store
            the vector file in a subdirectory under the ``save_dir`` that was
            specified. The integer value specifies the number of splits that we
            will make in the stringification of this descriptor's UUID. If there
            happen to be dashes in this stringification, we will remove them
            (as would happen if given an uuid.UUID instance as the uuid
            element).
        :type subdir_split: None | int

        """
        super(FileClassificationElement, self).__init__(type_name, uuid)

        self.save_dir = osp.abspath(osp.expanduser(save_dir))

        # Saving components
        self.subdir_split = subdir_split
        if subdir_split and int(subdir_split) > 0:
            save_dir = osp.join(self.save_dir,
                                *partition_string(str(uuid).replace('-', ''),
                                                  int(subdir_split))
                                )
        else:
            save_dir = self.save_dir

        self.filepath = osp.join(save_dir,
                                 "%s.%s.classification.pickle"
                                 % (self.type_name, str(self.uuid)))

    def get_config(self):
        return {
            "save_dir": self.save_dir,
            'subdir_split': self.subdir_split
        }

    def has_classifications(self):
        """
        :return: If this element has classification information set.
        :rtype: bool
        """
        return osp.isfile(self.filepath)

    def get_classification(self):
        """
        Get classification result map, returning a label-to-confidence dict.

        We do no place any guarantees on label value types as they may be
        represented in various forms (integers, strings, etc.).

        Confidence values are in the [0,1] range.

        :raises NoClassificationError: No classification labels/confidences yet
            set.

        :return: Label-to-confidence dictionary.
        :rtype: dict[collections.Hashable, float]

        """
        if not self.has_classifications():
            raise NoClassificationError("No classification values.")
        with open(self.filepath) as f:
            return cPickle.load(f)

    def set_classification(self, m=None, **kwds):
        """
        Set the whole classification map for this element. This will strictly
        overwrite the entire label-confidence mapping (vs. updating it)

        Label/confidence values may either be provided via keyword arguments or
        by providing a dictionary mapping labels to confidence values.

        The sum of all confidence values, must be ``1.0`` (e.g. input cannot be
        empty). Due to possible floating point error, we round to the 9-th
        decimal digit.

        :param m: New labels-to-confidence mapping to set.
        :type m: dict[collections.Hashable, float]

        :raises ValueError: The given label-confidence map was empty or values
            did no sum to ``1.0``.

        """
        m = super(FileClassificationElement, self)\
            .set_classification(m, **kwds)
        with open(self.filepath, 'w') as f:
            cPickle.dump(m, f)