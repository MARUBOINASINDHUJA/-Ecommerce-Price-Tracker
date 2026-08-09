# 🛒 E-commerce Price Tracker (Amazon & Flipkart) 

This Django-based price tracker allows users to scrape and monitor product prices from major e-commerce platforms like **Amazon** and **Flipkart**. It fetches product details for a given keyword and exposes RESTful APIs to list, search, and track historical pricing data.

---

## 📌 Objective

Create a web-based system that:
- Scrapes product data from Amazon and Flipkart.
- Stores the data in a database.
- Exposes APIs to interact with the tracked products.

---

## 🧱 Project Structure

```
ECOMMERCE-PRICE-TRACKER/
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── db.sqlite3
├── price_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── tracker/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── scraper/
    │   ├── factory.py
    │   ├── amazon_scraper.py
    │   ├── flipkart_scraper.py
    ├── management/
    │   └── commands/
    │       └── scrape_products.py
```

---

## 🛠️ Features

### ✅ Core Functionality
- 🔎 Search and scrape product data by keyword (Amazon/Flipkart).
- 🧠 Factory Design Pattern to switch between scrapers.
- 📥 Store data in Django models with historical price tracking.
- 🔗 DRF APIs to:
  - List all tracked products.
  - Search products by title.
  - Get historical price data for a product.

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/yourusername/ECOMMERCE-PRICE-TRACKER.git
cd ECOMMERCE-PRICE-TRACKER
python -m venv venv
venv\Scripts\activate     # On Windows
# Or
source venv/bin/activate  # On Linux/macOS

pip install -r requirements.txt
```

### 🔑 Environment Setup

Create a `.env` file at the root with appropriate Django settings. Example:
```
DEBUG=True
SECRET_KEY=your-secret-key
```

### 🔨 Migrate DB

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Usage

### 📦 Scrape Product Data

To scrape products (e.g., smartphones from Flipkart):
```bash
python manage.py scrape_products --site flipkart --keyword smartphones --pages 3
```

Amazon example:
```bash
python manage.py scrape_products --site amazon --keyword laptops --pages 3
```

### 🔌 API Endpoints (via Django REST Framework)

| Endpoint                     | Method | Description                        |
|-----------------------------|--------|------------------------------------|
| `/api/products/`            | GET    | List all tracked products          |
| `/api/products/?search=tv` | GET    | Search products by keyword         |
| `/api/products/<id>/history/` | GET | Historical price data              |

---

## ✅ Testing

Run tests using Django's test framework:

```bash
python manage.py test
```

---

## 🧠 Tech Stack

- **Django**: Backend framework
- **Django REST Framework**: API layer
- **SQLite**: Default database (easily swappable)
- **BeautifulSoup & Requests**: Web scraping
- **Factory Pattern**: For switching scrapers based on site

---

## 🧾 Submission Notes

- All dependencies listed in `requirements.txt`.
- Code uses clear structure, error handling, and logging.
- Scraper supports multiple pages and adapts to layout changes.