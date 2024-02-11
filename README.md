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
  pip install -r requirements.txt
```

## Run script
`Usage: python -m package_comparison.main [OPTIONS] BRANCH BRANCH2`

```
  python -m package_comparison.main sisyphus p10
```
