from fastapi import FastAPI, status
from app import model
from app.db import engine
from app.routers import posts , users


# 🔌 Establish DB connection with retry (useful if DB starts late)
# while True:
#     try:
#         connection = psycopg.connect(
#             host="localhost",
#             user="postgres",
#             password="sweety@12345",
#             dbname="fastapi",
#             port=5432,
#             row_factory=dict_row  # return rows as dict instead of tuple
#         )
#         db = connection.cursor()

#         db.execute("SELECT NOW()")
#         print("Connected to DB:", db.fetchone())
#         break

#     except Exception as e:
#         print("DB connection failed:", e)
#         sleep(3)

# Create tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

# 🏠 Health check
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "welcome to the API"}