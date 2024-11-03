# Django API Boilerplate

## Project Description

This boilerplate project provides a starting point for developing Django applications with the following features:
- Custom User Model (using email for authentication instead of username)
- Pre-configured for Docker support (includes both the Django server and PostgreSQL)
- Basic test setup

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To get started with this project, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/guitrading/DjangoCustomUserBoilerplate.git
    cd DjangoCustomUserBoilerplate
    ```

2. **Set up virtual environment and install dependencies:**

    ```bash
    python -m venv env
    source env/bin/activate # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set up and run the Docker containers:**

    Make sure you have Docker installed on your machine. Then, build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. **Apply migrations:**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## Usage

Once the installation is complete, you can access the development server at `http://localhost:8000`. The Django Admin interface will be available at `http://localhost:8000/admin`.

## Running Tests

To run tests, you can use the following command:

```bash
docker-compose exec web python manage.py test
```

This project includes a basic suite of tests located in the `user/tests` directory.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes.
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature-branch`
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please reach out to [gui.bertoni@gmail.com].