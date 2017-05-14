from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, first_name, last_name, date_of_birth, address, city, state, country, mobile,
                     avatar, password, is_active, is_superuser, is_staff):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name,
                          date_of_birth=date_of_birth, address=address, city=city, state=state, country=country,
                          mobile=mobile, avatar=avatar, password=password, is_active=is_active,
                          is_superuser=is_superuser, is_staff=is_staff)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, date_of_birth, address, city, state, country,
                         mobile, avatar, password, is_active, is_superuser, is_staff):
        return self._create_user(username, email, first_name, last_name, date_of_birth, address, city, state, country,
                                 mobile, avatar, password, is_active, is_superuser, is_staff)
