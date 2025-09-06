import streamlit as st
import numpy as np
from PIL import Image, PngImagePlugin
import io
import datetime
import torch
from diffusers import StableDiffusionImg2ImgPipeline

# --- UI ---
st.title('Creative Future Portrait (Diffusers版)')

uploaded_file = st.file_uploader('写真をアップロード (JPG/PNG, 5〜20MB)', type=['jpg', 'jpeg', 'png'])
if uploaded_file:
    image = Image.open(uploaded_file)
    # EXIF削除
    data = list(image.getdata())
    image_no_exif = Image.new(image.mode, image.size)
    image_no_exif.putdata(data)
    st.image(image_no_exif, caption='プレビュー', use_column_width=True)
else:
    st.info('画像をアップロードしてください。')

# 夢テキスト
prompt_text = st.text_input('将来の夢を入力 (50文字以内)', max_chars=50, placeholder='例: 宇宙飛行士')

# 年数指定
years = st.slider('未来年数 (+5〜+40年)', min_value=5, max_value=40, value=20)

# スタイル選択
style = st.selectbox('スタイル', ['やわらか写実', '写実', 'イラスト'], index=0)

# ウォーターマークON/OFF
wm_on = st.checkbox('ウォーターマークを付与', value=True)
# メタデータON/OFF
meta_on = st.checkbox('PNGメタデータを埋め込む', value=True)

# --- Diffusersモデルロード（SDXL Turbo例） ---
@st.cache_resource

def load_pipeline():
    model_id = 'stabilityai/sdxl-turbo'
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to('cuda' if torch.cuda.is_available() else 'cpu')
    return pipe

pipe = load_pipeline()

# --- 生成ボタン ---
if st.button('未来イメージを生成'):
    if not uploaded_file or not prompt_text:
        st.error('画像と夢テキストを入力してください。')
    else:
        # プロンプト合成
        negative_prompt = 'nsfw, violence, weapon, logo, smoking, drinking, deformation, celebrity, cartoon'
        full_prompt = f"{prompt_text}, {years} years later, {style} style, portrait, positive, safe, child-friendly"
        # PIL→np→生成
        img = image_no_exif.resize((1024,1024)).convert('RGB')
        np_img = np.array(img)
        # Diffusers生成
        result = pipe(
            prompt=full_prompt,
            image=img,
            strength=0.4,
            negative_prompt=negative_prompt,
            guidance_scale=1.0,
            num_inference_steps=20
        )
        out_img = result.images[0]
        # ウォーターマーク
        if wm_on:
            wm_text = f"Creative Future Portrait — {datetime.date.today()} (Not a real prediction)"
            wm = Image.new('RGBA', out_img.size, (0,0,0,0))
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(wm)
            # フォントはColab環境に合わせて調整
            font = ImageFont.load_default()
            text_size = draw.textsize(wm_text, font=font)
            plate = Image.new('RGBA', (text_size[0]+20, text_size[1]+10), (255,255,255,140))
            draw_plate = ImageDraw.Draw(plate)
            draw_plate.rounded_rectangle([(0,0),(text_size[0]+20,text_size[1]+10)], radius=10, fill=(255,255,255,140))
            plate_draw = ImageDraw.Draw(plate)
            plate_draw.text((10,5), wm_text, font=font, fill=(0,0,0,255))
            wm.paste(plate, (out_img.size[0]-text_size[0]-30, out_img.size[1]-text_size[1]-30), plate)
            out_img = Image.alpha_composite(out_img.convert('RGBA'), wm)
        # PNGメタデータ
        meta = PngImagePlugin.PngInfo()
        if meta_on:
            meta.add_text('X-Notice', 'This is a creative, AI-generated future portrait (not a prediction).')
            meta.add_text('X-Generated-At', datetime.datetime.now().isoformat())
            meta.add_text('X-Backend', 'diffusers')
            meta.add_text('X-Years', str(years))
            meta.add_text('X-Dream', prompt_text)
            meta.add_text('X-Style', style)
        # ダウンロード
        buf = io.BytesIO()
        out_img.save(buf, format='PNG', pnginfo=meta if meta_on else None)
        st.image(out_img, caption='生成結果', use_column_width=True)
        st.download_button('画像をダウンロード', data=buf.getvalue(), file_name='future_portrait.png', mime='image/png')
