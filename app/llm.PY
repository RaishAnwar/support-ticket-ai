from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL


client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
  answer = ask_llm("Say hello Raish in one short sentence.")
  print(answer)