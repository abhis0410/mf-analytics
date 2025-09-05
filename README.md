# 📊 mf-analytics  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red?logo=streamlit)](https://streamlit.io/)  
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Storage-blue?logo=googlecloud&logoColor=white)](https://cloud.google.com/storage)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  

A simple **Mutual Fund Analytics** tool built with **Streamlit** and **Google Cloud Storage (GCS)**.  
It helps you analyze, visualize, and manage your mutual fund investments in an interactive dashboard.  

---

## ✨ Features
- 📈 Track mutual fund NAVs and investment performance  
- 📂 Store and fetch data securely from **Google Cloud Storage**  
- ⚡ Deploy seamlessly on **Streamlit Cloud**  
- 🔑 Secure authentication using **Google Service Accounts**  

---

## 🚀 Getting Started

### 1. Fork or Clone
Fork this repository or clone it to your local machine:
```bash
git clone https://github.com/your-username/mf-analytics.git
```

## 2. Add Configuration

This project uses **Streamlit secrets** for secure configuration.

```bash
# 1. In your local environment, create a file:
.streamlit/secrets.toml
```

# 2. Add your service account credentials:
[gcs]
service_account_json = """{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "",
  "universe_domain": "googleapis.com"
}"""

> ⚠️ **NOTE:**  
> - Make sure to follow the **exact JSON pattern** shown above.  
> - **Do not push** your `secrets.toml` file to GitHub (it contains sensitive credentials).  


# 3. When deploying on Streamlit Cloud:
App → Settings → Secrets
Paste the same configuration there
