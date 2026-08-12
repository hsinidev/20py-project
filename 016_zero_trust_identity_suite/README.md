# Zero-Trust Identity Verification Suite (Enterprise Edition)

![Cover](asset/cover.png)

## 🛡️ Overview
The **Zero-Trust Identity Verification Suite** is a high-security authentication gateway developed by **HSINI MOHAMED**. It implements the "Success-Trinity" model: Biometric Facial Matching, Multi-Factor Authentication (TOTP), and Hardware-bound Key Verification.

## 🚀 Key Features
- **AEDM Architecture**: Asynchronous Event-Driven Micro-Engine for high-performance security gates.
- **Neural Biometrics**: AI-powered facial recognition with liveness detection via OpenCV/DeepFace.
- **Trinity Auth Logic**: Triple-gate security (Face + TOTP + AES-Vault).
- **Identity Vault UI**: High-fidelity glassmorphism with Cyber-Pulse animations and blurred backdrops.
- **Encrypted Audit Trail**: Immutable, AES-256 encrypted logs of all access attempts for GRC compliance.
- **Frameless Tactical GUI**: Modern, draggable interface with sleek QSS skinning.

## 🛠️ Tech Stack
- **UI**: PyQt6, QSS, QPropertyAnimation
- **Biometrics**: OpenCV, DeepFace (VGG-Face)
- **Security**: PyOTP (RFC 6238), PyCryptodome (AES-256-GCM)
- **Database**: SQLite3 (Encrypted)

## 📥 Installation
```bash
pip install -r requirements.txt
python main.py
```

## 📜 License
Professional-grade security infrastructure.
**Credit**: Developed by HSINI MOHAMED.
