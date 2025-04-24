
pip download \
  --only-binary=:all: \
  --platform win_amd64 \
  --python-version 3.12 \
  --implementation cp \
  --abi cp312 \
  --no-deps \
  tokenizers==0.13.3


wget https://files.pythonhosted.org/packages/27/fe/4916ec8f2fc6a7a6dfaa2dd21622e969e813429deff546a09b17b121dee9/tokenizers-0.13.3-cp312-cp312-win_amd64.whl
