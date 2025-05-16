SECRET_KEY := $(shell python3 -c "import secrets; print(secrets.token_hex(32))")

DOTENV = .env

secret:
	@echo "Generate secret key"
	@echo "SECRET_KEY=$(SECRET_KEY)" > $(DOTENV)
	@echo "ALGORITHM=HS256" >> $(DOTENV)
	@echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> $(DOTENV)