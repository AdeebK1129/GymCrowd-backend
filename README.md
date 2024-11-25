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

### Log in a user

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

### Retrieve a user token

**POST** `/api/users/token/`

#### Description:

Generates a token for an authenticated user. The token is used for authenticating protected API endpoints.

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
  "user_id": <USER_ID>,
  "name": "<USER_NAME>",
  "email": "<USER_EMAIL>",
  "username": "<USER_USERNAME>"
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
    "user_id": <USER_ID>,
    "name": "<USER_NAME>",
    "email": "<USER_EMAIL>",
    "username": "<USER_USERNAME>",
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

### List all user preferences

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

### Create a new user preference

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

### Update a user preference

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

### Delete a user preference

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

### List all gyms

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

### Get a specific gym

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

### List all crowd data entries

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

### Get a specific crowd data entry

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

### List all exercises

**GET** `/api/workouts/exercises/`

#### Description:

Fetches a list of all available exercises in the system.

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

### Get a specific exercise

**GET** `/api/workouts/exercises/<exercise_id>/`

#### Description:

Fetches details of a specific exercise by its ID.

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

### List all user workouts

**GET** `/api/workouts/`

#### Description:

Fetches a list of all workout sessions for the authenticated user.

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

### Create a new workout session

**POST** `/api/workouts/`

#### Description:

Creates a new workout session for the authenticated user.

#### Request Body

```json
{
  "date": "<WORKOUT_DATE>",
  "workout_exercises": [
    {
      "exercise": <EXERCISE_ID>,
      "sets": <SETS>,
      "reps": <REPS>,
      "weight": <WEIGHT>
    },
    ...
  ]
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

1. **Status Code:** `400 Bad Request`

```json
{
  "error": "Invalid or missing fields in request."
}
```

---

### Get details of a specific workout

**GET** `/api/workouts/<workout_id>/`

#### Description:

Fetches details of a specific workout session by its ID.

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

### List all exercises in user workouts

**GET** `/api/workout-exercises/`

#### Description:

Fetches all exercises logged in the authenticated user's workouts.

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

## Notification Endpoints

### List all notifications

**GET** `/api/notifications/`

#### Description:

Fetches a list of all notifications for the authenticated user.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "notifications": [
    {
      "notification_id": <NOTIFICATION_ID>,
      "user": <USER_ID>,
      "gym": <GYM_ID>,
      "message": "<MESSAGE>",
      "sent_at": "<SENT_AT>"
    },
    ...
  ]
}
```

---

### Create a notification

**POST** `/api/notifications/`

#### Description:

Creates a new notification for a user about a specific gym.

#### Request Body

```json
{
  "user": <USER_ID>,
  "gym": <GYM_ID>,
  "message": "<MESSAGE>"
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "notification_id": <NOTIFICATION_ID>,
  "user": <USER_ID>,
  "gym": <GYM_ID>,
  "message": "<MESSAGE>",
  "sent_at": "<SENT_AT>"
}
```

#### Error Responses

1. **Status Code:** `400 Bad Request`

{
  "error": "Invalid or missing fields in request."
}

---

### Get a specific notification

**GET** `/api/notifications/<notification_id>/`

#### Description:

Fetches details of a specific notification by its ID.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "notification_id": <NOTIFICATION_ID>,
  "user": <USER_ID>,
  "gym": <GYM_ID>,
  "message": "<MESSAGE>",
  "sent_at": "<SENT_AT>"
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

### Delete a notification

**DELETE** `/api/notifications/<notification_id>/`

#### Description:

Deletes a specific notification by its ID.

#### Success Response

**Status Code:** `200 OK`

```json
{
  "notification_id": <NOTIFICATION_ID>,
  "message": "Notification deleted successfully."
}
```

#### Error Responses

1. **Status Code:** `404 Not Found`

```json
{
  "error": "Notification not found."
}
```

