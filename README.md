# elis_openai_plus
ChatGPT bot https://youtu.be/eSxNF9hsS1o

virtualenv venv
source venv/bin/activate

export PYTHONPATH="/home/pavel/github/Yandex_stt"
export PYTHONPATH="/home/pavel/github/Yandex_stt/venv/lib/python3.10/site-packages"

#pip install speechkit
pip install openai
pip install aiogram
pip install pyyaml
pip install pandas
pip install grpcio-tools
pip install pydub
pip install yandex-speechkit


help - Help Instruction.
dialog - Прямой диалог c ChatGPT.
correction - Коррекция текста. Исправление ошибок распознавания.
affect - Коррекция текста в ласковом тоне, чтобы было приятно читать.
medical - Коррекция текста по медицинской терминологии.

export IAM_TOKEN=`yc iam create-token`
curl -H "Authorization: Bearer ${IAM_TOKEN}"   https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds

export FOLDER_ID="b1g3ku6t41pjb00bids8"

