from django.contrib.auth.backends import ModelBackend

from .models import AgentCustomUserModel


class AgentCustomAuthBackend(ModelBackend):

	def authenticate(self, request, username=None, password=None, **kwargs):
		phone_number = kwargs['phone_number']
		try:
			user = AgentCustomUserModel.objects.get(phone_number=phone_number)
		except AgentCustomUserModel.DoesNotExist:
			pass

