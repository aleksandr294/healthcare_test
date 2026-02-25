import fastapi

from api import router

app = fastapi.FastAPI(root_path="/analytics", docs_url="/docs", redoc_url="/redoc")

router.configure(app)
