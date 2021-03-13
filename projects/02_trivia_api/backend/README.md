# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


<a name="api-documentaton"></a>
## API Documentation

Below documentation helps to understand the API Endpoints and proper way to consume it.

### Base URL

Local host 

**_http://127.0.0.1:5000/_**

### Available Endpoints

/questions/    
/categories/   
/quizzes/ 

### How to work with each endpoint

1. Questions
   1. [GET /questions/](#get-questions)
   2. [POST /questions/](#post-questions)
   3. [DELETE /questions/<question_id>/](#delete-questions)
2. Quizzes
   1. [POST /quizzes/](#post-quizzes)
3. Categories
   1. [GET /categories/](#get-categories)
   2. [GET /categories/<category_id>/questions/](#get-categories-questions)

# <a name="get-questions"></a>
### 1. GET /questions/

GET paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```
- Returns a list of dictionaries of questions with formated , all category type and  total questions.
- Request Arguments: 
    - **integer** `page` (per page questions limit is 10 , defaults to `1` when page is optional)
- Request Headers: **None**

#### Example response

```js
{
"categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"current_category":  Science,
"questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },

 [...]

  ],
  "success": true,
  "total_questions": 19
  "current_page_questions_count": 10
}

```
#### Errors

When question not exists

```bash
curl -X GET http://127.0.0.1:5000/questions?page=12452512
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}

```

# <a name="post-questions"></a>
### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'
```

Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a test question?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'
```

- Searches database for questions with a search term, if provided. Otherwise,
it will insert a new question into the database.
- Request Arguments: **None**
- Request Headers : (all are required)
  - if you want to **search** (_application/json_)
       1. **string** `searchTerm` 
  - if you want to **insert** (_application/json_) 
       1. **string** `question` 
       2. **string** `answer` 
       3. **string** `category` 
       4. **integer** `difficulty` 

#### Example response
Search Questions
```js
{
  "current_category": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },

   [...] 

  ],
  "questions": [
    {
      "answer": "Jup",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "Is this a test question?"
    }

    [...] 
  
  ],
  "success": true,
  "total_questions": 20
}

```
Create Question
```js
{
  "created": 26, 
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
   
   [...] 

  ],
  "success": true,
  "total_questions": 21
}

```


#### Errors
**Search related**

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 
```
when `question` which does not exist for that search term then will return

```js
{
  "error": 404,
  "message": "Search Term does not match with any questions.",
  "success": false
}
```
**Insert related**

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a question without an answer?", "category" : "1" , "difficulty" : 1 }' -H 'Content-Type: application/json'
```

when required field not passed , will return

```js
{
  "error": 404,
  "message": "Answer can not be blank",
  "success": false
}
```
# <a name="delete-questions"></a>
### 3. DELETE /questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
- Deletes specific question based on id
- Request Arguments: 
  - **integer** `question_id`
- Request Headers : **None**

#### Example response
```js
{
  "deleted": 10,
  "success": true
}
```

### Errors

```bash
curl -X DELETE http://127.0.0.1:5000/questions/7
```
When qustion id not valid , will return

```js
{
  "error": 404,
  "message": "Question does not exist.",
  "success": false
}
```

# <a name="post-quizzes"></a>
### 4. POST /quizzes

```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [11, 2, 5], "quiz_category" : {"type" : "Sports", "id" : "6"}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Headers : 
     1. **list** `previous_questions` [11, 2, 5]
     1. **dict** `quiz_category` (optional)

#### Example response
```js
{
  "question": {
    "answer": "Jup",
    "category": 6,
    "difficulty": 1,
    "id": 24,
    "question": "Who is Boss?"
  },
  "success": true
}

```
### Errors

```bash
curl -X POST http://127.0.0.1:5000/quizzes
```
when quiz game without a a valid JSON body , will return
```js
{
  "error": 400,
  "message": "Please provide a JSON body with previous question Ids and optional category.",
  "success": false
}

```
# <a name="get-categories"></a>
### 5. GET /categories

Get all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```
- Get a list of all `categories` with its `type` as values.
- Request Arguments: **None**
- Request Headers : **None**

#### Example response
```js
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```

# <a name="get-categories-questions"></a>
### 6. GET /categories/<category_id>/questions

Get all questions for the given `category`.

```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```
- Fetches all `questions`.
- Request Arguments:
  - **integer** `category_id` (required)
  - **integer** `page` (optinal)
- Request Headers: **None**

#### Example response

```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### Errors

```bash
curl -X GET http://127.0.0.1:5000/categories/10/questions?page=1
```
when category that does not exist , will return

```bash
{
  "error": 400,
  "message": "Invalid Category id.",
  "success": false
}
```

```bash
curl -X GET http://127.0.0.1:5000/categories/1/questions?page=5
```
When no more questions exists for this pag , will return
```bash
{
  "error": 404,
  "message": "No more questions exists for this page.",
  "success": false
}

```
