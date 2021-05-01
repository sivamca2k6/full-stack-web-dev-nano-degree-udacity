# Udacity Full Stack Web Developer Nano Degree - Final Capstone Project

## App Live URL

Application is hosted at Heroku.

**_https://udacasting-agency.herokuapp.com/_**

## Topics 

1. [Motivation / Project Overview ](#motivation)
2. [Tech Stack](#techstack)
3. [Testing Locally](#local)
4. [Authentification](#authentification)
5. [API Documentation](#api)

<a name="motivation"></a>
## 1. Project Overview: Casting Agency Management App

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 

#### Data Models: 
* Movies with attributes title and release date 
* Actors with attributes name, age and gender 
#### Endpoints : 
* GET /actors and /movies 
* DELETE /actors/ and /movies/ 
* POST /actors and /movies and 
* PATCH /actors/ and /movies/ 
#### Roles: 
* Casting Assistant 
    - Can view actors and movies 
* Casting Director 
    - All permissions a Casting Assistant has and… 
    - Add or delete an actor from the database 
    - Modify actors or movies 
* Executive Producer 
    - All permissions a Casting Director has and… 
    - Add or delete a movie from the database 
#### Unit Tests: 
* One test for success behavior of each endpoint 
* One test for error behavior of each endpoint 
* At least two tests of RBAC for each role 

<a name="techstack"></a>
## 2. Tech Stack (Dependencies)
Our tech stack will include the following:
 * **virtualenv** to create isolated Python environments
 * **Python3** and **Flask** as our server language and server framework
 * **PostgreSQL** as our database of choice
 * **SQLAlchemy ORM** as ORM library and data modeling
 * **REST API** using Flask
 * **Pytest** as our unit test with TDD
 * **Flask-Migrate** for creating and running schema migrations
 * **Auth0 RBAC JWT** for third party authentication integration
 * **Heroku** for Cloud Deployment

<a name="local"></a>
## 3. Testing locally

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
Make sure Postgres is installed and running. Update database connection strings at Models.setup_db by updating default url..Run the Migration if require.

#### Auth 
All Auth tokens for each roles placed inside auth class.This tokens need to be passed thru auth header during request for corresponding roles..

#### Unit Test
Run below command to execute unittest. Tokens already mapped with respective role test methods.

```bash
python test_app.py
```

#### Run 
Run below command to execute app.

```bash
flask run
```

<a name="authentification"></a>
## 4. Authentification

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions
    - view:actors   ; view:movies
    - create:actors ; create:movies
    - patch:actors  ; patch:movies
    - delete:actors ; delete:movies
6. Create new roles for:
    * Casting Assistant 
        - Can view actors and movies 
    * Casting Director 
        - All permissions a Casting Assistant has and… 
        - Add or delete an actor from the database 
        - Modify actors or movies 
    * Executive Producer 
        - All permissions a Casting Director has and… 
        - Add or delete a movie from the database 
7. Test your endpoints with [Postman]. Please use below collections from project folder.Token alread attached at role level.
    - heroku : heroku-udacity-fsnd-capstone.postman_collection
    - local : localhost-udacity-fsnd-capstone.postman_collection

<a name="api"></a>
## 5. API Documentation
Below documentation helps to understand the API Endpoints and proper way to consume it.

### How to work with each endpoint

Click on a link to directly get to the ressource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

# <a name="get-actors"></a>
### 1. GET /actors

Query paginated actors.

```bash
$ curl -X GET https://udacasting-agency.herokuapp.com/actors
```
- Returns a list of dictionaries of actors info
- Request Headers: **None**
- Requires permission: `read:actors`
#### Example response
```js
{
  "actors": [
    {
      "age": 25,
      "gender": "Male",
      "id": 1,
      "name": "Actor 1"
    }
  ],
  "success": true
}
```
#### Errors

When url not exists

```bash
curl -X GET  https://udacasting-agency.herokuapp.com/actors1
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}

```

# <a name="post-actors"></a>
### 2. POST /actors

Insert new actor into database.

```bash
$ curl -X POST https://udacasting-agency.herokuapp.com/actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` (<span style="color:red">*</span>required)
       2. **integer** `age` (<span style="color:red">*</span>required)
       3. **string** `gender`
- Requires permission: `create:actors`
- Returns: 
  1. **integer** `id from newly created actor`
  2. **boolean** `success`

#### Example response
```js
{
    "actor": [
        {
            "age": 30,
            "gender": "Other",
            "id": 11,
            "name": "Test Actor"
        }
    ],
    "success": true,
    "count": 5
}

```
#### Errors
If you try to create a new actor without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X POST https://udacasting-agency.herokuapp.com/actors
```

will return

```js
{
  "error": 422,
  "message": "Request body not valid or found.",
  "success": false
}
```

# <a name="patch-actors"></a>
### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH https://udacasting-agency.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `edit:actors`
#### Example response
```js
{
    "actor": [
        {
            "age": 30,
            "gender": "Other",
            "id": 1,
            "name": "Test Actor"
        }
    ],
    "success": true,
    "count": 5
}
```
#### Errors
If you try to update an actor with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://udacasting-agency.herokuapp.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "{id} not exists.Please provide valid data for update.",
  "success": false
}
```
# <a name="delete-actors"></a>
### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE https://udacasting-agency.herokuapp.com/actor/1
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`

#### Example response
```js
{
    "deleted_actor_id": 5,
    "success": true
}

```
#### Errors
If you try to delete actor with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://udacasting-agency.herokuapp.com/actor/125
```

will return

```js
{
  "error": 404,
  "message": "{id} not exists.Please provide valid actor info.",
  "success": false
}
```

# <a name="get-movies"></a>
### 5. GET /movies

```bash
$ curl -X GET https://udacasting-agency.herokuapp.com/movies
```
- Fetches a list of movies
- Request Headers: **None**
- Requires permission: `read:movies`

#### Example response
```js
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Matthew first Movie"
    }
  ],
  "success": true,
  "count": 5
}

```
#### Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl -X GET https://udacasting-agency.herokuapp.com/movies?page123124
```

will return

```js
{
  "error": 404,
  "message": "{id} not exists.Please provide valid data for update.",
  "success": false
}
```

# <a name="post-movies"></a>
### 6. POST /movies

Insert new Movie into database.

```bash
$ curl -X POST https://udacasting-agency.herokuapp.com/movies
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `title` (<span style="color:red">*</span>required)
       2. **date** `release_date` (<span style="color:red">*</span>required)
- Requires permission: `create:movies`

#### Example response
```js
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Matthew first Movie"
    }
  ],
  "success": true,
  "count": 5
}
```
#### Errors
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://udacasting-agency.herokuapp.com/movies?page123124
```

will return

```js
{
  "error": 422,
  "message": "no name provided.",
  "success": false
}
```

# <a name="patch-movies"></a>
### 7. PATCH /movies

Edit an existing Movie

```bash
$ curl -X PATCH https://udacasting-agency.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `edit:movies`

#### Example response
```js
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Matthew first Movie"
    }
  ],
  "success": true,
  "count": 5
}

```
#### Errors
If you try to update an movie with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://udacasting-agency.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "{id} not exists.Please provide valid data for update.",
  "success": false
}
```

# <a name="delete-movies"></a>
### 8. DELETE /movies

Delete an existing movie

```bash
$ curl -X DELETE https://udacasting-agency.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movies`

#### Example response
```js
{
    "deleted_movie_id": 5,
    "success": true
}

```
#### Errors
If you try to delete movie with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://udacasting-agency.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "{id} not exists.Please provide valid movie info.",
  "success": false
}
```





