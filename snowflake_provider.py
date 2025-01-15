import sys
import json
from snowflake.snowpark.session import Session

def create_snowflake_session():
    connection_parameters = {
        "account": "your_account",
        "user": "your_user",
        "password": "your_password",
        "warehouse": "your_warehouse",
        "database": "your_database",
        "schema": "your_schema"
    }
    return Session.builder.configs(connection_parameters).create()

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    prompt = input_data['prompt']
    
    session = create_snowflake_session()
    
    try:
        # Correct Cortex completion syntax
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                'claude-3-5-sonnet',  -- or another model from the supported list
                '{prompt}',
                {{
                    "temperature": 0,
                    "max_tokens": 100,
                    "response_format": {{"type": "json"}}
                }}
            ) as completion
        """).collect()[0]['COMPLETION']
        
        print(json.dumps({'output': result}))
        
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
