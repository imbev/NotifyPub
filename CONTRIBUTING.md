## Contributing

### Setting up the development environment

Required:

- Docker
- PyCharm / VS Code

Instructions:

- Open the project and create a devcontainer
- Add a new Python interpreter using Poetry
- Start Postgres instance using `service postgresql start`
  - If there is an error concerning a missing database, run `su -c /usr/bin/psql postgres` then enter the following in the psql shell:
  ```psql
  create database notifypub;
  \password postgres;
  ```
  Set a new password and enter `\q` to exit psql
- From the `Notifypub/notifypub` directory, run `python manage.py runserver`


### Conduct

See `CODE_OF_CONDUCT.md`