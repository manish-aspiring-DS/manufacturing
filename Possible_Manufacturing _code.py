# Importing Modules 
import pandas as pd 
import numpy as np

print('-------------------------------------------------------------')
print('              -----Import Completed-----                          ')
print('-------------------------------------------------------------')

# Function created to round off a number. 
def rof(num):
    a=round(num)
    return a
print('-------------------------------------------------------------')
print('              -----Function Created-----                          ')
print('-------------------------------------------------------------')

# Reading the csv file as dataframe with details of requirement of material for creating a unit of finished good   
df_raw=pd.read_excel('C://Users/admin/Desktop/Book1.xlsx')
##print(df_raw)

#Display the type of finished goods that can be Processed
print('Products:')
prod=df_raw['fg']
products=np.array(prod)
##print(np.unique(products))
# End user input user for selecting the product to be manufactured
to_manuf_prod=input('Choose the product to be manufactured!!')
to_manuf_prod=to_manuf_prod.upper()
# End user input for giving the number of items to me manufactured
number_of_items=int(input('How many products to be manufactured ?'))

# -------- Section to determine the quatity of material left after the being used for specified item---------
df_filter=df_raw[df_raw['fg']==to_manuf_prod]

df_filter.loc[:,'ur'] *= number_of_items
df_filter.loc[:,'total']=df_filter['total']-df_filter['ur']
df_filter_temp=df_filter[['Materials','total']]

df_temp_final=pd.merge(df_raw, df_filter_temp , on='Materials',how='left',suffixes=('_left','_remained'))
del df_filter
del df_filter_temp
del df_temp_final['total_left']
##print(df_temp_final)

#---- Section to determine the quatity which of fibished goods that can be produced with the remaining material
# Getting a sliced data frame
sub_df_temp_final= df_temp_final.loc[:,['fg']]
# Adding a max quantity column in sliced dataframe
sub_df_temp_final.loc[:,'Max Independent']=df_temp_final['total_remained']/df_temp_final['ur']
##print(sub_df_temp_final)

# Grouped it by fg column
df_temp_max=sub_df_temp_final.groupby('fg').min().apply(rof)
#print(df_temp_max)

# Joining two dataframes to get the max column value againts respective rows
df_final_out=pd.merge(df_temp_final,df_temp_max,on='fg',how='left')
del df_temp_final
del sub_df_temp_final
del df_temp_max
print(df_final_out.set_index(['fg','Materials']))
