# Cartify (Blinkit Clone) Premium

This is a fully containerized, premium MERN-style web application featuring a highly polished React UI, a powerful Flask (Python) backend, and a MySQL database orchestration—all seamlessly bundled with Docker.

## 🚀 Quick Setup (Docker)

To run the entire ecosystem locally without installing Node.js, Python, or MySQL natively, simply use the provided Docker Compose configuration:

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed and running on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop).

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gaurangp22/blinkit.git
   cd blinkit/project
   ```

2. **Start the application:**
   Launch the backend, frontend, and database simultaneously inside isolated containers:
   ```bash
   docker-compose up --build -d
   ```

3. **Access the application:**
   - **Storefront / User UI:** Open `http://localhost:4000`
   - The React frontend is production-built and optimized through Nginx, which proxies all API requests dynamically to the Flask backend.

## 🔧 Default Test Accounts
Docker automatically seeds the database with testing accounts on the first run.
- **Admin Account**: `admin@cartify.com` | Password: `admin123`
- **User Account**: `user@cartify.com` | Password: `user123`

## 🌟 Key Features
- **Premium Glassmorphic UI:** Smooth hover animations, highly refined custom forms, dynamic Apple-style category cards, and stunning cart mechanics.
- **Admin Dashboard:** Fully stylized administrative layout for category and product management.
- **Complete Authentication:** JWT-secured registration and login flows.
- **Automated Seeker Scripting:** The backend runs Python scripts internally to seed real, high-quality stock imagery and products.