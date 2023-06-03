# Overview

Welcome to my e-commerce website built using the Django framework. This website provides a complete online shopping experience for customers, including authentication, product browsing, shopping cart functionality, payment integration with PayPal, customer reviews, and a well-structured admin interface for backend management. Additionally, I have implemented a RESTful API to allow clients to retrieve product information and place orders securely with proper authentication and permissions.

# Project Structure

The project follows a standard Django project structure with the following notable components:

**authentication:** This app handles user authentication, including login, logout, and registration views. <br />
**products:** This app manages the product-related functionalities, including the "store" view for displaying all products with pagination, individual product views with customer reviews, and shopping cart functionality. <br />
**profiles:** This app handles the customer profile view, allowing registered customers to manage their personal information. <br />
**orders:** This app manages the order processing functionality, including the checkout process before payment and integration with the PayPal gateway. <br />
**shipping:** This app handles the shipping address management for each order. <br />
**reviews:** This app allows logged-in customers to review products they've purchased, and these reviews are displayed on the respective product pages. <br />
**admin:** Django's built-in admin interface is customized to provide a well-structured and user-friendly backend management system.

# Prerequisites

To run the project, ensure you have the following installed on your system:

Python (version 3.x)
Django (version 3.x)
Django REST Framework (version 3.x)
PayPal SDK (Python) for payment integration
Other dependencies listed in the requirements.txt file

# Installation and Setup

Follow these steps to run the project locally:

1. Clone the repository:
   ```
   git clone https://github.com/AAhadNur/DevExHub_assignment.git
   ```
2. Change into the project directory:
   ```
   cd DevExHub_assignment
   ```
3. Create a virtual environment:
   ```
   python -m venv myenv
   source myenv/bin/activate (For Unix/Mac)
   myenv\Scripts\activate  (For Windows)
   ```
4. Install the project dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up the database:
   ```
   python manage.py migrate
   ```
6. Create a superuser for the admin interface:
   ```
   python manage.py createsuperuser
   ```
7. Configure PayPal integration:
   - Obtain API credentials (sandbox or live) from your PayPal Developer Account.
   - Update the PayPal settings in the project's settings.py file with your API credentials.
8. Run the development server:
   ```
   python manage.py runserver
   ```
9. Access the website:
   Open a web browser and visit http://localhost:8000

# Usage

To browse products, go to the store page, which lists all available products with pagination functionality.
Click on a product to view its details, including customer reviews.
Login or register to access your customer profile, where you can update your details.
Add products to your shopping cart and proceed to checkout before making a payment.
The PayPal integration handles the payment process.
As an admin, you can access the admin interface by logging in with your superuser credentials. From there, you can manage products, customer profiles, orders, and reviews.

# Contributing

Thank you for your interest in contributing to this project. If you have any suggestions, bug reports, or feature requests, please open an issue on the project's GitHub repository.
