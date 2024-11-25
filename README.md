# **GymCrowd**

## **Overview**

GymCrowd is a gym management and workout tracking platform tailored for fitness enthusiasts. The platform enables users to log workouts, set gym crowd level preferences, and receive notifications about gym activities. With robust user authentication and real-time updates, GymCrowd ensures a personalized and secure fitness experience.

## **Features**
- **User Authentication**: Secure user sign-up, login, token-based authentication, and logout functionality.
- **Workout Tracking**: Log workouts, add exercises to specific sessions, and view detailed workout histories.
- **Gym Preferences**: Set maximum acceptable crowd levels for gyms and customize preferences.
- **Notifications**: Receive notifications for updates, alerts, and gym crowd statuses.
- **Real-Time Updates**: Stay informed with the latest gym crowd data and activity alerts.

## **Project Structure**

### **Backend (Django + PostgreSQL)**
- **Django**: Backend framework for robust application logic.
- **Django REST Framework (DRF)**: Handles API endpoints for communication with the frontend.
- **PostgreSQL**: Relational database for storing user, workout, and notification data.
- **RESTful API Design**: Provides a modular and scalable backend structure.

## **Table of Contents**

- [Getting Started](#getting-started)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [PostgreSQL Setup](#postgresql-setup)
- [Usage](#usage)
- [API Specification](#api-specification)

## **Getting Started**

### **Prerequisites**
Before running this project, ensure you have the following installed on your system:
- **Python** (>=3.8)
- **PostgreSQL** (>=13.x)
- **pip** (Python package manager)

### **Tech Stack**
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL

## **Installation**

### **Backend Setup**
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/gymcrowd.git
    cd gymcrowd
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `secrets.json` file inside the `gymcrowd` directory with the following structure:
    {
      "environment": "development", 
      "database_name": "your-database-name",
      "database_user": "your-database-user",
      "database_password": "your-database-password",
      "database_host": "localhost",
      "database_port": "5432"
    }

    Replace the placeholder values with your PostgreSQL database information.

5. Run migrations and start the Django development server:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

---

## **PostgreSQL Setup**

### **Installing PostgreSQL**
1. Download and install PostgreSQL from the [official website](https://www.postgresql.org/).
2. Follow the installation wizard and set up the following:
   - **Username**: Choose a database admin username (e.g., `postgres`).
   - **Password**: Set a strong password for the admin account.
   - **Port**: Use the default port `5432` or customize as needed.

### **Configuring PostgreSQL**
1. Log into the PostgreSQL terminal:
    ```bash
    psql -U postgres
    ```

2. Create a new database:
    ```sql
    CREATE DATABASE gymcrowd;
    ```

3. Create a new user with a password:
    ```sql
    CREATE USER gymcrowd_user WITH PASSWORD 'your-password';
    ```

4. Grant privileges to the new user:
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE gymcrowd TO gymcrowd_user;
    ```

5. Exit the PostgreSQL terminal:
    ```bash
    \q
    ```

### **Testing the Connection**
Ensure the `secrets.json` file has the proper database credentials:
{
    "environment": "development", 
    "database_name": "your-database-name",
    "database_user": "your-database-user",
    "database_password": "your-database-password",
    "database_host": "localhost",
    "database_port": "5432"
}

Run the following command to verify the connection:
```bash
python manage.py runserver
```

## **Usage**

### **Start the Development Server**
To start the development server, run the following command:

```bash
python manage.py runserver
```

### **Access the Application**
Once the server is running, you can access the application at:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### **Test the API**
Use an API client like **Postman** or **cURL** to test the API endpoints. Make sure to include appropriate headers (e.g., Authorization tokens) where required.

### **Explore the Features**
- **User Authentication**: Sign up, log in, retrieve tokens, and log out.
- **Workout Management**: Add workouts, track exercises, and retrieve workout history.
- **Gym Preferences**: Set and update gym crowd level preferences.
- **Notifications**: Receive notifications about gym activities and updates.

# API Specification

Contributors: Adeeb Khan, Arjun Maitra, Ethan Zhang

## NOTE ABOUT ERROR RESPONSES

The server should return an error response for:

- POST requests, if the user does not supply one of the required fields in the body (e.g., email, password, etc.) with a status code of `400 Bad Request`.
- Any request if an invalid or missing parameter is provided, with an appropriate status code and error message.

### Error Response Format
```json
{
  "error": "Your error message here"
}
```

---

## User Endpoints

### Log in a User

**POST** `/api/users/login/`

#### Description:

Validates user credentials (username and password) and logs the user into the application if the credentials are valid.

#### Request Body

```json
{
  "username": "user123",
  "password": "securepassword123"
}
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "user": {
    "user_id": <USER_ID>,
    "username": "<USER_USERNAME>",
    "name": "<USER_NAME>",
    "email": "<USER_EMAIL>",
    "preferences": [],
    "workouts": [],
    "notifications": []
  },
  "message": "Login successful."
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Username and password are required."
}
```

2. **Status Code:** `401 Unauthorized`

```json
{
  "error": "Invalid username or password."
}
```

---

### Retrieve a User Token

**POST** `/api/users/token/`

#### Description:

Generates a token for an authenticated user. The token is used for authenticating protected API endpoints. Note that this route can also be used for user login.

#### Request Body

```json
{
  "username": "<USER_USERNAME>",
  "password": "securepassword123"
}
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "token": "<USER_TOKEN>",
  "user": {
    "user_id": <USER_ID>,
    "username": "<USER_USERNAME>",
    "name": "<USER_NAME>",
    "email": "<USER_EMAIL>",
    "preferences": [],
    "workouts": [],
    "notifications": []
  }
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Username and password are required."
}
```

2. **Status Code:** `401 Unauthorized`

```json
{
  "error": "Invalid username or password."
}
```

---

### Sign up a new user

**POST** `/api/users/signup/`

#### Description:

Allows users to create a new account by providing their name, email, username, and password. Passwords are hashed before being stored in the database.

#### Request Body

```json
{
  "name": "<USER_NAME>",
  "email": "<USER_EMAIL>",
  "username": "<USER_USERNAME>",
  "password": "securepassword123"
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "user": {
    "user_id": "<USER_ID>",
    "username": "<USER_USERNAME>",
    "name": "<USER_NAME>",
    "email": "<USER_EMAIL>",
    "preferences": [],
    "workouts": [],
    "notifications": []
  },
  "message": "Account created successfully."
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

Missing Fields:

```json
{
  "error": "Name, email, username, and password are required."
}
```

Email Already Exists:

```json
{
  "error": "An account with this email already exists."
}
```

Username Already Exists:

```json
{
  "error": "An account with this username already exists."
}
```

2. **Status Code:** `500 Internal Server Error`

```json
{
  "error": "Failed to create account: <ERROR_MESSAGE>"
}
```

---

### Log Out a User

**POST** `/api/users/logout/`

#### Description:

Logs the user out by deleting the authentication token associated with their account.

#### Headers

Authorization: Token `<USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "message": "Logout successful."
}
```

#### Error Responses

1. **Status Code:** `401 Unauthorized`

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### List All User Preferences

**GET** `/api/users/preferences/`

#### Description:

Retrieves a list of all preferences set by the authenticated user. Each preference is linked to a gym and specifies the maximum acceptable crowd level.

#### Headers

Authorization: Token `<USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "preferences": [
    {
      "preference_id": 1,
      "user": 1,
      "gym": 2,
      "max_crowd_level": 0.8,
      "created_at": "2024-11-24T18:00:00Z"
    },
    {
      "preference_id": 2,
      "user": 1,
      "gym": 3,
      "max_crowd_level": 0.6,
      "created_at": "2024-11-25T18:00:00Z"
    }
  ]
}
```

#### Error Responses

1. **Status Code:** `403 Forbidden`

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### Create a New User Preference

**POST** `/api/users/preferences/`

#### Description:

Allows the authenticated user to create a new gym preference. This includes specifying the gym and the maximum acceptable crowd level.

#### Headers

Authorization: Token `<USER_TOKEN>`

#### Request Body

```json
{
  "gym": 2,
  "max_crowd_level": 0.8
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "preference_id": 1,
  "user": 1,
  "gym": 2,
  "max_crowd_level": 0.8,
  "created_at": "2024-11-24T18:00:00Z"
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Gym and max_crowd_level are required."
}
```

2. **Status Code:** `403 Forbidden`

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### Update a User Preference

**PUT** `/api/users/preferences/<preference_id>/`

#### Description:

Allows the authenticated user to update an existing gym preference. This includes modifying the gym or the maximum acceptable crowd level.

#### Headers

Authorization: Token `<USER_TOKEN>`

#### Request Body

```json
{
  "gym": 3,
  "max_crowd_level": 0.7
}
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "preference_id": 1,
  "user": 1,
  "gym": 3,
  "max_crowd_level": 0.7,
  "updated_at": "2024-11-25T18:30:00Z"
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Invalid fields provided."
}
```

2. **Status Code:** `403 Forbidden`

```json
{
  "detail": "Authentication credentials were not provided."
}
```

3. **Status Code:** `404 Not Found`

```json
{
  "error": "Preference not found."
}
```

---

### Delete a User Preference

**DELETE** `/api/users/preferences/<preference_id>/`

#### Description:

Allows the authenticated user to delete an existing gym preference.

#### Headers

Authorization: Token `<USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "message": "Preference deleted successfully."
}
```

#### Error Responses

1. **Status Code:** `403 Forbidden`

```json
{
  "detail": "Authentication credentials were not provided."
}
```

2. **Status Code:** `404 Not Found`

```json
{
  "error": "Preference not found."
}
```

---

## Gym Endpoints

### List All Gyms

**GET** `/api/gyms/`

#### Description:

Fetches a list of all gyms in the system, including their details and associated crowd data.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "gyms": [
    {
      "gym_id": <GYM_ID>,
      "name": "<GYM_NAME>",
      "location": "<GYM_LOCATION>",
      "type": "<GYM_TYPE>",
      "crowd_data": [
        {
          "crowd_id": <CROWD_ID>,
          "occupancy": <OCCUPANCY>,
          "percentage_full": <PERCENTAGE_FULL>,
          "last_updated": "<LAST_UPDATED>"
        }
      ]
    },
    ...
  ]
}
```

---

### Get a Specific Gym

**GET** `/api/gyms/<id>/`

#### Description:

Fetches the details of a specific gym by its ID, including associated crowd data.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "gym_id": <GYM_ID>,
  "name": "<GYM_NAME>",
  "location": "<GYM_LOCATION>",
  "type": "<GYM_TYPE>",
  "crowd_data": [
    {
      "crowd_id": <CROWD_ID>,
      "occupancy": <OCCUPANCY>,
      "percentage_full": <PERCENTAGE_FULL>,
      "last_updated": "<LAST_UPDATED>"
    }
  ]
}
```

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Gym not found."
}
```

---

### List All Crowd Data Entries

**GET** `/api/gyms/crowddata/`

#### Description:

Fetches a list of all crowd data entries in the system.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "crowd_data": [
    {
      "crowd_id": <CROWD_ID>,
      "gym": <GYM_ID>,
      "occupancy": <OCCUPANCY>,
      "percentage_full": <PERCENTAGE_FULL>,
      "last_updated": "<LAST_UPDATED>"
    },
    ...
  ]
}
```

---

### Get a Specific Crowd Data Entry

**GET** `/api/gyms/crowddata/<id>/`

#### Description:

Fetches details of a specific crowd data entry by its ID.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "crowd_id": <CROWD_ID>,
  "gym": <GYM_ID>,
  "occupancy": <OCCUPANCY>,
  "percentage_full": <PERCENTAGE_FULL>,
  "last_updated": "<LAST_UPDATED>"
}
```

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Crowd data entry not found."
}
```

