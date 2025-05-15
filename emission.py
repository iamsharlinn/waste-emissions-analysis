#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 15 02:18:06 2025

@author: sharlin
"""

import pandas as pd

file_path = '/Users/sharlin/Desktop/waste_emission/flight.xls'  
df = pd.read_excel(file_path)

print(df.head())
print(df.columns)
print(df.info())

df = df[df['FACILITY NAME'].notnull()]

# Sort by emissions
df_sorted = df.sort_values(by='TOTAL REPORTED EMISSIONS', ascending=False)

# top 10 emitters
print(df_sorted[['FACILITY NAME', 'STATE', 'TOTAL REPORTED EMISSIONS']].head(10))

import matplotlib.pyplot as plt

#  top 10 emitters
top10 = df_sorted.head(10)
plt.figure(figsize=(12, 6))
plt.barh(top10['FACILITY NAME'], top10['TOTAL REPORTED EMISSIONS'], color='green')
plt.xlabel('Emissions (Metric Tons of CO2e)')
plt.title('Top 10 Emitting Waste Facilities in 2023')
plt.gca().invert_yaxis()  # highest at top
plt.tight_layout()
plt.show()


# Emissions by state

state_emissions = df.groupby('STATE')['TOTAL REPORTED EMISSIONS'].sum().sort_values(ascending=False)
print(state_emissions.head(10))

plt.figure(figsize=(12, 6))
state_emissions.head(10).plot(kind='bar', color='steelblue')
plt.ylabel('Total Emissions (Metric Tons of CO2e)')
plt.title('Top 10 States by Waste Facility CO2 Emissions (2023)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Map Facility Locations (with Emission Intensity)
import folium

map_usa = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
for _, row in top10.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=8,
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f"{row['FACILITY NAME']} ({row['TOTAL REPORTED EMISSIONS']} MT CO2e)"
    ).add_to(map_usa)

map_usa.save('top10_facilities_map.html')


# Estimate emissions reduction if 75% of methane was captured
df['CO2e_Reduced'] = df['TOTAL REPORTED EMISSIONS'] * 0.75
df['CO2e_Remaining'] = df['TOTAL REPORTED EMISSIONS'] * 0.25

# Show top 5 with this estimate
print(df[['FACILITY NAME', 'STATE', 'TOTAL REPORTED EMISSIONS', 'CO2e_Reduced', 'CO2e_Remaining']].head())

