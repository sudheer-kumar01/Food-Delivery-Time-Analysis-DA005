import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Food_Delivery_Times.csv')

df_clean = df.copy()
df_clean['Weather'].fillna(df_clean['Weather'].mode()[0], inplace=True)
df_clean['Traffic_Level'].fillna(df_clean['Traffic_Level'].mode()[0], inplace=True)
df_clean['Time_of_Day'].fillna(df_clean['Time_of_Day'].mode()[0], inplace=True)
df_clean['Courier_Experience_yrs'].fillna(df_clean['Courier_Experience_yrs'].median(), inplace=True)

df_clean['Is_Delayed'] = df_clean['Delivery_Time_min'] > 45

print("========================================")
print("   INVERTIS UNIVERSITY - PBL DA-005     ")
print("========================================")
print(f"Total Orders Analyzed : {len(df_clean)}")
print(f"Average Delivery Time : {df_clean['Delivery_Time_min'].mean():.2f} mins")
print(f"Median Delivery Time  : {df_clean['Delivery_Time_min'].median():.2f} mins")
print(f"Delayed Orders (>45m) : {df_clean['Is_Delayed'].sum()} ({df_clean['Is_Delayed'].mean()*100:.2f}%)")
print("========================================")

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.histplot(df_clean['Delivery_Time_min'], kde=True, ax=axes[0, 0], color='teal', bins=30)
axes[0, 0].axvline(45, color='red', linestyle='--', label='Delay Threshold (45 min)')
axes[0, 0].set_title('1. Delivery Time Distribution', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Delivery Time (minutes)')
axes[0, 0].set_ylabel('Order Count')
axes[0, 0].legend()

sns.scatterplot(data=df_clean, x='Distance_km', y='Delivery_Time_min', hue='Is_Delayed', palette={False: 'green', True: 'red'}, ax=axes[0, 1], alpha=0.7)
axes[0, 1].axhline(45, color='red', linestyle='--', label='45 min Threshold')
axes[0, 1].set_title('2. Distance vs Delivery Time', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Distance (km)')
axes[0, 1].set_ylabel('Delivery Time (minutes)')

time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
tod_summary = df_clean.groupby('Time_of_Day')['Is_Delayed'].agg(['count', 'sum']).reindex(time_order).reset_index()
tod_summary.columns = ['Time_of_Day', 'Total_Orders', 'Delayed_Orders']
sns.barplot(data=tod_summary, x='Time_of_Day', y='Total_Orders', color='lightblue', label='On-Time Orders', ax=axes[1, 0])
sns.barplot(data=tod_summary, x='Time_of_Day', y='Delayed_Orders', color='crimson', label='Delayed Orders', ax=axes[1, 0])
axes[1, 0].set_title('3. Time of Day Volume & Delays', fontsize=12, fontweight='bold')
axes[1, 0].legend()

sns.boxplot(data=df_clean, x='Traffic_Level', y='Delivery_Time_min', order=['Low', 'Medium', 'High'], ax=axes[1, 1], palette='Set2')
axes[1, 1].axhline(45, color='red', linestyle='--', label='Delay Threshold')
axes[1, 1].set_title('4. Traffic Level Impact on Delivery Time', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('real_food_delivery_visualizations.png', dpi=300)
print("Charts saved successfully as 'real_food_delivery_visualizations.png'")
plt.show()