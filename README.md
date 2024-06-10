# SIGMA-QUIZ Application

## Overview

SIGMA-QUIZ is a web-based application designed to create, manage, and take quizzes. Built with Django and Django Rest Framework (DRF), it offers a robust and scalable solution for educational purposes, enabling users to test their knowledge across various subjects.

## Features

- **User Authentication**: Secure user registration and login.
- **Quiz Management**: Admin users can create, update, and delete quizzes.
- **Question Management**: Admin users can add, update, and delete questions within quizzes.
- **Quiz Taking**: Users can take quizzes and receive instant feedback.
- **Score Tracking**: Users can view their quiz scores and history.
- **RESTful API**: Provides endpoints for all the main functionalities of the app.

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+

### Steps

1. **Clone the Repository**
   ```sh
   git clone https://github.com/SkillsForge-Community/Sigma-Quiz-Backend.git
   cd Sigma-Quiz-Backend
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README provides a comprehensive guide for setting up and using the SIGMA-QUIZ application. For any issues or feature requests, please open an issue on the GitHub repository.