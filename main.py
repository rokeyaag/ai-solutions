import uvicorn
from api.index import app
from config import config

if __name__ == "__main__":
    print(f"🚀 Starting AI SaaS Dashboard at http://{config.HOST}:{config.PORT}")
    uvicorn.run("api.index:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