---

## Workout Endpoints

### List All Exercises

**GET** `/api/workouts/exercises/`

#### Description:

Fetches a list of all available exercises in the system.

#### Requires:

No authentication required.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "exercises": [
    {
      "exercise_id": <EXERCISE_ID>,
      "name": "<EXERCISE_NAME>",
      "body_part": "<BODY_PART>",
      "equipment": "<EQUIPMENT>",
      "gif_url": "<GIF_URL>",
      "target": "<TARGET>",
      "secondary_muscles": "<SECONDARY_MUSCLES>",
      "instructions": "<INSTRUCTIONS>"
    },
    ...
  ]
}
```

---

### Get a Specific Exercise

**GET** `/api/workouts/exercises/<exercise_id>/`

#### Description:

Fetches details of a specific exercise by its ID.

#### Requires:

No authentication required.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "exercise_id": <EXERCISE_ID>,
  "name": "<EXERCISE_NAME>",
  "body_part": "<BODY_PART>",
  "equipment": "<EQUIPMENT>",
  "gif_url": "<GIF_URL>",
  "target": "<TARGET>",
  "secondary_muscles": "<SECONDARY_MUSCLES>",
  "instructions": "<INSTRUCTIONS>"
}
```

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Exercise not found."
}
```

---

### List All User Workouts

**GET** `/api/workouts/`

#### Description:

Fetches a list of all workout sessions for the authenticated user.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "workouts": [
    {
      "workout_id": <WORKOUT_ID>,
      "user": <USER_ID>,
      "date": "<WORKOUT_DATE>",
      "created_at": "<CREATED_AT>",
      "workout_exercises": [
        {
          "entry_id": <ENTRY_ID>,
          "exercise": <EXERCISE_ID>,
          "sets": <SETS>,
          "reps": <REPS>,
          "weight": <WEIGHT>
        },
        ...
      ]
    },
    ...
  ]
}
```

