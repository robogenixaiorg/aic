SHELL :=/bin/bash

.PHONY: clean check setup
.DEFAULT_GOAL=help
VENV_DIR = .venv
PYTHON_VERSION=python3.11

check: # Ruff check
	@ruff check .
	@echo "✅ Check complete!"

fix: # Fix auto-fixable linting issues
	@ruff check app.py --fix

clean: # Clean temporary and build files
	@echo "🧹 Cleaning up..."
	@rm -rf __pycache__ .pytest_cache
	@rm -rf build dist *.egg-info
	@rm -rf $(VENV_DIR)
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete
	@echo "✅ Clean-up complete!"

setup: # Install the package globally
	@echo "🔧 Installing the package globally..."
	@pip3 install .
	@if [ -z "$$AI_API_KEY" ] || [ -z "$$AI_API_URL" ]; then \
		echo "❌ Error: 'AI_API_KEY' and 'AI_API_URL' environment variables are not set."; \
		echo "➡️  Please set them using the following commands (Linux/MacOS):"; \
		echo "   export AI_API_KEY='your_api_key_here'"; \
		echo "   export AI_API_URL='https://your.api.url'"; \
		echo "➡️  Or (Windows):"; \
		echo "   setx AI_API_KEY 'your_api_key_here'"; \
		echo "   setx AI_API_URL 'https://your.api.url'"; \
		exit 1; \
	fi
	@echo -e "\n✅ Installation complete! Run the following command to verify:\n\n ➡️ aic"

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'