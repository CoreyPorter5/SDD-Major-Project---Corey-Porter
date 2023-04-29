import sys
import os
import hashlib
import json
from os import path
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QLabel, QLineEdit, QWidget, QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtCore import Qt, QTimer, QTime, QFile, QTextStream, QPoint, QRect, QPointF, QRectF, pyqtSignal, QObject
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPainter, QPen
import datetime as dt
import requests

#Sets the variables of the API and makes them global so they are able to be accessed below
global BASE_URL
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

global API_KEY
API_KEY = "2ffda1093e0831b26d053869237e7d95"

global CITY
CITY = "Sydney"



#checks a text file to see how many emails there are
with open('emailcount.txt', 'r') as reader:
            global email_number
            email_number_int=[line.rstrip('\n') for line in reader]  
            email_number = int(email_number_int[0])

with open('distance1.txt', 'w') as f:
    f.write('0')

            




        

#class for the login page

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        username_label = QLabel("Email:", self)
        username_label.move(76,40)
        

        self.username_input = QLineEdit(self)
        self.username_input.setFixedSize(210, 25)
        self.username_input.move(120, 40)
    


        password_label = QLabel("Password:", self)
        password_label.move(50,80)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(210, 25)
        self.password_input.move(120, 80)
        


        self.login_button = QPushButton ("Login", self)
        self.login_button.move(163, 110)
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.confirm_login)
        self.login_button.clicked.connect(self.login)


        create_account = QPushButton ("Create One", self)
        create_account.setFixedSize(110, 30)
        create_account.move(200, 200)
        create_account.clicked.connect(self.account)

        create_account_label = QLabel("Need an account?", self)
        create_account_label.setWordWrap(True)
        create_account_label.setGeometry(50,50,120,50)
        create_account_label.move(90, 188)


        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Login')
        self.show()
        
    
    #function that gets called when the user presses login
    def login(self):
        global number
        number = -1
           

        with open("database.json", "r") as ff:
            data = json.load(ff)
        
        for i in range(email_number):  
            
            
            check_email = (data["userdata"][number + 1]["email"])
            check_password = (data["userdata"][number + 1]["password"])
            number = number + 1
            password_0 = hashlib.sha256(password.encode()).hexdigest()
    
              
        
            if check_email == email and check_password == password_0:
                self.login_window = GolfTracker()
                self.login_window.show()
                self.close()
                
                

    def account(self):
        self.account_create = CreateAccount()
        self.account_create.show()
        self.close()


    #confirms user has inputted an email and password before allowing them to confirm
    
    def confirm_login(self):
        global email
        global password
        email = self.username_input.text()
        password = self.password_input.text()
        self.username_input.clear()
        self.password_input.clear()
        global hashed_password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        

    def update_confirm_login(self):
        email = self.username_input.text()
        password = self.password_input.text()
        if email and password:
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)

    def keyPressEvent(self, event):
        self.update_confirm_login()








#class for account creation

