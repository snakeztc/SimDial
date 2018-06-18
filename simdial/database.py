import numpy as np
import logging


class Database(object):
    """
    A table-based database class. Each row is an entry and each column is an attribute. Each attribute
    has vocabulary size called modality.
    
    :ivar usr_dirichlet_priors: the prior for each attribute : 2D list [[]*modality]
    :ivar num_usr_slots: the number of columns: Int
    :ivar usr_modalities: the vocab size of each column : List
    :ivar usr_pdf: the PDF for each columns : 2D list
    :ivar num_rows: the number of entries
    :ivar table: the content : 2D list [[] *num_rows]
    :ivar indexes: for efficient SELECT : [{attribute_word -> corresponding rows}]
    """

    logger = logging.getLogger(__name__)

    def __init__(self, usr_dirichlet_priors, sys_dirichlet_priors, num_rows):
        """
        :param usr_dirichlet_priors: 2D list [[]_0, []_1, ... []_k] for each searchable attributes
        :param sys_dirichlet_priors: 2D llst for each entry (non-searchable attributes)
        :param num_rows: the number of row in the database
        """
        self.usr_dirichlet_priors = usr_dirichlet_priors
        self.sys_dirichlet_priors = sys_dirichlet_priors

        self.num_usr_slots = len(usr_dirichlet_priors)
        self.usr_modalities = [len(p) for p in usr_dirichlet_priors]

        self.num_sys_slots = len(sys_dirichlet_priors)
        self.sys_modalities = [len(p) for p in sys_dirichlet_priors]

        # sample attr_pdf for each attribute from the dirichlet prior
        self.usr_pdf = [np.random.dirichlet(d_p) for d_p in self.usr_dirichlet_priors]
        self.sys_pdf = [np.random.dirichlet(d_p) for d_p in self.sys_dirichlet_priors]
        self.num_rows = num_rows

        # begin to generate the table
        usr_table, usr_index = self._gen_table(self.usr_pdf, self.usr_modalities, self.num_usr_slots, num_rows)
        sys_table, sys_index = self._gen_table(self.sys_pdf, self.sys_modalities, self.num_sys_slots, num_rows)

        # append the UID in the first column
        sys_table.insert(0, range(self.num_rows))

        self.table = np.array(usr_table).transpose()
        self.indexes = usr_index
        self.sys_table = np.array(sys_table).transpose()

    @staticmethod
    def _gen_table(pdf, modalities, num_cols, num_rows):
        list_table = []
        indexes = []
        for idx in range(num_cols):
            col = np.random.choice(range(modalities[idx]), p=pdf[idx], size=num_rows)
            list_table.append(col)
            # indexing
            index = {}
            for m_id in range(modalities[idx]):
                matched_list = np.squeeze(np.argwhere(col == m_id)).tolist()
                matched_list = set(matched_list) if type(matched_list) is list else {matched_list}
                index[m_id] = matched_list
            indexes.append(index)
        return list_table, indexes

    def sample_unique_row(self):
        """
        :return: a unique row in the searchable table
        """
        unique_rows = np.unique(self.table, axis=0)
        idxes = range(len(unique_rows))
        np.random.shuffle(idxes)
        return unique_rows[idxes[0]]

    def select(self, query, return_index=False):
        """
        Filter the database entries according the query.
        
        :param query: 1D [] equal to the number of attributes, None means don't care
        :param return_index: if return the db index
        :return return a list system_entries and (optional)index that satisfy all constrains
        
        """
        valid_idx = set(range(self.num_rows))
        for q, a_id in zip(query, range(self.num_usr_slots)):
            if q:
                valid_idx -= self.indexes[a_id][q]
                if len(valid_idx) == 0:
                    break
        valid_idx = list(valid_idx)
        if return_index:
            return self.sys_table[valid_idx, :], valid_idx
        else:
            return self.sys_table[valid_idx, :]

    def pprint(self):
        """
        print statistics of the database in a beautiful format. 
        """

        self.logger.info("DB contains %d rows (%d unique ones), with %d attributes"
                         % (self.num_rows, len(np.unique(self.table, axis=0)), self.num_usr_slots))
