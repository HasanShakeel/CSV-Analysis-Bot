from fastapi import APIRouter, Depends, HTTPException
from services.data_processing import read_csv_data, clean_data, compare_months, compare_yearly, compare_ytd
from services.openai_interaction import prepare_prompt, get_openai_response
from security.authenticate_token import verify_jwt_token
import re

app = APIRouter()

@app.post("/chatbot")
async def analyze(question: str, token: dict = Depends(verify_jwt_token)):
    try:
        df_results, df_targets = read_csv_data()
        df_results = clean_data(df_results)
        df_targets = clean_data(df_targets)
        
        comparison_df = None
        
        month_year_pattern = r'(\b\w+\b) (\d{4})'
        month_year_matches = re.findall(month_year_pattern, question)
        year_match = re.search(r'(\d{4})', question)
        
        if "compare the result of" in question and "to targets of" in question and len(month_year_matches) == 2:
            result_month_year = ' '.join(month_year_matches[0])
            target_month_year = ' '.join(month_year_matches[1])
            comparison_df = compare_months(df_results, df_targets, result_month_year, target_month_year)
        elif "year to date" in question or "YTD" in question and year_match:
            year = year_match.group(0)
            comparison_df = compare_ytd(df_results, df_targets, year)
        elif "year" in question and year_match:
            year = year_match.group(0)
            comparison_df = compare_yearly(df_results, df_targets, year)
        
        if comparison_df is not None:
            if comparison_df.empty:
                print("Comparison data is empty.")
                prompt = prepare_prompt(df_results, df_targets, question)
            else:
                prompt = prepare_prompt(df_results, df_targets, question, comparison_df)
        else:
            prompt = prepare_prompt(df_results, df_targets, question)
        
        # Print the prompt to console
        print("Prompt:", prompt)
        
        response = get_openai_response(prompt)
        
        # Remove newline characters from the response
        clean_response = response.replace('\n', ' ').replace('\r', ' ')
        
        return {"response": clean_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
