import pandas as pd
from dateutil import parser

def read_csv_data():
    df_results = pd.read_csv("results.csv")
    df_targets = pd.read_csv("targets.csv")
    return df_results, df_targets

def clean_data(df):
    df = df.fillna(0)
    df = df.drop_duplicates()
    return df

def parse_date_to_yearmonth(date_str):
    try:
        parsed_date = parser.parse(date_str)
        yearmonth = parsed_date.strftime("%Y%m")
        return yearmonth
    except ValueError:
        raise Exception(f"Unable to parse date: {date_str}")

def summarize_data(df):
    summary_columns = ['Business', 'Vertical', 'Subvertical', 'Platform', 'Zona', 'Pais', 'Partner']
    aggregated_data = df.groupby(summary_columns).sum().reset_index()
    return aggregated_data

def compare_months(df_results, df_targets, result_month_year, target_month_year):
    result_month_year_str = parse_date_to_yearmonth(result_month_year)
    target_month_year_str = parse_date_to_yearmonth(target_month_year)
    
    results_month = df_results[df_results['YearMonth'].astype(str) == result_month_year_str]
    targets_month = df_targets[df_targets['YearMonth'].astype(str) == target_month_year_str]
    
    if results_month.empty:
        print(f"No results found for the month-year: {result_month_year_str}")
    if targets_month.empty:
        print(f"No targets found for the month-year: {target_month_year_str}")
    
    results_summary = summarize_data(results_month)
    targets_summary = summarize_data(targets_month)
    
    comparison = pd.merge(results_summary, targets_summary, on=['Business', 'Vertical', 'Subvertical', 'Platform', 'Zona', 'Pais', 'Partner'], suffixes=('_result', '_target'))
    
    if comparison.empty:
        print(f"No matching data found between results and targets for months {result_month_year_str} and {target_month_year_str}")
    
    # Limit to top N rows to reduce the prompt size
    comparison = comparison.head(50)
    
    return comparison

def compare_yearly(df_results, df_targets, year):
    year_str = str(year)
    results_year = df_results[df_results['YearMonth'].astype(str).str.startswith(year_str)]
    targets_year = df_targets[df_targets['YearMonth'].astype(str).str.startswith(year_str)]
    
    if results_year.empty:
        print(f"No results found for the year: {year_str}")
    if targets_year.empty:
        print(f"No targets found for the year: {year_str}")
    
    results_summary = summarize_data(results_year)
    targets_summary = summarize_data(targets_year)
    
    comparison = pd.merge(results_summary, targets_summary, on=['Business', 'Vertical', 'Subvertical', 'Platform', 'Zona', 'Pais', 'Partner'], suffixes=('_result', '_target'))
    
    if comparison.empty:
        print(f"No matching data found between results and targets for the year {year_str}")
    
    # Limit to top N rows to reduce the prompt size
    comparison = comparison.head(50)
    
    return comparison

def compare_ytd(df_results, df_targets, year):
    year_str = str(year)
    current_month = pd.Timestamp.now().month
    ytd_str = [f"{year_str}{str(month).zfill(2)}" for month in range(1, current_month + 1)]
    results_ytd = df_results[df_results['YearMonth'].astype(str).isin(ytd_str)]
    targets_ytd = df_targets[df_targets['YearMonth'].astype(str).isin(ytd_str)]
    
    if results_ytd.empty:
        print(f"No results found for the year to date: {year_str}")
    if targets_ytd.empty:
        print(f"No targets found for the year to date: {year_str}")
    
    results_summary = summarize_data(results_ytd)
    targets_summary = summarize_data(targets_ytd)
    
    comparison = pd.merge(results_summary, targets_summary, on=['Business', 'Vertical', 'Subvertical', 'Platform', 'Zona', 'Pais', 'Partner'], suffixes=('_result', '_target'))
    
    if comparison.empty:
        print(f"No matching data found between results and targets for the year to date {year_str}")
    
    # Limit to top N rows to reduce the prompt size
    comparison = comparison.head(50)
    
    return comparison
