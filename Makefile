.PHONY: clean test run dev install

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache data/*.db runtime/*.pid runtime/*.json runtime/*.log logs/*.log
	@echo "Clean OK"

test:
	python -m pytest tests/ -v

run:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

dev: clean test run

install:
	pip install -e .

check:
	python -m py_compile $$(find . -name "*.py" | grep -v __pycache__)
	@echo "Compile OK"
	python -c "from api.main import app; print(f'Routers: {len(app.routes)}')"
	python -c "from ai.knowledge import AIKnowledge; k=AIKnowledge(); print('AI Knowledge OK')"
