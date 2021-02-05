CMD     = python3
TARGETS = test

all: $(TARGETS)

test:
	@echo
	@echo Running all test files
	@echo
	@cd ooapi/test/; $(CMD) -m unittest -v
	@cd server/test/; $(CMD) -m unittest -v

test-separate:
	@echo
	@echo Running all test files separately
	@echo
	@cd ooapi/test/; $(CMD) test_tv_library.py -v
	@cd server/test/; $(CMD) test_tv_shows.py -v; $(CMD) test_users_key.py -v; \
	                  $(CMD) test_users_index.py -v; $(CMD) test_reset_endpoint.py -v

test-library:
	@echo
	@echo Running test_tv_library.py
	@echo
	@cd ooapi/test/; $(CMD) test_tv_library.py -v

test-tv:
	@echo
	@echo Running test_tv_shows.py
	@echo
	@cd server/test/; $(CMD) test_tv_shows.py -v

test-users:
	@echo
	@echo Running all users test files
	@echo
	@cd server/test/; $(CMD) test_users_key.py -v; $(CMD) test_users_index.py -v

test-users-key:
	@echo
	@echo Running test_users_key.py
	@echo
	@cd server/test/; $(CMD) test_users_key.py -v

test-users-index:
	@echo
	@echo Running test_users_index.py
	@echo
	@cd server/test/; $(CMD) test_users_index.py -v

test-reset:
	@echo
	@echo Running test_reset_endpoint.py
	@echo
	@cd server/test/; $(CMD) test_reset_endpoint.py -v

clean:
	@echo
	@echo Clearing pycaches...
	@rm -rf ooapi/__pycache__/
	@rm -rf server/__pycache__/
	@rm -rf ooapi/test/__pycache__/
	@rm -rf server/test/__pycache__/