---

### Create a New Workout Session

**POST** `/api/workouts/`

#### Description:

Creates a new workout session for the authenticated user.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Request Body

```json
{
  "date": "<WORKOUT_DATE>"
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "workout_id": <WORKOUT_ID>,
  "user": <USER_ID>,
  "date": "<WORKOUT_DATE>",
  "created_at": "<CREATED_AT>",
  "workout_exercises": []
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Invalid or missing fields in request."
}
```

---

### Get Details of a Specific Workout

**GET** `/api/workouts/<workout_id>/`

#### Description:

Fetches details of a specific workout session by its ID.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "workout_id": <WORKOUT_ID>,
  "user": <USER_ID>,
  "date": "<WORKOUT_DATE>",
  "created_at": "<CREATED_AT>",
  "workout_exercises": [
    {
      "entry_id": <ENTRY_ID>,
      "exercise": <EXERCISE_ID>,
      "sets": <SETS>,
      "reps": <REPS>,
      "weight": <WEIGHT>
    },
    ...
  ]
}
```

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Workout not found."
}
```

---

### List All Exercises in User Workouts

**GET** `/api/workouts/workout-exercises/`

#### Description:

Fetches all exercises logged in the authenticated user's workouts.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "workout_exercises": [
    {
      "entry_id": <ENTRY_ID>,
      "workout": <WORKOUT_ID>,
      "exercise": <EXERCISE_ID>,
      "sets": <SETS>,
      "reps": <REPS>,
      "weight": <WEIGHT>
    },
    ...
  ]
}
```

---

### Add an Exercise to a Workout

**POST** `/api/workouts/workout-exercises/`

#### Description:

Adds a new exercise entry to a specific workout session for the authenticated user.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Request Body

```json
{
  "workout": <WORKOUT_ID>,
  "exercise": <EXERCISE_ID>,
  "sets": <SETS>,
  "reps": <REPS>,
  "weight": <WEIGHT>
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "entry_id": <ENTRY_ID>,
  "workout": <WORKOUT_ID>,
  "exercise": <EXERCISE_ID>,
  "sets": <SETS>,
  "reps": <REPS>,
  "weight": <WEIGHT>
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Invalid or missing fields in request."
}
```

2. **Status Code:** `403 Forbidden`

```json
{
  "error": "You do not have permission to add exercises to this workout."
}
```

---

## Notifications Endpoints

### List All Notifications

**GET** `/api/notifications/`

#### Description:

Fetches a list of all notifications in the system.

#### Requires:

No authentication required.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "notifications": [
    {
      "notification_id": 1,
      "user": 12,
      "gym": 3,
      "message": "Your session is confirmed.",
      "sent_at": "2024-01-01T12:00:00Z"
    },
    ...
  ]
}
```

