from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import main
from flask_login import current_user


class AuthenticatedView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return 'sorry. your not authorized'


class HomeView(AdminIndexView):
	@expose('/')
	def index(self):
		return self.render('admin/index.html')


class pflanzlistetable(AuthenticatedView):
	main.app.app_context().push()
	can_create = True
	can_delete = True
	can_edit = True
	can_export = True
	can_set_page_size = 532


class obstsortentable(AuthenticatedView):
	main.app.app_context().push()
	can_create = True
	can_delete = True
	can_edit = True
	can_export = True
	can_set_page_size = 532

class imagetable(AuthenticatedView):
	main.app.app_context().push()
	can_create = True
	can_delete = True
	can_edit = True
	can_export = True
	can_set_page_size = 532