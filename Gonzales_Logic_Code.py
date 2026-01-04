from PyQt5 import QtWidgets
from Gonzales_UI_Code import Ui_MainWindow   
from PyQt5.QtGui import QMovie, QPixmap, QTransform
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QTimer, QRect, Qt
from statistics import mean, median
import datetime, random, math
from abc import ABC,abstractmethod

class Scorehandler:
    def __init__(self, score, target_score, hearts, sStreak, streak, mistakes, correct):
        self.score = score
        self.target_score = target_score
        self.hearts = hearts
        self.sStreak = sStreak
        self.streak = streak
        self.mistakes = mistakes
        self.correct = correct  
        self.history = []
    
    def handlerGetter(self):
        return self.score, self.target_score, self.hearts, self.sStreak, self.streak, self.mistakes, self.correct
    
# ito ung base class 
class Status(ABC):
    @abstractmethod
    def status_update(self, ui: Ui_MainWindow, handler: Scorehandler):
        pass
# mga child class or subclass ng Status class    
class SoloStatus(Status):
    def status_update(self, ui, handler):
        ui.score.setText(f"{handler.score}/{handler.target_score}")
        ui.Heart.setText(f"{handler.hearts}")
        ui.Streak.setText(f"{handler.streak}")
        ui.mistakes.setText(f"{handler.mistakes}")

class PlayerOneStatus(Status):
    def status_update(self, ui, handler):
        ui.score_3.setText(f"{handler.score}/{handler.target_score}")
        ui.Heart_3.setText(f"{handler.hearts}")
        ui.Streak_3.setText(f"{handler.streak}")
        ui.mistakes_3.setText(f"{handler.mistakes}")
        
class PlayerTwoStatus(Status):
    def status_update(self, ui, handler):
        ui.score_4.setText(f"{handler.score}/{handler.target_score}")
        ui.Heart_4.setText(f"{handler.hearts}")
        ui.Streak_4.setText(f"{handler.streak}")
        ui.mistakes_4.setText(f"{handler.mistakes}")

