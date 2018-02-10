[![Python 3](https://pyup.io/repos/github/jpvlsmv/didactic-spork/python-3-shield.svg)](https://pyup.io/repos/github/jpvlsmv/didactic-spork/)
[![Build Status](https://travis-ci.org/jpvlsmv/didactic-spork.svg?branch=master)](https://travis-ci.org/jpvlsmv/didactic-spork)  
# didactic-spork

Arrange digital media and files in a protected, redundant, accessible way.

# Goals:
Drag and Drop files into the application.
Copies will be saved in 2+ physical locations (2+ storage providers)
Duplicate copies will be stored by reference
Metadata stored associated to the files
Access control based on metadata and external auth.

# Eventually:
Concept of file-quality:  An MP3 can be regenerated from .FLAC but not vice-versa.  Keep the latter, and a reference to the former.
Multi-file bundles: A CD image (.iso) is made up of thousands of chunks, which are sometimes actual files.  cf/ Jigdo.
VFS interface/IFS driver perhaps, webdav? What cloud plumbing would be needed?

# Interface:
For photos, a jQuery-based gallery with timeline, permissions levels, file list/metadata stored json in cloud.
