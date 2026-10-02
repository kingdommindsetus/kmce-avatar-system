@echo off
echo Creating Python virtual environment...
python -m venv liveavatar_env
call liveavatar_env\Scripts\activate.bat

echo Installing PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

echo Installing Flash Attention...
pip install flash-attn==2.7.1.post2 --no-build-isolation

echo Installing requirements...
pip install -r requirements.txt

echo Downloading models...
pip install huggingface-hub
huggingface-hub download Quark-Vision/Live-Avatar --local-dir .\ckpt\Live-Avatar
huggingface-hub download Wan-AI/Wan2.2-S2V-14B --local-dir .\ckpt\Wan2.2-S2V-14B

echo.
echo ✅ Setup complete!
echo.
echo Next: liveavatar_env\Scripts\activate.bat
echo Then:  python -m gradio liveavatar/gradio_single_gpu.py
echo.
pause
