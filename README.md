# # Project: payment_app

A simple online store with connected Stripe API payment system.


<details><summary>Test task (RUS):</summary>

Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
- [x]	Django Модель Item с полями (name, description, price) 

- [x]	API с двумя методами:
    - [x]	GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
    - [x]	GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
 - [x]	Залить решение на Github, описать запуск в Readme.md
 - [x]	Опубликовать свое решение чтобы его можно было быстро и легко протестировать.

Бонусные задачи: 
 - [x]	Запуск используя Docker
 - [x]	Использование environment variables
 - [x]	Просмотр Django Моделей в Django Admin панели
 - [ ]	Запуск приложения на удаленном сервере, доступном для тестирования
 - [x] - Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
 - [x] - Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. ---  # для привязки скидки к заказу используются промокоды. Пользователь вводит промокод, если такой есть в БД -> заказ получает скидку. / Налоги прикреплены к категории товара, в зависимости от категории назначается налог, также к каждому заказу при создании добавляется "налог платежной системы" (далее можно придумать другую логику для добавления налогов). 
 - [x]	Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте. --- # Создано 2 компании в рамках аккаунта и в зависимости от валюты выбирается оплата на нужный аккаунт. Также при оплате пользователь выбирает в какой валюте платить - исходя из этого добавлена модель Exchange - для конвертации валюты в случаях если в корзину добавлены товары в разных валютах.
 - [x]	Реализовать не Stripe Session, а Stripe Payment Intent. --- после подтверждения заказа пользователю предлагается оплатить или через Stripe Session, или Stripe Payment Intent.
 ###### # TODO 1. Stripe webhooks
 ###### # TODO 2. Github actions


</details>

___


## Contents:

- [Technologies](#technologies)
- [Description](#description)
- [Installation and starting](#installation-and-starting)
- [Authors](#authors)

---

## Technologies


**Programming languages and modules:**

[![Python](https://img.shields.io/badge/-python_3.11^-464646?logo=python)](https://www.python.org/)
[![os](https://img.shields.io/badge/-os-464646?logo=python)](https://docs.python.org/3/library/os.html)
[![dataclasses](https://img.shields.io/badge/-dataclasses-464646?logo=python)](https://docs.python.org/3/library/dataclasses.html)
[![uuid](https://img.shields.io/badge/-uuid-464646?logo=python)](https://docs.python.org/3/library/uuid.html)
[![sys](https://img.shields.io/badge/-sys-464646?logo=python)](https://docs.python.org/3/library/sys.html)
[![dacite](https://img.shields.io/badge/-dacite-464646?logo=python)](https://pypi.org/project/dacite/)
[![pillow](https://img.shields.io/badge/-pillow-464646?logo=python)](https://python-pillow.org/)
[![python-dotenv](https://img.shields.io/badge/-python_dotenv-464646?logo=python)](https://pypi.org/project/python-dotenv/)
[![stripe](https://img.shields.io/badge/-stripe-464646?logo=python)](https://pypi.org/project/stripe/)


**Frameworks:**

[![Django](https://img.shields.io/badge/-Django-464646?logo=Django)](https://www.djangoproject.com/)

**Databases:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)


**Containerization:**

[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)

[⬆️Contents](#contents)

---
## Description:

***Payment_app is a simple online store with connected Stripe API payment system..***

The main page of the store displays all products available in the Database.

If the database is empty - products can be added in the "Add product" tab.

Extended product info is displayed on the product page "/item/{item_id}."

You can buy an item by clicking the "buy now" button. Or you can add an item to your cart and buy all the items in your cart in one order.

After clicking the "buy now" button from the product card (or checkout from the cart), the user is redirected to the order confirmation form.

In the order confirmation form, the user must be sure to add an email. It is also possible to add a promo code (enter a value) and if there is such a promo code in the database - the corresponding discount will be applied to the order.

The default list of discounts is available on the "Available discounts" tab. New discounts can be added from the admin panel.

Taxes are attached to the product category, depending on the category the tax is assigned, also "Sales stripe tax" is added to each order at creation (further we can think of other logic for adding taxes).

Stripe Session API is used as a payment acceptance system.


 ###### # TODO 1. Stripe webhooks

<h1></h1>

[⬆️Contents](#contents)

---

## Installation and starting

<details><summary>Pre-conditions</summary>

It is assumed that the user has installed [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on the local machine or on the server where the project will run. You can check if they are installed using the command:

```bash
docker --version && docker-compose --version
```

***It is assumed that the user has [Stripe](https://stripe.com) account!***
</details>


Local launch:

1. Clone the repository from GitHub and enter the data for the environment variables in the [.env] file:
```bash
git clone https://github.com/Kosalexx/payment_app.git
```
<details><summary>Local launch: Django/PostgreSQL</summary><br>

***!!! It is assumed that the user has installed [PostgreSQL](https://www.postgresql.org/) and [poetry](https://python-poetry.org/) !!!***

1.1* Create a new PostgreSQL database and pass the credentials to the [.env] file as specified in the [.env.template] file.

2. All required dependencies described in **pyproject.toml** file. To install all required libraries and packages, run the command:
```bash
poetry install
```

3. Run the migrations, create a superuser, and launch the application:
```bash
python src/payment_app/manage.py makemigrations && \
python src/payment_app/manage.py migrate && \
python src/payment_app/manage.py createsuperuser --noinput && \
python tree_menu/manage.py runserver
```
The project will run locally at `http://127.0.0.1:8000/`

</details>

<details><summary>Local launch: Docker Compose/PostgreSQL</summary>

2. From the root directory of the project, execute the command:

```bash
docker-compose -f docker-compose.yml up -d --build
```

!On the first run, the application container may not go up right away because the database container is not yet ready for use. In this case, repeat the command:

```bash
docker-compose -f docker-compose.yml up -d --build
```

The project will be hosted in two docker containers (db, app) at `http://localhost:8000/`.

To create super user run comand

```bash
docker exec payment_app-app-1 python ./src/payment_app/manage.py createsuperuser --noinput
```

3. You can stop docker and delete containers with the command from the root directory of the project:
```bash
docker-compose -f docker-compose.yml down
```
add flag -v to delete volumes ```docker-compose -f docker-compose.yml down -v```
</details><h1></h1>

[⬆️Contents](#contents)

---

## Authors:

[Aliaksei Kastsiuchonak](https://github.com/Kosalexx)<br>
<h1></h1>

[⬆️ Back to top](#project-payment_app)