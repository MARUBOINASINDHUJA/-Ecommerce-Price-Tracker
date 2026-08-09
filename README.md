
# 🛒 E-Commerce Price Tracker

A Django-based web application that helps users track product prices from e-commerce websites and monitor whether products reach their desired target price.

## 📌 Project Overview

The E-Commerce Price Tracker allows users to enter a product URL and a target price. The application retrieves product information and price data, stores price history, and provides a dashboard for monitoring tracked products.

The project was originally inspired by an existing open-source GitHub project. I customized and extended the project by modifying the backend functionality and creating a user-friendly frontend/dashboard.

## ✨ Features

- 🔐 User registration and login
- 🛒 Add products using product URLs
- 🎯 Set a target price
- 💰 Track current product prices
- 📊 Maintain product price history
- 📈 Display price history using charts
- 🔔 Target-price notification functionality
- 📧 Email notification support
- 🖥️ User-friendly dashboard
- 🗑️ Manage tracked products

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend
- Python
- Django

### Database
- SQLite for local development

### Libraries / Tools
- Requests
- BeautifulSoup
- Git
- GitHub

## 🏗️ Project Structure

```text
Ecommerce-Price-Tracker/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── price_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── tracker/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── scraper/
│   ├── templates/
│   ├── static/
│   └── management/
│
└── ...
