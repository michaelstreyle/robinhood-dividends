# Robinhood Dividends with Django


## Objective

This project aims to build a Django web application that uses the Robhinhood API to access a user's portfolio and summarize the portfolio's holdings and dividend history. The application is hosted publicly on Google Cloud Platform using a Standard App Engine environment. The project serves as addtional practice with some of the Django functionality we learned in class, as well as diving deeper into more advanced webpages. 

## Important Notes


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Requirements and Dependencies](#requirements-and-dependencies)
- [Robinhood Class](#robinhood-class)
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

![Database Schema](/robinhood/templates/robinhood/database.png)



## Viewing the Deployment

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
