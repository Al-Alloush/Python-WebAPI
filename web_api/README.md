# python-API using Flask
---
## add flask jwt(Json Web Token) extended to get Authentication token
- install flask_jwt_extended library
- add configration in app.py
- create Test class to test the Authentication
- add TestAuthentication endpoint in API
- add token black list in redis database.
- add some jwt functions in app.py
- logout, expire the token time
- add the Authorization to gives users permission to access a resource.


Note: change find_user parameters.


---
## add account conformation
- create an asccount in sendGrid website
- install sendGrid library
- add new token column in user table
- add new endpoint in API
- add EmailSender class to send activation email using sendGrid API
- create activation link in controllers.UserRegister class

--
## add unittest
### for synchronous applicaton we use **unittest**, but for asynchronous applicaton we use **pytest**
[Link ,pytest](https://docs.pytest.org/en/stable/contents.html) has an asymc library, that allow us to uest our code better.

and big difference between **Unittest** and **pytest** is that, the **pytest** doesnt require classess

in the same directory of test file ```> python -m pytest -v``` to test the code

---

## we can't testing API resources, for that I create a new files *_crud.py (CRUD) it's like the controller in asp.net



---
## user Types:
- 1 = SuperAdmin
- 2 = Admin
- 3 = Editor
- 4 = User




