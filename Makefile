run:
	uvicorn app.main:app --reload

lint:
	ruff check .

format:
	black .