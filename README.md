# register-database-api

An API to provide CRUD operations between sever and database. Currently the api is not hosted anywhere and will need to executed on a local machine.   The API will interact with the postgres database hosted on AWS providing get and list operations for the scope of Sprint 1. Currently the API is using the other repository, we will eventually decommission. 
 
## Getting Started

A good understanding of REST principles and building flask applications would be beneficial when working with this code base. 


### Prerequisites

Python 3 installed on the machine

For Mac OS 

```
Install homebrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
```

### Running the API locally

A step by step series of examples that tell you how to get a development env running

Inside the repository create a virtualenv
```
python3 -m venv .venv
```
Activate virtualenv
```bash
 source .venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Export the database uri
```bash
DATABASE_URL=<uri>
```

Start flask web application

```bash
 python register_database_api/api.py     
```

Example Build:
```bash
http://127.0.0.1:5000/api/v1/products/all

------ Returns ------------
[
  {
    "count": 100, 
    "creation": "Thu, 30 Jan 2020 18:24:50 GMT", 
    "id": "722bfe1f-68fb-476b-bdaa-e8c9b91fb294", 
    "lookup-code": "lookupcode1"
  }, 
  {
    "count": 125, 
    "creation": "Thu, 30 Jan 2020 18:24:50 GMT", 
    "id": "963ceeed-3318-4a2e-8537-096a3c18ca22", 
    "lookup-code": "lookupcode2"
  }, 
  {
    "count": 150, 
    "creation": "Thu, 30 Jan 2020 18:24:50 GMT", 
    "id": "648d5dc3-252d-434e-910c-dcaed2349435", 
    "lookup-code": "lookupcode3"
  }
]

```


### Coding style 

[PEP8 style](https://www.python.org/dev/peps/pep-0008/)

[Google Style Guide](http://google.github.io/styleguide/pyguide.html)


## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Flask](https://palletsprojects.com/p/flask/) - lightweight python web framework

## Version
0.0.1

