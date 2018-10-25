# Transcriptional_model

## Setting your environment up

1. Create virtualenv for python3 and activate. (Ensure you have python3 installed):

``` 
python3 -m virtualenv tm-env
source tm-env/bin/activate
```
Remember type `deactivate` if you want to run out of this virtualenv.

2. First clone this repo:
``` 
git clone https://github.com/macperez/transcriptional_model.git
```

3. Go into the proyect in your local path: 
``` 
cd transcriptional_model
```

4. Install dependencies:
``` 
pip install -r requirements.txt
```

5. Pick up of your email (with subjet **transcriptional-model-key.json**) a copy of Google Drive key and save it as `transcriptional-model-key.json`. Put inside of transcriptional_model folder (where the python's scripts are). 

6. Execute the main script:

``` 
python calculate_params.py
```
