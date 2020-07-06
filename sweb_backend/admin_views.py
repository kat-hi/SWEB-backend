from flask_admin.contrib.sqla import ModelView
from . import main
from flask_login import current_user


class AuthenticatedView(ModelView):
	def is_accessible(self):
		main.app.logger.info('CURRENT USER AUTH VIEW: ' + str(current_user))
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return 'sorry. your not authorized'


class pflanzlistetable(AuthenticatedView):
	main.app.app_context().push()
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = True


class obstsortentable(AuthenticatedView):
	main.app.app_context().push()
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = True


class imagetable(AuthenticatedView):
	main.app.app_context().push()
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = True
