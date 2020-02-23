# register-database-api

An API to provide CRUD operations between sever and database. The API runtime environment is a custom docker container that can be found in the Dockerfile. This container executes in a dyno runtime environment.  The API will interact with the postgres database hosted on AWS providing CRUD operations.  
 
## Getting Started

A good understanding of REST principles and building flask applications would be beneficial when working with this code base. 


### Prerequisites

1. Python 3 installed on the machine
2. Docker 

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

### Example API Calls Products

***Creating record:***
```bash
  curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"lookup_code":"lookupcode4","count":"400"}' \
  http://https://peaceful-bastion-45955.herokuapp.com/api/v1/products/create

```

***Get record:***
```bash
curl http://https://peaceful-bastion-45955.herokuapp.com/api/v1/products\?lookup\=lookupcode1
```

***Delete record:***
```bash
  curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"lookup_code":"lookupcode4","id":"8fb27442-53a4-11ea-92cf-acde48001122"}' \
  http://https://peaceful-bastion-45955.herokuapp.com/api/v1/products/delete
```

### Employee Record Conventions:

***Classification:***
1. General Manager
2. Shift Manager
3. Cashier

***When managerid is ''***
Defaults managerid to 00000000-0000-0000-0000-000000000000 indicating no manager is present for user. 

### Example API Calls Employee

***Create record:***
```bash
  curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
        "active": true,
        "classification": 3,
        "employeeid": 34523,
        "firstname": "Bossom",
        "lastname": "Roller",
        "managerid": "8c460ba4-6358-4a78-9493-850ab8c43545", or  "managerid": ''
        "password": "notnew56"
      }' \
  http://https://peaceful-bastion-45955.herokuapp.com/api/v1/employee/create

```
***Delete record:***
```bash
  curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
        "id": "8e678603-9a42-457e-8dfb-12e0cb0bdd32"
      }' \
  http://https://peaceful-bastion-45955.herokuapp.com/api/v1/employee/delete
```
***List records:***
```bash
curl http://https://peaceful-bastion-45955.herokuapp.com/api/v1/employee/all
```
***Get Record:***
```bash
curl http://https://peaceful-bastion-45955.herokuapp.com/api/v1/employee?employeeid=123456
```

### Deployment Locally
In the docker file replace database_uri with the actual uri 
```dockerfile
ENV DATABASE_URL '<database_uri>'
```

At the root of this repository execute the command:
```bash
docker build -t dev-api .
```

Start the API:
```bash
docker run -it initial-api
```


### Coding style 

[PEP8 style](https://www.python.org/dev/peps/pep-0008/)

[Google Style Guide](http://google.github.io/styleguide/pyguide.html)



## Built With

* [Flask](https://palletsprojects.com/p/flask/) - lightweight python web framework
* [Docker](https://www.docker.com/resources/what-container) - container run time for flask application

## Version
0.0.1
