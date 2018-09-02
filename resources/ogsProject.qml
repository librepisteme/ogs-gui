import QtQuick.XmlListModel 2.0

XmlListModel {
	id: xmlModel
	xml: url
	XmlRole { name: "mesh"; query: mesh/string() }
	XmlRole { name: "geometry"; query: mesh/geometry() }
}

