# Loan Management API

This Flask application provides a RESTful API for managing loans. It allows creating, retrieving, updating, and deleting loan records, as well as calculating loan repayments.

## Features

- Create new loans
- Retrieve all loans or a single loan by ID
- Update existing loans
- Delete loans
- Calculate monthly and total repayments for a loan
- Update loan status

## Prerequisites

- Python 3.x
- Flask
- Flask-JWT-Extended
- SQLAlchemy (for database operations)
- Marshmallow (for object serialization/deserialization)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```
export FLASK_APP=application.py
export FLASK_DEBUG=1
flask run
```

### API Endpoints

- **Create a new loan**
  - `POST /loan`
  - Body: JSON object with loan details

- **Get all loans**
  - `GET /get_loans`

- **Get a single loan**
  - `GET /get_loan/<id>`

- **Update a loan**
  - `PUT /update_loan/<id>`
  - Body: JSON object with updated loan details

- **Delete a loan**
  - `DELETE /delete_loan/<id>`

- **Calculate loan repayment**
  - `GET /loan/<id>/calculate_repayment`

- **Update loan status**
  - `PUT /loan/<id>/status`
  - Body: JSON object with new loan status

## Authentication

This API intends to use JWT for authentication. Most endpoints are currently commented out with `@jwt_required()`, but you can uncomment these decorators to enable authentication after further updates to the system.

## Models

The main model used in this application is the `Loan` model, which includes fields for:

- Borrower name
- Loan amount
- Interest rate
- Loan term
- Loan status

## Helper Functions

The application includes helper functions for calculating monthly and total repayments.


## License

This project is licensed under the [MIT License](LICENSE).