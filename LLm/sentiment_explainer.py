class LLMSentimentExplainer:
    def __init__(self, client=None):
        self.client = client  # OpenAI / local LLM later

    def explain(self, posts, numeric_score):
        if not self.client:
            return "LLM disabled. Numeric sentiment used."

        prompt = f"""
        Posts:
        {posts}

        Numeric sentiment score: {numeric_score}

        Explain public perception in 2 sentences.
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