---

### Create a New Notification

**POST** `/api/notifications/`

#### Description:

Creates a new notification associated with the authenticated user.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Request Body

```json
{
  "gym": <GYM_ID>,
  "message": "<NOTIFICATION_MESSAGE>"
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "notification_id": <NOTIFICATION_ID>,
  "user": <USER_ID>,
  "gym": <GYM_ID>,
  "message": "<NOTIFICATION_MESSAGE>",
  "sent_at": "<TIMESTAMP>"
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Invalid or missing fields in request."
}
```

---

### Get a Specific Notification

**GET** `/api/notifications/<notification_id>/`

#### Description:

Fetches details of a specific notification by its ID.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "notification_id": <NOTIFICATION_ID>,
  "user": <USER_ID>,
  "gym": <GYM_ID>,
  "message": "<NOTIFICATION_MESSAGE>",
  "sent_at": "<TIMESTAMP>"
}
```

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Notification not found."
}
```

---

### List Notifications for a User

**GET** `/api/notifications/user/<user_id>/`

#### Description:

Fetches all notifications for a specific user.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Success Response

**Status Code:** `200 OK`

```json
{
  "notifications": [
    {
      "notification_id": 1,
      "gym": 3,
      "message": "Your session is confirmed.",
      "sent_at": "2024-01-01T12:00:00Z"
    },
    ...
  ]
}
```

#### Error Responses

1. **Status Code:** `403 Forbidden`

```json
{
  "error": "You do not have permission to view these notifications."
}
```

---

### Delete a notification

**DELETE** `/api/notifications/<notification_id>/`

#### Description:

Deletes a specific notification by its ID.

#### Requires:

A token in the header.

**Header:**

`Authorization: Token <USER_TOKEN>`

#### Success Response

**Status Code:** `204 No Content`

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Notification not found."
}
```
