# Lunch APP #
A restaurant registers and uploads their menu for the day. Employees view the current day's menus and vote for their preferred menu. 
Once voting concludes, the results are computed. The restaurant with the most votes wins, but can't be the winner for 3 consecutive working days.
Employees can view the winning restaurant for the day.


## Installation Instructions (for linux) and Project Run Instructions

Run the commands in a terminal or command-prompt.

- Install `Python 3.7 or >3.7` for your operating system, if it does not already exist.

  - For [Mac](https://www.python.org/downloads/macos/)

  - For [Windows](https://www.python.org/downloads/windows/)

  - For Ubuntu/Debian

  ```bash
  sudo apt-get install python3.7
  ```

  Check if correct version of Python (3.7) is installed.

  ```bash
  python --version
  ```
  
* Clone the project from github on your local machine.   
    ```
    git clone https://github.com/anisrfd/lunch-app.git
    ```

* open the project directory.
    ```
    cd lunch-app/
    ```
* Get `virtualenv`.

    ```bash
    pip install virtualenv
    ``` 
* Create a virtual environment named `venv` using python`3.7` or > `3.7` and activate environment.  
    ```
    python3 -m venv venv
    ```
    ```
    source venv/bin/activate
    ```
* Upgrade pip if needed.  
    ```
    pip install --upgrade pip
    ```
* Install python dependencies from requirements.txt.
    ```
    pip install -r requirements.txt
    ```
    ```
* To run the project locally:
    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```
  
* To run the tests:
    ```
    python manage.py test tests.{TEST_FILE_NAME}
    ```
  For example run:
    ```
    python manage.py test tests.logout_api_tests
    ```

* Build the Docker image:
  First make sure the docker is installed in your machine and enable the docker (See [here](https://docs.docker.com/engine/install/)). Open a terminal, 
  navigate to your project's directory (where the Dockerfile is located), and run the following command to build the Docker image:

    ```
    docker build -t lunchapp-image .
    ```

* To check the logs go to the logs folder under the root project. The log file name would be 'api_logs.log'


## API Endpoints and Information

### Authentication

To access the API, you need to obtain an authentication token. You can do this by sending a POST request to the `api-token-auth/` endpoint with your username and password. Include the token in the `Authorization` header of your requests.

### Obtain Authentication Token

- **URL**: `/api-token-auth/`
- **Method**: POST
- **Parameters**:
  - `username` (string): Your username
  - `password` (string): Your password

### User Registration

Register a new user by providing a username and password.

- **URL**: `/register/`
- **Method**: POST
- **Parameters**:
  - `username` (string): User's username
  - `password` (string): User's password

### Create Restaurant

Create a new restaurant.

- **URL**: `/restaurant/create/`
- **Method**: POST
- **Authentication**: Token-based authentication required
- **Parameters** (JSON):
  - `name` (string): Restaurant name
  - Add any additional restaurant information as required by your application.

### Upload Menu for Restaurant

Upload a menu for a specific restaurant.

- **URL**: `/restaurant/<int:id>/menu/upload/`
- **Method**: POST
- **Authentication**: Token-based authentication required
- **Parameters**:
  - `id` (integer): ID of the restaurant to upload the menu for
  - Add the menu items as required by your application.

### Create Employee

Create a new employee.

- **URL**: `/employee/create/`
- **Method**: POST
- **Authentication**: Token-based authentication required
- **Parameters** (JSON):
  - `name` (string): Employee's name
  - Add any additional employee information as required by your application.

### Today's Menu

Retrieve today's menu.

- **URL**: `/menu/today/`
- **Method**: GET
- **Authentication**: Token-based authentication required
- **Response**: List of menu items for the current date.

### Vote for Menu

Vote for a specific menu item.

- **URL**: `/menu/<int:menu_id>/vote/`
- **Method**: POST
- **Authentication**: Token-based authentication required
- **Parameters**:
  - `menu_id` (integer): ID of the menu item to vote for

### Get Winning Restaurant

Retrieve the winning restaurant for the current date.

- **URL**: `/menu/results/`
- **Method**: GET
- **Authentication**: Token-based authentication required
- **Response**: The name of the winning restaurant.

#### Logout

Log out and invalidate the authentication token.

- **URL**: `/logout/`
- **Method**: POST
- **Authentication**: Token-based authentication required

### Example Usage

Here's an example of how to use the LunchApp API:

1. Obtain an authentication token by sending a POST request to `/api-token-auth/` with your username and password.

2. Use the obtained token in the `Authorization` header for subsequent requests to the protected endpoints.

3. Create restaurants, upload menus, create employees, and vote for menus using the provided endpoints.

4. Retrieve today's menu and view the winning restaurant.

5. Log out by sending a POST request to `/logout/`.
