from pyjstat import pyjstat
import requests
import pandas as pd
import os
os.makedirs('data', exist_ok=True)

#Life satisfaction over time
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw01?lang=en&isced11=TOTAL&indic_wb=LIFESAT&sex=T&age=Y_GE16&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=ME&geo=MK&geo=AL&geo=RS&geo=TR&geo=XK&time=2023&time=2022&time=2021&time=2018&time=2013')
df = dataset.write('dataframe')
rename_dict = {
    'Czechia': 'Czech Rep.',
    'European Union - 27 countries (from 2020)': 'EU27',
    'Türkiye': 'Turkey'
}
df.replace(rename_dict, inplace=True)
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Time', values='value')
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Time.csv', index=True)

#Life satisfaction change compared to 2022
for year in ['2013', '2018', '2021', '2022']:
    df_new[year] = pd.to_numeric(df_new[year], errors='coerce')
df_new['difference 2013'] = df_new['2022'] - df_new['2013']
df_new['difference 2018'] = df_new['2022'] - df_new['2018']
df_new['difference 2021'] = df_new['2022'] - df_new['2021']
df_change = df_new[['difference 2013', 'difference 2018', 'difference 2021', '2022']]
df_change = df_change.dropna()
df_change = df_change.round(2)
df_change.to_csv('data/Eurostat_Life_Satisfaction_Overall_Time_Change.csv', index=True)

#Life satisfaction average and max min
yearly_metrics = {
    'Year': [],
    'Average Score': [],
    'Lowest Score': [],
    'Highest Score': []
}
for year in ['2013', '2018', '2021', '2022']:
    yearly_metrics['Year'].append(year)
    yearly_metrics['Average Score'].append(df_new[year].mean())
    yearly_metrics['Lowest Score'].append(df_new[year].min())
    yearly_metrics['Highest Score'].append(df_new[year].max())
df_yearly_metrics = pd.DataFrame(yearly_metrics)
df_yearly_metrics.to_csv('data/Eurostat_Life_Satisfaction_Overall_Time_AvgMaxMin.csv', index=False)

#Life Satisfaction by age in 2022
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw01?lang=en&isced11=TOTAL&indic_wb=LIFESAT&sex=T&age=Y16-19&age=Y16-24&age=Y16-29&age=Y_GE16&age=Y20-24&age=Y25-29&age=Y25-34&age=Y25-64&age=Y35-49&age=Y50-64&age=Y65-74&age=Y_GE65&age=Y_GE75&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=ME&geo=MK&geo=AL&geo=RS&geo=TR&geo=XK&time=2022')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Age class', values='value')
df_new = df_new.dropna()
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Age_Total.csv', index=True)

#Life satisfaction 16-24 over time
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw01?lang=en&isced11=TOTAL&indic_wb=LIFESAT&sex=T&age=Y16-24&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=ME&geo=MK&geo=AL&geo=RS&geo=TR&geo=XK&time=2023&time=2022&time=2021&time=2018&time=2013')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Time', values='value')
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Age_Young.csv', index=True)

#Life satisfaction 65+ over time
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw01?lang=en&isced11=TOTAL&indic_wb=LIFESAT&sex=T&age=Y_GE65&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=ME&geo=MK&geo=AL&geo=RS&geo=TR&geo=XK&time=2023&time=2022&time=2021&time=2018&time=2013')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Time', values='value')
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Age_Old.csv', index=True)

#Life satisfaction by sex 
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw01?lang=en&isced11=TOTAL&indic_wb=LIFESAT&sex=T&sex=M&sex=F&age=Y_GE16&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=ME&geo=MK&geo=AL&geo=RS&geo=TR&geo=XK&time=2022')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Sex', values='value')
df_new = df_new.dropna()
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Sex.csv', index=True)

#Life satisfaction by education level
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw01?lang=en&isced11=TOTAL&isced11=ED0-2&isced11=ED3_4&isced11=ED5-8&indic_wb=LIFESAT&sex=T&age=Y_GE16&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=ME&geo=MK&geo=AL&geo=RS&geo=TR&geo=XK&time=2022')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='International Standard Classification of Education (ISCED 2011)', values='value')
df_new = df_new.dropna()
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Education.csv', index=True)

#Life satisfaction by income level 
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw02?lang=en&deg_urb=TOTAL&quantile=TOTAL&quantile=QU1&quantile=QU2&quantile=QU3&quantile=QU4&quantile=QU5&indic_wb=LIFESAT&hhtyp=TOTAL&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=MK&geo=AL&geo=RS&time=2022')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Quantile', values='value')
df_new = df_new.dropna()
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Income.csv', index=True)

#Life satisfaction by household
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw02?lang=en&deg_urb=TOTAL&quantile=TOTAL&indic_wb=LIFESAT&hhtyp=A1&hhtyp=A2&hhtyp=A_GE3&hhtyp=HH_NDCH&hhtyp=HH_DCH&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=MK&geo=AL&geo=RS&time=2022')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Type of household', values='value')
df_new = df_new.dropna()
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Household.csv', index=True)

#Life satisfaction by degree of urbanisation
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_pw02?lang=en&deg_urb=DEG1&deg_urb=DEG2&deg_urb=DEG3&quantile=TOTAL&indic_wb=LIFESAT&hhtyp=TOTAL&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=IS&geo=NO&geo=CH&geo=UK&geo=MK&geo=AL&geo=RS&time=2022')
df = dataset.write('dataframe')
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Degree of urbanisation', values='value')
df_new = df_new.dropna()
df_new.to_csv('data/Eurostat_Life_Satisfaction_Overall_Urbanisation.csv', index=True)