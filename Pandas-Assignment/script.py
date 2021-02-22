import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3_seaborn
import glob 


# Read all 9 csv files
census_files = glob.glob('states*.csv')

df_list = []
for filename in census_files:
  data = pd.read_csv(filename)
  df_list.append(data)
us_census = pd.concat(df_list,  ignore_index=True)

#Useless column and interfeeres with the drop duplicates
us_census.drop('Unnamed: 0', inplace=True, axis=1)
print(us_census.columns)
print(us_census.dtypes)
print(us_census.head())

# Clean the income column (remove the $) and convert it into a number
us_census['Income'] = us_census['Income'].replace('[\$,]', '', regex=True)
us_census['Income'] = pd.to_numeric(us_census.Income)

print(us_census.Income.head())

# Split Men and Women population
us_census['Men'] = us_census['GenderPop'].str.split('(_)', expand=True)[0]
us_census['Women'] = us_census['GenderPop'].str.split('(_)', expand=True)[2]
print(us_census.head())

# Remove the M of F character from the Men and Women's columns 
us_census['Men'] = us_census['Men'].replace('[M,]', '', regex=True)
us_census['Women'] = us_census['Women'].replace('[F,]', '', regex=True)

# Convert the Men and Women columns into a number
us_census['Men'] = pd.to_numeric(us_census.Men)
us_census['Women'] = pd.to_numeric(us_census.Women)
print(us_census.head())

#Plot Women's income
plt.scatter(us_census.Women, us_census.Income)
plt.xlabel('Women')
plt.ylabel('Income')
plt.show() 
plt.clf()
print(us_census['Women'])

#Replace the Women's Nan's values with the difference between TotalPop minus the Men's population
us_census['Women'] = us_census['Women'].fillna(us_census.TotalPop - us_census.Men)
print(us_census['Women'])

print(us_census.duplicated())

# Remove suplicates I've had to drop a useless column before to be able to do this.
clean_us_census = us_census.drop_duplicates()

# Plot WOmen's income again with clean data
plt.scatter(clean_us_census.Women, clean_us_census.Income)
plt.xlabel('Women')
plt.ylabel('Income')
plt.show() 
plt.clf()
print(clean_us_census.columns)

#Create a function to clean column data. Replace a string and convert into a number.
def clean_column(df, columns, string):
  for column in columns:
    df[column] = df[column].replace(string, '', regex=True)
    df[column] = pd.to_numeric(df[column])
  return df

# Create a list of races or PC Ehtnicities to clean the data for  
columns = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']

# Call function to clean data
clean_us_census = clean_column(clean_us_census, columns, '[\%,]')

#Calculate the missing Pacific ehtnic data
nan_pacific = 100 - clean_us_census.White - clean_us_census.Hispanic - clean_us_census.Black - clean_us_census.Asian

# Replace the Pacific ehtnicity % with real data
clean_us_census['Pacific'] = clean_us_census.Pacific.fillna(value=nan_pacific)

# Drop duplicates just in case
final_us_census = clean_us_census.drop_duplicates()
print(final_us_census)

#Create functionm to plot different columns
def print_histogram(df, columns):
  for column in columns:
    plt.hist(df[column])
    plt.title('Figure : ' + column)
    plt.show()
    plt.clf()

# Create a list of columns to plot
columns = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']

# call function to plot a list of columns
print_histogram(final_us_census, columns)
