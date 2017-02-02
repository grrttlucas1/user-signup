#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi


form = """
    <form method="post">
        <h1>Signup</h1>
        <br>
        <label>Username
            <input type="text" name="username" value="%(username)s">
            <span style="color: red"> %(username_error)s </span>
        </label>
        <br>
        <label>Password
            <input type="password" name="password">
            <span style="color: red"> %(password_error)s </span>
        </label>
        <br>
        <label>Verify Password
            <input type="password" name="verify">
        </label>
        <br>
        <label>Email (optional)
            <input type="text" name="email" value="%(email)s">
            <span style="color: red"> %(email_error)s </span>
        </label>
        <br>
        <input type=submit>
"""


def valid_user(username):
    username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username_re.match(username)
    

def valid_pw(password, verify):
    password_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    if password == verify:
        return password_re.match(password)
    return False
    
    
def valid_email(email):
    email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    if email:
        return email_re.match(email)
    return True


def escape_html(s):
    return cgi.escape(s, quote=True)

    
class MainHandler(webapp2.RequestHandler):

    def write_form(self,
                   username="",
                   email="",
                   username_error="",
                   password_error="",
                   email_error=""):
        self.response.write(form % {"username"       : escape_html(username),
                                    "email"          : escape_html(email),
                                    "username_error" : username_error,
                                    "password_error" : password_error,
                                    "email_error"    : email_error
                                    })
    def get(self):
        self.write_form()
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        pwverify = self.request.get('verify')
        email    = self.request.get('email')
        
        username_isvalid = valid_user(username)
        password_isvalid = valid_pw(password, pwverify)
        email_isvalid    = valid_email(email)
        
        if not username_isvalid:
            self.write_form(username, 
                            email, 
                            username_error="Invalid Username")
        elif not password_isvalid:
            self.write_form(username, 
                            email, 
                            password_error="Invalid Password Combo")
        elif not email_isvalid:
            self.write_form(username, 
                            email, 
                            email_error="Invalid Email Address")
        else:
            self.redirect("/welcome?username=" + username)
            

class WelcomeHandler(webapp2.RequestHandler):
    
    def get(self):
        username = self.request.get('username')
        self.response.out.write("<h1>Welcome, " + username + "!</h1>")
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
