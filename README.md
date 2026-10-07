# 🇮🇳 GARBA CONNECT

Garba Connect is a modern, responsive web platform designed to help people across India find a compatible Navratri/Garba partner in their city.

This repository contains the full-stack Django application as conceptualized.

## Tech Stack
*   **Backend Framework:** Django 6.x
*   **API Framework:** Django REST Framework (DRF)
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
*   **Database:** SQLite (development), PostgreSQL ready (production)
*   **Authentication:** Custom Email/Phone auth + JWT
*   **Environment Variables:** python-dotenv

## Features Currently Bootstrapped
*   ✅ **Django Core Configuration:** Complete `settings.py` wired securely.
*   ✅ **Accounts Module:** Custom `User` model, `UserProfile`, `IdentityVerification`, and `City`.
*   ✅ **Matching Module:** `ConnectionRequest`, `Match`, `GarbaPlan`.
*   ✅ **Chat Module:** `Conversation` and `Message`.
*   ✅ **Events Module:** `GarbaEvent`.
*   ✅ **Django Admin Console:** Fully integrated for moderation and dashboarding.
*   ✅ **Landing Page:** Beautiful, modern, dark-themed responsive UI for finding partners.

## Installation & Setup

1. **Clone the project & CD into the directory:**
   ```bash
   cd garba_project
   ```

2. **Activate the Virtual Environment:**
   ```powershell
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations (Already completed in dev):**
   ```bash
   python manage.py migrate
   ```

5. **Start Development Server:**
   ```bash
   python manage.py runserver
   ```

## Development Milestones to Finish
To fully complete the remaining phases of the project:
1. **Views & APIs:** Implement the DRF views for OTP generation, profile uploading, matching algorithms, and city-based search.
2. **WebSockets (Channels):** Integrate `channels` and `redis` for real-time 1-on-1 chatting.
3. **Frontend Templates:** Create the internal Dashboard, User Discovery Feed, and Chat UI using the `base.html` structure.

**Important Note for Privacy:**
Please ensure that Identity Verification views are secured with object-level permissions so that Aadhaar/Gov ID information is strictly visible to SuperAdmins only.
