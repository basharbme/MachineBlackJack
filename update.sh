git reset --hard
git pull
BASE_DIR=$(dirname "$BASH_SOURCE")
chmod -R 777 /home/MachineBlackJack
setup_script="${BASE_DIR}/setup.sh"
source $setup_script