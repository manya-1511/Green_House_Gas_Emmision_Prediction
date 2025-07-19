import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

excel_file = 'SupplyChainEmissionFactorsForUSIndustriesCommodities.xlsx' 
xlsx = pd.ExcelFile(excel_file)


target_sheets = [sheet for sheet in xlsx.sheet_names if "Summary_Commodity" in sheet]

print("Filtered Sheets:", target_sheets)

os.makedirs("plots_by_year", exist_ok=True)

combined_df = pd.DataFrame()

for sheet in target_sheets:
    df = xlsx.parse(sheet)

    df.columns = [str(col).strip() for col in df.columns]

    df.dropna(how='all', inplace=True)

    df.fillna(0, inplace=True)

    if 'Commodity Name' not in df.columns or 'Supply Chain Emission Factors without Margins' not in df.columns:
        continue

    df['Year'] = sheet.split('_')[0]

    combined_df = pd.concat([combined_df, df], ignore_index=True)

print("Combined data shape:", combined_df.shape)

combined_df.to_csv("cleaned_emissions_data.csv", index=False)
print("✅ Cleaned data saved as 'cleaned_emissions_data.csv'")

top_emitters = combined_df.groupby('Commodity Name')['Supply Chain Emission Factors without Margins'] \
                          .mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_emitters.values, y=top_emitters.index, palette='viridis')
plt.title('Top 10 Commodities by Avg Emission Factor (All Years)')
plt.xlabel('Average Emission Factor')
plt.ylabel('Commodity Name')
plt.tight_layout()
plt.savefig("top_10_overall_emitters.png")
plt.show()
print("✅ Overall plot saved as 'top_10_overall_emitters.png'")

for sheet in target_sheets:
    df = xlsx.parse(sheet)
    df.columns = [str(col).strip() for col in df.columns]
    df.dropna(how='all', inplace=True)
    df.fillna(0, inplace=True)

    if 'Commodity Name' not in df.columns or 'Supply Chain Emission Factors without Margins' not in df.columns:
        continue

    top_emitters_year = df.groupby('Commodity Name')['Supply Chain Emission Factors without Margins'] \
                          .mean().sort_values(ascending=False).head(5)

    plt.figure(figsize=(10,5))
    sns.barplot(x=top_emitters_year.values, y=top_emitters_year.index, palette='coolwarm')
    year = sheet.split('_')[0]
    plt.title(f'Top 5 Emitters in {year}')
    plt.xlabel('Emission Factor')
    plt.tight_layout()
    plt.savefig(f"plots_by_year/plot_{year}.png")
    plt.close()

print("✅ Year-wise plots saved in 'plots_by_year/' folder.")
