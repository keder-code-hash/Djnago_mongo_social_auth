from django.contrib import admin

from users.models.JwtTokwnModels import BlacklistedToken,OutstandingToken

admin.site.register(BlacklistedToken)
admin.site.register(OutstandingToken)
