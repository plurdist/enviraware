import pandas as pd
from scipy.stats import describe
import matplotlib.pyplot as plt
import numpy as np
import os

if not os.path.exists('daily_plots'):
    os.makedirs('daily_plots')

feeds = pd.read_csv('feeds_cleaned.csv')

# cheese_subset = feeds.head(1000)
# cheese_desc = feeds.describe()

# print(cheese_subset.iloc[:,1])

feeds['created_at'] = pd.to_datetime(feeds['created_at'], errors='coerce', utc=True)

feeds['created_at_date'] = feeds.created_at.dt.date


# desired_date = input("provide the date: ")
# filtered_df = feeds[feeds['created_at'].dt.date == pd.to_datetime(desired_date).date()]


for date, subset in feeds.groupby('created_at_date'):
    x = subset.iloc[:, 0]
    y = subset.iloc[:, 9]
    fig, ax = plt.subplots()
    ax.plot(x,y)
    plt.savefig(f'daily_plots/{date}.png')
    plt.close(fig)

# for index, row in feeds.iterrows():
#     filtered_df = feeds[feeds['created_at'].dt.date == pd.to_datetime(row['created_at_date']).date()]
#     x = filtered_df.iloc[:,0]
#     y = filtered_df.iloc[:,9]
#     fig, ax = plt.subplots()
#     ax.plot(x,y)
#     plt.savefig(f'daily_plots/{row["created_at_date"]}.png')
#     plt.close(fig)


# desired_date = '2023-10-14'
summary_stats_list = []

# Iterate over numerical columns
for col in feeds.select_dtypes(include='number').columns:
    column_stats = describe(feeds[col], axis=0, nan_policy='omit')
    
    # Create a dictionary for each column
    col_dict = {
        'Column': col,
        'Count': column_stats.nobs,
        'Min': column_stats.minmax[0],
        'Max': column_stats.minmax[1],
        'Mean': column_stats.mean,
        'Variance': column_stats.variance,
        'Skewness': column_stats.skewness,
        'Kurtosis': column_stats.kurtosis
    }
    
    # Append the dictionary to the list
    summary_stats_list.append(col_dict)

# Create a DataFrame from the list of dictionaries
summary_stats_df = pd.DataFrame(summary_stats_list)

# Print or further process the summary_stats_df
print(summary_stats_df)

