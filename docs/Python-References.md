# Python Learning References

Use these references in order while building features in this project.

## 1. Python Fundamentals

Start with the [Python Tutorial](https://docs.python.org/3/tutorial/index.html), especially:

- [Control flow and functions](https://docs.python.org/3/tutorial/controlflow.html)
- [Data structures](https://docs.python.org/3/tutorial/datastructures.html)

## 2. Modules and Environments

- [Modules and Packages](https://docs.python.org/3/tutorial/modules.html) explains imports and organizing code across files.
- [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) introduces `venv` and `pip`.
- The [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) provides practical environment setup instructions, including for Windows.

## 3. Types and Data Modeling

- FastAPI's [Python Types introduction](https://fastapi.tiangolo.com/python-types/) gives a practical overview of annotations.
- Python's [typing reference](https://docs.python.org/3/library/typing.html) documents type hints.
- Python's [dataclasses reference](https://docs.python.org/3/library/dataclasses.html) covers data-focused classes.
- FastAPI's [request body and model tutorial](https://fastapi.tiangolo.com/tutorial/body/) introduces request validation and models.

## 4. Errors and Testing

- Read Python's [Errors and Exceptions tutorial](https://docs.python.org/3/tutorial/errors.html) to learn how to raise and handle errors.
- Follow pytest's [Get Started guide](https://docs.pytest.org/en/stable/getting-started.html) to write and run tests.
- Practice writing a test for expected behavior before implementing that behavior.

## 5. Web APIs

- Follow the [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) from the beginning to learn routes, request data, responses, and validation.
- Read FastAPI's [async and await guide](https://fastapi.tiangolo.com/async/) when you reach asynchronous code.

## 6. Project Design

- Read this repository's [Clean Architecture guide](clean-architecture.md) for the intended layer responsibilities and dependency direction.
- FastAPI's [Dependencies guide](https://fastapi.tiangolo.com/tutorial/dependencies/) demonstrates dependency injection.
- FastAPI's [Bigger Applications guide](https://fastapi.tiangolo.com/tutorial/bigger-applications/) shows how to organize a larger application across files.

## Suggested First Pass

Work through topics 1 through 4 first. Then build a small API endpoint while studying topics 5 and 6.