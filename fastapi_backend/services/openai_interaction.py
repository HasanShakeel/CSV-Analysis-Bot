import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

def prepare_prompt(df_results, df_targets, question, comparison_df=None):
    summary_results = df_results.describe(include='all').to_dict()
    summary_targets = df_targets.describe(include='all').to_dict()
    comparison_summary = comparison_df.to_dict() if comparison_df is not None else {}
    
    prompt = (
        f"You have the following data available:\n"
        f"Results data summary: {summary_results}\n"
        f"Targets data summary: {summary_targets}\n"
        f"Comparison data: {comparison_summary}\n"
        f"Based on this data, {question}"
    )
    return prompt

def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response['choices'][0]['message']['content'].strip()
