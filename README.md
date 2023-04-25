# gaminect
Web interface for playnite games


## Motivation
Playnite has the csv exporter and the html exporter
but they are not flexible enough, there is a project
called sharenite, looks promising but the backend uses
karafka, which is a kafka implementation in ruby, and
I don't have a PRO license to make it work, it makes sense
to use kafka for this, but I want a simple solution, so
I'm going to make this with fastapi and some frontend framework.
This implementation will be readonly, and will use the playnite
as the source of truth.


## Installation
- pip install -r requirements.txt
- python start.py