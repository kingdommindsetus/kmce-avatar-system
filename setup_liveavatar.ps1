Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv liveavatar_env
& ".\liveavatar_env\Scripts\Activate.ps1"

Write-Host "Installing PyTorch..." -ForegroundColor Yellow
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

Write-Host "Installing Flash Attention..." -ForegroundColor Yellow
pip install flash-attn==2.7.1.post2 --no-build-isolation

Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Downloading models..." -ForegroundColor Yellow
pip install huggingface-hub
huggingface-hub download Quark-Vision/Live-Avatar --local-dir "ckpt\Live-Avatar"
huggingface-hub download Wan-AI/Wan2.2-S2V-14B --local-dir "ckpt\Wan2.2-S2V-14B"

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "Next: .\liveavatar_env\Scripts\Activate.ps1"
Write-Host "Then:  python -m gradio liveavatar/gradio_single_gpu.py"
