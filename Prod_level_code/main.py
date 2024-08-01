# main.py

from fastapi import FastAPI
import uvicorn

from api.routers import auth, chat

app = FastAPI()

# Grouping the endpoint based on there functionality

app.include_router(auth.router)  # Router is using for authentication  
app.include_router(chat.router)  # Router is using for chat

# # Include authentication router
# app.include_router(auth.router, prefix="/auth")

# # Include chat router with versioning
# app.include_router(chat.router, prefix="/v1/chat")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
