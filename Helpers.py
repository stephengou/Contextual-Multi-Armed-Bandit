import pandas as pd
import numpy as np

def create_design_matrix(input_df, formula, add_bias = True):
    '''
    :param input_df:
    :param formula: for eaxmple "y ~ x0 + x1 + x2 + x0 * x1 + x1 * x2"
    :return: the design matrix as a dataframe, each row corresponds to a data point, and each column is a regressor in regression
    '''

    #parse formula
    formula = formula.strip()
    all_vars_str = formula.split('~')[1].strip()
    dependent_var = formula.split('~')[0].strip()
    vars_list = all_vars_str.split('+')
    vars_list = list(map(str.strip, vars_list))
    print(vars_list)
    print(dependent_var)

    ''''#sanity check to ensure each var used in
    for var in vars_list:
        if var not in input_df.columns:
            raise Exception('variable {} not in the input dataframe'.format((var)))'''

    #build design matrix
    D_df = pd.DataFrame()
    for var in vars_list:
        if '*' in var:
            interacting_vars = var.split('*')
            interacting_vars = list(map(str.strip,interacting_vars))
            col = input_df[interacting_vars[0]]
            for i in range(1,len(interacting_vars)):
                col *= input_df[interacting_vars[i]]
            D_df[var] = col
        else:
            D_df[var] = input_df[var]

    #add dummy column for bias
    return  D_df

#example
data = np.random.randn(30,3)
df = pd.DataFrame(data)
df.columns = ['x0','x1','x2']
print(df.head())
D = create_design_matrix(df,"y ~ x0 + x1 + x2 + x0 * x1 + x1 * x2")
print(D.head())

