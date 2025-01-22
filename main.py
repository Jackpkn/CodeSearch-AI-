import asyncio

from fastapi import FastAPI, WebSocket  # type: ignore
from pydantic_models.chat_body import ChatBody
from services.llm_service import LLMService
from services.search_service import SearchService
from services.sort_source_service import SortSortService

app = FastAPI()
search_service = SearchService()
sort_source_service = SortSortService()
llm_service = LLMService()

# WebSocket endpoint for chat
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await asyncio.sleep(1)
        data = await websocket.receive_json()
        query = data.get("query")  # Corrected dictionary access
        if not query:
            await websocket.close(code=1008, reason="Query not provided")
            return

        search_results = search_service.web_search(query)
        print("Search Results:", search_results)
        sorted_results = sort_source_service.sort_source(query, search_results)
        await asyncio.sleep(0.1)
        await websocket.send_json({"type": "search_result", "data": sorted_results})

        for chunk in llm_service.generate_response(query, sorted_results):
            print("Generated Chunk:", chunk)
            await asyncio.sleep(0.1)
            await websocket.send_json({"type": "content", "data": chunk})

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        await websocket.close(code=1011, reason=f"Server error: {str(e)}")
    else:
        await websocket.close(code=1000, reason="Normal closure")

# HTTP POST endpoint for chat
@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_result = search_service.web_search(body.query)
    sorted_result = sort_source_service.sort_sources(body.query, search_result)
    response = llm_service.generate_response(body.query, sorted_result)
    return response