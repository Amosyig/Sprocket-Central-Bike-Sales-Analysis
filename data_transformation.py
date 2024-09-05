#import python modules

import pandas as pd
import numpy as np

#making the dataframe of the sales transactions, saved in the 1st excel sheet:
transactions_df = pd.read_excel('data.xlsx', sheet_name = 1, header = 1)

#dropping any blank roles present in the brand column:
transactions_df = transactions_df.dropna(subset = 'brand')


#making the new customers df, saved in the 2nd excel sheet:
new_customer_df = pd.read_excel('data.xlsx', sheet_name = 2, header = 1)


#making df of the customer demographics, saved in the 3rd excel sheet:
customerdemographic_df = pd.read_excel('data.xlsx', sheet_name = 3, header = 1)



#making a df of the customer's dddress, saved in the 4th excel sheet:
customeraddress_df = pd.read_excel('data.xlsx', sheet_name = 4, header = 1)


#merging two of these dataframes (customerdemographic_df & customeraddress) into a single one:
first = pd.merge(customerdemographic_df, customeraddress_df, how = 'inner', on = 'customer_id')

df = pd.merge(first, transactions_df, how = 'inner', on = 'customer_id')


#deleting the 'default' column from df:
del df['default']


#fixed data inconsitencies of values in the gender & state columns: 
df['gender'] = df['gender'].replace(to_replace = ['F', 'Femal', 'M'], value = ['Female', 'Female', 'Male'])


df['state'] = df['state'].replace(to_replace = ['New South Wales', 'Victoria'], value = ['NSW', 'VIC'])



#performed data transformation by turning the values of the online order into true and false 
df['online_order'] = df['online_order'].replace(to_replace = [1.0, 0.0], value = [True, False])


#removed blank ows from the DOB column:
df = df.dropna(subset = 'DOB')


#converted the values of the 'DOB' column from a string to date type:
df['DOB'] = pd.to_datetime(df['DOB'])


#adding a new column called the Age
today = pd.to_datetime('today')
df['Age'] = ((today - df['DOB'])/365.25).astype(str).str.slice(0,2)
df['Age']



#chaned data type of age column as integers
df['Age'] = df['Age'].astype(int)


#grouping the ages into brackets
df['Age Bracket'] = pd.cut(df['Age'],bins = [20, 35, 50, 65, 80, 95],labels = ['Young Adults: 20-35', 'Middle-Aged Adults: 35-50', 'Mature Adults: 50-65', 'Senior Adults: 65-80', 'Elderly Adults: 80-95'])



#now dropping the records with the guy being born in 1843 (clearly an issue of data)
df = df.drop(df[df['customer_id'] == 34].index)
df


#created a df groupoing the data on customer_id, first_name, last_name based on number of transactions, total amount spent & total product cost:
grouped_df = df.groupby(['customer_id','first_name', 'last_name']).agg(count = ("order_status", "count"),
                                                          total_amount_spent = ('list_price', 'sum'),
                                                                total_product_cost = ('standard_cost', 'sum'))
                                                          

#reset the index of  grouped_df, saving it as grouped_df_1: 
grouped_df_1 = grouped_df.reset_index()



#created a new dataframe of a distinct list of the customers information: 
grouped_df_2 = df.groupby('customer_id').agg({'gender': 'first', 'past_3_years_bike_related_purchases': 'first', 'job_title': 'first',
                              'job_industry_category': 'first', 'wealth_segment': 'first', 
                              'tenure': 'first', 
                              'address': 'first', 
                              'state': 'first', 
                              'Age': 'first', 
                              'Age Bracket': 'first'}).reset_index()




#merged the grouped_df_1 & grouped_df_2 column based on the 'customer_id' column:
df_2 = pd.merge(grouped_df_1, grouped_df_2, how = 'inner', on = 'customer_id')

#added the total_profit column to df_2
df_2['total_profit'] = df_2['total_amount_spent'] - df_2['total_product_cost']


#imporing the postcode data into memory:
postcode_df = pd.read_excel('postcode_data.xlsx')


#getting a distinct list of the county names:
postcode_df = postcode_df.groupby('postcode').agg({'locality': 'first'}).reset_index()


#merged the postcode_df & df, inorder to add the 'locality' column of postcode_df to df:
df_1 = pd.merge(df, postcode_df, how ='inner', on = 'postcode')


#made a new df (grouped_postcode_df) of the a distinct list of county location & postcode of the customers:
grouped_postcode_df = df_1.groupby('customer_id').agg({'locality': 'first', 'postcode': 'first'}).reset_index()



#merged the df_2 & grouped_postcode_df based on the customer_id
df_2 = pd.merge(df_2, grouped_postcode_df, how = 'inner', on = 'customer_id')
df_2.head()

#delete the locality_x from df_2
del df_2['locality_x']

#made a copy of locality_y and saved it as locality :
df_2['locality'] = df_2['locality_y'].copy()

#now deleting 'locality_y' from df_2
del df_2['locality_y']


#End of data cleaning and transformation:

#now exporting cleaned data to excel file:
df_2.to_excel('grouped_cleaned_data.xlsx', index = False)















