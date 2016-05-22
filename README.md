# ExperimentManager

## Synopsis

The main goal of this library is to provide and **efficient tool** to organize some **experiments**. The programmer can  organize with ease **wich parameter** can vary through all the experiments and he/she can specify wich **variable** we would like to observe.
The software is made to **easly mantain the history** of wich experiment were made and when, and with wich results. There is the possibility to describe the main goal of each experiment, to add some **tag** to lead the possibility of a future **"quick search"**.
An amaizing feature (that has not published yet) is to easy perform some **diagrams** / **video**, on the specified obeervable variables.


## Installation

To install the library just go in the ExperimentManager directory and type:

```sh
sudo python setup.py install
```

To run the **expman*** (that is the executable version of the library), go in the ExperimentManager directory and type:

```sh
source expman_setup.sh
```

## Tests

python -m unittest ExpMan.test.experimentManagerTest
