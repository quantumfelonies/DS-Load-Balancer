# Makefile to install Docker on Ubuntu for Windows (WSL)

.PHONY: all install_docker install_ubuntu update_upgrade clean

all: install_docker update_upgrade

install_docker:
	@echo "Installing Docker..."
	@sudo apt-get update
	@sudo apt-get install -y \
		apt-transport-https \
		ca-certificates \
		curl \
		software-properties-common
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	@sudo add-apt-repository \
		"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	@sudo apt-get update
	@sudo apt-get install -y docker-ce
	@sudo service docker start
	@sudo usermod -aG docker ${USER}

update_upgrade:
	@echo "Updating and upgrading system..."
	@sudo apt-get update
	@sudo apt-get upgrade -y
	@sudo apt-get dist-upgrade -y
	@sudo apt-get autoremove -y
	@sudo apt-get autoclean -y

clean:
	@echo "Cleaning up..."
	@sudo apt-get autoremove -y
	@sudo apt-get autoclean -y
