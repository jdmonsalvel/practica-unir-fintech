install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

run-docker:
	docker build -t fintech-weather . && docker run -p 8000:8000 fintech-weather

test:
	pytest tests/ -v
