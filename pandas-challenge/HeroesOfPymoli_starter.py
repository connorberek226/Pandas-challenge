#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

purchase_data


# ## Player Count

# * Display the total number of players
# 

# In[2]:


#Equation to find the total amount of players
total = purchase_data["SN"].nunique()

summary1_df = pd.DataFrame({"Total Players": [total]})

summary1_df


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


# Variables to be inserted as columns in summary DataFrame to calculate the number of unique items,
# Average Price, Number of Purchases and total revenue from purchase_data DataFrame.
num_unique = purchase_data["Item ID"].nunique()
total_revenue = purchase_data["Price"].sum()
num_purchases = purchase_data["Purchase ID"].count()
avg_price = total_revenue / num_purchases

# Dataframe used to store the variables above in a summary table
summary2_df = pd.DataFrame({"Number of Unique Items": [num_unique], "Average Price": [avg_price], 
                            "Number of Purchases": [num_purchases], "Total Revenue": [total_revenue]})

# Used to convert the values in the Average Price and Total Revenue columns to dollar values.
summary2_df["Average Price"] = summary2_df["Average Price"].astype(float).map("${:,.2f}".format)
summary2_df["Total Revenue"] = summary2_df["Total Revenue"].astype(float).map("${:,.2f}".format)

summary2_df


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


# Variables to store the values of each count and store them
male_count = purchase_data["SN"].loc[purchase_data["Gender"] == "Male"].nunique()
female_count = purchase_data["SN"].loc[purchase_data["Gender"] == "Female"].nunique()
other_count = purchase_data["SN"].loc[purchase_data["Gender"] == "Other / Non-Disclosed"].nunique()

# Variable to store the total count to the get the percentage of players for each gender
total_count = male_count + female_count + other_count

percent_male = (male_count / total_count) *100
percent_female = (female_count / total_count) *100
percent_other = (other_count / total_count) *100

# Dataframe used to store above variables in a meaningful table
gender_demo = pd.DataFrame({"Total Count": [male_count, female_count, other_count], 
                            "Gender": ["Male", "Female", "Other / Non-Disclosed"],
                           "Percentage of Players": [percent_male, percent_female, percent_other]})

# Formats the "Percentage of Players" column
gender_demo["Percentage of Players"] = gender_demo["Percentage of Players"].astype(float).map("{:,.2f}%".format)

gender_demo = gender_demo.set_index("Gender")

gender_demo


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[5]:


# Used to calculate the number of purchases made by each gender
male_pur_count = purchase_data["Purchase ID"].loc[purchase_data["Gender"] == "Male"].count()
female_pur_count = purchase_data["Purchase ID"].loc[purchase_data["Gender"] == "Female"].count()
other_pur_count = purchase_data["Purchase ID"].loc[purchase_data["Gender"] == "Other / Non-Disclosed"].count()
# Used to calculate the total amount purchased by each gender
male_tot_pur = purchase_data["Price"].loc[purchase_data["Gender"] == "Male"].sum()
female_tot_pur = purchase_data["Price"].loc[purchase_data["Gender"] == "Female"].sum()
other_tot_pur = purchase_data["Price"].loc[purchase_data["Gender"] == "Other / Non-Disclosed"].sum()
# Used to calculate the average price per purchase
avg_male_pur = male_tot_pur / male_pur_count
avg_female_pur = female_tot_pur / female_pur_count
avg_other_pur = other_tot_pur / other_pur_count
# Used to calculate how much, on average, each person paid for their purchase based on Gender
avg_total_male = male_tot_pur / purchase_data["SN"].loc[purchase_data["Gender"] == "Male"].nunique()
avg_total_female = female_tot_pur / purchase_data["SN"].loc[purchase_data["Gender"] == "Female"].nunique()
avg_total_other = other_tot_pur / purchase_data["SN"].loc[purchase_data["Gender"] == "Other / Non-Disclosed"].nunique()

# Dataframe used to store the variables above in a table
purchase_analysis1 = pd.DataFrame({"Purchase Count": [male_pur_count, female_pur_count, other_pur_count], 
                                 "Average Purchase Price":[avg_male_pur, avg_female_pur, avg_other_pur], 
                                 "Total Purchase Value": [male_tot_pur, female_tot_pur, other_tot_pur], 
                                 "Avg Total Purchase per Person": [avg_total_male, avg_total_female, avg_total_other], 
                                 "Gender": ["Male", "Female", "Other / Non-Disclosed"]})

# Cleaner formatting of data
purchase_analysis1["Average Purchase Price"] = purchase_analysis1["Average Purchase Price"].astype(float).map("${:,.2f}".format)
purchase_analysis1["Total Purchase Value"] = purchase_analysis1["Total Purchase Value"].astype(float).map("${:,.2f}".format)
purchase_analysis1["Avg Total Purchase per Person"] = purchase_analysis1["Avg Total Purchase per Person"].astype(float).map("${:,.2f}".format)

