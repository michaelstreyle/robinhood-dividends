# Robinhood Dividends with Django


## Objective

This project aims to build a Django web application that uses the Robhinhood API to access a user's portfolio and summarize the portfolio's holdings and dividend history. The application is hosted publicly on Google Cloud Platform using a Standard App Engine environment. The project serves as addtional practice with some of the Django functionality we learned in class, as well as diving deeper into more advanced webpages. 

*Disclaimer: I am new to Django/web development (other than pset6) and new to GCP, so some of the solutions used may not be the most efficient. Any and all suggestions welcome in that regard :)

## Important Notes


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*


- [Requirements and Dependencies](#requirements-and-dependencies)
- [Robinhood Class](#robinhood-class)
- [Database](#database)
- [Django Web Framework Overview](#django-web-framework-overview)
  - [Home](#home)
  - [Dividends](#dividends)
  - [Login and Logout](#login-and-logout)
- [Deployment to GCP](#deployment-to-gcp)
  - [Viewing the Deployment](#viewing-the-deployment)

- [Resources](#resources)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Requirements and Dependencies

This project used several requirements and dependencies. 

- Pandas
- Numpy
- Dask*
- [robin-stocks](https://robin-stocks.readthedocs.io/en/latest/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs)
- Google Cloud Platform Account
    - [Cloud SQL](https://cloud.google.com/sql/docs/mysql)
    - App Engine
    - DataStore
    - Google Cloud Storage Bucket

    - [ndb from google.cloud](https://cloud.google.com/appengine/docs/standard/python3/migrating-to-cloud-ndb)

- [Django 3](https://www.djangoproject.com/)


*required by future features


## Robinhood Class

The data for the Django application is pulled from a users Robinhood account using the robin_stocks python library.
For development purposes, the user's username and password can be specified in a .env file and accessed in the __init__ of the Robinhood class. 

```python
self.username = os.getenv('ROBIN_USERNAME')
self.password = os.getenv('ROBIN_PASSWORD')

```

However, when this application is deployed to Google Cloud, the credentials are stored in GCP's DataStore and accessed programmatically (discussed later)

The following methods are included in the Robinhood Class:
- get_holdings_df
- get_dividends
- dividend_summary
- show_value

The methods allow you to authenticate once, before using any of the methods. 

This class will be used to connect to Robinhood and populate the database for the DJango webapp.


## Database

The database for this project consists of a star schema and an independent table to track the portfolio value. 

![Database Schema](/images/database.png)



## Django Web Framework Overview

The web application has a home page, dividends page, recommendations page, as well as a Twitter link. 

### Home

At the top of the Home page is an Update button. This is discussed further down, but allows the data to be updated in the database and is also used by the cronjob to automatically update the data daily. The Home page also displays the current value of the portfolio as well as the current cash available. Then below the current value, there is a chart which displays the portfolio value over time. Finally, below the chart is an overview of the current holdings in the portfolio, including the tickers, current price, average cost, quantity, and current equity (current price x quantity). The holdings are sorted by highest equity.  I used a management command to load the portfolio into the database, and also included a --mock option to load fake data (seen in all these screenshots) for testing purposes. 

Here is a screenshot which shows an (zoomed out) overview of the home page. 
![Home](/images/home.png)


### Dividends

The main weakness in the Robinhood website/app is that it is quite difficult to find out a summary of the dividend payments you have received. This is quite a simple task, but something that is really useful to keep track of. This was the motivation behind the dividends page, which displays the dividend totals per year as well as the total dividends broken down by the Ticker symbols. Eventually, it would be cool to include a plot here, similar to the home page, but for yearly dividend income. However, that is not included here because there is not currently enough dividend history to create any usefulness from a plot. 

Here is a screenshot which shows an overview of the dividends page. 
![Dividends](/images/dividend.png)


### Login and Logout

One important aspect of this Django site is creating a login and logout page for user authentication. I learned several things while adding this functionality to my site including:

- Creating a login page
- Adding Login/Logout buttons to the Nav bar (changing to login/logout based on status)
- Managing user accounts 
- Requiring login before visiting pages with sensitive information
    - Using the @login_required decorator from Django in views.py

![Login](/images/login.png)



## Deployment to GCP 


This application is really only useful if I am able to use it on a device such as my phone or windows laptop (rather than linux desktop), so the biggest piece of this project that I was especially interested in working through was deploying my Django project to Google Cloud Platform. I decided to use GCP's Standard App Environment to deploy the application and a Cloud SQL MySQL server to host the database. Because Robinhood's API is still somewhat unofficial, there is not yet a great way to handle authentication other than using the username and password, which meant I had to find a way to securely store my credentials.

Several challenges arose during this deployment including:

- Securely managing my Robinhood Credentials
    - Solution: Using GCP's DataStore to store the credentials and a Settings class to retrieve the credentials from DataStore. This relies on Cloud NDB client library for Python 3. This turned into a rather elegant solution that I was glad to learn about because it exposed me to another GCP service. 
- Using App Engine Cron Jobs to update the database daily
    - This issue is what led to the creation of the Update button on the home page. This endpoint is what the cronjob uses to update the database on a daily basis

![Datastore](/images/datastore.png)

### Viewing the Deployment

I have created a login for those who are in my Advanced Python course and want to take a look at the deployed application...

The link to the live deployment is [here](https://robinhood-django.uc.r.appspot.com/)

**Login Credentials**


Username: csci-e-29

Password: First 8 characters of CSCI_SALT found in Canvas 

(Pset3-Student Embeddings Assignment - "3......5")




## Resources

- [Running Django on App Engine](https://cloud.google.com/python/django/appengine)
- [Django Documentation](https://docs.djangoproject.com/en/3.0/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
