# The Flask Admin

Flask commes with a small back office admin that helps a lot when building your API.

The flask admin will automatically allow you to create, update, delete any of your database information.

Here a 8 min video explaining the Flask Admin: [https://www.youtube.com/watch?v=ysdShEL1HMM](https://www.youtube.com/watch?v=ysdShEL1HMM)

## Adding your models to your Flask admin

With just on line of code you can integrate your model into the Flask Admin, for example if you have a `Car` model you can add the model into the admin like this:
```py
from models import Car
...
admin.add_view(ModelView(Car, db.session))
```

But you have ot add those two lines inside the `admin.py` file like this:

```py
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import db, Car # < ------ Import the model

def setup_admin(app):
    admin = Admin(app, name='your_admin_name', template_mode='bootstrap3')
    admin.add_view(ModelView(Car, db.session)) # < ------ Add the model to the admin
```

You can add as many models as you like like this:

```py
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import db, Car, Person, Patient # < ------ Import the model

def setup_admin(app):
    admin = Admin(app, name='your_admin_name', template_mode='bootstrap3')
    admin.add_view(ModelView(Car, db.session)) # < ------ Add the model to the admin
    admin.add_view(ModelView(Person, db.session)) # < ------ Add the model to the admin
    admin.add_view(ModelView(Pattient, db.session)) # < ------ Add the model to the admin
```


