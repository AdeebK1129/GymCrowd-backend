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

Validates user credentials (email and password) and logs the user into the application if the credentials are valid.

#### Request Body

```json
{
  "email": "user@example.com",
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
  "error": "Email and password are required."
}
```

2. **Status Code:** `401 Unauthorized`

```json
{
  "error": "Invalid email or password."
}
```

---

### Register a new user

**POST** `/api/users/signup/`

#### Description:

Allows users to create a new account by providing their name, email, and password. Passwords are hashed before being stored in the database.

#### Request Body

```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "password": "securepassword123"
}
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "user": {
    "user_id": <USER_ID>,
    "name": "John Doe",
    "email": "johndoe@example.com",
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
  "error": "Name, email, and password are required."
}
```

Email Already Exists:

```json
{
  "error": "An account with this email already exists."
}
```

2. **Status Code:** `500 Internal Server Error`

```json
{
  "error": "Failed to create account: <ERROR_MESSAGE>"
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

