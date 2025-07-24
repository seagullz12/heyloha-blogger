import asyncio
from agents import Runner
from ai_agents.news_agent import news_agent
import pprint # For pretty printing complex objects

async def test_single_agent():
    print("Testing NewsAgent directly...")
    result = await Runner.run(news_agent, input="artificial intelligence")

    print("\n--- Inspecting RunResult object ---")
    print(f"Type of result: {type(result)}")
    print(f"Content of result: {result}")
    print(f"Attributes available on result: {dir(result)}")
    print("-----------------------------------\n")

    # Correct way to access the output
    final_output = result.final_output

    if final_output:
        print("NewsAgent output found:")
        for article in final_output:
            print(f"- {article.title} ({article.source_name})")
    else:
        print("NewsAgent returned no final output.") # Modified message

if __name__ == "__main__":
    asyncio.run(test_single_agent())