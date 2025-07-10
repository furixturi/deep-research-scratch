import argparse
from api.models.model_router import call_model

def main():
    parser = argparse.ArgumentParser(description="Test model router via CLI")
    parser.add_argument("--provider", default=None, help="Model provider (aoai or openai)")
    parser.add_argument("--model", default=None, help="Model name (gpt-4o or o3)")
    parser.add_argument("--agent", default="single_agent", help="Agent ID (default, single_agent, planner_agent, search_agent)")
    parser.add_argument("--prompt", default="What is the capital of Germany?", help="User prompt")

    args = parser.parse_args()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": args.prompt}
    ]

    # session model override
    config = {}
    if args.provider and args.model:
        config = {
            "provider": args.provider,
            "model": args.model
        }

    try:
        print(f"\n Calling {args.provider or 'default provider aoai'} | {args.model or 'default model gpt-4o'} for Agent single_agent: {args.agent}")
        respose = call_model(messages, model_config=config, agent_id=args.agent)
        print(f"\nModel response: {respose}")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()