<a name="readme-top"></a>

<div align="center">

  <h3><b>Agri_Smart</b></h3>

</div>

# 📗 Table of Contents

- [📗 Table of Contents](#-table-of-contents)
- [📖 Agri_Smart ](#-agri_smart-)
  - [🛠 Built With ](#-built-with-)
    - [Tech Stack ](#tech-stack-)
    - [Key Features ](#key-features-)
  - [💻 Getting Started ](#-getting-started-)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Install](#install)
    - [Usage](#usage)
    - [Run tests](#run-tests)
  - [👥 Author ](#-author-)
  - [🔭 Future Features ](#-future-features-)
  - [🤝 Contributing ](#-contributing-)
  - [⭐️ Show your support ](#️-show-your-support-)
  - [🙏 Acknowledgments ](#-acknowledgments-)
  - [📝 License ](#-license-)

<!-- PROJECT DESCRIPTION -->

# 📖 Agri_Smart <a name="about-project"></a>

Agri_Smart is a comprehensive platform designed to assist farmers with various agricultural activities. It includes features such as crop management, marketplace transactions, weather updates, and MPesa payment integration. The platform aims to streamline agricultural processes and provide valuable insights to farmers.

## 🛠 Built With <a name="built-with"></a>

### Tech Stack <a name="tech-stack"></a>

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://www.djangoproject.com/">Django</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://www.djangoproject.com/">Django</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.mysql.com/">MySQL</a></li>
  </ul>
</details>

### Key Features <a name="key-features"></a>

- Users can sign up and manage their profiles.
- Users can add, edit, and delete crops.
- Users can list crops for sale in the marketplace.
- Users can initiate MPesa payments for marketplace transactions.
- Users can view weather updates.
- Users can participate in forums by creating posts and comments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💻 Getting Started <a name="getting-started"></a>

Clone this repository to your desired folder:
git clone git@github.com:jkanyi-web/Agri_Smart.git


### Prerequisites

In order to run this project you need:

- Python 3.12
- Browser (Google Chrome, Mozilla Firefox, Safari or any other browser)
- Django 5.0.2
- MySQL

### Setup

Clone this repository to your desired folder:

git clone git@github.com:jkanyi-web/Agri_Smart.git

cd agri_smart

### Install

Install this project with:

pip install -r requirements.txt


### Usage

Use this project in the browsers of desktops and mobile devices.

1. Configure the database in `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'agri_smart_db',
            'USER': 'your-db-user',
            'PASSWORD': 'your-db-password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

2. Run the following commands to create the database and run the migrations:
  
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Create a superuser to access the admin panel:
  
    ```sh
    python manage.py createsuperuser
    ```

4. Run the development server:
    
    ```sh
    python manage.py runserver
    ```

5. Run Background tasks:
    
    ```sh
    python manage.py process_tasks
    ```

6. Open the browser and go to `http://localhost:8000`

## 👥 Author <a name="authors"></a>

👤 **Victor Kanyi**

- GitHub: [@jkanyi-web](https://github.com/jkanyi-web)
- Twitter: [@V_Kanyi](https://twitter.com/V_Kanyi)
- LinkedIn: [LinkedIn](https://linkedin.com/in/victor-kanyi)

## 🔭 Future Features <a name="future-features"></a>

- Add more payment options
- Enhance weather data visualization
- Implement user notifications
- Add more user profile customization options

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing <a name="contributing"></a>

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/jkanyi-web/Agri_Smart/issues).

## ⭐️ Show your support <a name="support"></a>

If you like this project, please let me know and we can improve it further. You are welcome to support this project by giving suggestions for improvement.

## 🙏 Acknowledgments <a name="acknowledgements"></a>

Acknowledgements and suggestions for improvement are always welcome.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
