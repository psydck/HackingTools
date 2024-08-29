# Virtual Environment
activate:
	@powershell.exe .\.venv\Scripts\activate.bat

# Git
add:
	@echo -e "\n------------- \033[0;36m Staged \033[0m -------------\n" 
	@git add $(file)
	@git status

commit:
	@echo -e "\n------------- \033[1;32m Committed \033[0m -------------\n" 
	@git commit -m "$(message)" 
	@git status

unstage:
	@echo -e "\n------------- \033[0;31m Unstage \033[0m -------------\n" 
	@git restore --staged $(files)

status:
	@echo -e "\n-------------  Status \033[0m -------------\n" 
	@git status

# PIP Packages
install:
	@echo -e "\n------------- \033[0;35m Installing Requirements \033[0m -------------\n" 
	@powershell.exe .\.venv\Scripts\python -m pip install -r requirements.txt

freeze:
	@echo -e "\n------------- \033[1;32m List of Installed Packages \033[0m -------------\n" 
	@powershell.exe .\.venv\Scripts\python -m pip list

uninstall:
	@echo -e "\n------------- \033[0;31m Uninstalling a Package \033[0m -------------\n" 
	@powershell.exe .\.venv\Scripts\python -m pip uninstall $(package)

# Python
run:
	@powershell.exe .\.venv\Scripts\python main.py

test:
	@powershell.exe .\.venv\Scripts\python -m pytest

# Docker
image:
	@echo -e "\n------------- \033[1;32m Building Docker Image \033[0m -------------\n" 
	@docker build . -t hack

container:
	@echo -e "\n------------- \033[0;36m Creating Docker Container \033[0m -------------\n" 
	@docker run -d -p 8080:APP_PORT -name app hack

start_container:
	@echo -e "\n------------- \033[1;32m Starting Container \033[0m -------------\n" 
	@docker container start app

stop_container:
	@echo -e "\n------------- \033[0;31m Stopping Container \033[0m -------------\n" 
	@docker container stop app

save_image:
	@echo -e "\n------------- \033[0;35m Saving Image to zip File \033[0m -------------\n" 
	@docker save -o hack_docker_image.zip hack