# timer class na responsible sa pag set ng timer at pag start at stop ng timer
class Timer:
    def __init__(self, countdown):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self._countdown = countdown
    
    @property
    def countdown(self):
        return self._countdown

    @countdown.setter
    def countdown(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Countdown must be a non-negative integer.")
        self._countdown = value
        
    def _start(self, countdown):
        self._countdown = countdown
        self.timer.start()

    def _stop(self):
        self.timer.stop()
        
class SpriteAnimation:
    def __init__(
        self,
        label, 
        spritePath,
        frameW,
        frameH,
        frameCount,
        fps,
        loop,
        flip
        ):
        
        self.label = label
        self.sprite = QPixmap(spritePath)
        self.frameW = frameW
        self.frameH = frameH
        self.frameCount = frameCount
        self.loop = loop
        self.currentFrame = 0
        self.flip = flip
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.setInterval(int(1000/fps))
        
    def startAnim(self):
        self.currentFrame = 0
        self.timer.start()
        
    def stopAnim(self):
        self.timer.stop()
        
    def nextFrame(self):
        if self.currentFrame >= self.frameCount:
            if self.loop:
                self.currentFrame = 0
            else:
                self.stopAnim()
                
        x = self.currentFrame * self.frameW
        frame = self.sprite.copy(
            QRect(x, 0, self.frameW, self.frameH)
        )
        
        if self.flip:
            frame = frame.transformed(QTransform().scale(-1, 1))

        scale = 3
        frame = frame.scaled(
            self.frameW * scale,
            self.frameH * scale,
            Qt.IgnoreAspectRatio,
            Qt.FastTransformation,
        )
        
        self.label.setPixmap(frame)
        self.currentFrame +=1
        
class Animation:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        
        self.knightIdle = SpriteAnimation(
            self.ui.character1, "public/sprites/knight/idle (48 x 48).png",
            48, 48,
            4, 5, True, False
        )
        
        self.hollyIdle = SpriteAnimation(
            self.ui.character2, "public/sprites/holly/idle (32 x 32).png",
            32, 32,
            9, 5, True, True
        )
        
        self.knightAttack = SpriteAnimation(
            self.ui.character1, "public/sprites/knight/Combo_swings (80 x 64).png",
            64, 120,
            2, 3, False, False
        )
        
        self.hollyAttack = SpriteAnimation(
            self.ui.character2, "public/sprites/holly/Aerial_swing (64 x 64).png",
            64, 120,
            2, 3, False, True
        )
        
        self.knightHurt = SpriteAnimation(
            self.ui.character1, "public/sprites/knight/Hurt (48 x 48).png",
            48, 48,
            2, 5, False, False
        )
        
        self.hollyHurt = SpriteAnimation(
            self.ui.character2, "public/sprites/holly/Hurt (32 x 32).png",
            32, 32,
            2, 5, False, True
        )
        
        self.knightRun = SpriteAnimation(
            self.ui.character1, "public/sprites/knight/Running (48 x 48).png",
            48, 48,
            6, 5, False, False
        )
        
        self.hollyRun = SpriteAnimation(
            self.ui.character2, "public/sprites/holly/Running (32 x 32).png",
            32, 32,
            6, 5, False, True
        )
        
        self.knightIdle.startAnim()
        self.hollyIdle.startAnim()
        
    def idleAnim(self, char):
        if char == 1:
            self.knightIdle.startAnim()
        elif char == 2:
            self.hollyIdle.startAnim()
            
    def attackAnim(self, char):
        self.hollyIdle.stopAnim()
        self.knightIdle.stopAnim()
        if char == 1:
            self.knightAttack.startAnim()
            QTimer.singleShot(2000, lambda: self.idleAnim(1))
        elif char == 2:
            self.hollyAttack.startAnim()
            QTimer.singleShot(2000, lambda: self.idleAnim(2))
            
    def hurtAnim(self, char):
        if char == 1:
            self.knightIdle.stopAnim()
            self.knightHurt.startAnim()
            QTimer.singleShot(600, lambda: self.idleAnim(1))
        elif char == 2:
            self.hollyIdle.stopAnim()
            self.hollyHurt.startAnim()
            QTimer.singleShot(600, lambda: self.idleAnim(2))
            
    def runAnim(self, char):
        if char == 1:
            self.knightIdle.stopAnim()
            self.knightRun.startAnim()
            QTimer.singleShot(600, lambda: self.idleAnim(1))
        elif char == 2:
            self.hollyIdle.stopAnim()
            self.hollyRun.startAnim()
            QTimer.singleShot(600, lambda: self.idleAnim(2))      
            
# this class is responsible sa pag create ng mga question at mga operation na gagawin sa mga question 
class QuestionBase(ABC):
    @abstractmethod
    def _create_question(self, *args):
        pass

class QuestionFormat:
    def _format_question(self, question, answer):
        self.__Qp = question
        self.__Ca = answer
        return self.__Qp, self.__Ca
# ito ang mga extended classes 
class AdditionQuestion(QuestionBase):  
    def _create_question(self, firstnum, secondnum, thirdnum, question, answer):
        Format = QuestionFormat()
        question = f"{firstnum} + {secondnum} + {thirdnum} ?"
        answer = firstnum + secondnum + thirdnum
        return "ADDITION", "FIND THE SUM:", *Format._format_question(question, answer)

class SubtractionQuestion(QuestionBase):
    def _create_question(self, firstnum, secondnum, question, answer):
        Format = QuestionFormat()
        question = f"{firstnum} - {secondnum} ?"
        answer = firstnum - secondnum
        return "SUBTRACTION", "FIND THE DIFFERENCE:", *Format._format_question(question, answer)
        
class MultiplicationQuestion(QuestionBase):
    def _create_question(self, firstnum, secondnum, question, answer):
        Format = QuestionFormat()
        question = f"{firstnum} * {secondnum} ?"
        answer = firstnum * secondnum
        return "MULTIPLICATION", "FIND THE PRODUCT:", *Format._format_question(question, answer)
    
class DivisionQuestion(QuestionBase):
    def _create_question(self, firstnum, secondnum, question, answer):
        Format = QuestionFormat()
        question = f"{firstnum} ÷ {secondnum} ?"
        answer = firstnum // secondnum
        return "DIVISION", "FIND THE QUOTIENT:", *Format._format_question(question, answer)
    
class FactorialQuestion(QuestionBase):
    def _create_question(self, factorialNumber, Num, Denom, question, answer):
        Format = QuestionFormat()
        self.factorialType = random.choice(["Basic", "Hard"])
        if self.factorialType == 'Basic':
            question = f"{factorialNumber}!"
            answer = round(math.factorial(factorialNumber))
        else:
            self.Frac = Num / Denom
            question = f"{Num}!/{Denom}!" if Num % Denom != 0 else f"{Num}!//{Denom}!"
            answer = round(math.gamma(self.Frac + 1))
        return "FACTORIAL", "FIND THE FACTORIAL:", *Format._format_question(question, answer)
    
class PhysicsQuestion(QuestionBase):
    def _create_question(self, Mass, Accelerate, fricCoeff, question, answer):
        Format = QuestionFormat()
        self.RandomProblem = random.choice(["Force", "Mass", "Acceleration"])
        self.fricForce = Mass * 9.81 * fricCoeff
        self.force = Mass * Accelerate - self.fricForce

        if self.RandomProblem == 'Force':
            question = f"M= {Mass}kg, A= {Accelerate}m/s², μ= {round(fricCoeff, 2)}"
            answer = round(self.force)
            return "PHYSICS", "FIND THE FORCE:", *Format._format_question(question, answer)
        elif self.RandomProblem == 'Mass':
            question = f"F= {round(self.force, 2)}N, A= {Accelerate}m/s², μ= {round(fricCoeff, 2)}"
            answer = round((self.force + self.fricForce) / Accelerate)
            return "PHYSICS", "FIND THE MASS:", *Format._format_question(question, answer)
        else:
            question = f"M = {Mass}kg, F = {round(self.force, 2)}N"
            answer = round((self.force + self.fricForce) / Mass)
            return "PHYSICS", "FIND THE ACCELERATION:", *Format._format_question(question, answer)
    
class SquareRootQuestion(QuestionBase):
    def _create_question(self, number, question, answer):
        Format = QuestionFormat()
        question = f"√{number}?"
        answer = round(math.sqrt(number))
        return "SQUARE ROOT", "FIND THE SQUARE ROOT:", *Format._format_question(question, answer)
    
class CalculusQuestion(QuestionBase):
    def _create_question(self, ValueOfx, PolyX, PolyY, PolyZ, base, exp, RatioX, RatioY, RatioZ, RatioQ, question, answer):
        Format = QuestionFormat()
        self.CalculusType = random.choice(["Polynoms", "Exponentials", "Rationals"])
    
        if self.CalculusType == 'Polynoms':
            question = f"(x to {ValueOfx}) of f(x)={PolyX}x^2 + {PolyY}x + {PolyZ}"
            answer = PolyX * ValueOfx**2 + PolyY * ValueOfx + PolyZ
            return "CALCULUS", "FIND x:", *Format._format_question(question, answer)
        elif self.CalculusType == 'Exponentials':
            question = f"(x to {ValueOfx}) of f(x)={base}^{exp}*x"
            answer = base ** (exp * ValueOfx)
            return "CALCULUS", "FIND THE x:", *Format._format_question(question, answer)
        else:
            question = f"(x to {ValueOfx}) of f(x)={RatioX}x^2 + {RatioY} / {RatioZ}x + {RatioQ}"
            if RatioZ * ValueOfx + RatioQ != 0:
                answer = round(RatioX * ValueOfx**2 + RatioY) // (RatioZ * ValueOfx + RatioQ)
            else:
                answer = float('infinity')
            return "CALCULUS", "FIND THE x:", *Format._format_question(question, answer)
        
class AlgerbraQuestion(QuestionBase):
    def _create_question(self, r, s, t, question, answer):
        Format = QuestionFormat()
        while r == 0:
            r = random.randint(-30, 30)
        question = f" {r}x + {s} = {t}"
        answer = round((t - s) / r)
        return "ALGEBRA", "FIND THE VALUE OF x:", *Format._format_question(question, answer)
    
class StatisticsQuestion(QuestionBase):
    def _create_question(self, Rangenumber, question, answer):
        Format = QuestionFormat()
        self.StatisticChoices = random.choice(["Mean", "Median", "Mode", "Range"])
        question = f"{Rangenumber}."

        if self.StatisticChoices == 'Mean':
            answer = round(mean(Rangenumber))
            return "STATISTICS", "FIND THE MEAN:", *Format._format_question(question, answer)
        elif self.StatisticChoices == 'Median':
            answer = round(median(Rangenumber))
            return "STATISTICS", "FIND THE MEDIAN:", *Format._format_question(question, answer)
        elif self.StatisticChoices == 'Mode':
             self.Freq = {num: Rangenumber.count(num) for num in Rangenumber}
             self.FullFreq = max(self.Freq.values())
             self.ModeVal = [key for key, value in self.Freq.items() if value == self.FullFreq]
             if self.FullFreq == 1 or len(self.ModeVal) > 1:
                 answer = 0
             else:
                    answer = self.ModeVal[0]
             return "STATISTICS", "FIND THE MODE:", *Format._format_question(question, answer)
        else:
             answer = max(Rangenumber) - min(Rangenumber)
             return "STATISTICS", "FIND THE RANGE:", *Format._format_question(question, round(answer, 2))
         
class GeometryQuestion(QuestionBase):
    def _create_question(self, rd, Angle, question, answer):
        Format = QuestionFormat()        
        self.geoType = random.choice(["Circumference", "Sector Area", "Arc Length", "Segment Area", "Area"])

        if self.geoType == "Area":
            question = f"Radius = {rd}"
            answer = round(math.pi * rd ** 2)
            return "GEOMETRY", "FIND THE AREA:", *Format._format_question(question, answer)
        elif self.geoType == "Circumference":
            question = f"Radius = {rd}"
            answer = round(2 * math.pi * rd, 2)
            return "GEOMETRY", "FIND THE CIRCUMFERENCE:", *Format._format_question(question, answer)
        elif self.geoType == "Sector Area":
            question = f"Radius = {rd}, Angle = {Angle}°"
            answer = round((Angle / 360) * math.pi * rd ** 2)
            return "GEOMETRY", "FIND THE SECTOR AREA:", *Format._format_question(question, answer)
        elif self.geoType == "Arc Length":
            question = f"Radius = {rd}, Angle = {Angle}°"
            answer = round((Angle / 360) * 2 * math.pi * rd)
            return "GEOMETRY", "FIND THE ARC LENGTH:", *Format._format_question(question, answer)
        else:
            question = f"Radius = {rd}, Angle = {Angle}°"
            self.secArea = (Angle / 360) * math.pi * rd ** 2
            self.triangArea = 0.5 * rd ** 2 * math.sin(math.radians(Angle))
            answer = round(self.secArea - self.triangArea)
            return "GEOMETRY", "FIND THE SEGMENT AREA:", *Format._format_question(question, answer)

class LogarithmQuestion(QuestionBase):
    def _create_question(self, logNum, logBase, question, answer):
        Format = QuestionFormat()
        question = f"log{logBase}({logNum})?"
        if logNum > 0 and logBase > 0 and logBase != 1:
            answer = round(math.log(logNum, logBase))
        else:
            answer = 0
        return "LOGARITHM", "FIND THE LOG:", *Format._format_question(question, answer) 
# in this part Factory Pattern Based type ng DIP 
#   This decouples the high-level logic from the concrete implementations.
class QuestionType: # kung saa ndito ung class nato is ung high level of module that depends on the abstraction
    creators = {
        "ADDITION": (AdditionQuestion, (lambda: (random.randint(1, 50), random.randint(1, 25), random.randint(1, 15), "", 0))),
        "SUBTRACTION": (SubtractionQuestion, (lambda: (random.randint(1, 50), random.randint(1, 50), "", 0))),
        "MULTIPLICATION": (MultiplicationQuestion, (lambda: (random.randint(1, 100), random.randint(1, 50), "", 0))),
        "DIVISION": (DivisionQuestion, (lambda: (random.randint(1, 100), random.randint(1, 50), "", 0))),
        "FACTORIAL": (FactorialQuestion, (lambda: (random.randint(1, 10), random.randint(1, 20), random.randint(2, 4), "", 0))),
        "PHYSICS": (PhysicsQuestion, (lambda: (random.randint(10, 100), random.randint(10, 30), random.uniform(0.1, 0.5), "", 0))),
        "SQUARE ROOT": (SquareRootQuestion, (lambda: (random.randint(1, 100), "", 0))),
        "CALCULUS": (CalculusQuestion, (lambda: (
                random.randint(-5, 5),  
                random.randint(-5, 5),  
                random.randint(-5, 5),   
                random.randint(-5, 5),   
                random.randint(2, 5),    
                random.randint(1, 3),    
                random.randint(-5, 5),   
                random.randint(-5, 5),  
                random.randint(-5, 5),  
                random.randint(-5, 5), 
                "",                      
                0                      
            ))),
        "ALGEBRA": (AlgerbraQuestion, (lambda: (random.randint(-30, 30), random.randint(-30, 30), random.randint(-30, 30), "", 0))),
        "STATISTICS": (StatisticsQuestion, (lambda: (tuple(random.randint(1, 15) for _ in range(random.randint(5, 10))), "", 0))),
        "GEOMETRY": (GeometryQuestion, (lambda: (random.randint(5, 20), random.randint(30, 180), "", 0))),
        "LOGARITHM": (LogarithmQuestion, (lambda: (random.randint(2, 100), random.randint(2, 10), "", 0)))
    }
    
    @classmethod
    def getCreator(cls, operation):
        if operation not in cls.creators:
            return None
        questionBase, args_func = cls.creators[operation]
        return questionBase(), args_func
    
class QuestionCreator:
    # High-level module responsible for creating questions without depending
    # on concrete question implementations directly.
    # It relies on the abstraction QuestionType to get the appropriate creator.
    def _create_question(self, operation, QTP: QuestionType):
        creator, args_func = QTP.getCreator(operation)
        if creator: # the creator is the 
            args = args_func() if callable(args_func) else args_func  
            return creator._create_question(*args)  # dito na nangyayari ung polymorph
        return None
# class para sa gathering data na marerecord after malaro ang game na mapupunta sa history page
class History:
    def __init__(self, ui: Ui_MainWindow, 
                 status: Scorehandler):
        self.ui = ui
        self.status = status

    def historyPage(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        table = self.ui.tableWidget
        table.setRowCount(0)
        for data in self.status.history:
            rp = table.rowCount()
            table.insertRow(rp)
            table.setItem(rp, 0, QTableWidgetItem(data['Dt']))
            table.setItem(rp, 3, QTableWidgetItem(str(data['operation'])))
            table.setItem(rp, 4, QTableWidgetItem(str(data['score'])))
            table.setItem(rp, 5, QTableWidgetItem(str(data['mistakes'])))
            table.setItem(rp, 6, QTableWidgetItem(str(data['hearts'])))

    def recorded(self):
        self.recordStatus()
        self.historyPage()
        
    def recordStatus(self):
        Dt = datetime.datetime.now().strftime("%Y-%m-%d")
        operations = {
            self.ui.rb1_3: "ADDITION",
            self.ui.rb2_3: "SUBTRACTION",
            self.ui.rb3_3: "MULTIPLICATION",
            self.ui.rb4_3: "DIVISION",
            self.ui.rb9: "FACTORIAL",
            self.ui.rb10: "PHYSICS",
            self.ui.rb5_3: "SQUARE ROOT",
            self.ui.rb6_3: "CALCULUS",
            self.ui.rb7_3: "ALGEBRA",
            self.ui.rb8_5: "STATISTICS",
            self.ui.rb4_5: "GEOMETRY",
            self.ui.rb12: "LOGARITHM"
        }
        
        operation = next((op for rb, op in operations.items() if rb.isChecked()), "UNKNOWN")
        
        data = {
            'Dt': Dt,
            'score': self.status.score,
            'hearts': self.status.hearts,
            'mistakes': self.status.mistakes,
            'operation': operation,
        }
        
        self.status.history.append(data)

class ModeChoice:
    def __init__(self, ui: Ui_MainWindow, player_id, timer: Timer):
        self.ui = ui
        self.player_id = player_id
        self.timer = timer
        
    def ModeChoice(self):
        if self.ui.SOLORB.isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)
        elif self.ui.PVPRB.isChecked():
            self.ui.stackedWidget.setCurrentIndex(2 if self.player_id == 1 else 2)  
        self.ModeChoiceDisAndAble()
        
    def ModeChoiceDisAndAble(self):
        if self.player_id == "solo" or self.ui.SOLORB.isChecked():
            self.ui.Le1.setDisabled(False)
            self.ui.Submit.setDisabled(False)
            self.ui.pb2.setDisabled(True)
            self.ui.Retry.setDisabled(True)
        elif self.player_id == 1 or self.player_id == 2:    
            self.ui.Le1_2.setDisabled(False)  
            self.ui.Submit_2.setDisabled(False)
            self.ui.pb2_2.setDisabled(True)
            self.ui.Retry_2.setDisabled(True)
        self.ModeTime()
        
    def ModeTime(self):
        self.timer._countdown = 30 if self.ui.rb1_3.isChecked() or self.ui.rb2_3.isChecked() else 40 if any(rb.isChecked() for rb in [self.ui.rb3_3, self.ui.rb4_3, self.ui.rb5_3, self.ui.rb7_3]) else 60

        if self.player_id == "solo" or self.ui.SOLORB.isChecked():
            self.ui.Timer.setText(str(self.timer._countdown))
        elif self.player_id == 1:
            self.ui.Timer_3.setText(str(self.timer._countdown))
        elif self.player_id == 2:
            self.ui.Timer_4.setText(str(self.timer._countdown))

        self.timer._start(self.timer._countdown)
# Class na ito ay may behavior na nagcocontrol sa mga operation na pinili ng player
class OperationLoader:
    def __init__(self, ui: Ui_MainWindow, status: Status, timer: Timer, 
                 player_id=None):
        self.ui = ui
        self.timer = timer
        self.status = status
        self.player_id = player_id   
        
        self.operation_buttons = [
            self.ui.rb1_3, self.ui.rb2_3, self.ui.rb3_3, self.ui.rb4_3,
            self.ui.rb5_3, self.ui.rb6_3, self.ui.rb7_3, self.ui.rb8_5,
            self.ui.rb9, self.ui.rb10, self.ui.rb4_5, self.ui.rb12
        ]
        self.disable_operations()

    def disable_operations(self):
        for button in self.operation_buttons:
            button.setDisabled(True)

    def enable_operations(self):
        for button in self.operation_buttons:
            button.setDisabled(False)

    def executeOperation(self):
        Qtype = QuestionCreator()
        QTP = QuestionType()
        mode = ModeChoice(self.ui, self.player_id, self.timer)
        if not (self.ui.SOLORB.isChecked() or self.ui.PVPRB.isChecked()):
            self.disable_operations()
            return

        self.enable_operations()

        operations = {
            self.ui.rb1_3: lambda: Qtype._create_question("ADDITION", QTP),
            self.ui.rb2_3: lambda: Qtype._create_question("SUBTRACTION", QTP),
            self.ui.rb3_3: lambda: Qtype._create_question("MULTIPLICATION", QTP),
            self.ui.rb4_3: lambda: Qtype._create_question("DIVISION", QTP),
            self.ui.rb5_3: lambda: Qtype._create_question("SQUARE ROOT", QTP),
            self.ui.rb6_3: lambda: Qtype._create_question("CALCULUS", QTP),
            self.ui.rb7_3: lambda: Qtype._create_question("ALGEBRA", QTP),
            self.ui.rb8_5: lambda: Qtype._create_question("STATISTICS", QTP),
            self.ui.rb9: lambda: Qtype._create_question("FACTORIAL", QTP),
            self.ui.rb10: lambda: Qtype._create_question("PHYSICS", QTP),
            self.ui.rb4_5: lambda: Qtype._create_question("GEOMETRY", QTP),
            self.ui.rb12: lambda: Qtype._create_question("LOGARITHM", QTP)
        }

        if not any(rb.isChecked() for rb in operations):
            return
        for rb, method in operations.items():
            if rb.isChecked():
                result = method()
                if result:  # Check if question was created successfully
                    Type, Find, Qp, self.status.correct = result
                    print(f"Operation [{Find}] - Answer [{self.status.correct}]")
                    break
                
        if self.player_id == "solo" or self.ui.SOLORB.isChecked():
            self.ui.lineEdit_3.setText(Type)
            self.ui.lineEdit_2.setText(Find)
            self.ui.lineEdit.setText(Qp)
        elif self.player_id == 1:
            self.ui.lineEdit_5.setText(Type)   
            self.ui.lineEdit_9.setText(Find)
            self.ui.lineEdit_7.setText(Qp)
        elif self.player_id == 2:
            self.ui.lineEdit_10.setText(Find)
            self.ui.lineEdit_8.setText(Qp)        
        mode.ModeChoice()

class AccessComponents:
    def __init__(self, ui: Ui_MainWindow, status_handler: Scorehandler,
                 timer: Timer, math_operation: OperationLoader, history_manager: History, animation: Animation):
        self.ui = ui
        self.status_handler = status_handler 
        self.timer = timer
        self.math_operation = math_operation
        self.history_manager = history_manager
        self.animation = animation
        
    def Components(self):
        return self.ui, self.status_handler, self.timer, self.math_operation, self.history_manager, self.animation

# LSP: for Status
def getStatus(status: list[Status], ui, handler):
    for stat in status:
        stat.status_update(ui, handler)

# this class is for game update
class GameUpdate(ABC):
    def __init__(self, parent: QtWidgets.QMainWindow, tools: AccessComponents,):
        self.parent = parent
        self.tools = tools
        
        solostat = SoloStatus()
        playerOne = PlayerOneStatus()
        playerTwo = PlayerTwoStatus()  
        self.Allstat = [
            solostat,
            playerOne,
            playerTwo
        ]
        
        
    @abstractmethod
    def clearUpdate(self, ui: Ui_MainWindow):
        pass
        
    @abstractmethod
    def DecisionUpdate(self, win: bool, ui: Ui_MainWindow):
        pass
    @abstractmethod
    def CleanUpdating(self, ui: Ui_MainWindow):
        pass
 
# exntend or child classes of game update    
class SoloUpdate(GameUpdate):
    def clearUpdate(self, ui):
        getStatus([self.Allstat[0]], ui, self.tools.status_handler)
        self.tools.status_handler.score = 0
        self.tools.status_handler.hearts = 3
        self.tools.status_handler.streak = 0
        self.tools.status_handler.mistakes = 0
        ui.lineEdit.setText("")     
        
    def DecisionUpdate(self, win, ui):
        self.tools.timer._stop()
        
        if win and self.tools.status_handler.mistakes == 0 :
            QMessageBox.information(self.parent, "CONGRATULATIONS!",
                                    f"PERFECT SCORE!, {self.tools.status_handler.score}/{self.tools.status_handler.target_score} YOU WIN THE GAME.")
        else:
            QMessageBox.critical(self.parent, "GAME OVER", 
                               f"FINAL SCORE: {self.tools.status_handler.score}/{self.tools.status_handler.target_score}, MISTAKES: {self.tools.status_handler.mistakes} YOU LOSE, KEEP PRACTICING!")
            
        ui.stackedWidget.setCurrentIndex(1)
        self.CleanUpdating(ui) 
        
    def CleanUpdating(self, ui):
        self.tools.history_manager.recordStatus()
        ui.pb2.setEnabled(True)
        ui.Retry.setEnabled(True)
        ui.Le1.setDisabled(True)
        ui.Submit.setDisabled(True)
        self.clearUpdate(ui)

class PlayerOneUpdate(GameUpdate):
    def clearUpdate(self, ui):
        getStatus([self.Allstat[1]], ui, self.tools.status_handler)
        self.tools.status_handler.score = 0
        self.tools.status_handler.hearts = random.randint(5, 10)  # Randomize hearts for Player 1
        self.tools.status_handler.streak = 0
        self.tools.status_handler.mistakes = 0
        ui.lineEdit_7.setText("")   
          
    def DecisionUpdate(self, win, ui):
        self.tools.timer._stop()
        
        if not win:

            # Disable current player's inputs
            self.tools.ui.Le1_2.setDisabled(True)
            self.tools.ui.Submit_2.setDisabled(True)
            
            other_hearts = int(self.tools.ui.Heart_4.text()) if self.tools.ui.Heart_4.text().isdigit() else 0
            other_alive = other_hearts > 0
            
            if other_alive:
                
                QMessageBox.information(self.parent, "Player Eliminated",
                                    "Player 1 is out! Player 2 continues.")
                 
                return
            else:
               
                # Disable both players if both are dead
                self.tools.ui.Le1_3.setDisabled(True)  
                self.tools.ui.Submit_3.setDisabled(True)   
                QMessageBox.critical(self.parent, "GAME OVER", 
                                "Both players have been eliminated!")
        else:
            QMessageBox.information(self.parent, "CONGRATULATIONS!", 
                                f"Player 1 wins with {self.tools.status_handler.score}/{self.tools.status_handler.target_score}!")
            QMessageBox.information(self.parent, "Player 2 Defeated", "Player 2 has been defeated. Game Over.")
            self.tools.ui.Le1_2.setDisabled(True)
            self.tools.ui.Submit_2.setDisabled(True)
            self.tools.ui.Le1_3.setDisabled(True)
            self.tools.ui.Submit_3.setDisabled(True)
        ui.stackedWidget.setCurrentIndex(2)
        self.CleanUpdating(ui)
        
    def CleanUpdating(self, ui):
        self.tools.history_manager.recordStatus()
        self.tools.ui.pb2_2.setEnabled(True)
        self.tools.ui.Retry_2.setEnabled(True)
        self.clearUpdate(ui)
        
class PlayerTwoUpdate(GameUpdate):
    def clearUpdate(self, ui):  
        getStatus([self.Allstat[2]], ui, self.tools.status_handler)
        self.tools.status_handler.score = 0
        self.tools.status_handler.hearts = random.randint(5, 10)   
        self.tools.status_handler.streak = 0
        self.tools.status_handler.mistakes = 0
        self.tools.ui.lineEdit_8.setText("")     
        
    def DecisionUpdate(self, win, ui):
        self.tools.timer._stop()
        
        if not win:
            self.tools.ui.Le1_3.setDisabled(True)
            self.tools.ui.Submit_3.setDisabled(True)
            other_hearts = int(self.tools.ui.Heart_3.text()) if self.tools.ui.Heart_3.text().isdigit() else 0
            other_alive = other_hearts > 0
            
            if other_alive:
                QMessageBox.information(self.parent, "Player Eliminated",
                                    "Player 2 is out! Player 1 continues.")
                 
                return
            else:
                self.tools.ui.Le1_2.setDisabled(True)   
                self.tools.ui.Submit_2.setDisabled(True)   
                QMessageBox.critical(self.parent, "GAME OVER", 
                                "Both players have been eliminated!")
        else:
            QMessageBox.information(self.parent, "CONGRATULATIONS!", 
                                f"Player 2 wins with {self.tools.status_handler.score}/{self.tools.status_handler.target_score}!")
            QMessageBox.information(self.parent, "Player 1 Defeated", "Player 1 has been defeated. Game Over.")
            self.tools.ui.Le1_3.setDisabled(True)
            self.tools.ui.Submit_3.setDisabled(True)
            self.tools.ui.Le1_2.setDisabled(True)
            self.tools.ui.Submit_2.setDisabled(True)
        ui.stackedWidget.setCurrentIndex(2)
        self.CleanUpdating(ui)

    def CleanUpdating(self, ui):
        self.tools.history_manager.recordStatus()
        self.tools.ui.pb2_2.setEnabled(True)
        self.tools.ui.Retry_2.setEnabled(True)
        self.clearUpdate(ui)    
        
# LSP: for GameUpdate in Decision method
def getGameUpdate(updates: list[GameUpdate], win, ui):
    for update in updates:
        update.DecisionUpdate(win, ui)

# this is for game checking 
class GameChecking(ABC):
    def __init__(self, gameUpdate: GameUpdate):
        self.tools = gameUpdate.tools
        self.parent = gameUpdate.parent
        self.gameUpdate = gameUpdate
        
        self.Allstat = gameUpdate.Allstat
        
        soloUpdate = SoloUpdate(self.parent, self.tools)
        playerOneUpdate = PlayerOneUpdate(self.parent, self.tools)
        playerTwoUpdate = PlayerTwoUpdate(self.parent, self.tools)
        
        self.AllUpdates = [
            soloUpdate,
            playerOneUpdate,
            playerTwoUpdate
        ]
        
        self.tools.timer.timer.timeout.connect(lambda: self.CheckTimer())
        
    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def CheckTimer(self):
        pass
        
  
# ito ang mga subclasses ng check and update class 
class SoloGameChecking(GameChecking):
    def check(self): # solo checking behavior
        if not self.tools.ui.Le1.text():  
            self.tools.ui.lineEdit_4.setText("PLEASE ENTER AN ANSWER!")
            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_4.clear())
            return
            
        try:
            soloInput = self.tools.ui.Le1.text()
            soloAnswer = float(soloInput) if '.' in str(self.tools.status_handler.correct) or '-' in str(self.tools.status_handler.correct) else int(soloInput)
            self.tools.ui.Le1.clear()

            if soloAnswer == self.tools.status_handler.correct:
                self.tools.status_handler.score += 1
                self.tools.status_handler.sStreak += 1
                self.tools.ui.lineEdit_4.setText("YOU NAILED IT!")
                if self.tools.status_handler.sStreak >= 2:
                    self.tools.status_handler.streak += 1
            else:
                self.tools.status_handler.hearts -= 1 
                self.tools.status_handler.streak = 0
                self.tools.status_handler.mistakes += 1
                self.tools.ui.lineEdit_4.setText(f"YOU ARE WRONG. THE ANSWER IS {self.tools.status_handler.correct}")
                
            self.tools.ui.Le1.setFocus()

            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_4.clear())
            getStatus([self.Allstat[0]], self.tools.ui, self.tools.status_handler)

            if (self.tools.status_handler.mistakes == 1 and self.tools.status_handler.score == 9) or \
            (self.tools.status_handler.mistakes == 2 and self.tools.status_handler.score == 8) or \
            (self.tools.status_handler.hearts == 0):
                getGameUpdate([self.AllUpdates[0]], False, self.tools.ui)
            elif self.tools.status_handler.score >= self.tools.status_handler.target_score:
                getGameUpdate([self.AllUpdates[0]], True, self.tools.ui)
            else:
                self.tools.math_operation.executeOperation()
                
        except ValueError:
            self.tools.ui.lineEdit_4.setText("Please enter a valid number!")
            self.tools.ui.Le1.clear()
            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_4.clear())
     
        
    def CheckTimer(self):
        if self.tools.timer._countdown > 0:
            self.tools.timer._countdown -= 1
            self.tools.ui.Timer.setText(str(self.tools.timer._countdown))
        else:
            self.tools.timer._stop()
            self.tools.status_handler.hearts -= 1
            self.tools.ui.Heart.setText(str(self.tools.status_handler.hearts))

            if self.tools.status_handler.hearts == 0:
                getGameUpdate([self.AllUpdates[0]], False, self.tools.ui)
            else:
                self.tools.math_operation.executeOperation()

