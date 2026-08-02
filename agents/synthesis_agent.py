import os
from dotenv import load_dotenv
from openai import OpenAI
from agents.data_agent import DataAgent
from agents.knowledge_agent import KnowledgeAgent

load_dotenv()


class SynthesisAgent:
    def __init__(self):
        self.data_agent = DataAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

    def generate_report(self, district, query):
        district_data = self.data_agent.analyze_district(district=district)

        knowledge = self.knowledge_agent.retrieve(query=query, k=3)
        context = "\n\n".join(
            [f"Source: {item['source']}\n{item['content']}" for item in knowledge]
        )

        prompt = f"""
You are a public health assistant.

District Data:
{district_data}

Retrieved Knowledge:
{context}

User Request:
{query}

Generate a structured dengue risk assessment report.
Include:
1. Current Situation
2. Weather Analysis
3. Epidemiological Analysis
4. Risk Level
5. Recommended Actions

Only use the supplied information.
Do not invent statistics.
"""

        response = self.client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {"role": "system", "content": "You are an epidemiological analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        report = response.choices[0].message.content

        reflection_prompt = f"""
Review the report below.

District Data:
{district_data}

Report:
{report}

Check whether:
- The report agrees with the supplied data.
- No unsupported claims are made.
- No new statistics are invented.
- Recommendations are consistent with the evidence.

If everything is correct,
return the report unchanged.
Otherwise,
correct the report and return the corrected version only.
"""

        reflection = self.client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {"role": "system", "content": "You are a quality assurance reviewer."},
                {"role": "user", "content": reflection_prompt}
            ],
            temperature=0,
            max_tokens=1500
        )
        final_report = reflection.choices[0].message.content

        return final_report


if __name__ == "__main__":
    agent = SynthesisAgent()
    report = agent.generate_report(
        district="Colombo",
        query="Generate a dengue risk assessment for Colombo."
    )
    print(report)