mkdir -p agents
touch agents/__init__.py

# Create main.py
cat > main.py << EOF
import asyncio
from agents.orchestrator_agent import orchestrator_agent
from agents import Runner

async def main():
    result = await Runner.run(orchestrator_agent, "Get latest real estate news and write a blog post.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
EOF

# Create agents/news_agent.py
cat > agents/news_agent.py << EOF
from agents import Agent, function_tool

@function_tool
async def fetch_news() -> str:
    """Simulate fetching recent real estate news."""
    return "Latest real estate news headlines."

news_agent = Agent(
    name="News Agent",
    instructions="Fetch recent real estate news articles.",
    tools=[fetch_news],
)
EOF

# Create agents/blog_agent.py
cat > agents/blog_agent.py << EOF
from agents import Agent, function_tool

@function_tool
async def write_blog(news: str) -> str:
    """Simulate writing a blog post about news."""
    return f"Blog post based on news: {news}"

blog_agent = Agent(
    name="Blog Agent",
    instructions="Write blog posts about real estate news.",
    tools=[write_blog],
)
EOF

# Create agents/orchestrator_agent.py
cat > agents/orchestrator_agent.py << EOF
from agents import Agent

from agents.news_agent import news_agent
from agents.blog_agent import blog_agent

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="Coordinate news fetching and blog writing.",
    handoffs=[news_agent, blog_agent],
)
EOF
