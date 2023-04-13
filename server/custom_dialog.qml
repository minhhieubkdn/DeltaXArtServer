import QtQuick
import QtQuick.Controls

//import "../controls"
Item {
    id: cd
    width: 0
    height: 0

    property color bgColor: "transparent"
    property alias bgRadius: rMain.radius
    property alias tiText: ti.text
    property real activeWidth: 300
    property real activeHeight: 200

    signal accepted
    signal rejected

    function open() {
        cd.width = activeWidth
        cd.height = activeHeight
    }

    function close() {
        cd.width = 0
        cd.height = 0
    }

    Rectangle {
        id: rMain
        anchors.fill: parent
        color: "transparent"

        Rectangle {
            id: rTop
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.bottom: rButtons.top

            TextInput {
                id: ti
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width * 0.8
                height: 40
                text: "Delta X S D400"

            }
        }

        Rectangle {
            id: rButtons
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: parent.height * 0.25

            CustomButton {
                id: btOk
                anchors.left: parent.left
                anchors.top: parent.top
                width: parent.width * 0.5
                height: parent.height
                onClicked: {
                    close()
                    accepted()
                }
            }

            CustomButton {
                id: btCancel
                anchors.right: parent.right
                anchors.top: parent.top
                width: parent.width * 0.5
                height: parent.height
                onClicked: {
                    close()
                    rejected()
                }
            }
        }
    }
}
