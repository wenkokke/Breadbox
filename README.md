# Breadbox

'Breadbox' is an implementation of the game 'Plenty Questions', which
is a variant of the "popular" game '20 Questions'. The game has two
players, which we'll call Allie and Blake:

  - Allie thinks of something

  - For the first question, Blake asks *"Is it a breadbox?"*

  - Allie---who obviously wouldn't choose a breadbox---answers *"No, it
    isn't!"*

From then on, all Blake's questions have to be of the form *"Is it more
like a breadbox or more like a _____?"*
If it is, then whatever Blake tried will replace the breadbox in that
question. If it isn't, then we'll keep stick with the breadbox. A
typical game will look like this:


    Allie: I'm thinking of something...
    Blake: Is it a breadbox?
    Allie: No, it's not.
    Blake: Is it more like a breadbox or more like a dog?
    Allie: It's more like a dog...
    Blake: Is it more like a dog or more like a cat?
    Allie: It's more like a cat...
    Blake: Is it more like a cat or more like a unicorn?
    Allie: It's more like a cat...
    Blake: Is it more like a cat or more like a garden?
    Allie: It's more like a garden...
    Blake: Is it more like a garden or more like a house?
    Allie: It's more like a house...
    Blake: Is it more like a house or more like a friend?
    Allie: It's more like a friend...
    Blake: Is it more like a friend or more like a lover?
    Allie: It's more like a friend...
    Blake: Is it more like a friend or more like a relative?
    Allie: It's more like a friend...
    Blake: Is it more like a friend or more like a neighbour?
    Allie: That's exactly what I was thinking of!


# Installing

To run it, you need
[dissect](https://github.com/composes-toolkit/dissect/) from the
COMPOSES toolkit, and [names](https://pypi.python.org/pypi/names/).

When you have these, clone the repository and run `make`.


# Running

To run an instance of 'breadbox' it is important to first start the
server---because you don't want to load several gigabytes of data for
every run of the game.

    python semantic_space/semantic_space.py

When the server has started, you can run the game from the
command-line using:

    python cli/main.py

I hope to make a web interface in the future, but I don't have a
server where I can run a several gigabyte consuming process right
now.


---


Thanks to [UnicornPower](github.com/UnicornPower) for introducing me
to the game! :)
