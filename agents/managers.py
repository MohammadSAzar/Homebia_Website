from django.contrib.auth.base_user import BaseUserManager


class AgentCustomUserManager(BaseUserManager):
	def create_user(self, phone_number, password=None, **other_fields):
		if not phone_number:
			raise ValueError('Mobile is required!')
		user = self.model(phone_number=phone_number, **other_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, phone_number, password=None, **other_fields):
		pass


