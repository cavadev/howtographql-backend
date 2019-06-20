Howtographql Backend Example
===================


This project is an example of implementation for [howtographql backend](https://www.howtographql.com/graphql-python/0-introduction/) (Graphene-Python & Django).

## Overview

* **GraphQL Server Backend:** Run a backend with [`graphene-django`](https://github.com/graphql-python/graphene-django)
* **Custom Email Authentication:** Use a custom authentication backend class for authenticate with email or username.
* **JWT Authentication:** JSON Web Token authentication with  [`django-graphql-jwt`](https://github.com/flavors/django-graphql-jwt)
* **CORS:** Handling the server headers required for Cross-Origin Resource Sharing with [`django-cors-headers`](https://github.com/ottoyiu/django-cors-headers)
* **Compatible with Apollo Client Tutorial:** Works with GraphQL clients built in  [howtographql frontend](https://www.howtographql.com/react-apollo/0-introduction/) (React & Apollo)
* **SQLite:** Use the default Django SQLite database.
* **No Includes Subscriptions:** Doesn't support GraphQL subscriptions.

## Install

Clone the repo:

```sh
git clone https://github.com/cavadev/howtographql-backend.git
cd howtographql-backend
```

Use a virtual enviroment:

```sh
python3 -m venv env
source env/bin/activate
```
Then

```sh
pip install -r requirements.txt
python src/manage.py migrate
python src/manage.py migrate --run-syncdb
python src/manage.py runserver
```

And finally access to GraphiQL (in-browser IDE for exploring GraphQL) in http://localhost:8000/graphql/

## Relay

### Without Relay version

You can see the "Without Relay" version of this code in [Tag 0.1.0](https://github.com/cavadev/howtographql-backend/tree/0.1.0), and in your cloned repository with the next command:

```sh
git checkout tags/0.1.0
```

### With Relay version

You can see the "With Relay" version of this code in the master branch or in [Tag 0.2.0](https://github.com/cavadev/howtographql-backend/tree/0.2.0), and in your cloned repository with the next command:

```sh
git checkout master
```

or

```sh
git checkout tags/0.1.0
```

## Queries

### Users

* Create one user (return the new user and a valid JWT)

```graphql
mutation Signup {
  signup(
    email:"first.last@example.com",
    password:"123",
    firstName:"First",
    lastName:"Last"
  ){
    token
    user {
      username
      email
    }
  }
}
```

* Login

```graphql
mutation Login {
  login(
    username: "first.last@example.com",
    password:"123"
  ){
    token
    user {
      username
      email
    }
  }
}
```

### Links

* Create a new link (need JWT Authorization Header)

```graphql
mutation LinkMutation {
  createLink(
    url: "https://example.com/account",
    description: "Github Account"
  ){
    id
    url
    description
    created
    postedBy {
      id
      username
      email
    }
    votes {
      id
      user {
        id
      }
    }
  }
}
```

* Vote for a link (need JWT Authorization Header)

```graphql
mutation VoteMutation {
  createVote(linkId: 1){
    link {
      votes {
        id
        user {
          id
        }
      }
    }
    user {
      id
    }
  }
}
```

* Get a list of Links

```graphql
query getlinks {
  links {
    id
    created
    url
    description
    postedBy {
      id
      username
    }
    votes {
      id
      user {
        id
      }
    }
  }
  count
}
```

(*) For the queries that need a JWT Authorization Header you can use a REST client like [`insomnia`](https://insomnia.rest/graphql/)

(*) Tested on Python 3.6.

(*) To get the most of the project, please read the [tutorial](https://www.howtographql.com/graphql-python/0-introduction/).
