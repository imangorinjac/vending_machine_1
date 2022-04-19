
# Vending machine using Python(Flask)



## Task
Language: 

- Python

Libraries: 

- any you see fit

What to use?

- Flask framework + any rest api library you see fit
- Database: postgres or mysql
- SQL Alchemy for ORM
- Alembic for database migrations
- JWT token for authentication

Requirements: Create only APIs, no visual user interface is required

Brief:

Design an API for a vending machine, allowing users with a “seller” role to add, update or remove products, while users with a “buyer” role can deposit coins into the machine and make purchases. Your vending machine should only accept 5, 10, 20, 50 and 100 cent coins.

Tasks:

REST API should be implemented consuming and producing “application/json”

Implement product model with amountAvailable, cost, productName and sellerId fields

Implement user model with username, password, deposit and role fields

Implement CRUD for users (POST shouldn’t require authentication)

Implement CRUD for a product model (GET can be called by anyone, while POST, PUT and DELETE can be called only by the seller user who created the product)

Implement /deposit endpoint so users with a  “buyer” role can deposit 5, 10, 20, 50 and 100 cent coins into their vending machine account

Implement /buy endpoint (accepts productId, amount of products) so users with a “buyer” role can buy products with the money they’ve deposited. API should return total they’ve spent, products they’ve purchased and their change if there’s any (in 5, 10, 20, 50 and 100 cent coins)

Implement /reset endpoint so users with a “buyer” role can reset their deposit

Take time to think about possible edge cases and access issues that should be solved

Tips:

- make sure that all endpoints return correct status codes on each response
- create additional endpoints as needed to fulfil requirements of the task (login, registration, etc.)

Evaluation criteria:

- Python best practices
- Edge cases covered
- Authentication
- Authorization
## Setup:
You first have to activate virtual environment.

For MAC users:
$ mkdir myproject

$ cd myproject

$ python3 -m venv venv

And after that write next line:

$ . venv/bin/activate

For Windows users:
> mkdir myproject

> cd myproject

> py -3 -m venv venv

And after that write nex line:
> venv\Scripts\activate

You are now enabled to use this code in your editor.

