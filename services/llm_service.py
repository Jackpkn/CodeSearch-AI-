
import google.generativeai as genai  # type: ignore
from config import Settings

settings = Settings()
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model =genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config,
        )

    def generate_response(self, query: str, search_results: list[dict]):
        context_text = "\n\n".join(
            [
                f"Source {i+1} ({result['url']}):\n{result['content']}"
                for i, result in enumerate(search_results)
            ]
        )

        full_prompt = (
            "Context from web search:\n"
            f"{context_text}\n\n"
            f"Query: {query}\n\n"
            "Please provide a comprehensive, detailed, well-cited accurate response using the above context.\n"
            "Think and reason deeply. Ensure it answers the query the user is asking. Do not use your knowledge until it is absolutely necessary."
        )

        response = self.model.generate_content(full_prompt, stream=True)

        for chunk in response:
            yield chunk.text
