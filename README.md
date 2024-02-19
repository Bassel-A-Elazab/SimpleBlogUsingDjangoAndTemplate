
# Full-Featured Blog with Django and Bootstrap

## Introduction
This project is a full-fledged blog built using Django and Bootstrap, showcasing the practical application of knowledge in Django web development and front-end design. \
It aims to provide a fully-functional and aesthetically pleasing blog platform.

## Features
- **Stunning Design:** Enjoy a modern, responsive UI powered by Bootstrap. 
- **Bootstrap Styling:** Utilize Bootstrap to enhance the front-end design and user experience.
- **Django Web Framework:** Leverage the power of Django for robust backend development.
- **Full-Fledged Blog Functionality:** Implement essential features like creating, editing, and deleting blog posts, user authentication, and more. 

## Getting Started

To run this project locally, follow these steps:

#### 1. Clone the Repository:

```bash
git clone https://github.com/Bassel-A-Elazab/SimpleBlogUsingDjangoAndTemplate.git
```
```bash
cd SimpleBlogUsingDjangoAndTemplate
```

#### 2. Install Tools:

- Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) with [python3.8](https://www.python.org/downloads/release/python-380/) 
- Install [poetry](https://python-poetry.org/docs/#installation).
- Install [PostgreSQL 15](https://www.postgresql.org/about/news/postgresql-15-released-2526/)
  
#### 3. Set Up Environment Variables:
* Create a `.env` file in the project/ directory (see `.env.example`) and set the values accordingly.
#### 4. Install Dependencies and Run Server:

>Install dependencies:
```bash
poetry install
```

 >Run migrations:
```bash
poetry run python manage.py migrate
```
> Start the server:
```bash
poetry run python manage.py runserver
```

#### 5. Access the Application: 
&nbsp;&nbsp;  Visit http://localhost:8000 in your browser to access the blog application.
