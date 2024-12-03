import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm  # for progress bar

def process_regional_data():
    print("Starting regional data processing...")
    
    # Define base path for data files
    base_path = Path('public/data')
    
    # List all files first
    files = sorted(base_path.glob('industry_region_monthly_frequency_*.xlsx'))
    print(f"Found {len(files)} files to process")

    # Dictionary for Chinese to English translations
    region_translations = {
        # Municipalities (直辖市)
        '北京': 'Beijing',
        '天津': 'Tianjin', 
        '上海': 'Shanghai',
        '重庆': 'Chongqing',
        
        # Provinces (省)
        '河北': 'Hebei',
        '山西': 'Shanxi',
        '辽宁': 'Liaoning', 
        '吉林': 'Jilin',
        '黑龙江': 'Heilongjiang',
        '江苏': 'Jiangsu',
        '浙江': 'Zhejiang',
        '安徽': 'Anhui',
        '福建': 'Fujian',
        '江西': 'Jiangxi',
        '山东': 'Shandong',
        '河南': 'Henan',
        '湖北': 'Hubei',
        '湖南': 'Hunan',
        '广东': 'Guangdong',
        '海南': 'Hainan',
        '四川': 'Sichuan',
        '贵州': 'Guizhou',
        '云南': 'Yunnan',
        '陕西': 'Shaanxi',
        '甘肃': 'Gansu',
        '青海': 'Qinghai',
        '台湾': 'Taiwan',
        
        # Autonomous Regions (自治区)
        '内蒙古': 'Inner Mongolia',
        '广西': 'Guangxi',
        '西藏': 'Tibet',
        '宁夏': 'Ningxia',
        '新疆': 'Xinjiang',
        
        # Special Administrative Regions (特别行政区)
        '香港': 'Hong Kong',
        '澳门': 'Macau',
        
        # Other Common Categories
        '其他': 'Others',
        '深圳': 'Shenzhen',
        '大连': 'Dalian',
        '青岛': 'Qingdao',
        '宁波': 'Ningbo',
        '厦门': 'Xiamen',
        '苏州': 'Suzhou',
        '武汉': 'Wuhan',
        '广州': 'Guangzhou'
    }

    industry_translations = {
        '信息技术': 'Information Technology',
        '农业机械': 'Agricultural Machinery',
        '新材料': 'New Materials',
        '新能源汽车': 'New Energy Vehicles',
        '机器人': 'Robotics',
        '海洋工程': 'Ocean Engineering',
        '生物医药': 'Biopharmaceuticals',
        '电力装备': 'Electric Power',
        '航空航天': 'Aerospace',
        '轨道交通': 'Rail Transit'
    }

    all_data = []
    
    # Use tqdm for progress bar
    for file in tqdm(files, desc="Processing files"):
        year = int(file.stem.split('_')[-1])
        print(f"\nProcessing {file.name}...")
        
        df = pd.read_excel(file)
        
        # Rename columns
        df.columns = ['Industry', 'Region'] + list(range(1, 13))  # 1-12 for months
        
        print(f"Converting {year} data to long format...")
        # Melt the monthly data into rows
        df_melted = df.melt(
            id_vars=['Industry', 'Region'],
            value_vars=list(range(1, 13)),
            var_name='Month',
            value_name='Frequency'
        )
        
        # Add year column
        df_melted['Year'] = year
        
        print(f"Translating {year} data...")
        # Translate industry and region names
        df_melted['Industry'] = df_melted['Industry'].map(industry_translations)
        df_melted['Region'] = df_melted['Region'].map(region_translations)
        
        all_data.append(df_melted)
    
    print("\nCombining all data...")
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("Cleaning and sorting data...")
    # Clean data
    combined_df = combined_df.dropna()
    
    # Sort data
    combined_df = combined_df.sort_values(['Year', 'Month', 'Industry', 'Region'])
    
    # Save processed data
    output_path = base_path / 'processed_regional_data.csv'
    print(f"\nSaving processed data to {output_path}")
    combined_df.to_csv(output_path, index=False)
    
    print("\n✅ Processing completed successfully!")
    return combined_df

if __name__ == "__main__":
    try:
        df = process_regional_data()
        print("\nData Overview:")
        print(f"Total number of records: {len(df)}")
        print(f"Years covered: {df['Year'].min()} to {df['Year'].max()}")
        print(f"Number of unique regions: {df['Region'].nunique()}")
        print(f"Number of unique industries: {df['Industry'].nunique()}")
        print("\nUnique regions:", sorted(df['Region'].unique()))
        print("\nUnique industries:", sorted(df['Industry'].unique()))
        
        print("\n✨ Script execution completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")