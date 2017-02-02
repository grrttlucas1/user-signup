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

form = """
    <form method="post">
        <h1>Signup</h1>
        <br>
        <label>Username
            <input type="text" name="username">
        </label>
        <br>
        <label>Password
            <input type="password" name="password">
        </label>
        <br>
        <label>Verify Password
            <input type="password" name="verify">
        </label>
        <br>
        <label>Email (optional)
            <input type="text" name="email">
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
    

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)
        
    def post(self):
        user_username = valid_user(self.request.get('username'))
        user_password = self.request.get('password')
        user_pwverify = self.request.get('verify')
        user_pwvalid  = valid_pw(user_password, user_pwverify)
        user_email    = valid_email(self.request.get('email'))
        
        if not (user_username and user_pwvalid and user_email):
            self.response.out.write(form)
        else:
            self.response.out.write("Welcome!")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
