add-uv:
	@echo "[INFO:] Installing UV ...."	
	# add mac / linux
	curl -LsSf https://astral.sh/uv/install.sh | sh

install:
	@echo "--- 🚀 Installing project ---"
	uv sync