# Sets the index to gender for the values above to be meaningful
purchase_analysis1 = purchase_analysis1.set_index("Gender")

purchase_analysis1


# ## Age Demographics

# In[6]:


# Bins used to group the players based on their age range.
bins = [0, 9, 14, 19, 24, 29, 34, 39, 100]
# Names of the age groups each player falls into.
# 1 less value in "group_names" than "bins" always so that each group can fill the gaps of the bins.
group_names = ["<10", "10-14", "15-20", "20-25", "25-30", "30-34", "35-40", "40+"]

# Allows the data to be grouped based on their age and creates a new column "Age Group" that stores
# this value for each player.
purchase_data["Age Group"] = pd.cut(purchase_data["Age"], bins, labels = group_names, include_lowest = True)

# Groups the data based on the age group they fall in,
age_demo = purchase_data.groupby(["Age Group"])

# Variables used to find total count of players in each age group and percentage of that age group
# on the total count of players.
total_count = age_demo["SN"].nunique()
percent_player = ((total_count/(total_count.sum()))*100)

# Dataframe used to store the variables above and maintain the new index of "Age Group"
age_analysis1 = pd.DataFrame({"Total Count": total_count, 
                              "Percentage of Players": percent_player.astype(float).map("{:,.2f}%".format)})

age_analysis1


# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


# Bins used to group the players based on their age range.
bins = [0, 9, 14, 19, 24, 29, 34, 39, 100]
# Names of the age groups each player falls into.
group_names = ["<10", "10-14", "15-20", "20-25", "25-30", "30-34", "35-40", "40+"]

# Allows the data to be grouped based on their age and creates a new column "Age Group" that stores
# this value for each player.
purchase_data["Age Group"] = pd.cut(purchase_data["Age"], bins, labels = group_names, include_lowest = True)

age_purchasing = purchase_data.groupby(["Age Group"])

# Variables used to find values such as the purchase count in each age group, 
# total purchase value, average purchase price and average total per person.
purchase_count = age_purchasing["Purchase ID"].count()
total_price = age_purchasing["Price"].sum()
avg_price = total_price / purchase_count
# **Average total per person is different than average purchase price because
# there are more purchases than there are players**
avg_total = total_price / (age_purchasing["SN"].nunique())

# Dataframe used to store the variables above and maintain the new index of "Age Group"
age_purchase_analysis2 = pd.DataFrame({"Purchase Count": purchase_count, 
                                       "Average Purchase Price": avg_price.astype(float).map("${:,.2f}".format), 
                                       "Total Purchase Value": total_price.astype(float).map("${:,.2f}".format), 
                                       "Average Total Purchase per Person": avg_total.astype(float).map("${:,.2f}".format)})

age_purchase_analysis2


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[93]:


top_spenders = purchase_data.groupby(["SN"])

# Variables used to find purchase count of each player, total purchase value,
# and average purchase price of each player.
purchase_count = top_spenders["Purchase ID"].count()

total_purchase = top_spenders["Price"].sum()

avg_purchase = top_spenders["Price"].mean()

topspenders2 = pd.DataFrame({"Purchase Count": purchase_count, 
                           "Average Purchase Price": avg_purchase.astype(float).map("${:,.2f}".format), 
                           "Total Purchase Value": total_purchase})

# Sorts the table in descending order based on the "Total Purchase Value".
summary_topspenders = topspenders2.sort_values("Total Purchase Value", ascending = False)

summary_topspenders.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[86]:


# 1st Dataframe to store the extracted variables
most_popular1 = purchase_data[["Item ID", "Item Name", "Price"]]
# 2nd Dataframe to group the above dataframe by "Item ID" and "Item Name"
most_popular2 = most_popular1.groupby(["Item ID", "Item Name"])

# Variables used to find the purchase_count, item price and total purchase value
purchase_count = most_popular2["Price"].count()

item_price = most_popular2["Price"].unique()

total_value = most_popular2["Price"].sum()


# 3rd Dataframe created with new variables above
summary = pd.DataFrame({"Purchase Count": purchase_count, 
                       "Item Price": item_price, "Total Purchase Value": total_value.astype(float).map("${:,.2f}".format)})

# 4th Dataframe created to store the collected values
summary_mostpopular = summary.sort_values("Purchase Count", ascending = False)

summary_mostpopular.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[87]:


summary_mostprofitable = summary_mostpopular.sort_values("Total Purchase Value", ascending = False)

summary_mostprofitable


# In[ ]:




