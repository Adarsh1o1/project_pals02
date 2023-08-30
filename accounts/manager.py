from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, username, email, password=None, password2=None,  **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('password is required')
        email = self.normalize_email(email)
        user = self.model(email = email,username = username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, email, password=None, password2=None, **extra_fields):
        user = self.create_user(
            username,
            email,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    