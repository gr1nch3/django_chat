# Chat (Django)

A Django chat application (without `Django_channels`) forked from **@gr1nch3**'s [django_chat](https://github.com/gr1nch3/django_chat).

### Current Django Version in use: 4.2 (LTS)

### # System Requirements

* `Git`
* `Python >= 3.8`

### # Installation

1. Clone the repository

```bash
# [URL] https://github.com/christian80gabi/chat_django.git
-> git clone [URL] 
```

2. create a virtual environnement inside the root directory

```bash
-> cd chat_django
-> python3 -m venv ./.venv
-> source .venv/bin/activate # macos/linux
```

3. Install Django and Tailwind

```bash
-> pip install Django crispy-tailwind
```

5. Install node modules 

```bash
-> cd theme
-> npm install
```

4. Run migrations

```
-> python manage.py makemigrations
-> python manage.py migrate
```

5. Run/Debug

```bash
-> python manage.py runserver
```

Christian Gabi ( [@christian80gabi](https://github.com/christian80gabi) )