# dito naman ma plano ako dito sa behavior ng class na to pero for sooner muna
class PlayerOneGameChecking(GameChecking):
    def check(self): # Player 1 Combo getter when 5 consecutive correct answers
        if not self.tools.ui.Le1_2.text():  
            self.tools.ui.lineEdit_11.setText("Please enter an answer!")
            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_11.clear())
            return
            
        try:
            playerOneInput = self.tools.ui.Le1_2.text()
            playerOneAnswer = float(playerOneInput) if '.' in str(self.tools.status_handler.correct) or '-' in str(self.tools.status_handler.correct) else int(playerOneInput)
            self.tools.ui.Le1_2.clear()

            if playerOneAnswer == self.tools.status_handler.correct:
                self.tools.status_handler.score += 1
                self.tools.status_handler.sStreak += 1
                self.tools.ui.lineEdit_11.setText("YOU ARE CORRECT!")
                self.tools.animation.attackAnim(1)
                QTimer.singleShot(200, lambda: self.tools.animation.hurtAnim(2))
                if self.tools.status_handler.sStreak % 5 == 0 and self.tools.status_handler.sStreak > 0:
                    self.tools.status_handler.score += 3
                    self.tools.ui.lineEdit_11.setText("🔥 COMBO BONUS! EXTRA POINT!")
            else:
                self.tools.status_handler.hearts -= 1 
                self.tools.status_handler.streak = 0
                self.tools.status_handler.mistakes += 1
                self.tools.animation.attackAnim(2)
                self.tools.ui.lineEdit_11.setText(f"YOU ARE WRONG. THE ANSWER IS {self.tools.status_handler.correct}")
                QTimer.singleShot(200, lambda: self.tools.animation.hurtAnim(1))

            self.tools.ui.Le1_2.setFocus()

            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_11.clear())
            getStatus([self.Allstat[1]], self.tools.ui, self.tools.status_handler)

            if (self.tools.status_handler.mistakes == 1 and self.tools.status_handler.score == 9) or \
            (self.tools.status_handler.mistakes == 2 and self.tools.status_handler.score == 8) or \
            (self.tools.status_handler.hearts == 0):
                getGameUpdate([self.AllUpdates[1]], False, self.tools.ui)
            elif self.tools.status_handler.score >= self.tools.status_handler.target_score:
                getGameUpdate([self.AllUpdates[1]], True, self.tools.ui)
            else:
                self.tools.math_operation.executeOperation()
                
        except ValueError:
            self.tools.ui.lineEdit_11.setText("Please enter a valid number!")
            self.tools.ui.Le1_2.clear()
            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_11.clear())

    def CheckTimer(self):
        if self.tools.timer._countdown > 0:
            self.tools.timer._countdown -= 1
            self.tools.ui.Timer_3.setText(str(self.tools.timer._countdown))
        else:
            self.tools.timer._stop()
            self.tools.status_handler.hearts -= 3
            self.tools.ui.Heart_3.setText(str(self.tools.status_handler.hearts))

            if self.tools.status_handler.hearts == 0:
            
                getGameUpdate([self.AllUpdates[1]], False, self.tools.ui)
            else:
                self.tools.math_operation.executeOperation()


