# Author: Ao Chen, 26-12-2021, Sion. 
import numpy as np
import pandas as pd

def write_excel(xlsx_output, filename_xlsx, materialsDB_df):
    if xlsx_output == 1:
        with pd.ExcelWriter(filename_xlsx, mode='a', if_sheet_exists='replace') as writer:
            materialsDB_df.to_excel(writer, sheet_name='Materials-DB')

def write_json(json_output, filename_json, materialsDB_df):
    if json_output == 1:
        materialsDB_df.to_json(filename_json, orient="table")

def computing(filename_xlsx):
    materials_db = pd.ExcelFile(filename_xlsx)
    country_df = materials_db.parse('Country-list')
    materials_df = materials_db.parse('Materials')

    Country = country_df['Country']
    Material = materials_df['Material']
    Index = pd.MultiIndex.from_product([Country, Material], names=['Country', 'Material'])

    kgCO2eq_kWh = country_df['1 kWh Medium voltage (kg CO2-Eq)']
    energy_material = materials_df['Energy']
    CO2eq = materials_df['CO2eq']
    kgCO2eq = np.empty(len(Index)) # Initialization
    ISO2_CC = np.empty(len(Index), dtype=object)
    ISO3_CC = np.empty(len(Index), dtype=object)
    Unit    = np.empty(len(Index), dtype=object)

    for i in range(len(country_df)):
        for j in range(len(materials_df)):
            kgCO2eq[i*len(materials_df)+j] = kgCO2eq_kWh[i]*energy_material[j]+CO2eq[j]
            ISO2_CC[i*len(materials_df)+j] = country_df['ISO2_CC'][i]
            ISO3_CC[i*len(materials_df)+j] = country_df['ISO3_CC'][i]
            Unit[i*len(materials_df)+j]    = materials_df['Unit'][j]

    Info = {'ISO2_CC': ISO2_CC, 'ISO3_CC': ISO3_CC, 'kgCO2eq': kgCO2eq, 'Unit': Unit,}
    materialsDB_df = pd.DataFrame(data=Info)
    materialsDB_df = materialsDB_df.set_index(Index)

    return materialsDB_df

def main():
    # TODO: set paramters below as needed.

    xlsx_output = 1 #use 1 to output xlsx, 0 not. 
    json_output = 1 
    # sql_output  = 1 #specific sql engine should be defined
    filename_xlsx = 'Materials_DB/22122021CSC_Materials_DB.xlsx' #to be changed for different files
    filename_json = 'Materials_DB/22122021CSC_Materials_DB.json' #same as above
    # filename_sql  = '22122021CSC_Materials_DB.sql'
    materialsDB_df = computing(filename_xlsx)
    write_excel(xlsx_output, filename_xlsx, materialsDB_df)
    write_json(json_output, filename_json, materialsDB_df)

if __name__ == "__main__":
    main()