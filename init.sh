git rm --cached python_utils
rm -r python_utils
git submodule add git@github.com:ChenZaichuang/Python-Utils.git python_utils
pip install -r python_utils/requirements.txt