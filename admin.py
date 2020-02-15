from flask_admin.contrib.sqla import ModelView
import main
from flask_login import current_user


class AuthenticatedView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		# redirect to login page if user doesn't have access
		return 'sorry. your not authorized'


class pflanzlistetable(AuthenticatedView):
	main.app.app_context().push()
	can_create = False
	can_delete = False
	can_edit = False
	can_export = True
	can_set_page_size = 532


class obstsortentable(AuthenticatedView):
	main.app.app_context().push()
	can_create = False
	can_delete = False
	can_edit = False
	can_export = True
	can_set_page_size = 532


class patentable(AuthenticatedView):
	main.app.app_context().push()
	can_edit = False
	can_export = True
	can_set_page_size = 532
