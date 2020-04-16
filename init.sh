SCRIPT_PATH=$(pwd)
${SCRIPT_PATH}/init_submodule.sh python_utils git@github.com:ChenZaichuang/Python-Utils.git
pip install -r ${SCRIPT_PATH}/requirements.txt
find ${SCRIPT_PATH} -type d -empty -delete