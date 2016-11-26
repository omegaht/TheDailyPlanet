
# Daily Planet 

In two separate tabs run: 
    Server: `python app.py`
    Client: `npm run build`


These steps are explained in more detail below.

## Prerequisites

You'll need some package managers.

- `npm`
- `pip`

## Setup

For the backend:

```
virtualenv env
activate it
    Windows: env/Scripts/activate
    Linux: source venv/bin/activate
then install the requirements
pip install -r requirements.txt
```

For the frontend:

If you don't have webpack, install it:

```
npm install -g webpack
```

Then, use `npm` to install the remaining JavaScript dependencies.

```
npm install
```

## Development

The entry point for the app is in `app/index.js`. The starter React component is `js/Main.js`. 

While developing on the frontend, run `npm run dev` to keep re-compiling your JavaScript code.

Running `npm run build` creates a file in `static/bundle.js`, which is the bundled version of your frontend code.

The "backend" here is a bare-bones Flask app. Look in `app.py` if you want to make edits to the backend.

To run the application, follow the steps in the next section.

## Running the app

If you're using a virtualenv, activate it.

```
Windows: env/Scripts/activate
Linux: source venv/bin/activate
```

Then run the Flask app:

```
python app.py
```

