import subprocess
import sys

try:
    import pandas as pd
except:
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Example: Installing the 'requests' library
    install('pandas')
    install('numpy')
    import pandas as pd
    
def remove_outliers(df, column_name, multilplier = 1.5, return_limits = False):
    
    Q3 = df[column_name].quantile(0.75)
    Q1 = df[column_name].quantile(0.25)

    IQR = Q3 - Q1
    
    ll = Q1 - multilplier * IQR
    ul = Q3 + multilplier * IQR

    df_cleaned = df[(df[column_name] >=  ll) & (df[column_name] <=  ul)]
    outliers = df[(df[column_name] <  ll) | (df[column_name] >  ul)]
    
    if return_limits:
        return df_cleaned, outliers, ll, ul
    else:
        return df_cleaned, outliers

def flag_outliers(df, column_name, multilplier = 1.5):
    
    Q3 = df[column_name].quantile(0.75)
    Q1 = df[column_name].quantile(0.25)

    IQR = Q3 - Q1
    
    ll = Q1 - multilplier * IQR
    ul = Q3 + multilplier * IQR

    temp_df = df.copy()
    temp_df.loc[(temp_df[column_name] >=  ll) & (temp_df[column_name] <=  ul), 'Outlier'] = False
    temp_df['Outlier'].fillna(True, inplace = True) 
    
    return temp_df