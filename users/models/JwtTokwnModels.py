from djongo import models 


class OutstandingToken(models.Model):
    _id = models.ObjectIdField()
    
    user_id = models.CharField(max_length=200,blank=False,null=False)

    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()

    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:  
        abstract = False
        db_table = "OutstandingToken"
        ordering = ("created_at",)

    def __str__(self):
        return "Token for {} ({})".format(
            self.user_id,
            self.jti,
        )


class BlacklistedToken(models.Model):
    _id = models.ObjectIdField()

    token = models.CharField(max_length=100,blank=False,null=False)

    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        abstract = False
        db_table = "BlacklistedToken"

    def __str__(self):
        return f"Blacklisted token for {self.token}"