class PlayerTwoGameChecking(GameChecking):
    def check(self): # Player 2 behavior heart redemptionist nagagain sya ng buhay na dalawa after 4 cirrect answer
        if not self.tools.ui.Le1_3.text():  
            self.tools.ui.lineEdit_12.setText("Please enter an answer!")
            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_12.clear())
            return
            
        try:
            playerTwoInput = self.tools.ui.Le1_3.text()
            playerTwoAnswer = float(playerTwoInput) if '.' in str(self.tools.status_handler.correct) or '-' in str(self.tools.status_handler.correct) else int(playerTwoInput)
            self.tools.ui.Le1_3.clear()

            if playerTwoAnswer == self.tools.status_handler.correct:
                self.tools.status_handler.score += 1
                self.tools.status_handler.sStreak += 1
                self.tools.animation.attackAnim(2)
                self.tools.ui.lineEdit_12.setText("YOU ARE CORRECT!")
                QTimer.singleShot(200, lambda: self.tools.animation.hurtAnim(1))
                if self.tools.status_handler.sStreak % 4 == 0 and self.tools.status_handler.sStreak > 0:
                    self.tools.status_handler.hearts += 2
                    self.tools.ui.Heart_4.setText(str(self.tools.status_handler.hearts)) 
                    self.tools.ui.lineEdit_12.setText("❤️ REDEMPTION! YOU GAINED A HEART!")
            else:
                self.tools.status_handler.hearts -= 1 
                self.tools.status_handler.streak = 0
                self.tools.status_handler.mistakes += 1
                self.tools.animation.attackAnim(1)
                self.tools.ui.lineEdit_12.setText(f"YOU ARE WRONG. THE ANSWER IS {self.tools.status_handler.correct}")
                QTimer.singleShot(200, lambda: self.tools.animation.hurtAnim(2))
            
            self.tools.ui.Le1_3.setFocus()

            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_12.clear())
            getStatus([self.Allstat[2]], self.tools.ui, self.tools.status_handler)

            if (self.tools.status_handler.mistakes == 1 and self.tools.status_handler.score == 9) or \
            (self.tools.status_handler.mistakes == 2 and self.tools.status_handler.score == 8) or \
            (self.tools.status_handler.hearts == 0):
                getGameUpdate([self.AllUpdates[2]], False, self.tools.ui)
            elif self.tools.status_handler.score >= self.tools.status_handler.target_score:
                getGameUpdate([self.AllUpdates[2]], True, self.tools.ui)
            else:
                self.tools.math_operation.executeOperation()
                
        except ValueError:
            self.tools.ui.lineEdit_12.setText("Please enter a valid number!")
            self.tools.ui.Le1_3.clear()
            QTimer.singleShot(2000, lambda: self.tools.ui.lineEdit_12.clear())
   
    def CheckTimer(self):
        if self.tools.timer._countdown > 0:
            self.tools.timer._countdown -= 1
            self.tools.ui.Timer_4.setText(str(self.tools.timer._countdown))
        else:
            self.tools.timer._stop()
            self.tools.status_handler.hearts -= 2
            self.tools.ui.Heart_4.setText(str(self.tools.status_handler.hearts))

            if self.tools.status_handler.hearts == 0:
                 
                getGameUpdate([self.AllUpdates[2]], False, self.tools.ui)
            else:
                self.tools.math_operation.executeOperation()

