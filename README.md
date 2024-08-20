# Big T's Chophouse


![Home Screen]()

[View Big T's Chophouse Retreat live website here]()
- - -

## Table of Contents
### [User Experience](#user-experience-ux)
* [Project Goals](#project-goals)
* [Agile Methodology](#agile-methodology)
* [Target Audience](#target-audience)
* [First time user](#first-time-user)
* [Registered user](#registered-user)

### [Design](#design-1)
* [Color Scheme](#color-scheme)

* [Wireframes](#wireframes)
* [Data Model](#data-models)
* [User Journey](#user-journey)
* [Database Scheme](#database-scheme)
### [Security Features](#security-features-1)
### [Features](#features-1)
* [Existing Features](#existing-features)
* [Features Left to Implement](#features-left-to-implement)
### [Technologies Used](#technologies-used-1)
* [Languages Used](#languages-used)
* [Databases Used](#databases-used)
* [Frameworks Used](#frameworks-used)
* [Programs Used](#programs-used)
### [Deployment and Local developement](#deployment-and-local-developement-1)
* [Local Developement](#local-developement)
* [ElephantSQL Database](#elephantsql-database)
* [Cloudinary](#cloudinary)
* [Heroku Deployment](#heroku-deployment)
### [Testing](#testing-1)
### [References](#references-1)
* [Docs](#docs)
* [Content](#content)
* [Acknowledgments](#acknowledgments)

---

## User Experience (UX)


### Project Goals


### Agile Methodology

Agile Methodology was used to help prioritize and organize tasks, writting the user stories and using Project Boards on Github. Template was created to help write User Stories and define Epics

* Epics were written containing possible user stories and based on that the website was made.
* User stories were created by looking at epics and through iterations the project was advancing.
* Project Board is set to public.
* Project Board was used to track progression of the task through the Todo, In progress and Done columns
* Labels were added to sort the issues based on the importance.

<details>
<summary> User Stories Template
</summary>

![User Stories Template]()
</details>

<details>
<summary> User Stories, Issues
</summary>

![User Stories, Issues]()
</details>

<details>
<summary> Project Board
</summary>

![Project Board]()
</details>

### User Stories

#### Epics
* Initial Deployment
* Home Page
* User Registration
* Website Admin and Bookings
* Maintain consistent design with responsiveness in mind

#### User Stories
1. Initial Deployment
* 
2. Home Page
* 
3. User Registration
* 
4. 
*

Detailed look can be found in the [project board]()

### Target Audience

* 

### First time user

* 

### Registered User

* .

## Design


### Color Scheme
![Color Scheme]()

### Hero Images

All images were taken from [pixabay]().

### Logo

Vista was used [Vista]().

### Typography

Lora, Roboto

### Wireframes

<details>
<summary> Home Page
</summary>

![Home Page](G)
</details>

<details>
<summary> Home Page when logged in
</summary>

![Home Page when logged in]()
</details>

![User Login Page]()
</details>

<details>
<summary> User Logout Page
</summary>

![User Logout Page]()
</details>

<details>
<summary> User Sign Up Page
</summary>

![User Sign Up Page]()
</details>

### Data Models

1. AllAuth User Model
    * Django Allauth, the User model is the default user model provided by the Django authentication system
    * 
---
2. Reservation Model
    * 
---
3. Review Model
    * 
---
4. Profile Model
    * 

### User Journey 

![User Journey]()

### Database Schema

Entity Relationship Diagram (ERD)

![DataSchema]()

* 

## Security Features

### User Authentication

* Django Allauth is a popular authentication and authorization library for Django, which provides a set of features for managing user authentication, registration, and account management.

### Login Decorator

* create_reservation etc....: These views involve operations related to user bookings and require authentication with the login_required decorator.
* This ensures that only authenticated users can access these views.

### CSRF Protection

* Django provides built-in protection against Cross-Site Request Forgery (CSRF) attacks. CSRF tokens are generated for each user session, and they are required to submit forms or perform state-changing actions. When a user logs out, the session and associated CSRF token are invalidated, making it difficult for an attacker to forge a valid request using a copied URL.

### Form Validation

* 

### Maximum number of guests per Reservation

* 

### Custom error pages

* 404 Error Page, provides user with a button the redirect to home page.
* 500 Error Page, provides user with a button the redirect to home page.

## Features

* Home page showcases a rotating carousel that contains information and links to menu, book a table and events.
* The homepage navigation bar displaying the logo also provides links to Home, Menus, book a table and reviews.
* User can make an account and login from the right of the navigation bar.
* When logged in, users get access to create a booking or review and update their profile
* Users can edit and delete their bookings and reservations
* Every user action is accompanied by a corresponding message to ensure that users are promptly notified of any changes, updates or cancellations.

### Existing Features

* Home Page
    * Displays a navigation bar with logo displaying links, main heading on Hero carousel, about section, opening times and footer with contact details and social links. These are intentionally not active at this time.

![Home Page]()



![Book Now]()


* Logo
    * Logo was created using [Vista]() 

![Logo]()

* Navigation Bar
    * It differs if its a user or just a visitor

    * Navigation bar for a visitor

    ![Visitor]()

    * Navigation bar for a logged in user
    ![User]()


* Hero Carousel
    * 

![Carousel]()

* About Section
    * It contains a short description of Woodland Whispers Retreat and a short lake tale

![About]()

* Footer
    * Contains copyright information, creator and social links which are all linked to the creator of the website

![Footer](G)

* Sign up
    * User can create an account

![Sign Up]()

* Login
    * User can login into an account, if they have created one

![Login]()
![Login Message]()

* Logout
    * User can logout

![Logout]()


![Make a Reservation]()

* Booking Succesful
    * If booking is succesfull, user gets a notified message and an overview of the booking they just made.

![Booking Succesful]()

* Reservation List
    * Includes all of the user bookings, which have buttons to edit or delete bookings.

![Reservation Overview]()

* Already booked dates
    * User won't be able to make bookings if the restaurant is fully booked
    * Dates in the past are unavailable.

![Booked Dates]()

* Edit Booking
    * User can change their booking and save changes

![Edit Booking]()

* Delete Booking
    * User can delete their booking, before it is deleted it has to be confirmed.

![Delete Booking]()

* Alert messages
    * For every action there is an alert message to notify user
    * Here is one example

### Features Left to Implement 

* 

## Technologies Used

### Languages Used

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS3](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Databases Used

* [ElephantSQL](https://www.elephantsql.com/) - Postgres database
* [Cloudinary](https://cloudinary.com/) - Online static file storage

### Frameworks Used

* [Django](https://www.djangoproject.com/) - Python framework
* [Bootstrap 4.6.1](https://getbootstrap.com/docs/4.6/getting-started/introduction/) - CSS framework

### Programs Used

* [Github](https://github.com/) - Storing the code online
* [Gitpod](https://www.gitpod.io/) - To write the code.
* [Heroku](https://www.heroku.com/) - Used as the cloud-based platform to deploy the site.
* [Google Fonts](https://fonts.google.com/) - Import main font the website.
* [Figma](https://www.figma.com/) - Used to create wireframes and schemes
* [Am I Responsive](https://ui.dev/amiresponsive) - To show the website image on a range of devices.
* [Git](https://git-scm.com/) - Version control
* [Favicon Generator](https://realfavicongenerator.net/) - Used to create a favicon
* [JSHint](https://jshint.com/) - Used to validate JavaScript
* [W3C Markup Validation Service](https://validator.w3.org/) - Used to validate HTML
* [CSS Validation Service](https://jigsaw.w3.org/css-validator/) - Used to validate CSS
* [CI Python Linter](https://pep8ci.herokuapp.com/#) - Used to validate Python

## Deployment and Local Developement

Live deployment can be found on this [View Big T's Chophouse live website here]()

### Local Developement

#### How to Fork
1. Log in(or Sign Up) to Github
2. Go to repository for this project [Big T's Chophouse]()
3. Click the fork button in the top right corner

#### How to Clone
1. Log in(or Sign Up) to Github
2. Go to repository for this project [Big T's Chophouse]()
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type the following command in the terminal (after the git clone you will need to paste the link you copied in step 3 above)
6. Set up a virtual environment (this step is not required if you are using the Code Institute Template in GitPod as this will already be set up for you).
7. Install the packages from the requirements.txt file - run Command pip3 install -r requirements.txt

### ElephantSQL Database
[Big T's Chophouse]() is using [ElephantSQL](https://www.elephantsql.com/) PostgreSQL Database

1. Click Create New Instance to start a new database.
2. Provide a name (this is commonly the name of the project: tribe).
3. Select the Tiny Turtle (Free) plan.
4. You can leave the Tags blank.
5. Select the Region and Data Center closest to you.
6. Once created, click on the new database name, where you can view the database URL and Password.

### Cloudinary

### Heroku Deployment
* Log into [Heroku](https://www.heroku.com/) account or create an account.
* Click the "New" button at the top right corner and select "Create New App".
* Enter a unique application name
* Select your region
* Click "Create App"

#### Prepare enviroment and settings.py
* In your GitPod workspace, create an env.py file in the main directory.
* Add the DATABASE_URL value and your chosen SECRET_KEY value to the env.py file.
* Update the settings.py file to import the env.py file and add the SECRETKEY and DATABASE_URL file paths.
* Comment out the default database configuration.
* Save all files and make migrations.
* Add the Cloudinary URL to env.py
* Add the Cloudinary libraries to the list of installed apps.
* Add the STATIC files settings - the url, storage path, directory path, root path, media url and default file storage path.
* Link the file to the templates directory in Heroku.
* Change the templates directory to TEMPLATES_DIR
* Add Heroku to the ALLOWED_HOSTS list the format ['app_name.heroku.com', 'localhost']

#### Add the following Config Vars in Heroku:

* SECRET_KEY - This can be any Django random secret key
* CLOUDINARY_URL - Insert your own Cloudinary API key
* PORT = 8000
* DISABLE_COLLECTSTATIC = 1 - this is temporary, and can be removed for the final deployment
* DATABASE_URL - Insert your own ElephantSQL database URL here

#### Heroku needs two additional files to deploy properly

* requirements.txt
* Procfile

#### Deploy

1. Make sure DEBUG = False in the settings.py
2. Go to the deploy tab on Heroku and connect to GitHub, then to the required repository.
3. Scroll to the bottom of the deploy page and either click Enable Automatic Deploys for automatic deploys or Deploy Branch to deploy manually. Manually deployed branches will need re-deploying each time the GitHub repository is updated.
4. Click 'Open App' to view the deployed live site.

Site is now live

## Testing
Please see  [TESTING.md](TESTING.md) for all the detailed testing performed.

## References
### Docs

* [Stack Overflow](https://stackoverflow.com/)
* [Code Institute](https://learn.codeinstitute.net/dashboard)
* [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
* [Django docs](https://docs.djangoproject.com/en/4.2/releases/3.2/)
* [Django Allauth](https://django-allauth.readthedocs.io/en/latest/)
* [Django and Static Assets](https://devcenter.heroku.com/articles/django-assets)
* [Cloudinary](https://cloudinary.com/documentation/diagnosing_error_codes_tutorial)
* [Google](https://www.google.com/)

### Content

* 

### Acknowledgments

* I would like to thank my mentor for support and feedback throughout this project, Mitko Bachvarov.
* 