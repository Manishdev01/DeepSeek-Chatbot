# 🚀 DeepSeek-R1-1.5B Deployment Guide

Powered by Ollama

## 📥 Installation Requirements

### Ollama Setup

| Platform | Command/Link |
|---|---|
| 🐧 Linux | `curl -fsSL https://ollama.com/install.sh | sh` |
| 🍎 macOS | [Download Installer](https://ollama.com/) |
| 🪟 Windows | [Download Installer](https://ollama.com/) |

## 🤖 Model Installation

Get the DeepSeek R1 model from:

🔗 [Ollama Model Library](https://ollama.com/library)

\`\`\`bash
ollama run deepseek-r1:[TAG]  # Replace [TAG] with model version
\`\`\`

## 🖥️ VPS Configuration Guide

### Model Selection Matrix

| VPS Tier | Specifications | Recommended Model |
|---|---|---|
| 🐇 Low-End | 2-4 vCPU, <8GB RAM | \`deepseek-r1:1.5b\` |
| 🦌 Medium | 4-8 vCPU, 8-16GB RAM | \`deepseek-r1:7b\` |
| 🐎 High-End | 8+ vCPU, 16+GB RAM | \`deepseek-r1:14b\` |

### 🔧 Network Configuration

#### API Endpoint Setup

\`VPS_IP:11438\`

#### Firewall Rules

\`\`\`bash
sudo ufw allow 11438/tcp
sudo ufw reload
\`\`\`

For alternative setups, consider [reverse proxy configuration](https://www.google.com/url?sa=E&source=gmail&q=https://nginx.org/en/docs/http/reverse_proxy.html) (example link to nginx reverse proxy documentation).

### 🚦 Service Management

\`\`\`bash
# Create systemd service
sudo systemctl enable ollama
sudo systemctl start ollama
\`\`\`

## 🎉 Ready to Deploy\!

Your personal DeepSeek-R1 instance is now accessible at:

\`http://[YOUR_VPS_IP]:11438/api/generate\`

## 📌 Pro Tip:

For production environments, consider:

* 🔐 SSL/TLS encryption
* 🔄 Load balancing
* 📊 Monitoring with \`ollama serve --verbose\`

\`\`\`diff
+ Successfully deployed!
- Remember to secure your endpoint!
\`\`\`
