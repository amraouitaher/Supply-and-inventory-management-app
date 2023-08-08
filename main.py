import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from matplotlib import style

from modules import *
from widgets import *

import subprocess
from tabulate import tabulate
import inventorize3 as inv
from sklearn import linear_model


#os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%


widgets = None

sns.set_style('whitegrid')


demand = pd.read_csv("./DailyDemand.csv")
summary = pd.read_csv("./summary_stats.csv") 



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "GAdAS 2022"
        description = "GAdAS APP - Inventory Management GUI Application."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        
        #widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.classA_btn.clicked.connect(self.buttonClick)
        widgets.classB_btn.clicked.connect(self.buttonClick)
        widgets.classC_btn.clicked.connect(self.buttonClick)
        widgets.btnA.clicked.connect(self.buttonClick)
        widgets.btnB.clicked.connect(self.buttonClick)
        widgets.btnC.clicked.connect(self.buttonClick)
        widgets.pushButton.clicked.connect(self.buttonClick)
        widgets.pushButton_2.clicked.connect(self.buttonClick)
        widgets.btn_print.clicked.connect(self.buttonClick)
        widgets.btn_message.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        
        self.show()

        # SET HOME PAGE AND SELECT MENU
        
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        
    # BUTTONS CLICK
    
    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

     
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            
        if btnName == "pushButton_2":
            data1= summary[['Product Number','Purchase Cost' ,'Units Sold']]
            data1['revenue']=data1['Purchase Cost']*data1['Units Sold']
            data_abc= inv.ABC(data1[['Product Number','revenue']])
            widgets.label_abc.setText(tabulate(data_abc, headers=['Product Number--','--revenue--','--Percentage--','--comulative--','--Category'],showindex='never',tablefmt='html'))



        if btnName == "pushButton": 
            t= widgets.lineEdit_7.text()
            df= demand[demand[t]>0] 

            days = df['Product'].tolist()
            units = df[t].tolist()
            
            xs = np.array(days, dtype=np.float64)
            ys = np.array(units, dtype=np.float64)

            days_units = linear_model.LinearRegression()

            days_units.fit(xs.reshape(-1,1),ys)

            regression_line = days_units.predict(xs.reshape(-1,1))

            # Making predictions
            day_predicted = widgets.lineEdit_8.text()
            day_predicted = int(day_predicted)

            unit_predicted = days_units.predict(np.array([[day_predicted]]))[0]
            widgets.label_21.setText(f"{unit_predicted} units predicted on day {day_predicted} ")

            style.use('seaborn')
            plt.scatter(xs,ys,label='Daily demand', alpha=0.6,color='green',s=75)
            plt.scatter(day_predicted,unit_predicted, label='Prediction',color='red',s=100)
            plt.plot(xs,regression_line,label='Best Fit Line', color='orange',linewidth=4)
            plt.title('linear regression')
            plt.xlabel('DAYS')
            plt.ylabel('UNITS')
            plt.legend()
            plt.show()

        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.appro)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))


        if btnName == "classA_btn":
            widgets.stackedWidget.setCurrentWidget(widgets.classA)

        if btnName == "classB_btn":
            widgets.stackedWidget.setCurrentWidget(widgets.classB)

        if btnName == "classC_btn":
            widgets.stackedWidget.setCurrentWidget(widgets.classC)


        if btnName == "btnA":
            i= widgets.lineEdit.text()
            k= widgets.lineEdit_2.text()
            k = int(k)     
            dataC = continuous_review(k,i)
            col_names = ["Units arrived", "In Day:"]
            widgets.label_A.setText(tabulate(dataC['outbutD'], headers=col_names))

        if btnName == "btnB":
            i= widgets.lineEdit_3.text()
            k= widgets.lineEdit_4.text()
            k = int(k)
            data = Periodic_review(k,i)
            col_names = ["Units arrived", "In Day:"]
            widgets.label_B.setText(tabulate(data['outbutD'], headers=col_names))
        if btnName == "btnC":
            i= widgets.lineEdit_5.text()
            k= widgets.lineEdit_6.text()
            k = int(k)
            datam = MinMax(k,i)
            col_names = ["Units arrived", "In Day:"]
            widgets.label_C.setText(tabulate(datam['outbutD'], headers=col_names))

        if btnName == "btn_print":
            subprocess.Popen(r'explorer /open,"DailyDemand.csv"')

        if btnName == "btn_message":
            subprocess.Popen(r'explorer /open,"summary_stats.csv"')


    # RESIZE EVENTS
    
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()



