import pandas as pd

# Translation dictionary
translations = {
    '信息技术': 'Information Technology',
    '农业机械': 'Agricultural Machinery',
    '新材料': 'New Materials',
    '新能源汽车': 'New Energy Vehicles',
    '机器人': 'Robotics',
    '海洋工程': 'Ocean Engineering',
    '生物医药': 'Biopharmaceuticals',
    '电力': 'Electric Power',
    '航天': 'Aerospace',
    '轨道交通': 'Rail Transit'
}

# Read the original CSV file
df = pd.read_csv('/Users/kohanchen/Documents/Fall 2024/data315-au24/project/Final Project/final-project2-new/static/data/combined_frequency_data.csv')

# Create a new column with translated terms
df['Word_English'] = df['Word'].map(translations)

# Create new dataframe with English terms
df_english = df.copy()
df_english['Word'] = df_english['Word_English']
df_english = df_english.drop('Word_English', axis=1)

# Save to new CSV file
output_path = 'combined_frequency_data_english.csv'
df_english.to_csv(output_path, index=False)

print(f"Created English version at: {output_path}")