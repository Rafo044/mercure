# Python Dunder Methods (Magic Methods) Project

This project demonstrates how Python's dunder ("magic") methods work by implementing them in small, real-world inspired applications. Each example showcases a specific method or group of methods and how they affect the behavior of Python objects.

## Project Structure

- `book_library.py`: Demonstrates `__init__` and `__str__` for object creation and readable output.
- `library_collection.py`: Uses `__len__` to count elements in a collection.
- `vector_math.py`: Uses `__getitem__` and `__setitem__` to allow indexing and assignment in custom objects.
- `point_addition.py`: Uses `__add__` to define custom addition behavior for points.
- `student_gradebook.py`: Shows how `__eq__` and `__lt__` work for comparing students.
- `backpack_contains.py`: Demonstrates `__contains__` for membership testing using `in`.
- `greeter_callable.py`: Uses `__call__` to allow objects to be used like functions.
- `employee_repr.py`: Demonstrates `__repr__` for debugging-friendly object representation.
- `file_handler_context.py`: Uses `__enter__` and `__exit__` for safe resource handling with context managers.
- `counter_iterator.py`: Shows `__iter__` and `__next__` for custom iterator objects.
- `temp_file_del.py`: Demonstrates `__del__` for cleanup logic on object deletion.

## License
This project is licensed under the MIT License. See `LICENSE` for more information.
