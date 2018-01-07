from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Country, Region, Category, HandiCraft, Photo, Video, Myart, Artist
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///handmade.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
          if self.path.endswith("/crafts/new"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              message = ""
              message += "<html><body>"
              message += "Make a new Craft Category"
              message += "<form method='POST' enctype='multipart/form-data' action='/craft/new'>"
              message += "<input name='newCraftName' type='text' placeholder='What are you creating today?'>"
              message += "<input type='submit' value='Create'>"
              message += "</body></html>"
              message = message.encode('utf-8')
              self.wfile.write(message)
              return

          if self.path.endswith("/delete"):
              craftIDPath = self.path.split("/")[2]
              myCraftQuery = session.query(Category).filter_by(id=craftIDPath).one()
              if myCraftQuery:
                  self.send_response(200)
                  self.send_header('Content-type', 'text/html')
                  self.end_headers()
                  output = "<html><body>"
                  output += "<h1>Are you sure you want to delete %s" % myCraftQuery.name
                  output += "</h1>"
                  output += "<form method='POST' enctype='multipart/form-data' action = '/crafts/%s/delete' >" % craftIDPath
                  output += "<input type = 'submit' value = 'Delete'>"
                  output += "</form>"
                  output += "</body></html>"
                  self.wfile.write(output)

          if self.path.endswith("/edit"):
              craftIDPath = self.path.split("/")[2]
              myCraftQuery = session.query(Category).filter_by(id=craftIDPath).one()
              if myCraftQuery:
                  self.send_response(200)
                  self.send_header('Content-type', 'text/html')
                  self.end_headers()
                  output = "<html><body>"
                  output += "<h1>"
                  output += myCraftQuery.name
                  output += "</h1>"
                  output += "<form method='POST' enctype='multipart/form-data' action = '/crafts/%s/edit' >" %craftIDPath
                  output += "<input name = 'newCraftName' type='text' placeholder = '%s' >" % myCraftQuery.name
                  output += "<input type = 'submit' value = 'Rename'>"
                  output += "</form>"
                  output += "</body></html>"

                  self.wfile.write(output)

          if self.path.endswith("/craft"):
              crafts = session.query(Category).all()
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              message = ""
              message += "<html><body>"
              message += "<a href ='/crafts/new'> Make a new Craft Category</a><br><br>"

              for craft in crafts:
                message += craft.name
                message += "</br>"
                message += "<a href ='/crafts/%s/edit'>Edit</a>" % craft.id
                message += "</br>"
                message += "<a href ='/crafts/%s/delete'>Delete</a>" % craft.id
                message += "</br>"
                message += "</br>"
                message += "</body></html>"
              message = message.encode('utf-8')
              self.wfile.write(message)
              # print (message)
              return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
              ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
              craftIDPath =self.path.split("/")[2]
              myCraftQuery = session.query(Category).filter_by(id=craftIDPath).one()
              if myCraftQuery:
                session.delete(myCraftQuery)
                session.commit()

                # Redirect to take the attention back to the main Crafts page
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/craft')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
              ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
              if ctype == 'multipart/form-data':
                  fields=cgi.parse_multipart(self.rfile, pdict)
                  messageContent = fields.get('newCraftName')
                  craftIDPath =self.path.split("/")[2]

                  myCraftQuery = session.query(Category).filter_by(id=craftIDPath).one()
                  if myCraftQuery:
                    myCraftQuery.name = messageContent[0]
                    session.add(myCraftQuery)
                    session.commit()
                    # Redirect to take the attention back to the main Crafts page
                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/craft')
                    self.end_headers()
                    return

            if self.path.endswith("/crafts/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newCraftName')

                    # Create New Craft Category
                    newCraft = Category(name = messageContent[0])
                    session.add(newCraft)
                    session.commit()

                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/craft')
                    self.end_headers()
                    return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()