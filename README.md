## Task
У нас есть публичный REST API для нашей базы данных:
https://rdb.altlinux.org/api/

У него есть метод
/export/branch_binary_packages/{branch}
в качестве бранча можно использовать sisyphus и p10
Нужно сделать модуль python и cli утилиту linux (использующую этот модуль на python), которая:

1) получает списки бинарных пакетов ветки sisyphus и p10
2) делает сравнение полученных списков пакетов и выводит JSON (структуру нужно придумать), в котором будет отображено:
- все пакеты, которые есть в p10 но нет в sisyphus
- все пакеты, которые есть в sisyphus но их нет в p10
- все пакеты, version-release которых больше в sisyphus чем в p10

Это нужно сделать для каждой из поддерживаемых веткой архитектур (поле arch в ответе).
Процесс разработки нужно оформить в виде git репозитория с историей всех изменений с самого первого этапа (без переписывания коммитов) и выложить, например, на github
Утилита должна запускаться под операционной системой Linux (проверяться будет на ALT Linux, версии 10), к ней должно быть README на английском языке, содержащее инструкцию по запуску.
Сравнение version-release согласно правилам версионирования rpm пакетов.
Cайт работающий на базе этого API -  https://packages.altlinux.org/ru/sisyphus/.

<h1 align="center">Project Deployment</h1>

## Download the project

```
  git clone git@github.com:A-V-tor/package-comparison.git
```

```
  cd package-comparison
```

## Install dependencies
```
  pip install poetry
```
There are ready-made sources in the dist directory, but they require Python 3.11
You can change it to a manual version in the pyproject.toml file

## Build the utility
1) poetry build # if you changed the configuration file pyproject.toml
2) python -m pip install dist/package_comparison-0.1.0-py3-none-any.whl


## Run script
`Usage: basalt-start [OPTIONS] BRANCH BRANCH2`

```
  basalt-start sisyphus p10
```

## The result of the work is the following structure

```
  {
    'first_branch_difference': first_branch_difference, # many packages unique to the first branch set[Package]
    'second_branch_difference': second_branch_difference, # many packages unique to the second branch set[Package]
    'version_release_difference': version_release_difference, # many packages whose version is higher in the first branch compared to the second set[Package]
    'error': error_packages, # error counter when comparing versions
  }

```

## An example of the finished utility

[![asciicast](https://asciinema.org/a/WVAcxfr0uhJ2dTz4KJv19q4tw.svg)](https://asciinema.org/a/WVAcxfr0uhJ2dTz4KJv19q4tw)