# LSP: this function is used to clear the update
def getClearUpdate(updates: list[GameUpdate], ui):
    for update in updates:
        update.clearUpdate(ui)
        
# this class is for game retry
class GameRetry(ABC):
    def __init__(self, update: GameUpdate, gamechecking: GameChecking):
        self.update = update
        self.tools = update.tools

        self.Allstat = update.Allstat
        self.AllClearUpdates = gamechecking.AllUpdates
        
    def reset(self):
        self.tools.ui.lineEdit_4.setText("")
    
    @abstractmethod
    def retryStat(self, ui: Ui_MainWindow):
        pass
    
    @abstractmethod
    def try_again(self, ui: Ui_MainWindow):
        pass
        
    @abstractmethod
    def retry(self, ui: Ui_MainWindow):
        pass

class Soloretry(GameRetry):
    def retryStat(self, ui):
        getStatus([self.Allstat[0]], ui, self.tools.status_handler)
    
    def try_again(self, ui):
        getClearUpdate([self.AllClearUpdates[0]], ui)
        self.retryStat(ui)  # Add status update
        self.tools.ui.stackedWidget.setCurrentIndex(0)
        self.tools.ui.pb2.setEnabled(True)

    def retry(self, ui):
        getClearUpdate([self.AllClearUpdates[0]], ui)
        self.retryStat(ui)  # Add status update
        ui.Retry.setEnabled(False)
        ui.Le1.setEnabled(True)
        ui.Submit.setEnabled(True)
        ui.pb2.setDisabled(True)
        self.tools.timer._start(self.tools.timer._countdown)
        self.tools.math_operation.executeOperation()
    
