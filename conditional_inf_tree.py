import numpy as np


class Node(object):
    
    def __init__(self, index, var, split):
        self.data_index  = index    # index of the response
        self.variable    = var      # if var = -1 then parent node 
        self.split_point = split
        self.left  = None
        self.right = None
    
    def impurity(self, response):
        """Return impurity of the node"""
        node_data = response[self.data_index]
        freq =  np.array(self.__count_values__(node_data)['freq']) 
        return self.__gini__(freq * 1.0 / sum(freq))
    
    def __gini__(self, p):
        """Utility to compute gini"""
        return 1.0 - sum(np.square(p))
    
    def __count_values__(self, sequence):
        """Utility method to count values occurence in a sequence"""
        
        values_set = []      # keep track of set of values
        freq = []            # keep track of frequencies
        for val in sequence:
            if val in values_set:
                idx = np.where(values_set == val)[0][0]     # detect the idx
                freq[idx] += 1
            else:
                values_set.extend([val])
                freq.extend([1])
        return {'values': values_set, 'freq': freq}
    
    def set_left_child(self, node):
        self.left = node
        return self
    
    def set_right_child(self, node):
        self.right = node
        return self
    
    def get_left_child(self):
        return self.left
    
    def get_right_child(self):
        return self.right

def split_node(parent_node):
    # for each split point
    # split_points = idx_of_label_changed(y)
    
    parent_imp = parent_node.impurity(y)
    # stopping condition - pur node
    if parent_imp == 0.0:
        return
    
    best_split_all_var = 0     # id of split point
    max_gain_all_var   = 0.0
    best_variable      = 0

    # loop through variables
    for id_var in all_splits.keys():
        # keep track of best split and max gain among all variables
        max_gain = 0.0
        best_split_point = 0   # id of split point
    
        variable = X[id_var]   # data of variable
        # suppose variable is categorial variable 
        # k levels - split point at each levels - split point is the value of variable
        for id_split, split_point in enumerate(all_splits[id_var]):
    
            # left node - variable == split point
            left_node  = Node(index = np.where(variable == split_point)[0], var = id_var, 
                              split = [split_point])
            right_node = Node(index = np.where(variable != split_point)[0], var = id_var,
                              split = np.delete(levels, id_split))
    
            # impurity for the potential left node and right node
            weighted_imp = ( len(left_node.data_index) * left_node.impurity(y) 
                            + len(right_node.data_index) * right_node.impurity(y)) / len(variable)
            gain = parent_imp - weighted_imp
            if gain > max_gain:
                max_gain = gain
                best_split_point = id_split
    
        if max_gain > max_gain_all_var:
            max_gain_all_var   = max_gain
            best_split_all_var = best_split_point   # id of split point
            best_variable      = id_var             # idx of variable
        
            # update left node and right node - temporary keep track
            parent_node.set_left_child(left_node).set_right_child(right_node)

    print 'max gain ', max_gain_all_var
    
    if max_gain_all_var == 0.0:   # quit if no improvement 
        print 'leaf'
        return
    
    print 'best split value ', all_splits[best_variable][best_split_all_var]
    print 'id best variable ', best_variable
    
    # update the split tables
    if len(all_splits[best_variable]) == 2:   # variable has two levels left, remove the var
        all_splits.pop(best_variable)
    else:   # otherwise, remove the level value
        all_splits[best_variable] = np.delete(all_splits[best_variable], best_split_all_var)
    
    # continue splitting
    print '--- left'
    print
    split_node(parent_node.get_left_child()) 
    
    print '--- right'
    print
    split_node(parent_node.get_right_child()) 
    
    return parent_node



