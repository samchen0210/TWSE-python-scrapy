import main
import OHLC

def crawler(stock_id):
    stock_id = str(stock_id)
    os.chdir('C:\\Users\\SC.210\\FinTech\\stock') #Change the current working direct
    
    createFolder('./'+stock_id+'/') #Create new folder
    os.chdir('C:\\Users\\SC.210\\FinTech\\stock\\'+stock_id) #Change the current wor
    
    #Fetch data from TWSE (indiviual information)
    fetch_data(2010,1,stock_id)
    
    #Concat all the csv to signle file
    concat_csv(stock_id)
    
    print('Finish crawling stock: '+ stock_id)