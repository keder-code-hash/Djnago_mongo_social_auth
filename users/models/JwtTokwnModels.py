from djongo import models
from users.models.Users import Users


class OutstandingToken(models.Model):
    _id = models.ObjectIdField()
    user = models.EmbeddedField(
        model_container= Users
    )

    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()

    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:  
        abstract = False
        db_table = "OutstandingToken"
        ordering = ("user",)

    def __str__(self):
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class BlacklistedToken(models.Model):
    _id = models.ObjectIdField()
    token = models.EmbeddedField(model_container= OutstandingToken)

    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        abstract = False
        db_table = "BlacklistedToken"

    def __str__(self):
        return f"Blacklisted token for {self.token.user}"