class PlayerOneRetry(GameRetry):
    def retryStat(self, ui):
        getStatus([self.Allstat[1]], ui, self.tools.status_handler)
    
    def try_again(self, ui):
        getClearUpdate([self.AllClearUpdates[1]], ui)
        self.retryStat(ui)  # Add status update
        ui.stackedWidget.setCurrentIndex(0)
        ui.pb2_2.setEnabled(True)

    def retry(self, ui):
        getClearUpdate([self.AllClearUpdates[1]], ui)
        self.retryStat(ui)  # Add status update
        ui.Retry_2.setEnabled(False)
        ui.Le1_2.setEnabled(True)
        ui.Le1_3.setEnabled(True)
        ui.Submit.setEnabled(True)
        ui.Submit_2.setEnabled(True)
        ui.pb2_2.setDisabled(True)
        self.tools.timer._start(self.tools.timer._countdown)
        self.tools.math_operation.executeOperation()
        
class PlayerTwoRetry(GameRetry):
    def retryStat(self, ui):
        getStatus([self.Allstat[2]], ui, self.tools.status_handler)
    
    def try_again(self, ui):
        getClearUpdate([self.AllClearUpdates[2]], ui)
        self.retryStat(ui)  # Add status update
        ui.stackedWidget.setCurrentIndex(0)
        ui.pb2_2.setEnabled(True)

    def retry(self, ui):
        getClearUpdate([self.AllClearUpdates[2]], ui)
        self.retryStat(ui)  # Add status update
        ui.Retry_2.setEnabled(False)
        ui.Le1_2.setEnabled(True)
        ui.Le1_3.setEnabled(True)
        ui.Submit.setEnabled(True)
        ui.Submit_3.setEnabled(True)
        ui.pb2_2.setDisabled(True)
        self.tools.timer._start(self.tools.timer._countdown)
        self.tools.math_operation.executeOperation()
        
