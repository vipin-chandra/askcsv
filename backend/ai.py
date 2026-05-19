from openai import OpenAI
import re

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

def clean_sql(sql):
    sql = sql.replace("```sql", "").replace("```", "")
    return sql.strip()


def generate_schema(sample_data):
    prompt = f"""
    You are a PostgreSQL expert.

    Tasks:
    - Generate CREATE TABLE query
    - Use snake_case
    - Infer types
    - Add id SERIAL PRIMARY KEY

    Return ONLY SQL. No markdown.

    Data:
    {sample_data}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Return only SQL."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return clean_sql(response.choices[0].message.content)


def generate_query(user_prompt, table_name):
    prompt = f"""
    Convert to PostgreSQL SQL.

    Table: {table_name}

    Rules:
    - Only SQL
    - No explanations

    Query:
    {user_prompt}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Return only SQL."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return clean_sql(response.choices[0].message.content)