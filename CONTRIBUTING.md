# Reporting Issues

If you are a programmer ideally you should write a test that fails due to the problem you are reporting and make a merge request explaining the test.
If you are not able to write a test, please report the following:
* The steps needed to cause the problem
* The content of config.toml
* The expected result
* The actual result

# Contributing Code

## General Considerations

* Integration tests should be added for all new functionality
* Unit tests should be added for all new functionality
* Classes should inherit from a base abstract class
* Everything should be statically typed
* This project uses `Black` with default settings for style, `mypy` for type checking, and `pytest` for tests
* Simple tests should be written in the simpler `pytest` style
* Complex tests should be written in the `unittest` style
* Methods that return `Optional` values should start with `try_`
* I/O methods should catch exceptions

## Conventions

* Private methods and class variables start with an underscore
* Test classes do not have private methods or variables on account of not being used from other classes at all
