# NotifyPub

Required Environment Variables (compatible with .env)
- `HOST`
  - Base url of website
- `TITLE`
  - Title for website
- `ADMIN_PASSWORD`
  - Password for Admin to login to website
- `SECRET_KEY`
  - Randomly generated secret key for security
- `DATABASE`
  - Database connection url

```
# .env
HOST=notifypub.example.com
TITLE=NotifyPub

ADMIN_PASSWORD=password
SECRET_KEY=d5fb8c4fa8bd46638dadc4e751e0d68b
DATABASE=sqlite:////tmp/notifypub.sqlite
```

Copyright (c) Isaac Beverly 2022, AGPL-3.0-only