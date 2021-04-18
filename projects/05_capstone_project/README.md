# Udacity Full Stack - Final Capstone Project

## Project : Casting Agency Management App

### Project Specifications :

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 

#### Models / Tables : 
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

## Tech Stack (Dependencies)
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **Python3** and **Flask** as our server language and server framework
 * **PostgreSQL** as our database of choice
 * **REST API** as using Flask
 * **Pytest** as our unit test with TDD
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **Flask-Migrate** for creating and running schema migrations
 * **Auth0 RBAC JWT** for authentication integration
 * **Heroku** for Cloud Deployment