# ang style ko na lahat ng logic ay naka composition
class GameManager:
    def __init__(self, main_window, ui, player_id=None):
        PlayerStatus = {
            "solo": (SoloStatus, 3),
            1: (PlayerOneStatus, random.randint(5, 10)),
            2: (PlayerTwoStatus, random.randint(5, 10))
        }

        if player_id not in PlayerStatus:
            raise ValueError("Invalid player_id")

        Status, hearts = PlayerStatus[player_id]
        scorehandler = Scorehandler(0, 10, hearts, 0, 0, 0, None)
        self.status = Status()
        self.status.status_update(ui, scorehandler)
        # Initialize tools
        self.animation = Animation(ui)
        self.timer = Timer(0)
        self.history_manager = History(ui, scorehandler)
        self.math_operation = OperationLoader(ui, scorehandler, self.timer, player_id)
        self.mode = ModeChoice(ui, player_id, self.timer)

        self.Tools = AccessComponents(
            ui,
            scorehandler,
            self.timer,
            self.math_operation,
            self.history_manager,
            self.animation
        )
        
        # Initialize game logic
        if player_id == "solo":
            self.gameUpdate = SoloUpdate(main_window, self.Tools)
            self.game_actions = SoloGameChecking(self.gameUpdate)
            self.renew = Soloretry(self.gameUpdate, self.game_actions)
        elif player_id == 1:
            self.gameUpdate = PlayerOneUpdate(main_window, self.Tools)
            self.game_actions = PlayerOneGameChecking(self.gameUpdate)
            self.renew = PlayerOneRetry(self.gameUpdate, self.game_actions)
        elif player_id == 2:
            self.gameUpdate = PlayerTwoUpdate(main_window, self.Tools)
            self.game_actions = PlayerTwoGameChecking(self.gameUpdate)
            self.renew = PlayerTwoRetry(self.gameUpdate, self.game_actions)
