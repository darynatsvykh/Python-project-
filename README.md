# Python-project

# Project Overview

## Project Team Members
- **Sthefany**:
  - Create Account
  - Login/Logout
  - Models
  - CSRF Tokens
  - CSS Styling
  - Hobby Similarity Feature
  - Attempted Friend Request Feature, only send friend request works (can be seen in backend)
- **Daryna**:
  - Create Account
  - Models
  - Login/Logout
  - Filter by Age Feature
  - Reset Buttons
  - Attemped login test but it doesn't work
- **Yusra**:
  - Profile Page
  - Attempted profile test but doesn't work
- **Salma**:
  - Hobbies Page
  - Pagination Feature
  - Attempted signup test but doesn't work

---

## Admin User
- **Username**: `admin1`
- **Password**: `admin`

---

## Test Users
- **Username**: `john77`  
  **Password**: `john12345`

- **Username**: `mariaconstanta`  
  **Password**: `maria0987`

- **Username**: `iamlinda`  
  **Password**: `newyork2007`

- **Username**: `ana`  
  **Password**: `lima1995`

- **Username**: `mark5`  
  **Password**: `mark2002`

  Work in groups of 3-4 students (each group must have at least three members but no more than four members). You are being asked to develop a Single Page Application (SPA) using Django for the model-based web API and Vue/Vite for the reactive frontend. You must include frontend routing using Vue router and use a global store using Pinia. This coursework does not need to be checked by your demonstrator. The module leader will mark all the submissions. As with the individual coursework 2, you must use this Github repository as a starting point for your group coursework (download this template as a zip file and add files to your own private repo).
Your task is to develop a "hobbies" web app using the Django framework. The app should provide the following functionalities:

Users can create an account on the web app and login / logout. You should use a custom User model (as explained here) which inherits from Django's AbstractUser model, and make use of Django's authentication framework. The signup and login should be done using Django templates and forms (Server Side Rendering). The Vue SPA only needs to be used once the user is authenticated.
Your custom user model should include the user's name, email, date of birth and their list of hobbies (and password for login). The user should be able to edit all their profile data, including their list of hobbies and updating the password, in a "profile page".
The list of hobbies should be database driven, and users should be able to add new hobbies that are not yet listed on the DB. New hobbies added by one user should then be available to all other users to select from.
There should be a page where users can see a list of other users who have the most similar set of hobbies (i.e. for each two users you should count how many hobbies in common they have) and then list those users in descending order (users with most common hobbies first). Include some form of pagination, so that no more than 10 users are displayed at any given time.
From the list above users should be able to filter by age, e.g. only users with ages between 15 and 20. Make sure that the frontend does not receive the full list of all users, but only the users that are needed to be displayed on the page. So, changing the filter values should trigger an Ajax request for the new list of users.
Users should then be able to send a "friend request" to another user. These requests should also be sent via ajax. Requests need to be approved by the other user before the two users become friends.
All ajax requests must be done using the fetch API (with async-await) and Vue to reactively update the page.
Your Vue frontend should use typescript, and make good use of static typing, including custom interfaces for users and hobbies. Your Python backend should also make use of type annotations (type hints). So, both frontend and backend should support static type checking.
Your project should include automated tests that test: (1) account creation / signup, (2) login and (3) editing all the user's data on their profile page, (4) users page, with testing of filtering by age, (5) sending a friend request, (6) login as the other user and accept the friend requests sent. You should use selenium-based tests for full end-to-end (E2E) testing.
Outcome: Once fully tested, your application should be deployed to the EECS OpenShift platform (to be discussed in week 8) — one deployed app per team. Make sure your submitted application has at least 20 test users and at least 10 hobbies. Each group should submit the code including a README file which should contain:

list of group members, with a short description (one sentence) of what each member was assigned to do, and what they actually did in terms of contributing to the final deliverable
the URL of your deployed application (if deployed)
the username and password for the admin user
the username and passwords of at least 5 of the test users
