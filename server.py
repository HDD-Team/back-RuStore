from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import schemas
from model import llm_chain
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем пул потоков
executor = ThreadPoolExecutor(max_workers=12)

@app.post("/help_bot", response_model=schemas.Answer)
def asking(ask: schemas.Query):
    if ask:
        print(ask.query)
        # Выполняем функцию llm_chain() в отдельном потоке
        future = executor.submit(llm_chain, ask.query)
        # Ждем результата выполнения функции
        res = future.result()
        return res

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
