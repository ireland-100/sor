import pandas as pd

california = pd.read_csv("06ecological_acs_pl.csv")
massachusetts = pd.read_csv("25ecological_acs_pl.csv")
michigan = pd.read_csv("26ecological_acs_pl.csv")
newyork = pd.read_csv("36ecological_acs_pl.csv")
texas = pd.read_csv("48ecological_acs_pl.csv")

list_of_data_frames = [california, massachusetts, michigan, newyork, texas]
sub_populations = ['hispanic_PL', 'white_PL', 'black_PL', 'sor_PL', 'hispanic_ACS', 'white_ACS', 'black_ACS', 'sor_ACS', 'brazilian_ACS',
       'guyanese_ACS', 'cabo_verdean_ACS', 'belizean_ACS', 'armenian_ACS',
       'cypriot_ACS', 'egyptian_ACS', 'iranian_ACS', 'iraqi_ACS',
       'israeli_ACS', 'jordanian_ACS', 'lebanese_ACS', 'maltese_ACS',
       'moroccan_ACS', 'palestinian_ACS', 'sudanese_ACS', 'syrian_ACS',
       'turkish_ACS', 'arab_ACS', 'arab_arab_ACS', 'arab_other_ACS',
       'chaldean_ACS', 'mena_world_bank_ACS', 'mena_unhcr_ACS',
       'mena_unsd_ACS']


for i in range(len(list_of_data_frames)):
    list_of_data_frames[i] = list_of_data_frames[i].drop(columns=list_of_data_frames[i].columns[list_of_data_frames[i].columns.str.contains("pct")])



def create_percents(df, total_population, sub_population):
    df[sub_population + "_pct"] = (df[sub_population] / df[total_population]) #for EI, we want the decimals, not the percent. so we don't multiply by 100

for i in range(len(list_of_data_frames)):
    for j in range(len(sub_populations)):
        if "PL" in sub_populations[j]:
            total_population = "totpop_PL"
        else:
            total_population = "totpop_ACS"
        create_percents(list_of_data_frames[i], total_population, sub_populations[j])

## Now, we want to rename the columns with the variable names, from the appropriate Census/ACS table

pl_vars_swapped = {
    "totpop_PL": "P1_001N",
    "hispanic_PL": "P2_002N",
    "white_PL": "P1_002N",
    "black_PL": "P1_004N",
    "sor_PL": "P1_008N"
}

acs_vars_swapped = {
    "totpop_ACS": "B03002_001E",
    "hispanic_ACS": "B03002_012E",
    "white_ACS": "B02001_002E",
    "black_ACS": "B02001_003E",
    "sor_ACS": "B02001_007E",
    "brazilian_ACS": "B04004_022E",
    "guyanese_ACS": "B04004_045E",
    "cabo_verdean_ACS": "B04004_074E",
    "belizean_ACS": "B04004_097E",
    "armenian_ACS": "B04004_016E",
    "cypriot_ACS": "B04004_030E",
    "egyptian_ACS": "B04004_007E",
    "iranian_ACS": "B04004_048E",
    "iraqi_ACS": "B04004_008E",
    "israeli_ACS": "B04004_050E",
    "jordanian_ACS": "B04004_009E",
    "lebanese_ACS": "B04004_010E",
    "maltese_ACS": "B04004_056E",
    "moroccan_ACS": "B04004_011E",
    "palestinian_ACS": "B04004_012E",
    "sudanese_ACS": "B04004_084E",
    "syrian_ACS": "B04004_013E",
    "turkish_ACS": "B04004_091E",
    "arab_ACS": "B04004_006E",
    "arab_arab_ACS": "B04004_014E",
    "arab_other_ACS": "B04004_015E",
    "chaldean_ACS": "B04004_017E"
}

for i in range(len(list_of_data_frames)):
    list_of_data_frames[i].rename(columns = pl_vars_swapped, inplace = True)
    list_of_data_frames[i].rename(columns = acs_vars_swapped, inplace = True)

list_of_data_frames[0].to_csv("/csv_files/06ecological_df.csv", index = False)
list_of_data_frames[1].to_csv("/csv_files/25ecological_df.csv", index = False)
list_of_data_frames[2].to_csv("/csv_files/26ecological_df.csv", index = False)
list_of_data_frames[3].to_csv("/csv_files/36ecological_df.csv", index = False)
list_of_data_frames[4].to_csv("/csv_files/48ecological_df.csv", index = False)