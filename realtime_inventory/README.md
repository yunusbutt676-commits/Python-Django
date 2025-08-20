# Inventory Dashboard (Django + Tailwind + Chart.js)

## Overview
A real-time inventory and sales dashboard built with Django, Tailwind CSS, and Chart.js.  
Tracks orders, stock levels, and top-selling products.

## Features
- **Product Management**: CRUD for products with stock tracking.  
- **Customer Management**: Add and manage customers.  
- **Order Management**: Add orders with multiple items.  
- **Automatic Stock Updates**: Stock decreases on order creation and validates availability.  
- **Real-time Charts**:
  - Sales over the last 10 orders.
  - Top products by quantity (including unsold products).  
- **Admin Friendly**: Inline order items, auto-calculated order totals, and friendly error messages.

## Tech Stack
- **Backend**: Django 4.1, Python 3.12  
- **Frontend**: Tailwind CSS, Chart.js  
- **Database**: SQLite/MySQL (configurable)  
- **Real-time Updates**: Optional WebSocket support  

## Installation
1. Clone the repository:  
   ```bash
   git clone <repo_url>
   cd realtime_inventory
