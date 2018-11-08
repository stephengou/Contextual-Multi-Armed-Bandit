import pandas as pd
import numpy as np

'''
Todo: 1. handle missing data in input_df
      2. support exponential expression
'''

def create_design_matrix(input_df, formula, add_intercept = True):
    '''
    :param input_df:
    :param formula: for eaxmple "y ~ x0 + x1 + x2 + x0 * x1 + x1 * x2"
    :param add_intercept: whether to add dummy columns of 1.
    :return: the design matrix as a dataframe, each row corresponds to a data point, and each column is a regressor in regression
    '''

    D_df = pd.DataFrame()
    input_df = input_df.astype(np.float64)

    # parse formula
    formula = formula.strip()
    all_vars_str = formula.split('~')[1].strip()
    dependent_var = formula.split('~')[0].strip()
    vars_list = all_vars_str.split('+')
    vars_list = list(map(str.strip, vars_list))

    ''''#sanity check to ensure each var used in
    for var in vars_list:
        if var not in input_df.columns:
            raise Exception('variable {} not in the input dataframe'.format((var)))'''

    # build design matrix
    for var in vars_list:
        if '*' in var:
            interacting_vars = var.split('*')
            interacting_vars = list(map(str.strip,interacting_vars))
            D_df[var] = input_df[interacting_vars[0]]
            for i in range(1, len(interacting_vars)):
                D_df[var] *= input_df[interacting_vars[i]]
        else:
            D_df[var] = input_df[var]

    # add dummy column for bias
    if add_intercept:
        D_df.insert(0, 'Intercept', 1.)

    return D_df

#example
np.random.seed(1717)
df = pd.DataFrame(np.random.randint(1,5,(30,3)),columns = ['x0','x1','x2'])
formula = "y ~ x1 + x2 + x0 * x1 + x1 * x2 + x0 * x1 * x2"
print(df.head())
print('formula: ' + formula)
D = create_design_matrix(df, formula, add_intercept=True)
print(D.head())
