# Technical Documentation: Zero-Trust Identity Verification Suite

## 1. System Architecture
The application utilizes an **Asynchronous Event-Driven Micro-Engine (AEDM)**. This architecture ensures that computationally intensive tasks (like DeepFace neural inference) do not block the UI thread, providing a fluid user experience even during complex cryptographic operations.

## 2. Biometric Layer
- **Detection**: Uses OpenCV Haar Cascades or MTCNN for initial face localization.
- **Recognition**: Leverages `DeepFace` with the `VGG-Face` model to generate 4096-dimensional face vectors.
- **Comparison**: Uses Cosine Similarity to compare live frames against encrypted stored templates ($T \ge 0.95$).
- **Liveness**: Implemented via motion variance analysis to prevent spoofing with static photos.

## 3. Security & Cryptography
- **MFA**: Implements RFC 6238 Time-based One-Time Passwords (TOTP).
- **Vaulting**: Uses `cryptography.hazmat` to implement AES-256-GCM. This provide Authenticated Encryption, ensuring that any tampering with the credential database is detected immediately.
- **Key Derivation**: Uses PBKDF2 with SHA-256 and 100,000 iterations to derive storage keys from master passwords.

## 4. UI/UX Specifications
- **Frameless Engine**: A custom `QMainWindow` implementation that overrides mouse events for window dragging.
- **Glassmorphism**: Achieved using semi-transparent QFrame backgrounds and `QGraphicsBlurEffect` for backdrop filtering.
- **Cyber-Pulse**: A custom QWidget with `QPropertyAnimation` that modulates ring radius and opacity to simulate an active biometric scan.

## 5. Persistence
- **Encrypted Audit Trail**: All authentication events are logged to a local SQLite database.
- **Privacy**: No biometric data or PII ever leaves the local machine. The system is designed for 100% air-gapped operation.

---
**Developer**: HSINI MOHAMED
**Version**: 2.2.0
