# Udacity Nano Degree - Full Stack Web Developer 

Tech Stack

* **VS Code** as IDE.
 * **virtualenv** to create isolated Python environments.
 * **Python3** and **Flask** as our server language and server framework.
 * **PostgreSQL** as our database of choice.
 * **SQLAlchemy ORM** as ORM library and data modeling.
 * **REST API** using Flask.
 * **Pytest** as our unit test with TDD.
 * **Flask-Migrate** for creating and running schema migrations.
 * **Auth0 RBAC JWT** for third party authentication integration.
 * **Docker Kuebernetes AWS EKS** for creating and deploying containers at cloud.
 * **Heroku** for Easier Cloud Deployment
 * **GIT** for source version control.

## Overview

The goal of the Full Stack Web Developer Nanodegree program is to equip learners with the unique skills
they need to build database-backed APIs and web applications. 

A graduate of this program will be able to:
• Design and build a database for a software application
• Create and deploy a database-backed web API (Application Programming Interface)
• Secure and manage user authentication and access control for an application backend
• Deploy a Flask-based web application to the cloud using Docker and Kubernetes

This program includes 4 courses and 5 projects. Each project you build will be an opportunity to
apply what you’ve learned in the lessons and demonstrate to potential employers that you have practical
full-stack development skills

## Module 1 - SQL and Data Modeling for the Web
Master relational databases with the power of SQL, and leverage Python to incorporate database logic into your programs.

## Module 2 - API Development and Documentation
Learn how to use APIs to control and manage web applications, including best practices for API testing and documentation.

## Module 3 - Identity Access Management
Implement authentication and authorization in Flask and understand how to design against key security principle. You will also gain experience with role-based control design patterns, securing a REST API, and applying software system risk and compliance principles.

## Module 4 - Server Deployment and Containerization
Develop an understanding of containerized environments, use Docker to share and store containers, and deploy a Docker container to a Kubernetes cluster using AWS


## Project 1 - Design a Venue Booking Database 
you’ll be building out the data models and database for an artist/venue booking application. The fictitious
startup Fy-yur is building a website that facilitates bookings between artists who can play at venues, and venues who want to book artists.

This site:
• Lets venue managers and artists sign up, fill out their information, and list their availability for shows.
• Lets artists browse venues where they can play, and see what past/upcoming artists have been booked at a venue.
• Lets a venue manager browse artists that would like to play in their city, and see what past/upcoming venues where the artist
 has played/will be playing.

The goal of this project is to build out the data models for this booking application. A prototype design of the web app will be
provided. You’ll use SQLAlchemy and Postgresql to build out the data models upon which this site will rely. You’ll write out both the
raw SQL and SQLAlchemy commands to run for powering the backend functionality of the website

## Project 2 - Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Project 3 - Coffee Shop Full Stack

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

This project will give you a hands-on chance to practice and demonstrate what you've learned in this lesson, such as:

• Implementing authentication and authorization using Auth0 in   Flask
• Designing against key security principals
• mplementing role-based control design patterns
• Securing a REST API
• Applying software system risk and compliance principles

## Project 4 - Deploying a Flask API Container to Kubernetes using AWS EKS

In this project you will containerize and deploy a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

The Flask app that will be used for this project consists of a simple API with three endpoints:

- `GET '/'`: This is a simple health check, which returns the response 'Healthy'. 
- `POST '/auth'`: This takes a email and password as json arguments and returns a JWT based on a custom secret.
- `GET '/contents'`: This requires a valid JWT, and returns the un-encrpyted contents of that token. 

The app relies on a secret set as the environment variable `JWT_SECRET` to produce a JWT. The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready [Gunicorn](https://gunicorn.org/) server when deploying the app.

Completing the project involves several steps:

1. Write a Dockerfile for a simple Flask API
2. Build and test the container locally
3. Create an EKS cluster
4. Store a secret using AWS Parameter Store
5. Create a CodePipeline pipeline triggered by GitHub checkins
6. Create a CodeBuild stage which will build, test, and deploy your code

## Project 5 Capstone - Casting Agency Management App

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

#### Auth0 - Third Party Auth integration :

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
6. Create new roles for:


