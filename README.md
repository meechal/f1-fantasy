## f1-fantasy team calculator
This simple package finds the best f1-fantasy team within budget.
Team is generated only based on average points scored by constructors and drivers.

Running the code fetch all needed data like scored points and price.
Team will include Turbo Driver, but does not have option for Mega Driver, since it could be played on any driver.

### install
Clone repository to your local driver and install requirements.
```commandline
git clone xxx && cd f1-fantasy
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### running
Edit `constants.py` file and set up your `BUDGET`.
Running following command will print best teams.
```commandline
python main.py
```
You can save it to file e.g.
```commandline
python main.py > teams.txt
```