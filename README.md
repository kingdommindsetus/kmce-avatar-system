# 🎬 KMCE Avatar System

> **Real-time AI Avatar Generation for Dental CE Courses**  
> Powered by Alibaba-Quark Live Avatar + OpenAI + Google Cloud

## ⚡ Quick Start

```bash
# 1. Setup (5 minutes)
setup_liveavatar.bat

# 2. Activate environment
liveavatar_env\Scripts\activate.bat

# 3. Generate avatars
python -m gradio liveavatar/gradio_single_gpu.py

# 4. Open: http://localhost:7860
```

## 📊 What's Included

- 🎭 **13 Agent Avatars** - Simon, Naomi, Aria, Mark, Rio, Lila, Tube, Lucy, Snake, Adam, Evan, Jordan, Booker
- 🔊 **OpenAI TTS Integration** - Natural voices for each agent
- 🎬 **45 FPS Real-time Video** - Professional quality
- 💰 **92% Cheaper than HeyGen** - $800/month vs $10k/month
- 🌍 **Multi-language Support** - Generate in any language
- 📈 **White-Label Resale** - Sell to other dental CE providers

## 🚀 Key Features

| Feature | Value |
|---|---|
| **FPS** | 45 FPS real-time |
| **Latency** | 1.2 sec to first frame |
| **Video Length** | Unlimited (infinite generation) |
| **GPU Requirements** | 80GB (multi-GPU) or 48GB (FP8) |
| **Cost** | <$0.10 per video |

## 📖 Documentation

- **[QUICK_START.md](./QUICK_START.md)** - 5-minute setup guide
- **[KMCE_Avatar_Build_Plan.md](./KMCE_Avatar_Build_Plan.md)** - Full implementation (4-6 weeks)
- **[.env.example](./.env.example)** - Configuration template

## 💻 Installation

### Windows (Auto)
```bash
setup_liveavatar.bat
```

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File setup_liveavatar.ps1
```

### Manual
```bash
python -m venv liveavatar_env
liveavatar_env\Scripts\activate.bat
pip install -r requirements.txt
huggingface-hub download Quark-Vision/Live-Avatar --local-dir ./ckpt/Live-Avatar
huggingface-hub download Wan-AI/Wan2.2-S2V-14B --local-dir ./ckpt/Wan2.2-S2V-14B
```

## 🎯 Use Cases

1. **CE Courses** - Generate instructor-led videos for dental education
2. **Marketing** - Create personalized promotional videos
3. **Sales** - Agent-led product demonstrations
4. **Support** - AI-powered customer education

## 🔌 Integration

### With OpenAI TTS
```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Welcome to dental sleep medicine!"
)
```

### With Shopify
```html
<video src="/api/avatar/simon_intro.mp4" controls></video>
```

### With KMCE App
```tsx
<AvatarPlayer agentId="simon" courseId="AGD-DSM" />
```

## 💰 ROI

| Model | Monthly Cost | Cost/Video |
|---|---|---|
| **HeyGen** | $10,000 | $10 |
| **KMCE Self-Hosted** | $800 | $0.80 |
| **Savings** | **$9,200** | **92% cheaper** |

## 📈 Timeline

- **Week 1-2:** Local setup + testing
- **Week 2-3:** API integration + OpenAI TTS
- **Week 3-4:** 13 agent avatars created
- **Week 4-6:** Production deployment + white-label

## 🐛 Troubleshooting

### CUDA Not Available
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

### Out of Memory
Set `ENABLE_FP8=true` in `.env`

### Models Missing
```bash
cd ckpt
huggingface-hub download Quark-Vision/Live-Avatar --local-dir .
```

## 📚 Resources

- **GitHub:** https://github.com/Alibaba-Quark/LiveAvatar
- **Models:** https://huggingface.co/Quark-Vision/Live-Avatar
- **Paper:** https://arxiv.org/abs/2512.04677
- **OpenAI:** https://platform.openai.com/docs

## 📝 License

Apache License 2.0 - See [LICENSE](./LICENSE)

Uses:
- Alibaba-Quark Live Avatar (Apache 2.0)
- WanS2V base model (Apache 2.0)
- PyTorch (BSD)
- OpenAI API (Commercial)

## 🤝 Support

- **Issues:** GitHub Issues
- **Questions:** Discussions
- **Email:** kingdom.kmdsm@gmail.com

## 🎉 Get Started

```bash
git clone https://github.com/kingdommindsetus/kmce-avatar-system.git
cd kmce-avatar-system
./setup_liveavatar.bat
```

**Made with ❤️ for Kingdom Mindset CE**

*Educate • Equip • Empower with AI Avatars*

---

*Last Updated: October 2, 2026*
