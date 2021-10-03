git reset --hard
git pull
BASE_DIR=$(dirname "$BASH_SOURCE")
setup_script="${BASE_DIR}/setup.sh"
source $setup_script