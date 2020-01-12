from flask_admin.contrib.sqla import ModelView
import main

class pflanzlistetable(ModelView):
	main.app.app_context().push()
	can_delete = False
	can_edit = False
	can_export = True
	can_set_page_size = 532


class obstsortentable(ModelView):
	main.app.app_context().push()
	can_delete = False
	can_edit = False
	can_export = True
	can_set_page_size = 532


class patentable(ModelView):
	main.app.app_context().push()
	can_edit = False
	can_export = True
	can_set_page_size = 532
