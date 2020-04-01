from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import main
from flask_login import current_user


# class AuthenticatedView(ModelView):
# 	def is_accessible(self):
# 		return current_user.is_authenticated
#
# 	def inaccessible_callback(self, name, **kwargs):
# 		return 'sorry. your not authorized'


# class WelcomeView(AdminIndexView):
# 	@expose('/')
# 	def index(self):
# 		return self.render('admin/logout.html')
#
#
# class LogoutView(AuthenticatedView):
# 	@expose('/logout/')
# 	def index(self):
# 		return self.render('admin/logout.html')


class pflanzlistetable(ModelView):
	main.app.app_context().push()
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = 532


class obstsortentable(ModelView):
	main.app.app_context().push()
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = 532


class imagetable(ModelView):
	main.app.app_context().push()
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = 532