# Simulating for 1 year
def Periodic_review( k,i, review_period=30):
        l = int(i)
        lead_time = summary['Lead Time'][l-1]
        inventory = summary['Starting Stock'][l - 1]

        mean = np.mean([ demand[i] ])
        sd = np.std([ demand[i] ])
        
        ss = k * sd * np.sqrt(lead_time)
        widgets.label_B1.setText(f"stock sécurité = {ss}")
        demand_lead = summary['Lead Time'][l-1] * mean
        ndr = mean * (review_period + lead_time ) + ss
        widgets.label_1B.setText(f"niveau de recomplètement = {ndr}")

        q = 0
        stock_out = 0
        counter = 0
        order_placed = False
        # dictionary to store the information
        data = {'inv_level': [], 'orders': [], 'units_sold': [], 'outbutQ': [], 'outbutD': []}

        for day in range(1, 365):
            day_demand = demand[i][day-1]
            

            if day % review_period == 0:
                
                # Placing the order
                q = ndr - inventory + demand_lead
                order_placed = True
                data['orders'].append(q)

                
            if order_placed:
                counter += 1
            
            if counter == lead_time:
                # Restocking day
                inventory += q
                data['outbutQ'].append(q)
                data['outbutQ'].append(day)
                data['outbutD'].append(data['outbutQ'])
                data['outbutQ']=data['outbutQ'][:-2]
                order_placed = False
                counter = 0
            if inventory - day_demand >= 0:
                data['units_sold'].append(day_demand)
                inventory -= day_demand
            elif inventory - day_demand < 0:
                data['units_sold'].append(inventory)
                inventory = 0
                stock_out += 1

        
            data['inv_level'].append(inventory)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(25,8))
        plt.plot(data['inv_level'], linewidth = 1.5)
        plt.axhline(ndr,  linewidth=2 , color="grey", linestyle=":" )
        text(5 , ndr+2 , "NdR = %d" %ndr , fontsize=14  )
        plt.xlim(0,365)
        ax.set_ylabel('Inventory Level (units)', fontsize=18)
        ax.set_xlabel('Day', fontsize=18)
        ax.set_title(f"Periodic Review Model : Number of Orders {len(data['orders'])}", fontsize=18)
        plt.show()
                

        return data

    ## Continuous Review
def continuous_review(k,i):
        l = int(i)
        lead_time = summary['Lead Time'][l-1]
        Co = summary['Co'][l - 1]
        Ch = summary['Ch'][l - 1]
        inventory = summary['Starting Stock'][l - 1]


        mean = np.mean([ demand[i] ])
        sd = np.std([ demand[i] ])        

        ss = k * sd * np.sqrt(lead_time)
        widgets.label_22.setText(f"stock sécurité = {ss}")
        r = mean * lead_time + ss
        widgets.label_2A.setText(f"Reorder Point = {r}")
        qec = np.sqrt(2*Co*sum(demand[i])/Ch)
        widgets.label_1A.setText(f"QEC = {qec}")

        order_placed = False
        order_time = 0
        stock_out = 0
        # dictionary to store the information
        dataC = {'inv_level': [], 'orders': [],'units_sold': [], 'outbutQ': [], 'outbutD': []}

        
        for day in range(1, 365):
            day_demand = demand[i][day-1]

            if inventory <= r and not order_placed:
                order_placed = True
                order_time = day

            if order_placed and (day-order_time) == lead_time:
                dataC['orders'].append(qec)
                inventory += qec
                dataC['outbutQ'].append(qec)
                dataC['outbutQ'].append(day)
                dataC['outbutD'].append(dataC['outbutQ'])
                dataC['outbutQ']=dataC['outbutQ'][:-2]
                order_placed = False
                order_time = 0
                
            if inventory - day_demand >= 0:
                dataC['units_sold'].append(day_demand)
                inventory -= day_demand
            elif inventory - day_demand < 0:
                dataC['units_sold'].append(inventory)
                inventory = 0
                stock_out += 1

            dataC['inv_level'].append(inventory)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(25,8))
        plt.plot(dataC['inv_level'], linewidth = 1.5)
        plt.axhline(r, linewidth=2, color="grey", linestyle=":")
        text(5 , r+2 , "r = %d" %r , fontsize=14  )
        plt.xlim(0,365)
        ax.set_ylabel('Inventory Level (units)', fontsize=18)
        ax.set_xlabel('Day', fontsize=18)
        ax.set_title(f"Continuous Review Model : Number of Orders {len(dataC['orders'])}", fontsize=18)
        plt.show()

        return dataC

def MinMax( k,i, review_period=30):
        l = int(i)
        lead_time = summary['Lead Time'][l-1]
        inventory = summary['Starting Stock'][l - 1]
        sd = np.std([ demand[i] ])
        
        ss = k * sd * np.sqrt(lead_time)
        widgets.label_23.setText(f"stock sécurité = {ss}")

        q = 0
        stock_out = 0
        counter = 0
        order_placed = False
        # dictionary to store the information
        datam = {'inv_level': [], 'orders': [], 'outbutQ': [], 'outbutD': []}

        for day in range(1, 365):
            day_demand = demand[i][day-1]
            

            if day % review_period == 0:
                
                # Placing the order
                q = summary['Starting Stock'][l - 1] - inventory
                order_placed = True
                datam['orders'].append(q)

                
            if order_placed:
                counter += 1
            
            if counter == lead_time:
                # Restocking day
                inventory += q
                datam['outbutQ'].append(q)
                datam['outbutQ'].append(day)
                datam['outbutD'].append(datam['outbutQ'])
                datam['outbutQ']=datam['outbutQ'][:-2]
                order_placed = False
                counter = 0
            if inventory - day_demand >= 0:
                inventory -= day_demand
            elif inventory - day_demand < 0:
                inventory = 0
                stock_out += 1
        
            datam['inv_level'].append(inventory)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(25,8))
        plt.plot(datam['inv_level'], linewidth = 1.5)
        plt.xlim(0,365)
        ax.set_ylabel('Inventory Level (units)', fontsize=18)
        ax.set_xlabel('Day', fontsize=18)
        ax.set_title(f" Number of Orders {len(datam['orders'])}", fontsize=18)
        plt.show()
                

        return datam



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
