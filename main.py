#!/usr/bin/env python

# Copyright 2017 Google Inc.
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

# [START sample]
"""A sample app that uses GCS client to operate on bucket and file."""

# [START imports]
import os

import cloudstorage as gcs
from google.appengine.api import app_identity

import webapp2

# [END imports]


class MainPage(webapp2.RequestHandler):
    """Main page for GCS demo application."""
    def get(self):
        self.response.out.write('<html><body>')
        # [START form]
        self.response.out.write("""
              <form action="/img"
                    enctype="multipart/form-data"
                    method="post">
                <div>
                    <img src="/image/Racerx.jpg"></img>
                </div>
                <br>
                <div><label>Choose your Avatar</label></div>
                <br>
                <div><input type="file" name="file"/></div>
                <br>
                <div><input type="submit" value="Upload"></div>
              </form>
            </body>
          </html>""")

class UploadHandler(webapp2.RequestHandler):
    def post(self):
        uploaded_file = self.request.POST.get("file")
        uploaded_file_content = uploaded_file.file.read()
        uploaded_file_filename = uploaded_file.filename
        uploaded_file_type = uploaded_file.type
        bucket_name ='hn-avatars'        
        #bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        
        # This write_retry_params params bit isn't essential, but Google's examples recommend it
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(
            "/" + bucket_name + "/" + uploaded_file_filename,
            "w",
            content_type=uploaded_file_type,
            retry_params=write_retry_params
        )
        gcs_file.write(uploaded_file_content)
        gcs_file.close()


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/img', UploadHandler)],
                              debug=True)
# [END sample]
