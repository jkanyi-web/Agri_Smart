<a name="readme-top"></a>

<div align="center">

  <h3><b>Blog-App</b></h3>

</div>

# 📗 Table of Contents

- [📗 Table of Contents](#-table-of-contents)
- [📖 Blog Hub ](#-blog-hub-)
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

# 📖 Blog-App <a name="about-project"></a>

Blog app that is built with Ruby on Rails. It is a simple blog app that allows users to create posts and comment on them. It also allows users to like posts. It has a simple UI that allows users to navigate through the app easily. The users have profiles that they can edit and add a profile picture to along with their name and bio.

## 🛠 Built With <a name="built-with"></a>

### Tech Stack <a name="tech-stack"></a>

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://rubyonrails.org">Ruby on Rails</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://rubyonrails.org">Ruby on Rails</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.postgresql.org/">PostgreSQL</a></li>
  </ul>
</details>

### Key Features <a name="key-features"></a>

- Users can sign up.
- Users can create posts.
- Users can comment on posts.
- Users can like posts.
- Users can view posts.
- Users can view comments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💻 Getting Started <a name="getting-started"></a>

Clone this repository to your desired folder:

```
git clone git@github.com:jkanyi-web/Blog-App.git
```

### Prerequisites

In order to run this project you need:

- Python 3.12
- Browser (Google Chrome, Mozilla Firefox, Safari or any other browser)
- Django 5.0.2
- MySQL

### Setup

Clone this repository to your desired  folder:

```
git clone git@github.com:jkanyi-web/Agri_Smart.git

cd agri_smart
```

### Install

Install this project with:
pip install -r [requirements.txt](http://_vscodecontentref_/1)

### Usage

Use this project in the browsers of desktops and mobile devices


1. Configure the database in settings.py:

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

2. Run the following commands to create the database and run the migrations:
  
      python manage.py makemigrations
      python manage.py migrate

3. Create a superuser to access the admin panel:
  
        python manage.py createsuperuser

4. Run the development server:
    
          python manage.py runserver

5. Run Background tasks:
    
          python manage.py process_tasks

6. Open the browser and go to http://loca

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

Acknowledgements and suggestions for improvement are always welcome

- https://stackoverflow.com/questions/53510040/carrierwave-argument-error-nil-location-provided-cant-build-uri-for-an-image

<p align="right">(<a href="#readme-top">back to top</a>)</p>