class CreateAccount(QWidget):
        

    def __init__(self):
        super().__init__()


        back = QPushButton("Back", self)
        back.move(310, 215)
        back.clicked.connect(self.back)

        self.create_email = QLabel("Enter an email: ", self)
        self.create_email.move(30, 30)
        self.create_email_input = QLineEdit(self)
        self.create_email_input.move(105, 27)
        

        self.create_password = QLabel("Create password: ", self)
        self.create_password.move(17, 70)
        self.create_password_input = QLineEdit(self)
        self.create_password_input.move(105, 67)
        self.create_password_input.setEchoMode(QLineEdit.Password)


        

        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Create Account')
        
        
        self.confirm_account = QPushButton("Confirm", self)
        self.confirm_account.move(130, 110)
        self.confirm_account.setEnabled(False)
        self.confirm_account.clicked.connect(self.show_confirm_msg)
        self.confirm_account.clicked.connect(self.confirm_signup)
        self.confirm_account.clicked.connect(self.back)

        self.setWindowTitle("Create Account")


    # create message box

    def show_confirm_msg(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Account confirmed!")
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Create Account')
        self.show()

    #back button

    def back(self):
        self.login_window = Login()
        self.login_window.show()
        self.close()

    #confirms user has inputted an email and password before allowing them to confirm
    
    def confirm_signup(self):
        global email_number
        email_number = email_number + 1
        email_create = self.create_email_input.text()
        password_create = self.create_password_input.text()
        self.create_email_input.clear()
        self.create_password_input.clear()
        hashed_create_password = hashlib.sha256(password_create.encode()).hexdigest()
        
        
        
        #opens email number text file and writes new email count over it depending on if a new email has been entered

        with open('emailcount.txt', 'w') as reader:
            reader.write(str(email_number))
        

        #open json file and append a new email and new encrypted password to it
         
        def write_json(data, filename="database.json"): 
            with open (filename, "w") as f:
                json.dump(data, f, indent=4)
                
        

        with open ("database.json") as json_file:
            data = json.load(json_file)
            temp = data["userdata"]
            y = {"email": email_create, "password": hashed_create_password}
            temp.append(y) 
               
        write_json(data)

                             
            

    def update_confirm_account(self):
        email = self.create_email_input.text()
        password = self.create_password_input.text()
        if email and password:
            self.confirm_account.setEnabled(True)
        else:
            self.confirm_account.setEnabled(False)

    def keyPressEvent(self, event):
        self.update_confirm_account()











#class for the golf tracker menu

class GolfTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        input_button = QPushButton ("Enter Club Distances", self)
        input_button.move(5, 15)
        input_button.setFixedSize(160, 25)
        input_button.clicked.connect(self.enter_distances)

        course_label = QLabel("Select Course:", self)
        course_label.move(15, 60)

        course_selector = QComboBox(self)
        course_selector.addItem("Bondi Golf Course")
        course_selector.move(103, 65)
        course_selector.setFixedSize(160, 25)

        track_game = QPushButton ("Track my game", self)
        track_game.move(7, 110)
        track_game.setFixedSize(130, 70)
        track_game.clicked.connect(self.tracker)

        logout_button = QPushButton ("Logout", self)
        logout_button.move(295, 220)
        logout_button.clicked.connect(self.logout)

        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Golf Tracker')
        self.show()

#function to send the user to the tracker
    def tracker(self):
        self.tracker_menu = Tracker()
        self.tracker_menu.show()
        self.close()

#function gets called when a user presses logout
    def logout(self):
        self.login_window = Login()
        self.login_window.show()
        self.close()

#function gets called when a user presses enter distances
    def enter_distances(self):
        self.login_window = Distance()
        self.login_window.show()
        self.close()









#class for the distance inputs

class Distance(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        sand_wedge = QLabel("Sand Wedge: ", self)
        sand_wedge.move(15,15)
        global sand_wedge_input
        sand_wedge_input = QLineEdit(self)
        sand_wedge_input.setMaxLength(3)
        sand_wedge_input.setText("45")
        sand_wedge_input.move(90, 10)
        sand_wedge_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        sand_wedge_input.setValidator(validator)
        

        pitching_wedge = QLabel("Pitching Wedge: ", self)
        pitching_wedge.move(5, 60)
        global pitching_wedge_input
        pitching_wedge_input = QLineEdit(self)
        pitching_wedge_input.setMaxLength(3)
        pitching_wedge_input.setText("75")
        pitching_wedge_input.move(90, 55)
        pitching_wedge_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        pitching_wedge_input.setValidator(validator)
        

        nine_iron = QLabel("9 Iron: ", self)
        nine_iron.move(50, 105)
        global nine_iron_input
        nine_iron_input = QLineEdit(self)
        nine_iron_input.setMaxLength(3)
        nine_iron_input.setText("91")
        nine_iron_input.move(90, 100)
        nine_iron_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        nine_iron_input.setValidator(validator)

        eight_iron = QLabel("8 Iron: ", self)
        eight_iron.move(50, 150)
        global eight_iron_input
        eight_iron_input = QLineEdit(self)
        eight_iron_input.setMaxLength(3)
        eight_iron_input.setText("110")
        eight_iron_input.move(90, 145)
        eight_iron_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        eight_iron_input.setValidator(validator)

        seven_iron = QLabel("7 Iron: ", self)
        seven_iron.move(50, 195)
        global seven_iron_input
        seven_iron_input = QLineEdit(self)
        seven_iron_input.setMaxLength(3)
        seven_iron_input.setText("121")
        seven_iron_input.move(90, 190)
        seven_iron_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        seven_iron_input.setValidator(validator)

        #second collumn

        six_iron = QLabel("6 Iron: ", self)
        six_iron.move(250,15)
        global six_iron_input
        six_iron_input = QLineEdit(self)
        six_iron_input.setMaxLength(3)
        six_iron_input.setText("130")
        six_iron_input.move(290, 10)
        six_iron_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        six_iron_input.setValidator(validator)

        five_iron = QLabel("5 Iron: ", self)
        five_iron.move(250, 60)
        global five_iron_input
        five_iron_input = QLineEdit(self)
        five_iron_input.setMaxLength(3)
        five_iron_input.setText("141")
        five_iron_input.move(290, 55)
        five_iron_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        five_iron_input.setValidator(validator)

        four_iron = QLabel("4 Iron: ", self)
        four_iron.move(245, 105)
        global four_iron_input
        four_iron_input = QLineEdit(self)
        four_iron_input.setMaxLength(3)
        four_iron_input.setText("150")
        four_iron_input.move(290, 100)
        four_iron_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        four_iron_input.setValidator(validator)

        three_wood = QLabel("3 Wood: ", self)
        three_wood.move(245, 150)
        global three_wood_input
        three_wood_input = QLineEdit(self)
        three_wood_input.setMaxLength(3)
        three_wood_input.setText("169")
        three_wood_input.move(290, 145)
        three_wood_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        three_wood_input.setValidator(validator)

        driver = QLabel("Driver: ", self)
        driver.move(250, 195)
        global driver_input
        driver_input = QLineEdit(self)
        driver_input.setMaxLength(3)
        driver_input.setText("190")
        driver_input.move(290, 190)
        driver_input.setFixedSize(40, 30)
        validator = QtGui.QIntValidator()
        driver_input.setValidator(validator)

        save_distances = QPushButton("Save", self)
        save_distances.move(150 , 225)
        save_distances.setFixedSize(90, 20)
        save_distances.clicked.connect(self.save_distances)
        save_distances.clicked.connect(self.exit_save_distances)


        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Distances in meters')
        self.show()

#function gets called when user presses save distances
    def exit_save_distances(self):
        self.login_window = GolfTracker()
        self.login_window.show()
        self.close()

    def save_distances(self):
        global sand_wedge_distance
        sand_wedge_distance = sand_wedge_input.text()
       
        global pitching_wedge_distance
        pitching_wedge_distance = pitching_wedge_input.text()
        
        global nine_iron_distance
        nine_iron_distance = nine_iron_input.text()
        
        global eight_iron_distance
        eight_iron_distance = eight_iron_input.text()
        
        global seven_iron_distance
        seven_iron_distance = seven_iron_input.text()
        
        #second collum

        global six_iron_distance
        six_iron_distance = six_iron_input.text()
        
        global five_iron_distance
        five_iron_distance = five_iron_input.text()
        
        global four_iron_distance
        four_iron_distance = four_iron_input.text()

        global three_wood_distance
        three_wood_distance = three_wood_input.text()
        
        global driver_distance
        driver_distance = driver_input.text()
        







#class for the tracker

class Tracker(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hole1_button= QPushButton("Hole 1 ", self)
        hole1_button.move(35, 10)
        hole1_button.clicked.connect(self.hole1)

        hole2_button= QPushButton("Hole 2 ", self)
        hole2_button.move(35, 40)
        hole2_button.clicked.connect(self.hole2)

        hole3_button= QPushButton("Hole 3 ", self)
        hole3_button.move(35, 70)
        hole3_button.clicked.connect(self.hole3)

        hole4_button= QPushButton("Hole 4 ", self)
        hole4_button.move(35, 100)
        hole4_button.clicked.connect(self.hole4)

        hole5_button= QPushButton("Hole 5 ", self)
        hole5_button.move(35, 130)
        hole5_button.clicked.connect(self.hole5)

        hole6_button= QPushButton("Hole 6 ", self)
        hole6_button.move(35, 160)
        hole6_button.clicked.connect(self.hole6)

        hole7_button= QPushButton("Hole 7 ", self)
        hole7_button.move(35, 190)
        hole7_button.clicked.connect(self.hole7)

        hole8_button= QPushButton("Hole 8 ", self)
        hole8_button.move(35, 220)
        hole8_button.clicked.connect(self.hole8)

        hole9_button= QPushButton("Hole 9 ", self)
        hole9_button.move(35, 250)
        hole9_button.clicked.connect(self.hole9)

        back_button = QPushButton("Back", self)
        back_button.move(35, 280)
        back_button.setStyleSheet("background-color: black; color: white;")
        back_button.clicked.connect(self.exit_hole_selection)



        self.setGeometry(300, 300, 150, 310)
        self.setWindowTitle('Bondi Golf Course Tracker')
        self.show()

    def exit_hole_selection(self):
        self.login_window = GolfTracker()
        self.login_window.show()
        self.close()


    #graphical hole interface

    def hole1(self):
        self.login_window = HoleOne(image_path='hole1.png')
        self.login_window.show()
        self.close()

    def hole2(self):
        self.login_window = HoleTwo(image_path='hole2.png')
        self.login_window.show()
        self.close()

    def hole3(self):
        self.login_window = HoleThree(image_path='hole3.png')
        self.login_window.show()
        self.close()

    def hole4(self):
        self.login_window = HoleFour(image_path='hole4.png')
        self.login_window.show()
        self.close()

    def hole5(self):
        self.login_window = HoleFive(image_path='hole5.png')
        self.login_window.show()
        self.close()

    def hole6(self):
        self.login_window = HoleSix(image_path='hole6.png')
        self.login_window.show()
        self.close()
    
    def hole7(self):
        self.login_window = HoleSeven(image_path='hole7.png')
        self.login_window.show()
        self.close()

    def hole8(self):
        self.login_window = HoleEight(image_path='hole8.png')
        self.login_window.show()
        self.close()

    def hole9(self):
        self.login_window = HoleNine(image_path='hole9.png')
        self.login_window.show()
        self.close()
    











#Class for the pin
    
class Pin(QGraphicsItem):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        

    def boundingRect(self):
        return QRectF(self.x-5, self.y-5, 10, 10)

    def paint(self, painter, option, widget):
        painter.setBrush(Qt.green)
        painter.drawEllipse(QPointF(self.x, self.y), 5, 5)












#Class for Hole 1

class HoleOne(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 1 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(200)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(200)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 820)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(335, 820)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.1659 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver and aim for the fairway')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_2 = HoleTwo(image_path="hole2.png")
        self.hole_2.show()
        self.close()











#Class for hole 2

class HoleTwo(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 2 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(200)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(200)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 960)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(380, 960)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.13115 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver and aim for the fairway')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_3 = HoleThree(image_path="hole3.png")
        self.hole_3.show()
        self.close()








#Class for hole 3

class HoleThree(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 3 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(200)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(200)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 920)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(390, 920)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.134 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver and aim for the fairway')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_4 = HoleFour(image_path="hole4.png")
        self.hole_4.show()
        self.close()








#Class for hole 4


class HoleFour(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 4 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(200)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(200)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 950)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(295, 950)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.1681 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver and aim for the fairway')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_5 = HoleFive(image_path="hole5.png")
        self.hole_5.show()
        self.close()

        







#Class for hole 5



class HoleFive(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 5 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(140)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(105)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 950)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(340, 950)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.297 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_6 = HoleSix(image_path="hole6.png")
        self.hole_6.show()
        self.close()








#Class for hole 6



class HoleSix(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 6 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(140)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(105)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 930)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(345, 930)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.120806 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_7 = HoleSeven(image_path="hole7.png")
        self.hole_7.show()
        self.close()













#Class for hole 7



class HoleSeven(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 7 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(140)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(105)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 950)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(340, 950)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.1644581105 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_8 = HoleEight(image_path="hole8.png")
        self.hole_8.show()
        self.close()









#Class for hole 8



class HoleEight(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 8 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(140)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(105)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 925)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Next Hole", self)
        self.next_hole.move(350, 925)
        self.next_hole.setStyleSheet("background-color: green; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.13726 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_9 = HoleNine(image_path="hole9.png")
        self.hole_9.show()
        self.close()








#Class for hole 9



class HoleNine(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowTitle('Hole 9 - Bondi')
        self.initUI()
        self.hide()
        
        
        
    def initUI(self):
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene, self)
        pixmap = QPixmap(self.image_path)
        scene.addPixmap(pixmap)
        view.setSceneRect(QRectF(pixmap.rect()))
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setFixedSize(pixmap.width(), pixmap.height()) 
        self.setFixedSize(pixmap.width(), pixmap.height()) 
        
        
        global distance
        distance = 0
        self.distance = QLabel("Distance : " + str(distance), self)
        self.distance.move(10, 5)

        self.wind_speed = QLabel("Wind speed: ", self)
        self.wind_speed.move(10, 25)

        self.wind_direction = QLabel("Wind direction: ", self)
        self.wind_direction.move(10, 45)

        global recommended_club
        recommended_club = " "
        self.club_recommendation = QLabel("Use:" + str(recommended_club) ,self)
        self.club_recommendation.move(10, 65)
        self.club_recommendation.setFixedWidth(140)
        self.club_recommendation.setStyleSheet("font-weight: bold; color: white;")


        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind_speed_var = response['wind']['speed']
        degrees = response['wind']['deg']
        self.wind_speed.setText('Wind speed: '+ str(wind_speed_var) + 'm/s')
        self.wind_speed.setFixedWidth(105)


        if degrees >= 337.5 or degrees < 22.5:
            self.wind_direction.setText("Wind direction: N")
        elif degrees >= 22.5 and degrees < 67.5:
            self.wind_direction.setText("Wind direction: NE")
        elif degrees >= 67.5 and degrees < 112.5:
            self.wind_direction.setText("Wind direction: E")
        elif degrees >= 112.5 and degrees < 157.5:
            self.wind_direction.setText("Wind direction: SE")
        elif degrees >= 157.5 and degrees < 202.5:
            self.wind_direction.setText("Wind direction: S")
        elif degrees >= 202.5 and degrees < 247.5:
            self.wind_direction.setText("Wind direction: SW")
        elif degrees >= 247.5 and degrees < 292.5:
            self.wind_direction.setText("Wind direction: W")
        elif degrees >= 292.5 and degrees < 337.5:
            self.wind_direction.setText("Wind direction: NW")
            


        with open('distance1.txt', 'r') as reader:
            distance_int=[line.rstrip('\n') for line in reader]  
            distance = (float(distance_int[0]))
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_label)
            self.timer.start(100)
            
        
        self.back = QPushButton("Back", self)
        self.back.move(5, 925)
        self.back.setStyleSheet("background-color: red; color: white;")
        self.back.clicked.connect(self.back1)

        self.next_hole = QPushButton("Finish", self)
        self.next_hole.move(325, 925)
        self.next_hole.setStyleSheet("background-color: black; color: white;")
        self.next_hole.clicked.connect(self.nexthole)
    

        self.pin = None
        self.line = None
        self.line_start_point = None

        view.mousePressEvent = self.onMousePress
        view.mouseMoveEvent = self.onMouseMove
        view.mouseReleaseEvent = self.onMouseRelease

        self.setCentralWidget(view)
        self.show()

    def update_label(self):
        # Update the QLabel text with the current time
        self.distance.setText('Distance: '+ str(round(distance, 2)) + ' m')



    def onMousePress(self, event):
        if event.button() == Qt.LeftButton:
            if not self.pin:
                x = event.pos().x()
                y = event.pos().y()
                self.pin = Pin(x, y)
                scene = self.centralWidget().scene()
                scene.addItem(self.pin)
            else:
                self.line_start_point = event.pos()
                self.pin_pos = event.pos()
                
        elif event.button() == Qt.RightButton:
            global distance
            distance = 0
            with open('distance1.txt', 'w') as f:
                f.write('0')
            if self.line:
                scene = self.centralWidget().scene()
                scene.removeItem(self.line)
                self.line = None
                self.line_start_point = None
                
                
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.pin:
                scene = self.centralWidget().scene()
                scene.removeItem(self.pin)
                self.pin = None
                self.pin_start_point = None
            


    def onMouseMove(self, event):
        if self.line_start_point:
            if not self.line:
                scene = self.centralWidget().scene()
                self.line = scene.addLine(self.line_start_point.x(), self.line_start_point.y(),
                                          event.pos().x(), event.pos().y(),
                                          QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                self.line.setLine(self.line_start_point.x(), self.line_start_point.y(),
                                   event.pos().x(), event.pos().y())
        

    def onMouseRelease(self, event):
        if event.button() == Qt.LeftButton:
            if self.pin and self.line:
                x2 = event.pos().x()
                y2 = event.pos().y()
                #Distance algorithm (Using Euclidean distance formula)
                global distance
                distance = ((x2 - self.pin_pos.x())**2 + (y2 - self.pin_pos.y())**2)**0.5 * 0.156565 #Multiplier
                distance3 = int(round(distance))
                with open('distance1.txt', 'w') as reader:
                    reader.write(str(round(distance, 3)))
                try:
                    distance3 = int(round(distance))
                except ValueError:
                    QMessageBox.warning(self, 'Invalid Distance', 'Please enter a valid distance.')
                    return
                
                if distance3 < 40:
                    self.club_recommendation.setText(f"Use: a soft sand wedge")
                    return

                clubs = {
                    'Driver': driver_distance,
                    '3 Wood': three_wood_distance,
                    '4 Iron': four_iron_distance,
                    '5 Iron': five_iron_distance,
                    '6 Iron': six_iron_distance,
                    '7 Iron': seven_iron_distance,
                    '8 Iron': eight_iron_distance,
                    '9 Iron': nine_iron_distance,
                    'Pitching Wedge': pitching_wedge_distance,
                    'Sand Wedge': sand_wedge_distance
                }

                global recommended_club
                recommended_club = None
                distance_diff = 1000
                for club, max_distance in clubs.items():
                    if int(max_distance) - distance3 < distance_diff and int(max_distance) - distance3 >= 0:
                        distance_diff = int(max_distance) - distance3
                        recommended_club = club

                if recommended_club:
                    if distance_diff >= 4:
                        self.club_recommendation.setText(f"Use: a soft {recommended_club}")
                    else:
                        self.club_recommendation.setText(f"Use: {recommended_club}")
                else:
                    self.club_recommendation.setText(f'You should use a Driver')

        

    def back1(self):
        global distance
        distance = 0
        with open('distance1.txt', 'w') as f:
                f.write('0')
        self.login_window = Tracker()
        self.login_window.show()
        self.close()

    def nexthole(self):
        self.hole_10 = GolfTracker()
        self.hole_10.show()
        self.close()




#MAIN

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    main_window = GolfTracker()
    distance_window = Distance()
    account_create = CreateAccount()
    tracker_menu = Tracker()
    hole_one = HoleOne(image_path='hole1.png')
    hole_one.hide()
    hole_two = HoleTwo(image_path='hole2.png')
    hole_two.hide()
    hole_three = HoleThree(image_path='hole3.png')
    hole_three.hide()
    hole_four = HoleFour(image_path='hole4.png')
    hole_four.hide()
    hole_five = HoleFive(image_path='hole5.png')
    hole_five.hide()
    hole_six = HoleSix(image_path='hole6.png')
    hole_six.hide()
    hole_seven = HoleSeven(image_path='hole7.png')
    hole_seven.hide()
    hole_eight = HoleEight(image_path='hole8.png')
    hole_eight.hide()
    hole_nine = HoleNine(image_path='hole9.png')
    hole_nine.hide()
    tracker_menu.hide()
    account_create.hide()
    distance_window.hide()
    login_window.show()
    main_window.hide()
    ex = HoleOne('hole1.png')
    sys.exit(app.exec_())


