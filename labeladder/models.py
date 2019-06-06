from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.TextField(unique=True)

    def __str__(self):
        return self.user_id


class FacebookPage(models.Model):
    access_token = models.TextField()
    original_id = models.TextField()

    def __str__(self):
        return self.original_id


class FacebookLabel(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, )
    page = models.ForeignKey("FacebookPage", on_delete=models.CASCADE)
    label_id = models.TextField()

    def __str__(self):
        return "owner {} \npage {} \n label_id {}".format(self.owner, self.page, self.label_id)