import numpy as np

class AssetMatrix:
    """
    variables: 
    self.n
    self.mat
    self.ext_asset
    self.ext_liability
    
    the matrix represents interbank asset or liability.
    self.mat[i, j] represents the amount of money bank i should give to bank j.
    If bank j should give money to bank i, then the value is negative. 
    
    methods: 
    __init__ 
    get_n
    get_mat
    get_int_asset
    get_int_liability
    get_element
    update_matrix
    update_element
    """
    def __init__(self, mat=None):
        """
        if no data is given then create a matrix with size 1, value = 0
        """
        if mat is None:
            mat = np.matrix([0])
        #
        self.mat = mat
        
        self.n = self.get_n()
        
    #
    
    def get_n(self):
        return self.n
    #
    
    def get_mat(self):
        return self.mat
    #
    
    
    def get_int_asset(self, i):
        """
        Add all the positive column values of the matrix to get the interbank asset. 
        """
        val = 0
        for bank_idx in range(self.n):
            if self.mat[bank_idx, i] > 0 : 
                val +=  self.mat[bank_idx, i]
        return val
    #
    
    def get_int_liability(self, j):
        """
        add all the positive row values of the matrix to get the interbank liability. 
        """
        val = 0
        for bank_idx in range(self.n):
            if self.mat[j, bank_idx] > 0 : 
                val +=  self.mat[bank_idx, j]
        return val
    # 

    
    def get_element(self, i,j):
        return self.mat[i,j]
    # 
    
    def update_matrix(self, mat):
        self.mat = mat
        pass 
    # 
    
    def update_element(self, i, j, val):
        self.mat[i,j] = val 
        pass
    # 
# 
    
    
class Simulator(): 
    """
    simulation module
    elements: 
    self.AssetMat
    self.LevMat
    self.alpha
    self.save_directory
    self.t
    self.default_set
    self.ext_asset
    self.ext_liability
    self.n 
    self.h 
    self.H
    self.time_series_data
    time_series_data :: dictionary type 
    keys : time_step (int)
    values : dictionary the following elements as keys: 
    "type"
    "bank index" 
    """
    
    def __init__(self, AssetMat, ext_asset, ext_liability, alpha, save_directory):
        """
        initialization
        """
        
        ### Asset information
        self.AssetMat = AssetMat
        
        ### alpha(devaluation rate of the external assets)
        self.alpha = alpha
        
        ### directory to save file 
        self.save_directory = save_directory
        
        ### current time step 
        self.t = 0 
        
        ### set of default bank 
        self.default_set = set() 
        
        ### external assets 
        self.ext_asset = ext_asset
        
        ### external liability
        self.ext_liability = ext_liability
        
        ### size of the matrix 
        self.n = AssetMat.get_n()
        
        ### leverage matrix 
        self.LevMat = AssetMatrix(mat = np.matrix(np.zeros(shape=(self.n, self.n))))
        
        self.time_series_data = {}
        
        ### Check conditions
        assert len(ext_liability) == self.n, "Length of the external liability list ( {:02d} given ) and dimension of the AssetMat ( {:02d} given ) should be same".format(len(ext_liability), self.n)
        assert len(ext_asset) == self.n, "Length of the external asset list ( {:02d} given ) and dimension of the AssetMat ( {:02d} given ) should be same".format(len(ext_asset), self.n)
        assert alpha >= 0 or alpha <= 1, "Alpha should be between 0 and 1"   
        
        ### update all the variables 
        self.update(init=True)
    #
        
            
    def get_ext_asset(self, i):
        """
        return external asset of bank i 
        """
        return self.ext_asset[i]
    #
    
    def get_ext_liability(self, i):
        """
        return etxternal liability of bank i 
        """
        return self.ext_liability[i]
    # 
    
    def upadate_leverage(self):
        """
        with current Asset matrix, update leverage matrix 
        """
        
        all_asset = [0 for _ in range(self.n)] 
        all_liability = [0 for _ in range(self.n)] 
        all_equity = [0 for _ in range(self.n)] 
        for bank_index in range(self.n):
            all_asset[bank_index] += self.AssetMat.get_int_asset(bank_index)
            all_asset[bank_index] += self.ext_asset[bank_index]
            
            all_liability[bank_index] += self.AssetMat.get_int_liability(bank_index)
            all_liability[bank_index] += self.ext_asset[bank_index]
            
            equity =   all_asset[bank_index] - all_liability[bank_index] 

            if equity < 0 : 
                self.default_set.add(bank_index)
                equity = 0
            # 
            
            all_equity[bank_index] = equity
        # 
        
        for bank_idx_i in range(self.n):
            for bank_index_j in range(self.n):
                val = min(self.AssetMat.get_mat()[bank_idx_i, bank_index_j] , 0) / equity[bank_index_j]
                self.LevMat.update_element(bank_idx_i, bank_index_j, val)
            #
        #
        pass   
    #
    
    def initial_shock(self):
        
    
    def update(self, init=False):
        """
        if init is True, then update all the variables except self.h, self.H
        if init is False, then 
        """
    