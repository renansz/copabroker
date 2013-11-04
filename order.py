import urllib, httplib, json


class OrderClient:
  def __init__(self, user_id, host='localhost', port=8000):
    self.user_id = user_id
    self.host = host
    self.port = port
  
  def __execute_POST(self, path, query):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode(query)
    conn = httplib.HTTPConnection(self.host, self.port)
    conn.request("POST", path, params, headers)
    return conn.getresponse()
  
  def __print_response(self, response):
    message = json.loads(response)
    print message
    try:
      print message['traceback']
    except:
      pass
  
  def Compra(self, ticker_id, qty, value):
    path = r"/api/new_order/"
    query = {
      'order_type': 'C', 
      'user_id': self.user_id, 
      'ticker_id': ticker_id, 
      'order_qty': qty, 
      'order_value': value}
    
    response = self.__execute_POST(path, query)
    self.__print_response(response.read())
  
  def Venda(self, ticker_id, qty, value):
    path = r"/api/new_order/"
    query = {
      'order_type': 'V', 
      'user_id': self.user_id, 
      'ticker_id': ticker_id, 
      'order_qty': qty, 
      'order_value': value}
    
    response = self.__execute_POST(path, query)
    self.__print_response(response.read())
  
  def Info(self, order_id):
    conn = httplib.HTTPConnection(self.host, self.port)
    conn.request("GET","/api/get_order_status/%d/"%order_id)
    response = conn.getresponse()
    self.__print_response(response.read())
  
  def Book(self, ticker):
    conn = httplib.HTTPConnection(self.host, self.port)
    conn.request("GET","/api/get_book/%s/"%ticker)
    response = conn.getresponse()
    self.__print_response(response.read())

def test_server(qty_users, num_tests):
  import random
  
  stocks= [1,2,3]
  target_value = 10.0
  target_variance = 3.0
  qty_lims = (1,20)
  
  clients = [OrderClient(i+1) for i in range(qty_users)]
  
  for x in range(num_tests):
    for c in clients:
      stock = random.choice(stocks)
      qty = random.randint(*qty_lims)
      value = random.normalvariate(target_value, target_variance)
      if random.choice([True, False]):
        c.Compra( stock, qty, value )
      else:
        c.Venda( stock, qty, value)
