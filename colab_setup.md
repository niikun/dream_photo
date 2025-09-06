# Google Colab用セットアップセル
!pip install streamlit ngrok diffusers torch transformers pillow numpy python-dotenv --quiet

# ngrokでStreamlitを外部公開する例
from pyngrok import ngrok
import os
os.system('streamlit run app.py &')
public_url = ngrok.connect(8501)
print('Streamlit URL:', public_url)

# 注意: Colabで実行する場合は、上記をノートブックの最初のセルに貼り付けてください。
