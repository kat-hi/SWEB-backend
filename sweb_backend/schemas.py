from marshmallow_sqlalchemy import TableSchema

class Tree(TableSchema):
	class Meta:
		fields = ("BaumNr", "BaumID", "Pflanzreihe", "PflanzreihePosition", "SortenID", "Sorte", "Frucht", "PatenID", "Longitude", "Latitude")


class Sorts(TableSchema):
	class Meta:
		fields = ("id", "frucht", "sorte", "andereNamen", "herkunft", "groesse", "beschreibung", "reifezeit",
		          "geschmack", "verwendung", "lager", "verbreitung")


class Treecoordinates(TableSchema):
	class Meta:
		fields = ("BaumNr", "Longitude", "Latitude")


class Admin(TableSchema):
	class Meta:
		fields = ("id", "email")


class Image(TableSchema):
	class Meta:
		fields = ("id", "uri")

